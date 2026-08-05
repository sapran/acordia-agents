## Why

`reframe-as-plugin` shipped the marketplace and archived cleanly. Reviewing it afterwards surfaced six findings, four of them defects in the thing that had just been declared done.

**The drift gate was a suggestion.** `plugin-packaging` makes `tools/build-plugins.py --check` normative, `CLAUDE.md` and `README.md` both call it "the gate", and nothing ran it. The repository had no `.github/`, no hook, no CI of any kind. Committed generated output with no enforcement is a drift machine.

**The version was hardcoded `1.0.0` with no path to change it.** omp's upgrade-all path compares catalog versions; a permanently frozen version means an edited agent never reaches an installed user. The distribution had no way to ship a fix.

**The read-only posture in Claude Code was unproven.** An unrecognised `disallowedTools` entry is ignored silently, so a typo would leave a "read-only" analyst able to write with no error anywhere.

**Existing omp users are silently shadowed.** The retired `--harness omp` path left translated agents in `~/.omp/agent/agents/`, which omp resolves *before* plugin roots and dedups first-wins. Installing the plugin over an old deployment runs the old prompts, undetectably.

Two smaller ones: the GitHub-source install path had never been exercised (only a local directory), and `README.md` claimed plugin agents are dispatched by bare name in Claude Code, which is false.

Current behaviour: an unenforced gate, an unshippable version, an unverified posture, and a shadowing hazard. Desired behaviour: CI enforces the gate, the version derives from content, the posture is verified, and the hazard has a migration.

## What Changes

### The version derives from source content

`1.0-<hash>`: a hand-kept `VERSION_EPOCH` plus seven hex characters of a sha256 over `analysts/`, `operators/`, `commands/acordia/`, and `tools/build-plugins.py`. The generator is hashed with the sources deliberately — a change to what it *emits* must reach installed users, and hashing only the sources would miss it.

Not a git revision. The version is written into six committed files, so the commit that lands a rebuild would change the SHA that rebuild embeds, and `--check` would fail on every push forever. Content hashing has no fixpoint and keeps working in a dirty tree, a shallow clone, or an export with no `.git`.

Not valid semver, on purpose and on evidence. Verified against omp 17.1.8: bare `omp plugin upgrade` reinstalls when two non-semver versions are unequal, in either direction, while two semver versions differing only in build metadata compare **equal** and never upgrade — so the obvious `1.0.0+<hash>` would have been a silent no-op.

### CI enforces every gate the specs already declare

`.github/workflows/check.yml` on pull request and push: `build-plugins.py --check`, `openspec validate --all --strict`, and `shellcheck -x` over the four shell files. It **fails** on drift rather than auto-committing a rebuild, so the generated diff stays part of the reviewed change.

The build additionally gains the missing half of the command bijection: `acordia-command-namespace` requires a canonical wrapper per agent, and only the reverse direction was enforced.

### A migration for the retired omp deployment

`tools/migrate-omp.sh`, dry-run by default. It cannot reuse `tools/ownership.sh` — that file's agent test is now byte-identity, and these agents are translated files that never matched their source — so it carries the provenance rule the old installer used: `by: tools/translate-omp.py` plus a `from:` path that really exists in this repository.

### Documentation corrected against verified behaviour

Claude Code namespaces plugin agents (`acordia-analysts:<agent>`; the bare name fails). omp needs `./.` rather than `.` for a local marketplace source. omp surfaces nothing while `claude-plugins` sits in `disabledProviders`.

## Capabilities

### Modified Capabilities

- `plugin-packaging` — version derivation and its non-semver rationale; CI as the enforcing gate; per-harness agent-name resolution.
- `acordia-command-namespace` — the canonical-wrapper requirement becomes build-enforced.
- `omp-harness-distribution` — adds the migration requirement for the retired deployment.

## Impact

- **New:** `.github/workflows/check.yml`, `tools/migrate-omp.sh`.
- **Modified:** `tools/build-plugins.py` (version derivation, wrapper bijection), `README.md`, `CLAUDE.md`, and the 6 generated files carrying the version.
- **Unchanged:** every source agent, skill, and command wrapper.
- **Verified during this change:** Claude Code enforces `disallowedTools` (a leg analyst's tools were `Bash, Read, Skill, ToolSearch` — `Edit`/`Write`/`NotebookEdit`/`Task` all absent) and honours the scoped mapping (`fusion-analyst` retains `Write`). A fresh clone of the branch is complete, so relative plugin sources resolve.
- **Still unverified:** Claude Code's upgrade behaviour for a non-semver version, answerable only from a git source once this reaches the default branch.
