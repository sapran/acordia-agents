## 1. Foundation

- [x] 1.1 Add the proposal, design and `skill-library` delta for `resolvable-reference-pointers`, with the failure established from the live session record on `mini` (`opwe` profile, 2026-09-14T10:35:01Z) rather than from recollection.
- [x] 1.2 Record that no literature search was run and why: the change decides how a body addresses a file it ships, which is distribution mechanism rather than a doctrinal claim, so it carries no `doctrine_source` and adds no attribution.

## 2. Pointers

- [x] 2.1 Rewrite the four pointers in `acordia-analysts/skills/credential-harvest-triage/SKILL.md` — step 3's pattern-library mention, step 9's report-layout pointer, and the `## Pattern library` and `## Report layout` paragraphs — so each carries `skill://credential-harvest-triage/references/<file>.md` as its link target with the relative filename as visible text.
- [x] 2.2 Rewrite the cross-skill pointers in `implant-payload-re`, `web-api-authflow-analysis` and `log-artefact-interpretation` to the same URI, removing the `../credential-harvest-triage/references/…` targets.
- [x] 2.3 Rewrite `aleph-entity-graph`'s bare code-span mention of the marker set into the same linked form, so the pointer that the published `aleph-entity-graph` requirement asks for is now openable.
- [x] 2.4 Add the addressing rule to `credential-harvest-triage`'s `## Cross-cutting notice`: where the files ship, the two addresses that open them, and the refusal to reconstruct a path into a harness skills directory.

## 3. Verification

- [x] 3.1 Assert the exact occurrence count of every substitution before applying it, and scan all 45 skills afterwards for any link target containing `references/` that does not begin `skill://` — expect none.
- [x] 3.2 Prove the URI resolves on the deployed host: a print-mode `opwe` session reads `skill://credential-harvest-triage/references/report-layout.md`, and the resolved path is taken from the session's tool record rather than from the model's reply.
- [x] 3.3 Run the four `CLAUDE.md` invariant checks — prompt slug resolution, grid-mark transcription, catalog byte-identity with all four JSON files parsing, and skill-set declaration against the prompts.

## 4. Release mechanics

- [x] 4.1 Bump `6.13.0` → `6.14.0` in lockstep across `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and `.omp-plugin/marketplace.json`.
- [x] 4.2 Regenerate `acordia-map.html` for 6.14.0 in the main checkout as a follow-up `docs:` commit on the integration branch — the map is derived from the merged tree and is never written into a worktree — and confirm the landing page paints with its agent and skill counts intact.
- [x] 4.3 `~/ai/checks/check-acordia.sh` in the worktree, before the PR.
- [x] 4.4 `openspec validate --all --strict`.
