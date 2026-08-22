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

# Resolve this script through any symlink chain before deriving the checkout, so
# that a convenience link such as ~/bin/acordia-install still finds the pillar.
self="${BASH_SOURCE[0]}"
while [ -L "$self" ]; do
	link="$(readlink "$self")"
	case "$link" in
	/*) self="$link" ;;
	*) self="$(dirname "$self")/$link" ;;
	esac
done
REPO_ROOT="$(cd "$(dirname "$self")/.." && pwd)"
PILLAR="$REPO_ROOT/$PILLAR_NAME"

agent_dir=""
profile=""
dry_run=0
linked=0

die() {
	printf 'error: %s\n' "$1" >&2
	exit 1
}

usage() {
	awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "$self"
}

# A failure partway through the link loop would otherwise leave a partial install
# with no explanation. Name the recovery instead of dying silently.
on_error() {
	if [ "$linked" -gt 0 ]; then
		printf '\nerror: failed after creating %d links — the install is partial.\n' "$linked" >&2
		printf 'Run tools/uninstall-omp.sh to remove what was created, then try again.\n' >&2
	fi
}
trap on_error ERR

require_value() { # require_value <flag> <count-remaining>
	[ "$2" -ge 2 ] || die "$1 needs a value"
}

profile_given=0
agent_dir_given=0

while [ $# -gt 0 ]; do
	case "$1" in
	--profile)
		require_value --profile $#
		profile="$2"
		profile_given=1
		shift 2
		;;
	--agent-dir)
		require_value --agent-dir $#
		agent_dir="$2"
		agent_dir_given=1
		shift 2
		;;
	--dry-run)
		dry_run=1
		shift
		;;
	-h | --help)
		usage
		exit 0
		;;
	*)
		die "unknown argument: $1"
		;;
	esac
done

if [ "$agent_dir_given" -eq 1 ] && [ "$profile_given" -eq 1 ]; then
	die "--agent-dir and --profile are mutually exclusive"
fi

# An empty value is a mistake, never a request for the default. Falling back
# silently is how a user installs into the wrong agent directory.
if [ "$profile_given" -eq 1 ] && [ -z "$profile" ]; then
	die "--profile was given an empty name"
fi
if [ "$agent_dir_given" -eq 1 ] && [ -z "$agent_dir" ]; then
	die "--agent-dir was given an empty path"
fi

# A profile is a bare name under ~/.omp/profiles; a path here escapes that root.
case "$profile" in
"") ;;
*/* | . | ..) die "--profile takes a bare profile name, not a path: $profile" ;;
esac

if [ -z "$agent_dir" ]; then
	if [ -n "$profile" ]; then
		agent_dir="$HOME/.omp/profiles/$profile/agent"
	else
		agent_dir="${PI_CODING_AGENT_DIR:-$HOME/.omp/agent}"
	fi
fi

[ -d "$PILLAR/agents" ] || die "no agents directory at $PILLAR/agents — run the copy inside a checkout, as <checkout>/tools/install-omp.sh"
[ -d "$PILLAR/skills" ] || die "no skills directory at $PILLAR/skills — run the copy inside a checkout, as <checkout>/tools/install-omp.sh"

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
	[ -e "$src" ] || continue
	dst="$agents_root/$(basename "$src")"
	if [ -e "$dst" ] || [ -L "$dst" ]; then
		ours "$dst" || collisions="$collisions  $dst
"
	fi
done
for src in "$PILLAR"/skills/*/; do
	[ -d "$src" ] || continue
	dst="$skills_root/$(basename "${src%/}")"
	if [ -e "$dst" ] || [ -L "$dst" ]; then
		ours "$dst" || collisions="$collisions  $dst
"
	fi
done

if [ -n "$collisions" ]; then
	printf 'error: these entries already exist and were not created by this checkout:\n' >&2
	printf '%s' "$collisions" >&2
	printf 'Nothing was installed.\n' >&2
	printf 'Links from another ACORDIA checkout: run tools/uninstall-omp.sh first — it removes those.\n' >&2
	printf 'Your own agents or skills of the same name: rename them, then run this again.\n' >&2
	exit 1
fi

link() { # link <src> <dst>
	if [ "$dry_run" -eq 1 ]; then
		printf '  would link %s\n' "$2"
		return
	fi
	ln -sfn "$1" "$2"
	linked=$((linked + 1))
}

if [ "$dry_run" -eq 0 ]; then
	mkdir -p "$agents_root" "$skills_root"
fi

agents=0
for src in "$PILLAR"/agents/*.md; do
	[ -e "$src" ] || continue
	link "$src" "$agents_root/$(basename "$src")"
	agents=$((agents + 1))
done

skills=0
for src in "$PILLAR"/skills/*/; do
	[ -d "$src" ] || continue
	src="${src%/}"
	link "$src" "$skills_root/$(basename "$src")"
	skills=$((skills + 1))
done

trap - ERR

if [ "$dry_run" -eq 1 ]; then
	printf 'dry run: %d agents and %d skills would be linked into %s\n' "$agents" "$skills" "$agent_dir"
	exit 0
fi

printf 'Linked %d agents into %s\n' "$agents" "$agents_root"
printf 'Linked %d skills into %s\n' "$skills" "$skills_root"
printf '\nThese are symlinks into %s, so a git pull changes what omp serves.\n' "$REPO_ROOT"
printf 'A running session holds its roster from startup: restart omp, then check /agents lists %d.\n' "$agents"
printf 'Command wrappers are not installed by this route — they need the plugin namespace.\n'
printf 'These names now win over a marketplace install of the same agents, silently. If you have one,\n'
printf 'uninstall it, or run tools/uninstall-omp.sh to go back to it.\n'
