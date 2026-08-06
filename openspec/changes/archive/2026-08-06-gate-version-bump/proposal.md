## Why

`plugin-packaging` already requires the version to be "bumped by whoever changes a source artifact," and `CLAUDE.md:22` calls an unbumped source edit "a release bug." Commit `cc7339a` — "docs: align the Aleph skill with the seventeen-tool server surface" — edited a source skill under `analysts/` and bumped nothing. Nothing caught it. It reached users only because `97c6b40` happened to bump to `2.2.0` an hour and a half later and swept it up.

Had `cc7339a` been the last commit before a release, the edit would never have arrived at anyone with the plugin already installed, and the failure is silent by construction: omp compares the catalog version against the installed one and skips when they match, so there is no error, no warning, and nothing to distinguish "up to date" from "your fix never shipped."

This is the same defect class the skill-frontmatter gate just closed — a contract stated in the specs and in contributor guidance, enforced nowhere. The generator gained the ability to fail on a malformed skill; it still cannot fail on an unbumped version.

Current behavior: a source artifact can change with `VERSION` untouched, and every gate in the repository passes. Desired behavior: `--check`, the gate that is already run before committing generated output, refuses a source change that carries no version bump.

## What Changes

### The generator — `--check` gains a version-drift gate

`tools/build-plugins.py --check` compares the working tree against a git base and fails when source artifacts changed but `VERSION` did not.

- **Source scope**: `analysts/`, `operators/`, and `commands/acordia/` — exactly the three paths `CLAUDE.md` names as triggering the obligation.
- **Base**: the merge base with the integration branch, resolved as the first of `origin/develop`, `origin/main`, `develop`, `main` that exists — so the comparison is per release, not per commit.
- **Comparison**: if any tracked file under those three paths differs from the base, `VERSION` must be strictly greater than the base's `VERSION`, compared as a semver tuple.
- **Failure**: exits non-zero naming the changed source paths, the base version, and the current one.
- **Degradation**: when git is unavailable, the repository is not a git checkout, or no base branch resolves, the check prints that it was skipped and does not fail. A missing base is not evidence of a missing bump.

The gate is added to `--check` only, never to a plain build. A plain build runs constantly during editing, and failing it on an unbumped version would make the generator unusable for its main purpose.

**Deliberately not added:** no CI, no pre-commit hook, no new script. Consistent with `harden-plugin-distribution` and with the frontmatter gate, this extends the one gate that already exists and is run by hand.

**Not in scope:** the `Method`-contract coverage gap across grid skills, tracked as its own change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plugin-packaging`: the existing requirement "The plugin version is hand-maintained and bumped on every change" gains enforcement. Today it states an obligation and records that the obligation must appear in contributor guidance; it does not require any gate to verify it. The requirement is modified to add that `--check` refuses a source change with no bump, with the base-branch semantics and the skip-on-missing-git degradation stated as part of the contract.

## Impact

- **Modified:** `tools/build-plugins.py` — a version-drift check invoked from `check()`.
- **Unchanged:** every agent prompt, every skill, every command wrapper, and all generated output. This change adds no artifact and alters no emitted byte, so `--check`'s existing drift comparison is unaffected.
- **Behavioral risk:** a false positive would block a legitimate build-check. The gate is scoped to three source paths and skips cleanly when it cannot resolve a base, so the failure mode under uncertainty is silence rather than obstruction.
- **Verified before proposing:** `cc7339a` changed one file under `analysts/` with no `VERSION` line in its diff, and `97c6b40` is the commit that later moved the version — so the gate proposed here would have failed on `cc7339a` at the moment it was authored.
