#!/usr/bin/env bash
# uninstall.sh — remove agents + skills this repo owns from a coding harness.
#
# Only removes artifacts whose name matches something in this repo — untouched
# files in the harness config stay put. Safe to re-run.
#
# Usage:
#   ./uninstall.sh                       # remove all pillars from opencode
#   ./uninstall.sh --harness omp         # remove from omp instead
#   ./uninstall.sh --harness both        # remove from both
#   ./uninstall.sh --pillar analysts     # remove only the named pillar
#   ./uninstall.sh --dry-run             # print actions, do nothing
#   ./uninstall.sh --target DIR          # override the selected harness's root
#   ./uninstall.sh --no-commands         # leave the /acordia: command wrappers
#   ./uninstall.sh --commands-target DIR # command tree to clean, if overridden

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_ROOT="$REPO_ROOT/.build"
OPENCODE_ROOT="${HOME}/.config/opencode"
OMP_ROOT="${HOME}/.omp/agent"
DRY_RUN=0
HARNESS="opencode"
TARGET_OVERRIDE=""
COMMANDS=1
COMMANDS_TARGET=""
PILLARS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)  DRY_RUN=1; shift ;;
    --pillar)   PILLARS+=("$2"); shift 2 ;;
    --target)   TARGET_OVERRIDE="$2"; shift 2 ;;
    --harness)  HARNESS="$2"; shift 2 ;;
    --no-commands)     COMMANDS=0; shift ;;
    --commands-target) COMMANDS_TARGET="$2"; shift 2 ;;
    -h|--help)  sed -n '1,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

case "$HARNESS" in
  opencode) HARNESSES=(opencode) ;;
  omp)      HARNESSES=(omp) ;;
  both)     HARNESSES=(opencode omp) ;;
  *) echo "unknown harness: $HARNESS (expected opencode, omp, or both)" >&2; exit 1 ;;
esac

if [[ -n "$TARGET_OVERRIDE" && "$HARNESS" == "both" ]]; then
  echo "--target is ambiguous with --harness both; uninstall one harness at a time" >&2
  exit 1
fi

if [[ ${#PILLARS[@]} -eq 0 ]]; then
  # Mirrors install.sh: a pillar is a VISIBLE top-level directory carrying
  # artifacts. Dot-prefixed directories are this repository's own tooling.
  while IFS= read -r -d '' dir; do
    [[ -d "$dir/agents" || -d "$dir/skills" ]] || continue
    PILLARS+=("$(basename "$dir")")
  done < <(find "$REPO_ROOT" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0)
fi

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

harness_root() {
  if [[ -n "$TARGET_OVERRIDE" ]]; then
    printf '%s' "$TARGET_OVERRIDE"
    return
  fi
  case "$1" in
    opencode) printf '%s' "$OPENCODE_ROOT" ;;
    omp)      printf '%s' "$OMP_ROOT" ;;
  esac
}

# Ownership evidence — what counts as "this repository put the file here" — is
# defined once in tools/ownership.sh and shared with install.sh, which must
# decline to overwrite exactly what this script declines to remove.
# shellcheck source=tools/ownership.sh
source "$REPO_ROOT/tools/ownership.sh"

# The command namespace's layout is defined once and shared with install.sh, so
# this script looks exactly where that one wrote.
# shellcheck source=tools/command-layout.sh
source "$REPO_ROOT/tools/command-layout.sh"

count_removed=0
count_skipped=0

for harness in "${HARNESSES[@]}"; do
  root="$(harness_root "$harness")"
  echo "== harness: $harness ($root) =="

  for pillar in "${PILLARS[@]}"; do
    pillar_root="$REPO_ROOT/$pillar"
    if [[ ! -d "$pillar_root" ]]; then
      continue
    fi

    echo "  -- $pillar --"

    # Source filenames and translated filenames agree, so one name list covers
    # both harnesses.
    if [[ -d "$pillar_root/agents" ]]; then
      for agent in "$pillar_root/agents"/*.md; do
        [[ -e "$agent" ]] || continue
        name="$(basename "$agent")"
        dst="$root/agents/$name"
        [[ -e "$dst" || -L "$dst" ]] || continue
        if owned_by_repo "$dst" "$agent" agent; then
          echo "  agent: $name"
          run rm -f "$dst"
          count_removed=$((count_removed + 1))
        else
          echo "  agent: $name — skipped, not deployed by this repository" >&2
          count_skipped=$((count_skipped + 1))
        fi
      done
    fi

    if [[ -d "$pillar_root/skills" ]]; then
      for skill_dir in "$pillar_root/skills"/*/; do
        [[ -e "$skill_dir/SKILL.md" ]] || continue
        slug="$(basename "$skill_dir")"
        dst="$root/skills/$slug"
        [[ -e "$dst" || -L "$dst" ]] || continue
        if owned_by_repo "$dst" "${skill_dir%/}" skill; then
          echo "  skill: $slug"
          run rm -rf "$dst"
          count_removed=$((count_removed + 1))
        else
          echo "  skill: $slug — skipped, not deployed by this repository" >&2
          count_skipped=$((count_skipped + 1))
        fi
      done
    fi

    if [[ "$harness" == "omp" && -d "$BUILD_ROOT/omp/$pillar" ]]; then
      echo "  build: .build/omp/$pillar"
      run rm -rf "$BUILD_ROOT/omp/$pillar"
    fi
  done

  if [[ "$COMMANDS" -eq 1 && -d "$REPO_ROOT/commands/acordia" ]]; then
    read -r cmd_dir cmd_shape <<<"$(commands_root "$harness")"
    if [[ -z "${cmd_dir:-}" ]]; then
      echo "  -- /acordia commands -- skipped: --target overrides the harness root; name the" >&2
      echo "     command tree with --commands-target DIR to clean it too." >&2
    else
      echo "  -- /acordia commands --"
      for wrapper in "$REPO_ROOT/commands/acordia"/*.md; do
        [[ -e "$wrapper" ]] || continue
        stem="$(basename "$wrapper" .md)"
        dst="$(command_dest "$cmd_dir" "$cmd_shape" "$stem")"
        [[ -e "$dst" || -L "$dst" ]] || continue
        if owned_by_repo "$dst" "$wrapper" command; then
          echo "  command: $(command_label "$cmd_shape" "$stem")"
          run rm -f "$dst"
          count_removed=$((count_removed + 1))
        else
          echo "  command: $stem — skipped, not deployed by this repository" >&2
          count_skipped=$((count_skipped + 1))
        fi
      done
      # Only the namespace directory this repository creates, and only when
      # nothing else is left in it.
      if [[ "$cmd_shape" == "nested" && -d "$cmd_dir/acordia" ]]; then
        if [[ -z "$(ls -A "$cmd_dir/acordia" 2>/dev/null)" ]]; then
          run rmdir "$cmd_dir/acordia"
        fi
      fi
    fi
  fi
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: would remove $count_removed artifact(s)"
else
  echo "removed $count_removed artifact(s)"
fi

if [[ "$count_skipped" -gt 0 ]]; then
  echo "left $count_skipped name-matching artifact(s) in place — this repository did not deploy them"
fi
