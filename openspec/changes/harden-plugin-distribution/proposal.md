## Why

`reframe-as-plugin` shipped the marketplace and archived cleanly. Reviewing it afterwards surfaced three defects in the thing that had just been declared done.

**The version was hardcoded `1.0.0` with no path to change it.** omp's upgrade-all path compares catalog versions, so a permanently frozen version means an edited agent never reaches an installed user. The distribution had no way to ship a fix — a defect in the distribution mechanism, not in tooling around it.

**The read-only posture in Claude Code was unproven.** An unrecognised `disallowedTools` entry is ignored silently, so a wrong tool name would leave a "read-only" analyst able to write with no error anywhere. `analyst-agent-roster` treats that posture as normative.

**Documentation contradicted verified behaviour.** `README.md` claimed plugin agents are dispatched by bare name in Claude Code; they are namespaced there and the bare name fails outright.

One further gap, in the build rather than the distribution: `acordia-command-namespace` requires a canonical wrapper per agent, and only the reverse direction — a wrapper naming a live agent — was ever enforced.

Current behaviour: an unshippable version, an unverified posture, a false instruction. Desired behaviour: the version derives from content, the posture is verified against a live harness, and the documentation matches what was observed.

## What Changes

### The version derives from source content

`1.0-<hash>`: a hand-kept `VERSION_EPOCH` plus seven hex characters of a sha256 over `analysts/`, `operators/`, `commands/acordia/`, and `tools/build-plugins.py`. The generator is hashed with the sources deliberately — a change to what it *emits* must reach installed users, and hashing only the sources would miss one.

Not a git revision. The version is written into six committed files, so the commit that lands a rebuild would change the SHA that rebuild embeds, and `--check` would then never pass. Content hashing has no fixpoint and keeps working in a dirty tree, a shallow clone, or an export with no `.git`.

Not valid semver, on evidence. Verified against omp 17.1.8: the upgrade-all path reinstalls when two non-semver versions are unequal, in either direction, while two semver versions differing only in build metadata compare **equal** and never upgrade — so `1.0.0+<hash>` would have been a silent no-op, worse than the frozen version it replaced.

Only files that actually ship feed the hash. Paths with a dot-prefixed component or a `__pycache__` segment are skipped, because a stray `.DS_Store` present in one checkout and absent in a clone otherwise makes the version depend on whose machine built it.

### The build closes the command bijection

The generator already failed on a wrapper naming no live agent. It now also fails when an agent has no wrapper whose stem is its own, so adding an agent cannot ship a roster with no handle for it.

### Documentation corrected against verified behaviour

Claude Code namespaces plugin agents (`acordia-analysts:<agent>`; the bare name fails). omp needs `./.` rather than `.` for a local marketplace source. omp surfaces nothing while `claude-plugins` sits in `disabledProviders`. Migrating off the retired `--harness omp` deployment is uninstall-then-install, and needs no tooling — it is stated as a step, not automated.

## Capabilities

### Modified Capabilities

- `plugin-packaging` — version derivation and its non-semver rationale; per-harness agent-name resolution.
- `acordia-command-namespace` — the canonical-wrapper requirement becomes build-enforced.

## Impact

- **Modified:** `tools/build-plugins.py` (version derivation, wrapper bijection), `README.md`, `CLAUDE.md`, and the 6 generated files carrying the version.
- **Unchanged:** every source agent, skill, and command wrapper.
- **Verified during this change:** Claude Code enforces `disallowedTools` (a leg analyst's tools were `Bash, Read, Skill, ToolSearch` — `Edit`/`Write`/`NotebookEdit`/`Task` all absent) and honours the scoped mapping (`fusion-analyst` retains `Write`). A fresh clone of the branch is complete, so relative plugin sources resolve.
- **Still unverified:** Claude Code's upgrade behaviour for a non-semver version, answerable only from a git source once this reaches the default branch.
- **Deliberately not added:** no CI, no hooks, no lint automation. This is a markdown distribution with one generator; `--check` is run by hand, like every other command here.
