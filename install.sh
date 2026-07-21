#!/usr/bin/env bash
# install.sh — deploy ACORDIA agents + skills into opencode's config dir.
#
# Idempotent. Safe to re-run. By default symlinks so edits here reflect
# instantly in opencode. Use --copy for a frozen snapshot.
#
# Usage:
#   ./install.sh                   # symlink all pillars
#   ./install.sh --copy            # copy instead of symlink
#   ./install.sh --dry-run         # print actions, do nothing
#   ./install.sh --pillar analysts # deploy only the named pillar
#   ./install.sh --target DIR      # override the default target (~/.config/opencode)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${HOME}/.config/opencode"
MODE="link"
DRY_RUN=0
PILLARS=()

usage() {
  sed -n '1,15p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)     MODE="copy"; shift ;;
    --link)     MODE="link"; shift ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --pillar)   PILLARS+=("$2"); shift 2 ;;
    --target)   TARGET="$2"; shift 2 ;;
    -h|--help)  usage ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ ${#PILLARS[@]} -eq 0 ]]; then
  while IFS= read -r -d '' dir; do
    PILLARS+=("$(basename "$dir")")
  done < <(find "$REPO_ROOT" -mindepth 1 -maxdepth 1 -type d \
             ! -name '.git' ! -name '.github' -print0)
fi

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

deploy_file() {
  local src="$1" dst="$2"
  run mkdir -p "$(dirname "$dst")"
  if [[ -e "$dst" || -L "$dst" ]]; then
    run rm -f "$dst"
  fi
  case "$MODE" in
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

count_deployed=0
for pillar in "${PILLARS[@]}"; do
  pillar_root="$REPO_ROOT/$pillar"
  if [[ ! -d "$pillar_root" ]]; then
    echo "skipping: pillar '$pillar' not found at $pillar_root" >&2
    continue
  fi

  echo "== $pillar =="

  if [[ -d "$pillar_root/agents" ]]; then
    for agent in "$pillar_root/agents"/*.md; do
      [[ -e "$agent" ]] || continue
      name="$(basename "$agent")"
      dst="$TARGET/agents/$name"
      echo "  agent: $name"
      deploy_file "$agent" "$dst"
      count_deployed=$((count_deployed + 1))
    done
  fi

  if [[ -d "$pillar_root/skills" ]]; then
    for skill_dir in "$pillar_root/skills"/*/; do
      [[ -e "$skill_dir/SKILL.md" ]] || continue
      slug="$(basename "$skill_dir")"
      dst="$TARGET/skills/$slug"
      echo "  skill: $slug"
      deploy_dir "${skill_dir%/}" "$dst"
      count_deployed=$((count_deployed + 1))
    done
  fi
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: would deploy $count_deployed artifact(s) via $MODE to $TARGET"
else
  echo "deployed $count_deployed artifact(s) via $MODE to $TARGET"
fi
