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
#   ./install.sh --force                # replace artifacts this repo does not own

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
FORCE=0
PILLARS=()

# Ownership evidence is shared with uninstall.sh: a destination that script
# declines to remove is one this script must decline to overwrite.
# shellcheck source=tools/ownership.sh
source "$REPO_ROOT/tools/ownership.sh"

usage() {
  sed -n '1,20p' "$0" | sed 's/^# \{0,1\}//'
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
    --force)    FORCE=1; shift ;;
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
  # A pillar is a VISIBLE top-level directory carrying artifacts. Everything in
  # this repository that is tooling configuration rather than distributable
  # content is dot-prefixed — `.git`, `.github`, `.build`, `.opencode`,
  # `.claude`, `.codex` — so the dot-prefix rule replaces an exclusion list that
  # kept growing. `docs`, `openspec`, and `tools` are visible but carry no
  # artifacts, hence the second test. `--pillar` bypasses both.
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

# Both harness roots are flat namespaces shared with the harness's own built-in
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
  local harness root pillar pillar_root agent skill_dir
  for harness in "${HARNESSES[@]}"; do
    root="$(harness_root "$harness")"
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
  done
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
count_forced=0
warned_link=0

preflight

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

if [[ "$count_forced" -gt 0 ]]; then
  echo "replaced $count_forced artifact(s) this repository did not deploy (--force)"
fi
