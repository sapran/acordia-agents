#!/usr/bin/env bash
# install.sh — deploy ACORDIA agents + skills into opencode.
#
# Idempotent. Safe to re-run. By default symlinks so edits here reflect
# instantly in the harness. Use --copy for a frozen snapshot.
#
# opencode only. It has no plugin system — no marketplace, no registry, and its
# "plugins" are JS/TS hook modules that cannot ship markdown — so a filesystem
# deployment into ~/.config/opencode/ is the only way in. omp and Claude Code
# are served by the plugin marketplace at the repository root instead; see
# README.md for those install paths.
#
# Usage:
#   ./install.sh                        # symlink all pillars into opencode
#   ./install.sh --copy                 # copy instead of symlink
#   ./install.sh --dry-run              # print actions, do nothing
#   ./install.sh --pillar analysts      # deploy only the named pillar
#   ./install.sh --target DIR           # override the opencode root
#   ./install.sh --force                # replace artifacts this repo does not own
#   ./install.sh --no-commands          # skip the /acordia- command wrappers
#   ./install.sh --commands-target DIR  # place the command tree explicitly

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCODE_ROOT="${HOME}/.config/opencode"
MODE="link"
DRY_RUN=0
TARGET_OVERRIDE=""
FORCE=0
COMMANDS=1
COMMANDS_TARGET=""
PILLARS=()

# Ownership evidence is shared with uninstall.sh: a destination that script
# declines to remove is one this script must decline to overwrite.
# shellcheck source=tools/ownership.sh
source "$REPO_ROOT/tools/ownership.sh"

# Where the /acordia command namespace lands, shared with uninstall.sh for the
# same reason. Sourced after harness_root's inputs are set; it calls that
# function, which is defined below.
# shellcheck source=tools/command-layout.sh
source "$REPO_ROOT/tools/command-layout.sh"

usage() {
  sed -n '1,23p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)     MODE="copy"; shift ;;
    --link)     MODE="link"; shift ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --pillar)   PILLARS+=("$2"); shift 2 ;;
    --target)   TARGET_OVERRIDE="$2"; shift 2 ;;
    --force)    FORCE=1; shift ;;
    --no-commands)     COMMANDS=0; shift ;;
    --commands-target) COMMANDS_TARGET="$2"; shift 2 ;;
    -h|--help)  usage ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ ${#PILLARS[@]} -eq 0 ]]; then
  # A pillar is a VISIBLE top-level directory carrying artifacts. Everything in
  # this repository that is tooling configuration rather than distributable
  # content is dot-prefixed — `.git`, `.github`, `.opencode`, `.claude`,
  # `.codex` — so the dot-prefix rule replaces an exclusion list that kept
  # growing. `docs`, `openspec`, `tools`, and the generated `plugins` tree are
  # visible but carry no `agents/` or `skills/` at their top level, hence the
  # second test. `--pillar` bypasses both.
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

# The opencode root is a flat namespace shared with opencode's own built-in
# agents and skills. Deploying used to remove whatever sat at the destination
# without asking what it was, so a name collision silently destroyed a foreign
# artifact. Now every destination needs the same ownership evidence uninstall.sh
# requires before it removes anything; --force is the deliberate override.
assert_replaceable() {
  local dst="$1" own_src="$2" kind="$3"
  [[ -e "$dst" || -L "$dst" ]] || return 0
  if owned_by_repo "$dst" "$own_src" "$kind"; then
    return 0
  fi
  if [[ "$FORCE" -eq 1 ]]; then
    echo "  forced over unowned $kind: $dst" >&2
    count_forced=$((count_forced + 1))
    return 0
  fi
  echo "refusing to overwrite $dst — this repository did not deploy it." >&2
  echo "move it aside, or re-run with --force to replace it." >&2
  exit 1
}

# Every destination is checked before anything is written, so a collision aborts
# with the harness untouched instead of leaving a half-deployed pillar whose
# orchestrator references legs that never arrived. Reads only, so it runs
# unchanged under --dry-run.
preflight() {
  local root pillar pillar_root agent skill_dir wrapper cmd_dir cmd_shape
  root="$(harness_root)"
  for pillar in "${PILLARS[@]}"; do
    pillar_root="$REPO_ROOT/$pillar"
    [[ -d "$pillar_root" ]] || continue
    for agent in "$pillar_root/agents"/*.md; do
      [[ -e "$agent" ]] || continue
      assert_replaceable "$root/agents/$(basename "$agent")" "$agent" agent
    done
    for skill_dir in "$pillar_root/skills"/*/; do
      [[ -e "$skill_dir/SKILL.md" ]] || continue
      assert_replaceable "$root/skills/$(basename "$skill_dir")" "${skill_dir%/}" skill
    done
  done

  if [[ "$COMMANDS" -eq 1 && -d "$REPO_ROOT/commands/acordia" ]]; then
    read -r cmd_dir cmd_shape <<<"$(commands_root)"
    if [[ -n "${cmd_dir:-}" ]]; then
      for wrapper in "$REPO_ROOT/commands/acordia"/*.md; do
        [[ -e "$wrapper" ]] || continue
        assert_replaceable "$(command_dest "$cmd_dir" "$cmd_shape" "$(basename "$wrapper" .md)")" "$wrapper" command
      done
    fi
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
  printf '%s' "$OPENCODE_ROOT"
}

count_deployed=0
count_forced=0

preflight

root="$(harness_root)"
echo "== opencode ($root) =="

for pillar in "${PILLARS[@]}"; do
  pillar_root="$REPO_ROOT/$pillar"
  if [[ ! -d "$pillar_root" ]]; then
    echo "skipping: pillar '$pillar' not found at $pillar_root" >&2
    continue
  fi

  echo "  -- $pillar --"

  if [[ -d "$pillar_root/agents" ]]; then
    for agent in "$pillar_root/agents"/*.md; do
      [[ -e "$agent" ]] || continue
      name="$(basename "$agent")"
      echo "  agent: $name"
      deploy_file "$agent" "$root/agents/$name" "$MODE"
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

if [[ "$COMMANDS" -eq 1 && -d "$REPO_ROOT/commands/acordia" ]]; then
  read -r cmd_dir cmd_shape <<<"$(commands_root)"
  if [[ -z "${cmd_dir:-}" ]]; then
    echo "  -- /acordia commands -- skipped: --target overrides the opencode root, but the" >&2
    echo "     command tree lives elsewhere. Name it with --commands-target DIR." >&2
  else
    echo "  -- /acordia commands --"
    for wrapper in "$REPO_ROOT/commands/acordia"/*.md; do
      [[ -e "$wrapper" ]] || continue
      stem="$(basename "$wrapper" .md)"
      dst="$(command_dest "$cmd_dir" "$cmd_shape" "$stem")"
      echo "  command: $(command_label "$cmd_shape" "$stem")"
      deploy_file "$wrapper" "$dst" "$MODE"
      count_deployed=$((count_deployed + 1))
    done
  fi
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: would deploy $count_deployed artifact(s) via $MODE"
else
  echo "deployed $count_deployed artifact(s) via $MODE"
fi

if [[ "$count_forced" -gt 0 ]]; then
  echo "replaced $count_forced artifact(s) this repository did not deploy (--force)"
fi
