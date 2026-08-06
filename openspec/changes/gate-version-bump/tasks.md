## 1. Base resolution

- [x] 1.1 Add a helper to `tools/build-plugins.py` that resolves the comparison base: try `origin/develop`, `origin/main`, `develop`, `main` in order via `git rev-parse --verify`, then `git merge-base HEAD <ref>`. Return `None` when git is absent, the tree is not a checkout, or no ref resolves. Every `subprocess` failure and `OSError` resolves to `None` rather than raising.
- [x] 1.2 Add a semver parse helper returning an integer 3-tuple, and `None` for anything that does not parse as strict `MAJOR.MINOR.PATCH`.

## 2. The version gate

- [x] 2.1 Add a `version_gate(repo_root)` returning a list of problem strings: resolve the base; read `VERSION` at that base via `git show <base>:tools/build-plugins.py`; list tracked files differing from the base under `analysts/`, `operators/`, `commands/acordia/` via `git diff --name-only <base> -- <paths>`; if any differ and the current version is not strictly greater than the base version, report the changed paths and both versions.
- [x] 2.2 Return an explicit skip — no problems, a printed note — when the base is unresolvable or either version fails to parse.
- [x] 2.3 Call it from `check()` only, never from the plain build path, and fold its problems into the existing non-zero exit alongside drift problems.

## 3. Verify the gate against real history

- [x] 3.1 Prove the true positive against the actual defect: in a throwaway worktree at `cc7339a`, confirm the gate reports the changed source path and the unmoved version. This is the commit that motivated the change, so it is the regression proof.
- [x] 3.2 Prove the true negative: at `97c6b40`, the commit that did bump, confirm the gate passes.
- [x] 3.3 Prove the current branch passes, since it changed sources and bumped `2.2.0` → `2.3.0`.
- [x] 3.4 Prove one-bump-per-branch: with the branch already bumped, touch a source file and confirm the gate still passes rather than demanding a second bump.
- [x] 3.5 Prove the docs-only case: a tree whose only differences lie outside the three source paths passes with the version unchanged.
- [x] 3.6 Prove the degradation path: with no resolvable base, confirm `--check` reports the gate as skipped and does not fail.
- [x] 3.7 Prove the plain build is unaffected: with a source change and no bump, confirm `python3 tools/build-plugins.py` still succeeds.

## 4. Regression and integration

- [x] 4.1 Confirm `--check` is clean on the current branch with the gate in place.
- [x] 4.2 Confirm the generator remains deterministic and the generated trees are byte-identical, since this change must emit nothing.
- [x] 4.3 Confirm the frontmatter gate still fires, so the two gates coexist on the check path.
