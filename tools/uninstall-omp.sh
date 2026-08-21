#!/usr/bin/env bash
# Remove an ACORDIA native install from omp's agent and skill roots.
#
# Removes only symlinks whose target path lies inside an `acordia-analysts`
# checkout. A real file is never deleted, and neither is a symlink pointing
# anywhere else — so a user's own agent or skill that happens to share a name
# survives, and so does an unrelated symlink farm in the same directory.
#
# Target resolution matches install-omp.sh. Because the match is on the symlink's
# recorded target rather than on any one checkout's contents, it also removes
# links left by a checkout that has since been deleted, renamed or moved — a
# dangling link is still readable and still matched.
#
# Usage:
#   tools/uninstall-omp.sh [--profile <name>] [--agent-dir <path>] [--dry-run]

set -euo pipefail

PILLAR_NAME="acordia-analysts"

self="${BASH_SOURCE[0]}"
while [ -L "$self" ]; do
	link="$(readlink "$self")"
	case "$link" in
	/*) self="$link" ;;
	*) self="$(dirname "$self")/$link" ;;
	esac
done

agent_dir=""
profile=""
dry_run=0
profile_given=0
agent_dir_given=0

die() {
	printf 'error: %s\n' "$1" >&2
	exit 1
}

usage() {
	awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "$self"
}

require_value() { # require_value <flag> <count-remaining>
	[ "$2" -ge 2 ] || die "$1 needs a value"
}

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

# An empty value is a mistake, never a request for the default. This script
# deletes: retargeting silently at ~/.omp/agent is exactly the wrong recovery.
if [ "$profile_given" -eq 1 ] && [ -z "$profile" ]; then
	die "--profile was given an empty name"
fi
if [ "$agent_dir_given" -eq 1 ] && [ -z "$agent_dir" ]; then
	die "--agent-dir was given an empty path"
fi

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

removed=0
kept=0

sweep() { # sweep <root> <expected-subdir>
	root="$1"
	subdir="$2"
	[ -d "$root" ] || return 0
	removed_here=0
	kept_here=0
	for entry in "$root"/*; do
		[ -e "$entry" ] || [ -L "$entry" ] || continue
		if [ ! -L "$entry" ]; then
			kept=$((kept + 1))
			kept_here=$((kept_here + 1))
			continue
		fi
		target="$(readlink "$entry")"
		case "$target" in
		*"/$PILLAR_NAME/$subdir/"*)
			if [ "$dry_run" -eq 1 ]; then
				printf '  would remove %s -> %s\n' "$entry" "$target"
			else
				rm -- "$entry"
				printf '  removed %s\n' "$entry"
			fi
			removed=$((removed + 1))
			removed_here=$((removed_here + 1))
			;;
		*)
			kept=$((kept + 1))
			kept_here=$((kept_here + 1))
			;;
		esac
	done

	# Remove the root only when this run emptied it. A directory that was already
	# empty, or that still holds something of the user's, is left alone. The test
	# is on the counters rather than on the directory, so a dry run reports the
	# removal it would perform instead of staying silent about it.
	if [ "$removed_here" -gt 0 ] && [ "$kept_here" -eq 0 ]; then
		if [ "$dry_run" -eq 1 ]; then
			printf '  would remove now-empty %s\n' "$root"
		else
			rmdir "$root" 2>/dev/null && printf '  removed now-empty %s\n' "$root" || :
		fi
	fi
}

sweep "$agent_dir/agents" agents
sweep "$agent_dir/skills" skills

if [ "$dry_run" -eq 1 ]; then
	printf 'dry run: %d ACORDIA links would be removed from %s, %d other entries untouched\n' \
		"$removed" "$agent_dir" "$kept"
	exit 0
fi

printf 'Removed %d ACORDIA links from %s\n' "$removed" "$agent_dir"
if [ "$kept" -gt 0 ]; then
	printf 'Left %d entries that are not ours.\n' "$kept"
fi
if [ "$removed" -gt 0 ]; then
	printf 'Restart omp: a running session keeps the roster it started with.\n'
fi
