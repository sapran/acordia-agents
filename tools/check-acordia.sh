#!/bin/bash
# acordia-agents drift gate. Checks the invariants whose build-time enforcer
# was deleted in 3.0.0 (see CLAUDE.md "Bump the version on every change"):
#   1. versions agree across all three JSON manifests (3 occurrences)
#   2. the two marketplace catalogs are byte-identical
#   3. every skill slug named in a `·`-separated prompt line resolves
#   4. version was bumped vs the base branch (only inside a feature worktree)
#   5. every skill `row:` resolves to a grid row id, and back (5.0.0)
#   6. every `doctrine_source` key resolves in docs/roles/sources.md (5.0.0)
#   7. the orchestrator body is byte-identical in agents/ and both wrappers (6.5.0)
#   8. no agent prompt body exceeds the ceiling in agent-roster spec (6.5.0)
# The distribution went single-pillar in 5.0.0: acordia-operators was removed,
# so the version now lives in three places, not six.
# Usage: check-acordia.sh [repo-root]   Exit 1 with named violations, 0 if clean.
set -u
cd "${1:-$(cd "$(dirname "$0")/.." && pwd)}" || exit 2
fail=0
say(){ printf '%s\n' "$*"; }

# 1. version lockstep
python3 - <<'PY' || fail=1
import json, re, sys
files = ["acordia-analysts/.claude-plugin/plugin.json",
         ".claude-plugin/marketplace.json",
         ".omp-plugin/marketplace.json"]
found = {}
def walk(o):
    if isinstance(o, dict):
        if "version" in o and isinstance(o["version"], str):
            found.setdefault(o["version"], 0); found[o["version"]] += 1
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for f in files:
    try:
        walk(json.load(open(f)))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL {f}: {e}"); sys.exit(1)
sem = [v for v in found if re.fullmatch(r"\d+\.\d+\.\d+", v)]
if len(sem) != 1:
    print(f"FAIL versions disagree: {found}"); sys.exit(1)
if sum(found.values()) != 3:
    print(f"FAIL expected 3 version occurrences, found {sum(found.values())}: {found}"); sys.exit(1)
print(f"ok  version {sem[0]} x3 across 3 files")
PY

# 2. catalog byte-identity
if diff -q .claude-plugin/marketplace.json .omp-plugin/marketplace.json >/dev/null; then
  say "ok  marketplace catalogs byte-identical"
else
  say "FAIL marketplace catalogs differ"; fail=1
fi

# 3. every prompt slug resolves
python3 - <<'PY' || fail=1
import glob, os, pathlib, re, sys
bad = 0
pil = "acordia-analysts"
have = {os.path.basename(os.path.dirname(s)) for s in glob.glob(f"{pil}/skills/*/SKILL.md")}
for a in glob.glob(f"{pil}/agents/*.md"):
    prev = ""
    for line in pathlib.Path(a).read_text().splitlines():
        s = line.strip()
        if s and prev.startswith("#") and re.fullmatch(r"[a-z0-9][\w.-]*( · [a-z0-9][\w.-]*)*", s):
            for slug in (x.strip() for x in s.split("·")):
                if slug not in have:
                    print(f"FAIL UNRESOLVED {a} {slug}"); bad += 1
        if s: prev = s
if bad: sys.exit(1)
print("ok  every prompt skill slug resolves")
PY

# 5. grid row ids <-> skill `row:` anchors, and no surviving line anchors
python3 - <<'PY' || fail=1
import glob, os, pathlib, re, sys
grid = pathlib.Path("docs/roles/operational-analyst.md").read_text()
ids = re.findall(r"^\|[^|]*\|\s*`([a-z0-9][a-z0-9-]*)`\s*\|", grid, re.M)
if len(ids) != len(set(ids)):
    dupes = {i for i in ids if ids.count(i) > 1}
    print(f"FAIL duplicate grid row ids: {sorted(dupes)}"); sys.exit(1)
gridset, bad = set(ids), 0
anchored = {}
for s in glob.glob("acordia-analysts/skills/*/SKILL.md"):
    t = pathlib.Path(s).read_text(); slug = os.path.basename(os.path.dirname(s))
    if "#L" in t:
        print(f"FAIL retired line anchor in {slug}"); bad += 1
    m = re.search(r"^\s*row:\s*([a-z0-9][a-z0-9-]*)\s*$", t, re.M)
    if m:
        anchored[slug] = m.group(1)
        if m.group(1) not in gridset:
            print(f"FAIL skill {slug} row '{m.group(1)}' matches no grid row"); bad += 1
    elif not re.search(r"grid_row:\s*null", t):
        print(f"FAIL skill {slug} is a grid-row skill with no `row:` anchor"); bad += 1
orphans = gridset - set(anchored.values())
if orphans:
    print(f"FAIL grid rows with no skill: {sorted(orphans)}"); bad += 1
if bad: sys.exit(1)
print(f"ok  {len(gridset)} grid rows <-> {len(anchored)} anchored skills, no line anchors")
PY

