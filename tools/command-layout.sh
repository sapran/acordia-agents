#!/usr/bin/env bash
# command-layout.sh — where the /acordia command namespace is deployed.
#
# Sourced, never executed. The caller must define `harness_root`, and have
# `TARGET_OVERRIDE` and `COMMANDS_TARGET` set (possibly empty) before calling.
#
# opencode only. omp and Claude Code now receive the command wrappers through
# the generated plugin trees under `plugins/<harness>/<plugin>/commands/`, where
# the namespace comes from the plugin name — `/acordia-analysts:fusion` — and no
# filesystem deployment is involved at all.
#
# opencode's own command discovery is flat: no subdirectory namespacing, so the
# prefix has to live in the filename.
#
#   <dir>/acordia-<stem>.md   invoked as /acordia-<stem>
#
# This repository's own OpenSpec commands already follow that split:
# `.opencode/commands/opsx-apply.md` beside `.claude/commands/opsx/apply.md`.
#
# Both directions of deployment need the same answer, for the same reason the
# ownership evidence is shared: a destination uninstall.sh looks for must be the
# one install.sh wrote. The namespace is carried by placement, never by renaming
# an artifact.

# Echoes "<dir> <shape>". The shape is always `flat`; it is still echoed so the
# call sites keep one signature and a second shape can return without touching
# every caller.
commands_root() {
  if [[ -n "${COMMANDS_TARGET:-}" ]]; then
    printf '%s flat' "$COMMANDS_TARGET"
    return
  fi
  printf '%s flat' "$(harness_root)/commands"
}

command_dest() {
  local dir="$1" shape="$2" stem="$3"
  case "$shape" in
    flat) printf '%s/acordia-%s.md' "$dir" "$stem" ;;
  esac
}

# The label a user actually types, for installer output.
command_label() {
  case "$1" in
    flat) printf '/acordia-%s' "$2" ;;
  esac
}
