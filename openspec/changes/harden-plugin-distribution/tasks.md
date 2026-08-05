## 1. Derive the version from source content

- [x] 1.1 Replace the `VERSION = "1.0.0"` constant with `VERSION_EPOCH = "1.0"` and a `VERSION_INPUTS` tuple naming `analysts`, `operators`, `commands/acordia`, and `tools/build-plugins.py`.
- [x] 1.2 Add `source_version(repo_root)`: sha256 over each input's files in sorted order, hashing the repository-relative path and then the bytes, returning `f"{VERSION_EPOCH}-{digest[:7]}"`. Document why it is not a git revision and why it is not semver.
- [x] 1.3 Skip any path with a dot-prefixed component or a `__pycache__` segment, so only what ships feeds the hash.
- [x] 1.4 Thread the derived version through `plugin_manifest()`, `marketplace()`, and `build()` so it is computed once per build from the real sources, never from the staging directory.
- [x] 1.5 Regenerate. Confirm exactly the 6 version-carrying files change.

## 2. Establish the version semantics empirically

- [x] 2.1 Confirm determinism: two consecutive builds leave the tree byte-identical and `--check` passes.
- [x] 2.2 Confirm sensitivity: a source edit and a generator edit each produce a distinct hash, and all three values differ.
- [x] 2.3 Confirm reproducibility across checkouts: build in a clean clone and compare the hash with the committed one. This is how the `.DS_Store` leak was caught — 101 files locally against 100 in the clone.
- [x] 2.4 Establish omp's comparison behaviour against a real install. **Use bare `omp plugin upgrade`** — a targeted `upgrade <name>@<marketplace>` reinstalls unconditionally and compares nothing, which produced a false positive on the first attempt until an equal-version control and an older-semver control exposed it.
- [x] 2.5 Record the transition table: equal → skip; hash → different hash → upgrade (either direction); `1.0.0+aaa` → `1.0.0+bbb` → skip; non-semver → `1.0.0` → skip; `2.0.0` → `1.5.0` → skip.
- [x] 2.6 Confirm Claude Code accepts a non-semver version: install, `plugin details`, and `plugin list` all render `1.0-<hash>` with no validation error. Record that its upgrade behaviour for one remains unverified, a directory-sourced marketplace being read live there.

## 3. Close the command bijection

- [x] 3.1 Fail the build when an agent has no canonical wrapper whose stem equals its own. The forward direction was already enforced; this reverse direction was normative and unchecked.
- [x] 3.2 Verify the assertion fires: removing a canonical wrapper exits non-zero naming that agent, and the committed tree survives intact because the build stages and swaps.

## 4. Correct documentation against verified behaviour

- [x] 4.1 `README.md`: the bare agent name does **not** resolve in Claude Code — it needs `acordia-analysts:<agent>`; omp and opencode are flat. Fix the two places that claimed otherwise.
- [x] 4.2 `README.md`: document the version scheme, the fixpoint reason it is content-derived, and the evidence it is non-semver, including the targeted-upgrade trap.
- [x] 4.3 `README.md`: state that the retired `--harness omp` deployment shadows the plugin and that clearing it is uninstall-then-install, no tooling.
- [x] 4.4 `CLAUDE.md`: add the version contract and the per-harness agent-resolution note to the generated-trees section; correct `omp plugin marketplace add ./.` — a bare `.` is rejected.

## 5. Verify

- [x] 5.1 `tools/build-plugins.py --check` clean; shape counts unchanged (4/5 agents, 43/30 skills, 8/9 commands).
- [x] 5.2 Claude Code enforces `disallowedTools`: a leg analyst reported `Bash, Read, Skill, ToolSearch` — `Edit`, `Write`, `NotebookEdit`, `Task` all absent — closing the `reframe-as-plugin` task 8.5 gap.
- [x] 5.3 Claude Code honours the scoped mapping: `fusion-analyst` **has** `Write` while `target-network-analyst` does not, proving the distinction and not merely that something is denied. The write itself was not executed: Claude Code's permission layer gates external-directory writes in headless mode for any agent.
- [x] 5.4 A fresh single-branch clone carries all four plugin trees complete, each with its manifest — nothing needed is gitignored, so relative plugin sources resolve from a clone.
- [x] 5.5 `openspec validate --all --strict` passes.
- [ ] 5.6 **Blocked until this branch is the default branch:** `omp plugin marketplace add sapran/acordia-agents` (GitHub shorthand clones the default branch, and `add` takes no ref flag), and Claude Code's upgrade behaviour for a non-semver version from a git source.

## 6. Reverted during this change

- [x] 6.1 A GitHub Actions workflow running `--check`, `openspec validate`, and `shellcheck` was added and then **deleted**. This repository is a markdown distribution with one generator and has deliberately never had a build pipeline; `CLAUDE.md` says so. `--check` is run by hand like every other command here. The `tools/ownership.sh` rewrite made only to satisfy an older distro `shellcheck` was reverted with it.
- [x] 6.2 A `tools/migrate-omp.sh` was written and **deleted**. Clearing the retired omp deployment is uninstall-then-install; it does not warrant 140 lines of provenance checking.
