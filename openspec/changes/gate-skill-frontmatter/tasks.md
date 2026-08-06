## 1. The generator gains the gate

- [x] 1.1 Add a `read_skill(path)` helper in `tools/build-plugins.py` alongside `read_agent()`, parsing a `SKILL.md` frontmatter block through the existing `split_frontmatter()` so a non-mapping raises `TranslationError` on the same path agents already use.
- [x] 1.2 Validate in `read_skill()`: `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, is ≤64 chars, and equals the containing directory name; `description` is 1–1024 chars; top-level keys are a subset of `{name, description, metadata}`; none of `sha256`, `signature`, `signed_by` is present. Each failure raises `TranslationError` naming the source path and the specific violation.
- [x] 1.3 Call the validation from `build()` for every `SKILL.md` in both pillars, before the skill tree is copied, so a violation fails before any staged tree is swapped into place.

## 2. Prove the gate catches the real defect

- [x] 2.1 With the gate in place and the description still malformed, run `python3 tools/build-plugins.py` and confirm it exits non-zero naming `analysts/skills/exhaustive-data-processing/SKILL.md`. This is the regression proof — the gate must be shown failing on the actual defect before that defect is repaired.
- [x] 2.2 Confirm both committed plugin trees are unchanged after that failed run, satisfying the staged-build guarantee.

## 3. The skill body is repaired

- [x] 3.1 Single-quote the `description` value at `analysts/skills/exhaustive-data-processing/SKILL.md:3`, changing no wording. Verified during design: the value contains no apostrophe, and the quoted form yields the identical 345-character description.
- [x] 3.2 Re-run `python3 tools/build-plugins.py` and confirm it now succeeds.

## 4. The version is bumped

- [x] 4.1 Set `VERSION` in `tools/build-plugins.py` to `2.3.0` — MINOR, because a repaired skill body reaches installed users.

## 5. Generated trees are regenerated and gate-checked

- [x] 5.1 Rebuild so the repaired skill and the new version land in both `plugins/` trees and the six version-carrying files.
- [x] 5.2 Run `python3 tools/build-plugins.py --check` and confirm a clean exit with no drift.
- [x] 5.3 Confirm the generator is still deterministic: run it twice and verify the second run leaves the tree byte-identical.

## 6. Whole-library verification

- [x] 6.1 Parse the frontmatter of all 73 source skills across both pillars and confirm zero failures, matching the pre-change measurement of exactly one.
- [x] 6.2 Confirm the defect is gone from both generated copies at `plugins/claude/acordia-analysts/skills/exhaustive-data-processing/SKILL.md` and the omp equivalent.
- [x] 6.3 Confirm the repaired `description` still satisfies its trigger-quality requirement — the wording is unchanged, so this is a read-back, not a rewrite.
