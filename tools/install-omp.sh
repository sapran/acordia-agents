#!/usr/bin/env bash
# Install the ACORDIA Analysis pillar into omp's native agent and skill roots.
#
# Why this exists: omp serves a marketplace plugin's agents only when the
# `claude-plugins` discovery provider is enabled, and that provider also pulls in
# every plugin registered in Claude Code's own plugin registry. A user who
# disables it — a reasonable choice if they do not want Claude Code's ecosystem —
# gets a marketplace install that reports success and contributes nothing, with
# no error. The native roots this script writes to are discovery inputs 1 and 2
# and are gated by no provider at all.
#
# What it does: symlinks each agent file and each skill directory from this
# checkout into the target agent directory. Symlinks, not copies, so a `git pull`
# updates what omp serves. Nothing outside the two roots is touched, no
# configuration file is edited, and an entry that is not ours is never replaced.
#
# Usage:
#   tools/install-omp.sh [--profile <name>] [--agent-dir <path>] [--dry-run]
#
# Target directory precedence: --agent-dir, then --profile (which resolves to
# ~/.omp/profiles/<name>/agent), then $PI_CODING_AGENT_DIR, then ~/.omp/agent.

set -euo pipefail

PILLAR_NAME="acordia-analysts"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PILLAR="$REPO_ROOT/$PILLAR_NAME"

agent_dir=""
profile=""
dry_run=0

die() {
	printf 'error: %s\n' "$1" >&2
	exit 1
}

while [ $# -gt 0 ]; do
	case "$1" in
	--profile)
		[ $# -ge 2 ] || die "--profile needs a name"
		profile="$2"
		shift 2
		;;
	--agent-dir)
		[ $# -ge 2 ] || die "--agent-dir needs a path"
		agent_dir="$2"
		shift 2
		;;
	--dry-run)
		dry_run=1
		shift
		;;
	-h | --help)
		sed -n '2,26p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
		exit 0
		;;
	*)
		die "unknown argument: $1"
		;;
	esac
done

if [ -n "$agent_dir" ] && [ -n "$profile" ]; then
	die "--agent-dir and --profile are mutually exclusive"
fi
if [ -z "$agent_dir" ]; then
	if [ -n "$profile" ]; then
		agent_dir="$HOME/.omp/profiles/$profile/agent"
	else
		agent_dir="${PI_CODING_AGENT_DIR:-$HOME/.omp/agent}"
	fi
fi

[ -d "$PILLAR/agents" ] || die "no agents directory at $PILLAR/agents — run this from a checkout"
[ -d "$PILLAR/skills" ] || die "no skills directory at $PILLAR/skills — run this from a checkout"

agents_root="$agent_dir/agents"
skills_root="$agent_dir/skills"

# Preflight: refuse to clobber anything that is not one of our own symlinks.
# A real file here is the user's own agent or skill of the same name; replacing
# it would silently take over their dispatch handle. Report every collision and
# change nothing.
collisions=""
ours() { # ours <path> — true when path is a symlink already pointing into this pillar
	[ -L "$1" ] || return 1
	case "$(readlink "$1")" in
	"$PILLAR"/*) return 0 ;;
	*) return 1 ;;
	esac
}

for src in "$PILLAR"/agents/*.md; do
	dst="$agents_root/$(basename "$src")"
	if [ -e "$dst" ] || [ -L "$dst" ]; then
		ours "$dst" || collisions="$collisions  $dst\n"
	fi
done
for src in "$PILLAR"/skills/*/; do
	dst="$skills_root/$(basename "${src%/}")"
	if [ -e "$dst" ] || [ -L "$dst" ]; then
		ours "$dst" || collisions="$collisions  $dst\n"
	fi
done

if [ -n "$collisions" ]; then
	printf 'error: these entries already exist and were not created by this script:\n' >&2
	printf "$collisions" >&2
	printf 'Nothing was installed. Rename or remove them, then run this again.\n' >&2
	exit 1
fi

link() { # link <src> <dst>
	if [ "$dry_run" -eq 1 ]; then
		printf '  would link %s\n' "$2"
		return
	fi
	ln -sfn "$1" "$2"
}

if [ "$dry_run" -eq 0 ]; then
	mkdir -p "$agents_root" "$skills_root"
fi

agents=0
for src in "$PILLAR"/agents/*.md; do
	link "$src" "$agents_root/$(basename "$src")"
	agents=$((agents + 1))
done

skills=0
for src in "$PILLAR"/skills/*/; do
	src="${src%/}"
	link "$src" "$skills_root/$(basename "$src")"
	skills=$((skills + 1))
done

if [ "$dry_run" -eq 1 ]; then
	printf 'dry run: %d agents and %d skills would be linked into %s\n' "$agents" "$skills" "$agent_dir"
	exit 0
fi

printf 'Linked %d agents into %s\n' "$agents" "$agents_root"
printf 'Linked %d skills into %s\n' "$skills" "$skills_root"
printf '\nThese are symlinks into %s, so a git pull changes what omp serves.\n' "$REPO_ROOT"
printf 'A running session holds its roster from startup: restart omp, then check /agents lists %d.\n' "$agents"
printf 'Command wrappers are not installed by this route — they need the plugin namespace.\n'
