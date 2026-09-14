## 1. Foundation

- [x] 1.1 Add the proposal, design and `skill-library` delta for `resolvable-reference-pointers`, with the failure established from the live session record on the operator's workstation (2026-09-14) rather than from recollection.
- [x] 1.2 Record that no literature search was run and why: the change decides how a body addresses a file it ships, which is distribution mechanism rather than a doctrinal claim, so it carries no `doctrine_source` and adds no attribution.

## 2. Pointers

- [x] 2.1 Rewrite the four pointers in `acordia-analysts/skills/credential-harvest-triage/SKILL.md` — step 3's pattern-library mention, step 9's report-layout pointer, and the `## Pattern library` and `## Report layout` paragraphs — so each carries `skill://credential-harvest-triage/references/<file>.md` as its link target with the file's own name as visible text.
- [x] 2.2 Rewrite the cross-skill reference pointers in `implant-payload-re`, `web-api-authflow-analysis` and `log-artefact-interpretation` to the same URI, removing the `../credential-harvest-triage/references/…` targets, and keep each sentence in its skill's own voice rather than leaving a filename in a noun-modifier slot.
- [x] 2.3 Rewrite `aleph-entity-graph`'s bare code-span mention of the marker set into the same linked form, so the pointer that the published `aleph-entity-graph` requirement asks for is now openable.
- [x] 2.4 Rewrite the seven `[`credential-harvest-triage`](../credential-harvest-triage/SKILL.md)` pointers — `cloud-controlplane-analysis`, `disk-memory-forensics`, `identity-directory-trust`, `implant-payload-re`, `log-artefact-interpretation`, `os-host-internals`, `web-api-authflow-analysis` — to `skill://credential-harvest-triage`, the address the failing sweep is on record as resolving.
- [x] 2.5 Add the addressing rule to `credential-harvest-triage`'s `## Cross-cutting notice`: both addresses stated literally, the refusal to reconstruct a path into a harness skills directory, and the terminal behaviour when neither address opens — ask the operator, never search the filesystem for a copy.

## 3. Verification

- [x] 3.1 Assert the exact occurrence count of every substitution before applying it, then scan every markdown link target under `acordia-analysts/skills/` for one beginning with neither `skill://` nor `http` — expect none.
- [x] 3.2 Prove the URI resolves on the deployed host: a print-mode session reads `skill://credential-harvest-triage/references/report-layout.md`, and the resolved path is taken from the session's tool record rather than from the model's reply.
- [x] 3.3 Run the four `CLAUDE.md` invariant checks — prompt slug resolution, grid-mark transcription, catalog byte-identity with all four JSON files parsing, and skill-set declaration against the prompts.
- [x] 3.4 Confirm after the sync that the published requirement and the archived delta carry an identical requirement block, and that no requirement or scenario was lost.

## 4. Release mechanics

- [x] 4.1 Bump `6.13.0` → `6.14.0` in lockstep across `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and `.omp-plugin/marketplace.json`.
- [ ] 4.2 Regenerate `acordia-map.html` for 6.14.0 in the main checkout as a follow-up `docs:` commit on the integration branch after merge — the map is derived from the merged tree and is never written into a worktree — and confirm the landing page paints with its agent and skill counts intact.
- [x] 4.3 `~/ai/checks/check-acordia.sh` in the worktree, before the PR.
- [x] 4.4 `openspec validate --all --strict`.
