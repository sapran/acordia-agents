#!/usr/bin/env bash
# install.sh — deploy ACORDIA agents + skills into a coding harness.
#
# Idempotent. Safe to re-run. By default symlinks so edits here reflect
# instantly in the harness. Use --copy for a frozen snapshot.
#
# Two harnesses are supported. `opencode` is the default and deploys the
# source artifacts as they are. `omp` needs its agent frontmatter translated
# (see tools/translate-omp.py) and receives generated copies instead.
#
# Usage:
#   ./install.sh                        # symlink all pillars into opencode
#   ./install.sh --harness omp          # deploy into omp instead
#   ./install.sh --harness both         # deploy into both
#   ./install.sh --copy                 # copy instead of symlink
#   ./install.sh --dry-run              # print actions, do nothing
#   ./install.sh --pillar analysts      # deploy only the named pillar
#   ./install.sh --target DIR           # override the selected harness's root
#   ./install.sh --autoload deep        # omp: preload each agent's deep skills

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_ROOT="$REPO_ROOT/.build"
OPENCODE_ROOT="${HOME}/.config/opencode"
OMP_ROOT="${HOME}/.omp/agent"
MODE="link"
DRY_RUN=0
HARNESS="opencode"
TARGET_OVERRIDE=""
AUTOLOAD="none"
PILLARS=()

usage() {
  sed -n '1,19p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)     MODE="copy"; shift ;;
    --link)     MODE="link"; shift ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --pillar)   PILLARS+=("$2"); shift 2 ;;
    --target)   TARGET_OVERRIDE="$2"; shift 2 ;;
    --harness)  HARNESS="$2"; shift 2 ;;
    --autoload) AUTOLOAD="$2"; shift 2 ;;
    -h|--help)  usage ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

case "$HARNESS" in
  opencode) HARNESSES=(opencode) ;;
  omp)      HARNESSES=(omp) ;;
  both)     HARNESSES=(opencode omp) ;;
  *) echo "unknown harness: $HARNESS (expected opencode, omp, or both)" >&2; exit 1 ;;
esac

case "$AUTOLOAD" in
  none|deep) ;;
  *) echo "unknown autoload: $AUTOLOAD (expected none or deep)" >&2; exit 1 ;;
esac

if [[ -n "$TARGET_OVERRIDE" && "$HARNESS" == "both" ]]; then
  echo "--target is ambiguous with --harness both; install one harness at a time" >&2
  exit 1
fi

if [[ ${#PILLARS[@]} -eq 0 ]]; then
  # A pillar is a top-level directory that actually carries artifacts; `docs`,
  # `openspec`, `tools`, and the build dir are not pillars.
  while IFS= read -r -d '' dir; do
    [[ -d "$dir/agents" || -d "$dir/skills" ]] || continue
    PILLARS+=("$(basename "$dir")")
  done < <(find "$REPO_ROOT" -mindepth 1 -maxdepth 1 -type d \
             ! -name '.git' ! -name '.github' ! -name '.build' -print0)
fi

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

deploy_file() {
  local src="$1" dst="$2" mode="$3"
  run mkdir -p "$(dirname "$dst")"
  if [[ -e "$dst" || -L "$dst" ]]; then
    run rm -f "$dst"
  fi
  case "$mode" in
    link) run ln -s "$src" "$dst" ;;
    copy) run cp "$src" "$dst" ;;
  esac
}

deploy_dir() {
  local src="$1" dst="$2"
  if [[ -e "$dst" || -L "$dst" ]]; then
    run rm -rf "$dst"
  fi
  case "$MODE" in
    link) run mkdir -p "$(dirname "$dst")"; run ln -s "$src" "$dst" ;;
    copy) run mkdir -p "$dst"; run cp -R "$src/." "$dst/" ;;
  esac
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

# Translate a pillar's opencode agents into omp form under .build/, echoing the
# directory that would hold them. Generated output — never edit, never commit.
# Under --dry-run this runs the translator in --check mode: the same parsing and
# the same failures, but nothing written, so a clean dry-run really does predict
# a clean install.
translate_pillar() {
  local pillar="$1" out="$BUILD_ROOT/omp/$1/agents"
  local -a args=(--out "$out" --autoload "$AUTOLOAD")
  if [[ "$DRY_RUN" -eq 1 ]]; then
    args+=(--check)
  else
    rm -rf "$out"
  fi
  "$REPO_ROOT/tools/translate-omp.py" "$REPO_ROOT/$pillar/agents"/*.md "${args[@]}" >&2
  printf '%s' "$out"
}

count_deployed=0
warned_link=0

for harness in "${HARNESSES[@]}"; do
  root="$(harness_root "$harness")"
  echo "== harness: $harness ($root) =="

  # Translated agents are regenerated on every install, so a symlink would
  # point at a build artifact rather than at a reviewable source file.
  agent_mode="$MODE"
  if [[ "$harness" == "omp" && "$MODE" == "link" ]]; then
    agent_mode="copy"
    if [[ "$warned_link" -eq 0 ]]; then
      echo "  note: agents are translated for omp, so they are copied, not linked"
      warned_link=1
    fi
  fi

  for pillar in "${PILLARS[@]}"; do
    pillar_root="$REPO_ROOT/$pillar"
    if [[ ! -d "$pillar_root" ]]; then
      echo "skipping: pillar '$pillar' not found at $pillar_root" >&2
      continue
    fi

    echo "  -- $pillar --"

    if [[ -d "$pillar_root/agents" ]]; then
      # For omp the deployed file is the translated one, so name the build path
      # as the source even in dry-run; the filenames are identical either way.
      agent_src_dir="$pillar_root/agents"
      if [[ "$harness" == "omp" ]]; then
        translate_pillar "$pillar" >/dev/null
        agent_src_dir="$BUILD_ROOT/omp/$pillar/agents"
      fi
      for agent in "$pillar_root/agents"/*.md; do
        [[ -e "$agent" ]] || continue
        name="$(basename "$agent")"
        echo "  agent: $name"
        deploy_file "$agent_src_dir/$name" "$root/agents/$name" "$agent_mode"
        count_deployed=$((count_deployed + 1))
      done
    fi

    if [[ -d "$pillar_root/skills" ]]; then
      for skill_dir in "$pillar_root/skills"/*/; do
        [[ -e "$skill_dir/SKILL.md" ]] || continue
        slug="$(basename "$skill_dir")"
        echo "  skill: $slug"
        deploy_dir "${skill_dir%/}" "$root/skills/$slug"
        count_deployed=$((count_deployed + 1))
      done
    fi
  done
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: would deploy $count_deployed artifact(s) via $MODE"
else
  echo "deployed $count_deployed artifact(s) via $MODE"
fi
