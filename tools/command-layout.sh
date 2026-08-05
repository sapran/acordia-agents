#!/usr/bin/env bash
# command-layout.sh — where the /acordia command namespace is deployed.
#
# Sourced, never executed. The caller must define `harness_root`, and have
# `TARGET_OVERRIDE` and `COMMANDS_TARGET` set (possibly empty) before calling.
#
# Both directions of deployment need the same answer, for the same reason the
# ownership evidence is shared: a destination uninstall.sh looks for must be the
# one install.sh wrote. The namespace is carried by placement, never by renaming
# an artifact, and the two harnesses need different placements:
#
#   Claude-format tree -> <dir>/acordia/<stem>.md   invoked as /acordia:<stem>
#     Scanned recursively, and a subdirectory registers a namespace alias
#     (`foo/bar.md` -> both `bar` and `foo:bar`). omp reads this tree too, so
#     one deployment serves omp and Claude Code alike.
#
#   opencode           -> <dir>/acordia-<stem>.md   invoked as /acordia-<stem>
#     Command discovery is flat, so the prefix has to live in the filename.
#     This repository's own OpenSpec commands already follow that split:
#     `.opencode/commands/opsx-apply.md` beside `.claude/commands/opsx/apply.md`.
#
# omp's own commands/ directory is deliberately unused: it is scanned
# non-recursively and therefore cannot express a namespace at all.

CLAUDE_COMMANDS_ROOT="${CLAUDE_COMMANDS_ROOT:-${HOME}/.claude/commands}"

# Echoes "<dir> <shape>" for a harness, or nothing when the step cannot be
# resolved and the caller must skip it with a message.
commands_root() {
  local harness="$1"
  if [[ -n "${COMMANDS_TARGET:-}" ]]; then
    case "$harness" in
      opencode) printf '%s flat' "$COMMANDS_TARGET" ;;
      omp)      printf '%s nested' "$COMMANDS_TARGET" ;;
    esac
    return
  fi
  case "$harness" in
    opencode) printf '%s flat' "$(harness_root opencode)/commands" ;;
    omp)
      # An overridden harness root says nothing about where the Claude command
      # tree lives, so inferring one would write outside anything the user named.
      [[ -n "${TARGET_OVERRIDE:-}" ]] && return
      printf '%s nested' "$CLAUDE_COMMANDS_ROOT"
      ;;
  esac
}

command_dest() {
  local dir="$1" shape="$2" stem="$3"
  case "$shape" in
    nested) printf '%s/acordia/%s.md' "$dir" "$stem" ;;
    flat)   printf '%s/acordia-%s.md' "$dir" "$stem" ;;
  esac
}

# The label a user actually types, for installer output.
command_label() {
  case "$1" in
    nested) printf '/acordia:%s' "$2" ;;
    flat)   printf '/acordia-%s' "$2" ;;
  esac
}
