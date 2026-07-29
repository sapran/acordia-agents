## 1. Shared ownership predicate

- [x] 1.1 Create `tools/ownership.sh` holding `owned_by_repo` verbatim from `uninstall.sh` (symlink / byte-identical file / translated-agent `from:` provenance / skill `SKILL.md` comparison), with a header comment stating it is sourced, not executed, and that `REPO_ROOT` must be set by the caller
- [x] 1.2 Replace the definition in `uninstall.sh` with a `source` of the shared file, keeping the explanatory comment at the call site
- [x] 1.3 Verify `./uninstall.sh --dry-run --harness both` still reports the same owned/skipped counts as before the extraction — output diffed byte-identical against `git show HEAD:uninstall.sh`

## 2. Install-time guard

- [x] 2.1 Source `tools/ownership.sh` in `install.sh`
- [x] 2.2 Add `--force` to argument parsing, the `usage()` text, and the header comment block
- [x] 2.3 Assert ownership for every destination in a `preflight()` pass that runs before any file is written, so a collision aborts with the harness untouched rather than half-deployed; `assert_replaceable` prints the conflicting path and exits non-zero, or reports and counts the overwrite under `--force`
- [x] 2.4 Cover skill directories in the same pass, comparing `SKILL.md` — superseded the original plan of gating inside `deploy_file`/`deploy_dir`, which refused only once it had already deployed the artifacts sorting before the collision
- [x] 2.5 Confirm the guard runs under `--dry-run` (it only reads) and makes a colliding dry run exit non-zero

## 3. Agent provenance tags

- [x] 3.1 Prepend `ACORDIA Analysis — ` to the `description` of all four agents under `analysts/agents/`, leaving the routing sentence and every permission block untouched
- [x] 3.2 Prepend `ACORDIA Operations — ` to the `description` of all five agents under `operators/agents/`, same constraint
- [x] 3.3 Confirm no agent name, filename, `task:` whitelist entry, or skill slug changed — the diff over both `agents/` trees touches 9 lines, all of them `description:`

## 4. Documentation

- [x] 4.1 Record the description tag in the `### Agents` format contracts for both pillars in `CLAUDE.md`, and note under "Extending the repo" that names and slugs stay unprefixed and why
- [x] 4.2 Document `--force`, the refuse-on-unowned behaviour, and the per-checkout nature of ownership in `README.md` (new "Namespace safety" section) and in `CLAUDE.md`'s commands block

## 5. Verification

- [x] 5.1 A previous deployment made from this checkout tests as owned: a repeat `./install.sh` replaces it and exits zero (5.4). Ownership is per checkout, so a dry run from a *different* checkout over an existing deployment correctly refuses — documented in `README.md` rather than treated as a defect
- [x] 5.2 With a scratch `--target` root seeded with a foreign `agents/operational-analyst.md` and a foreign `skills/analyst-loop/`, both the dry run and the real run exit 1 and leave the scratch root byte-identical (`diff -r` clean)
- [x] 5.3 The same scratch case with `--force` exits zero, replaces both, and reports `replaced 2 artifact(s) this repository did not deploy`
- [x] 5.4 A real install into an empty scratch root, run twice, deploys 46 artifacts both times and exits zero — for opencode/link and for omp/copy; an omp re-install whose source agent changed since the last run is still owned via its generated provenance and exits zero
- [x] 5.5 `opencode debug agent operational-analyst` against a scratch config root resolves the tagged description; the translated omp `operator.md` carries it too, with `--autoload deep` still populating `autoloadSkills`
- [x] 5.6 `openspec validate --all --strict` passes