# 6. doctrine_source keys resolve in the register
python3 - <<'PY' || fail=1
import glob, os, pathlib, re, sys
reg = pathlib.Path("docs/roles/sources.md")
if not reg.exists():
    print("FAIL docs/roles/sources.md missing"); sys.exit(1)
keys = set(re.findall(r"^\|\s*`([A-Za-z0-9][A-Za-z0-9._-]*)`\s*\|", reg.read_text(), re.M))
bad = 0
for s in glob.glob("acordia-analysts/skills/*/SKILL.md"):
    t = pathlib.Path(s).read_text(); slug = os.path.basename(os.path.dirname(s))
    m = re.search(r"^\s*doctrine_source:\s*\[(.*?)\]\s*$", t, re.M)
    if not m: continue
    for item in (x.strip() for x in m.group(1).split(",") if x.strip()):
        key = item.split("#", 1)[0]
        if key not in keys:
            print(f"FAIL {slug} cites unregistered work '{key}'"); bad += 1
if bad: sys.exit(1)
print(f"ok  every doctrine_source key resolves in the register ({len(keys)} registered)")
PY

# 7. orchestrator body byte-identical across agents/ and every wrapper that carries it
python3 - <<'PY7' || fail=1
import pathlib, sys
root = pathlib.Path("acordia-analysts")
agent = root/"agents/cyber-analyst.md"
if not agent.exists():
    print(f"FAIL missing {agent}"); sys.exit(1)
_, _, body = agent.read_text().split("---\n", 2)
body = body.strip("\n")
carriers = ["commands/cyber-analyst.md", "commands/analyst.md"]
bad = []
for c in carriers:
    f = root/c
    if not f.exists():
        bad.append(f"{c}: missing"); continue
    if body not in f.read_text():
        bad.append(f"{c}: does not contain the orchestrator body byte-identically")
if bad:
    for b in bad: print(f"FAIL {b}")
    print("     regenerate the wrapper from agents/cyber-analyst.md; they must not be edited apart")
    sys.exit(1)
print(f"ok  orchestrator body identical in agents/ and {len(carriers)} wrappers")
PY7

# 8. prompt-body ceiling — the spec asserts one; nothing enforced it until 6.5.0
python3 - <<'PY8' || fail=1
import pathlib, re, sys
CEILING = 10500
spec = pathlib.Path("openspec/specs/agent-roster/spec.md")
if spec.exists():
    m = re.search(r"SHALL NOT exceed ([\d,]+) characters|SHALL exceed ([\d,]+) characters", spec.read_text())
    if m:
        CEILING = int((m.group(1) or m.group(2)).replace(",", ""))
bad = []
for f in sorted(pathlib.Path("acordia-analysts/agents").glob("*.md")):
    parts = f.read_text().split("---\n", 2)
    if len(parts) < 3:
        bad.append(f"{f.name}: no frontmatter"); continue
    n = len(parts[2].strip())
    if n > CEILING:
        bad.append(f"{f.name}: body {n} chars exceeds ceiling {CEILING}")
if bad:
    for b in bad: print(f"FAIL {b}")
    print("     move technique detail into the skill that owns it; never delete routing or guardrails")
    sys.exit(1)
print(f"ok  every agent body within the {CEILING}-char ceiling")
PY8

# 4. version bump gate — only meaningful on a feature worktree off a base branch
# A linked worktree is where feature work happens: its --git-dir is
# <repo>/.git/worktrees/<slug> while --git-common-dir stays <repo>/.git.
# On the primary checkout the two are equal, and there is nothing to compare against.
if [ "$(git rev-parse --git-dir 2>/dev/null)" != "$(git rev-parse --git-common-dir 2>/dev/null)" ]; then
  wt=yes
else
  wt=no
fi
if [ "$wt" = yes ]; then
  base=""
  for b in develop main; do
    if git show-ref --verify -q "refs/heads/$b" || git show-ref --verify -q "refs/remotes/origin/$b"; then
      base=$b; break
    fi
  done
  if [ -n "$base" ]; then
    # artifacts changed without a version change = bug
    artifacts=$(git diff --name-only "$base"...HEAD -- acordia-analysts 2>/dev/null | grep -vE '\.claude-plugin/plugin\.json' | wc -l | tr -d ' ')
    version_files=$(git diff --name-only "$base"...HEAD -- '*/.claude-plugin/plugin.json' '.claude-plugin/marketplace.json' '.omp-plugin/marketplace.json' 2>/dev/null | wc -l | tr -d ' ')
    if [ "$artifacts" -gt 0 ] && [ "$version_files" -eq 0 ]; then
      say "FAIL $artifacts artifact files changed vs $base but no version file was bumped"; fail=1
    else
      say "ok  version-bump gate (artifacts=$artifacts, version files changed=$version_files vs $base)"
    fi
  fi
fi

[ $fail -eq 0 ] || exit 1
