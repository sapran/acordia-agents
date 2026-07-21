#!/usr/bin/env bash
# uninstall.sh — remove agents + skills this repo owns from opencode's config.
#
# Only removes artifacts whose name matches something in this repo — untouched
# files in ~/.config/opencode/ stay put. Safe to re-run.
#
# Usage:
#   ./uninstall.sh                   # remove all pillars
#   ./uninstall.sh --pillar analysts # remove only the named pillar
#   ./uninstall.sh --dry-run         # print actions, do nothing
#   ./uninstall.sh --target DIR      # override the default target

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${HOME}/.config/opencode"
DRY_RUN=0
PILLARS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)  DRY_RUN=1; shift ;;
    --pillar)   PILLARS+=("$2"); shift 2 ;;
    --target)   TARGET="$2"; shift 2 ;;
    -h|--help)  sed -n '1,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
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

count_removed=0
for pillar in "${PILLARS[@]}"; do
  pillar_root="$REPO_ROOT/$pillar"
  if [[ ! -d "$pillar_root" ]]; then
    continue
  fi

  echo "== $pillar =="

  if [[ -d "$pillar_root/agents" ]]; then
    for agent in "$pillar_root/agents"/*.md; do
      [[ -e "$agent" ]] || continue
      name="$(basename "$agent")"
      dst="$TARGET/agents/$name"
      if [[ -e "$dst" || -L "$dst" ]]; then
        echo "  agent: $name"
        run rm -f "$dst"
        count_removed=$((count_removed + 1))
      fi
    done
  fi

  if [[ -d "$pillar_root/skills" ]]; then
    for skill_dir in "$pillar_root/skills"/*/; do
      slug="$(basename "$skill_dir")"
      dst="$TARGET/skills/$slug"
      if [[ -e "$dst" || -L "$dst" ]]; then
        echo "  skill: $slug"
        run rm -rf "$dst"
        count_removed=$((count_removed + 1))
      fi
    done
  fi
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "dry-run: would remove $count_removed artifact(s) from $TARGET"
else
  echo "removed $count_removed artifact(s) from $TARGET"
fi
