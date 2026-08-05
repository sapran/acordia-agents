#!/usr/bin/env bash
# migrate-omp.sh — remove the retired omp filesystem deployment.
#
# Before this repository became a plugin marketplace, `install.sh --harness omp`
# translated the opencode agents and copied them into `~/.omp/agent/agents/`,
# with skill directories linked or copied into `~/.omp/agent/skills/`. That path
# is gone: omp now installs the distribution as a plugin.
#
# Those leftovers are not merely stale, they are ACTIVELY HARMFUL. omp resolves
# task agents from `~/.omp/agent/agents` BEFORE it reaches plugin roots, and
# dedups by name first-wins, so an old translated file silently shadows the
# plugin's agent of the same name. A user who installs the plugin and keeps the
# old deployment runs last month's prompts and cannot tell.
#
# Evidence, and why it is not tools/ownership.sh:
#
#   `ownership.sh` now tests a copied agent by byte-identity with its source,
#   because no opencode deployment is ever a translated file. These agents ARE
#   translated files — they never matched their source, by construction — so
#   that test would refuse to recognise every one of them. This script
#   therefore carries the rule the old installer used and the current one no
#   longer needs: a generated-provenance block naming a source inside this
#   repository, produced by the tool that wrote it.
#
#   translated agent -> `by: tools/translate-omp.py` AND a `from:` line naming
#                       a path that exists under this repository
#   skill            -> symlink into this repository, or a directory whose
#                       SKILL.md is byte-identical to the source's
#
# Anything failing its test is left alone and reported. Dry-run by default.
#
# Usage:
#   ./tools/migrate-omp.sh              # report what would be removed
#   ./tools/migrate-omp.sh --apply      # remove it
#   ./tools/migrate-omp.sh --target DIR # override the omp agent root

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OMP_ROOT="${HOME}/.omp/agent"
APPLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)  APPLY=1; shift ;;
    --target) OMP_ROOT="$2"; shift 2 ;;
    -h|--help) sed -n '1,35p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

# shellcheck source=tools/ownership.sh
source "$REPO_ROOT/tools/ownership.sh"

count_removed=0
count_skipped=0

run() {
  if [[ "$APPLY" -eq 1 ]]; then
    "$@"
  else
    printf '  [dry-run] %s\n' "$*"
  fi
}

# A translated agent carries its provenance in frontmatter. Both halves must
# hold: the tool that generated it, and a source path that is really in this
# repository — so a file merely mentioning the tool name cannot pass.
translated_by_repo() {
  local dst="$1" from
  grep -qF 'by: tools/translate-omp.py' "$dst" 2>/dev/null || return 1
  from="$(sed -n 's/^[[:space:]]*from:[[:space:]]*//p' "$dst" | head -1)"
  [[ -n "$from" && -f "$REPO_ROOT/$from" ]]
}

echo "== retired omp deployment ($OMP_ROOT) =="

if [[ ! -d "$OMP_ROOT" ]]; then
  echo "  nothing to do — no omp agent root at $OMP_ROOT"
  exit 0
fi

for pillar_root in "$REPO_ROOT"/*/; do
  [[ -d "$pillar_root/agents" || -d "$pillar_root/skills" ]] || continue
  pillar="$(basename "$pillar_root")"
  echo "  -- $pillar --"

  for agent in "$pillar_root/agents"/*.md; do
    [[ -e "$agent" ]] || continue
    name="$(basename "$agent")"
    dst="$OMP_ROOT/agents/$name"
    [[ -e "$dst" || -L "$dst" ]] || continue
    # A symlink resolving into this repository is the link-mode case; a
    # translated copy is the normal one.
    if owned_by_repo "$dst" "$agent" agent || translated_by_repo "$dst"; then
      echo "  agent: $name"
      run rm -f "$dst"
      count_removed=$((count_removed + 1))
    else
      echo "  agent: $name — skipped, no provenance from this repository" >&2
      count_skipped=$((count_skipped + 1))
    fi
  done

  for skill_dir in "$pillar_root/skills"/*/; do
    [[ -e "$skill_dir/SKILL.md" ]] || continue
    slug="$(basename "$skill_dir")"
    dst="$OMP_ROOT/skills/$slug"
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
done

if [[ "$APPLY" -eq 1 ]]; then
  echo "removed $count_removed artifact(s)"
else
  echo "dry-run: would remove $count_removed artifact(s) — re-run with --apply"
fi

if [[ "$count_skipped" -gt 0 ]]; then
  echo "left $count_skipped name-matching artifact(s) in place — no provenance from this repository"
fi

if [[ "$count_removed" -gt 0 && "$APPLY" -eq 1 ]]; then
  cat <<'EOF'

The plugin is now unshadowed. If you have not installed it yet:
  omp plugin marketplace add sapran/acordia-agents
  omp plugin install acordia-analysts@acordia
omp surfaces plugin content only while the `claude-plugins` capability provider
is enabled — remove it from `disabledProviders` in ~/.omp/agent/config.yml.
EOF
fi
