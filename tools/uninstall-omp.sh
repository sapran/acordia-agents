#!/usr/bin/env bash
# Remove an ACORDIA native install from omp's agent and skill roots.
#
# Removes only symlinks whose target path lies inside an `acordia-analysts`
# checkout. A real file is never deleted, and neither is a symlink pointing
# anywhere else — so a user's own agent or skill that happens to share a name
# survives, and so does an unrelated symlink farm in the same directory.
#
# Target resolution matches install-omp.sh. Because the match is on the symlink's
# recorded target rather than on this checkout's contents, it also removes links
# left by a checkout that has since been deleted, renamed or moved — a dangling
# link is still readable and still matched.
#
# Usage:
#   tools/uninstall-omp.sh [--profile <name>] [--agent-dir <path>] [--dry-run]

set -euo pipefail

PILLAR_NAME="acordia-analysts"

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
		sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
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

removed=0
kept=0

sweep() { # sweep <root> <expected-subdir>
	root="$1"
	subdir="$2"
	[ -d "$root" ] || return 0
	for entry in "$root"/*; do
		[ -e "$entry" ] || [ -L "$entry" ] || continue
		if [ ! -L "$entry" ]; then
			kept=$((kept + 1))
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
			;;
		*)
			kept=$((kept + 1))
			;;
		esac
	done
}

sweep "$agent_dir/agents" agents
sweep "$agent_dir/skills" skills

# Remove the two roots only if this script emptied them, so a directory the user
# populated themselves is left alone.
for root in "$agent_dir/agents" "$agent_dir/skills"; do
	[ -d "$root" ] || continue
	if [ -z "$(ls -A "$root")" ]; then
		if [ "$dry_run" -eq 1 ]; then
			printf '  would remove empty %s\n' "$root"
		else
			rmdir "$root"
			printf '  removed empty %s\n' "$root"
		fi
	fi
done

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
