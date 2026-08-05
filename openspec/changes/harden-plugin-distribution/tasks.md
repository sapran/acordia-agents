## 1. Derive the version from source content

- [x] 1.1 Replace the `VERSION = "1.0.0"` constant with `VERSION_EPOCH = "1.0"` and a `VERSION_INPUTS` tuple naming `analysts`, `operators`, `commands/acordia`, and `tools/build-plugins.py`.
- [x] 1.2 Add `source_version(repo_root)`: sha256 over each input's files in sorted order, hashing the repository-relative path and then the bytes, returning `f"{VERSION_EPOCH}-{digest[:7]}"`. Document why it is not a git revision and why it is not semver.
- [x] 1.3 Thread the derived version through `plugin_manifest()`, `marketplace()`, and `build()` so it is computed once per build from the real sources, never from the staging directory.
- [x] 1.4 Regenerate. Confirm exactly the 6 version-carrying files change.

## 2. Establish the version semantics empirically

- [x] 2.1 Confirm determinism: two consecutive builds leave the tree byte-identical and `--check` passes.
- [x] 2.2 Confirm sensitivity: a source edit and a generator edit each produce a distinct hash, and all three values differ.
- [x] 2.3 Establish omp's comparison behaviour against a real install. **Use bare `omp plugin upgrade`** — a targeted `upgrade <name>@<marketplace>` reinstalls unconditionally and compares nothing, which produced a false positive on the first attempt until an equal-version control and an older-semver control exposed it.
- [x] 2.4 Record the transition table: equal → skip; hash → different hash → upgrade (either direction); `1.0.0+aaa` → `1.0.0+bbb` → skip; non-semver → `1.0.0` → skip; `2.0.0` → `1.5.0` → skip.
- [x] 2.5 Confirm Claude Code accepts a non-semver version: install, `plugin details`, and `plugin list` all render `1.0-<hash>` with no validation error. Record that its upgrade behaviour for one remains unverified, a directory-sourced marketplace being read live there.

## 3. Enforce the gates in CI

- [x] 3.1 Add `.github/workflows/check.yml` on `pull_request` and `push` to `develop`/`main`, with `contents: read` only.
- [x] 3.2 Run `tools/build-plugins.py --check` via `astral-sh/setup-uv` — the generator is a uv script and resolves its own interpreter and dependencies from its inline metadata.
- [x] 3.3 Run `npx -y @fission-ai/openspec@1 validate --all --strict`.
- [x] 3.4 Run `shellcheck -x` over `install.sh`, `uninstall.sh`, and `tools/*.sh`. `-x` is required: without it the sourced helpers raise SC1091.
- [x] 3.5 Confirm the workflow fails on drift rather than committing a rebuild.

## 4. Close the command bijection

- [x] 4.1 Fail the build when an agent has no canonical wrapper whose stem equals its own. The forward direction was already enforced; this reverse direction was normative and unchecked.

## 5. Migration for the retired omp deployment

- [x] 5.1 Add `tools/migrate-omp.sh`, dry-run by default, `--apply` to remove, `--target` to override the omp agent root.
- [x] 5.2 Give it its own agent evidence rule — `by: tools/translate-omp.py` plus a `from:` path resolving to a real file in the repository — because `tools/ownership.sh` now tests agents by byte-identity, which no translated file satisfies. Skills keep the shared rule.
- [x] 5.3 Explain in the header why these leftovers shadow the plugin, not merely age.
- [x] 5.4 Verify against the real stale deployment on this machine: 9 translated agents and 73 skills identified, 0 skipped, nothing removed without `--apply`.
- [x] 5.5 `shellcheck -x` clean.

## 6. Correct documentation against verified behaviour

- [x] 6.1 `README.md`: the bare agent name does **not** resolve in Claude Code — it needs `acordia-analysts:<agent>`; omp and opencode are flat. Fix the two places that claimed otherwise.
- [x] 6.2 `README.md`: document the version scheme, the fixpoint reason it is content-derived, and the evidence it is non-semver, including the targeted-upgrade trap.
- [x] 6.3 `README.md`: add the migration section, stating that the old deployment silently shadows the plugin.
- [x] 6.4 `CLAUDE.md`: add the version and CI contracts and the per-harness agent-resolution note to the generated-trees section; add the migration script and `shellcheck` to the commands block; correct `omp plugin marketplace add ./.` — a bare `.` is rejected.

## 7. Verify

- [x] 7.1 `tools/build-plugins.py --check` clean; shape counts unchanged (4/5 agents, 43/30 skills, 8/9 commands).
- [x] 7.2 `shellcheck -x` clean across all four shell files.
- [x] 7.3 Claude Code enforces `disallowedTools`: a leg analyst reported `Bash, Read, Skill, ToolSearch` — `Edit`, `Write`, `NotebookEdit`, `Task` all absent — closing the `reframe-as-plugin` task 8.5 gap.
- [x] 7.4 Claude Code honours the scoped mapping: `fusion-analyst` **has** `Write` while `target-network-analyst` does not, proving the distinction and not merely that something is denied. The write itself was not executed: Claude Code's permission layer gates external-directory writes in headless mode for any agent.
- [x] 7.5 A fresh single-branch clone carries all four plugin trees complete, each with its manifest — nothing needed is gitignored, so relative plugin sources resolve from a clone.
- [x] 7.6 `openspec validate --all --strict` passes.
- [ ] 7.7 **Blocked until this branch is the default branch:** `omp plugin marketplace add sapran/acordia-agents` (GitHub shorthand clones the default branch, and `add` takes no ref flag), and Claude Code's upgrade behaviour for a non-semver version from a git source.
