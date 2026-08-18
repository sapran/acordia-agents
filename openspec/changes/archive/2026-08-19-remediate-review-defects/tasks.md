## 1. The generator

- [x] 1.1 `relative_files()` skips `.DS_Store` so a Finder artifact is not reported as generator drift
- [x] 1.2 `agent_color()` reads `metadata.acordia.role` alone; the `leg` fallback is removed
- [x] 1.3 Fatal gate: every agent declares `metadata.acordia.pillar` matching its source directory, `role` in `{orchestrator, specialist}` with `role: orchestrator` iff `mode: primary`, and no `leg`
- [x] 1.4 Fatal gate: every skill slug in a `·`-separated prompt line resolves in that agent's own pillar; skill lines are recognised by shape, not by heading string
- [x] 1.5 Fatal gate: every write-capable agent's `bash` deny set equals the canonical `OPERATOR_BASH_DENIES` constant
- [x] 1.6 A path-scoped `edit` appends `write` in omp, matching Claude Code; the `write_access` note states the outcome
- [x] 1.7 `browser: allow` gets a Claude-side comment note in the existing unmappable-posture style
- [x] 1.8 `--doctor`: install-state skew, native shadowing, prompt sizes, orphan skills, description proximity, prompt/skill duplication; exits 0, `--strict` makes the first two fatal
- [x] 1.9 `VERSION` 2.4.0 → 2.5.0

## 2. Agent sources

- [x] 2.1 All nine agents carry `metadata.acordia.{pillar, role}`; `leg` removed; analysts keep `column` and `source_paragraph`
- [x] 2.2 `analyst-loop` joins `operational-analyst`'s defining-spine line, first
- [x] 2.3 All four analysts declare `webfetch: allow` and `websearch: allow`
- [x] 2.4 `internal-network.md`'s three title-cased H2 headings move to sentence case

## 3. Documents

- [x] 3.1 Three placeholder spec Purposes written from the requirements present in each file
- [x] 3.2 `docs/implementation-notes.md`'s stale entry retired against current code
- [x] 3.3 `CLAUDE.md` and `README.md` narrow the omp marketplace-runtime claim to "no separate discovery path"

## 4. Build and verify

- [x] 4.1 Rebuild both plugin trees and the two catalogs
- [x] 4.2 `tools/build-plugins.py --check` exits 0
- [x] 4.3 `tools/build-plugins.py --doctor` run and its output recorded
- [x] 4.4 `openspec validate --all --strict` passes
