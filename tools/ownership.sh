#!/usr/bin/env bash
# ownership.sh — does this repository own the artifact at a given destination?
#
# Sourced, never executed. The caller must have REPO_ROOT set to this
# repository's absolute root before calling owned_by_repo.
#
# Both directions of deployment need the same answer. uninstall.sh must not
# remove an artifact this repository did not put there, and install.sh must not
# overwrite one — the harness roots are flat namespaces shared with the
# harness's own built-in agents and skills and with whatever the user keeps
# there. A name match is not proof of ownership, so both scripts gate on
# evidence, and the evidence is defined here once so the two cannot drift.
#
#   symlink      -> must resolve inside this repository
#   copied agent -> must be byte-identical to the source, or be a translated
#                   file whose provenance names that source
#   copied skill -> its SKILL.md must be byte-identical to the source's
#
# Usage: owned_by_repo <destination> <source> <agent|skill>
owned_by_repo() {
  local dst="$1" src="$2" kind="$3"

  if [[ -L "$dst" ]]; then
    local resolved
    resolved="$(cd "$(dirname "$dst")" && readlink -f "$(basename "$dst")" 2>/dev/null || true)"
    [[ -n "$resolved" && "$resolved" == "$REPO_ROOT"/* ]]
    return
  fi

  case "$kind" in
    agent)
      cmp -s "$dst" "$src" && return 0
      # Translated omp agents differ from their source by construction; they
      # carry the source path in their generated provenance block.
      grep -qF "from: ${src#"$REPO_ROOT/"}" "$dst" 2>/dev/null
      ;;
    skill)
      cmp -s "$dst/SKILL.md" "$src/SKILL.md"
      ;;
  esac
}
