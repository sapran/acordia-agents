## 1. Make the version shippable

- [x] 1.1 Replace the frozen `VERSION = "1.0.0"` with a hand-maintained `VERSION = "2.0.0"` — MAJOR, because this change reshapes the distribution.
- [x] 1.2 Document the bump obligation on the constant itself: MINOR for any change that reaches a user, MAJOR for the roster or the distribution's shape, real semver, no build metadata.
- [x] 1.3 Regenerate. Confirm exactly the 6 version-carrying files change and `--check` passes.

## 2. Establish the version semantics empirically

- [x] 2.1 Establish omp's comparison behaviour against a real install. **Use bare `omp plugin upgrade`** — a targeted `upgrade <name>@<marketplace>` reinstalls unconditionally and compares nothing, which produced a false positive on the first attempt until an equal-version control and an older-semver control exposed it.
- [x] 2.2 Record the transition table: equal → skip; newer semver → upgrade; older semver → skip; `1.0.0+aaa` → `1.0.0+bbb` → skip.
- [x] 2.3 Confirm the build-metadata form is a real trap and not merely a spec-reading: it is accepted by both harnesses and propagates in neither.

## 3. Write the bump rule where it will be read

- [x] 3.1 Add a top-level `## Bump the version on every change — no exceptions` section to `CLAUDE.md`, above `## Commands`, with the MINOR and MAJOR criteria and the reason the failure mode is silent.
- [x] 3.2 Add the same rule to `README.md` under the generated-trees section.
- [x] 3.3 Retain it in long-term memory so it survives a fresh session.

## 4. Close the command bijection

- [x] 4.1 Fail the build when an agent has no canonical wrapper whose stem equals its own. The forward direction was already enforced; this reverse direction was normative and unchecked.
- [x] 4.2 Verify the assertion fires: removing a canonical wrapper exits non-zero naming that agent, and the committed tree survives intact because the build stages and swaps.

## 5. Correct documentation against verified behaviour

- [x] 5.1 `README.md`: the bare agent name does **not** resolve in Claude Code — it needs `acordia-analysts:<agent>`; omp and opencode are flat. Fix the two places that claimed otherwise.
- [x] 5.2 `README.md`: state that the retired `--harness omp` deployment shadows the plugin and that clearing it is uninstall-then-install, no tooling.
- [x] 5.3 `CLAUDE.md`: add the version and per-harness agent-resolution contracts to the generated-trees section; correct `omp plugin marketplace add ./.` — a bare `.` is rejected.

## 6. Verify

- [x] 6.1 `tools/build-plugins.py --check` clean; shape counts unchanged (4/5 agents, 43/30 skills, 8/9 commands).
- [x] 6.2 Claude Code enforces `disallowedTools`: a leg analyst reported `Bash, Read, Skill, ToolSearch` — `Edit`, `Write`, `NotebookEdit`, `Task` all absent — closing the `reframe-as-plugin` task 8.5 gap.
- [x] 6.3 Claude Code honours the scoped mapping: `fusion-analyst` **has** `Write` while `target-network-analyst` does not, proving the distinction and not merely that something is denied. The write itself was not executed: Claude Code's permission layer gates external-directory writes in headless mode for any agent.
- [x] 6.4 A fresh single-branch clone carries all four plugin trees complete, each with its manifest — nothing needed is gitignored, so relative plugin sources resolve from a clone.
- [x] 6.5 `openspec validate --all --strict` passes.
- [x] 6.6 GitHub-source install, verified after merging to `develop`: `omp plugin marketplace add sapran/acordia-agents` resolves the clone, selects the **omp** tree over the Claude one, and installs `2.0.0`. Claude Code installs from the same shorthand and reports `2.0.0`.
- [x] 6.7 Claude Code's upgrade path, now answerable from a git source: **there isn't one.** `claude plugin update <name>` fails with "Plugin not found" for a marketplace plugin from either a directory or a GitHub source, and `claude plugin install` on an already-installed plugin reports "already installed" without refreshing. Only uninstall-then-reinstall updates it. The version string is therefore informational in Claude Code, which retroactively confirms the semver-versus-non-semver question was an omp-only concern.

## 7. Written and then reverted during this change

Recorded so a later pass does not re-add them.

- [x] 7.1 A **GitHub Actions workflow** running `--check`, `openspec validate`, and `shellcheck`. Deleted: this repository is a markdown distribution with one generator and has deliberately never had a build pipeline; `CLAUDE.md` says so. `--check` is run by hand like every other command here. The `tools/ownership.sh` rewrite made only to satisfy an older distro `shellcheck` was reverted with it.
- [x] 7.2 A **`tools/migrate-omp.sh`**. Deleted: clearing the retired omp deployment is uninstall-then-install, not 140 lines of provenance checking.
- [x] 7.3 A **content-hash version** (`1.0-<hash>` over the sources and the generator). Deleted: forty lines of hashing, plus a checkout-reproducibility bug where a gitignored `.DS_Store` made the version depend on whose machine built it, to avoid typing a number. Removing it also bought back real semver, since a hand-bumped version is monotonic where a hash is not — which retired the per-harness divergence problem the non-semver scheme had created for Claude Code.
