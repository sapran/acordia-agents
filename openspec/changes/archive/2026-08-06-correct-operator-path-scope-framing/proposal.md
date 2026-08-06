## Why

`reframe-report-sink-convention` corrected the analyst pillar's framing of the report sink: a path-scoped `edit` rule declares a destination, and **no harness enforces it**, because `bash: allow` is an open write channel at any path in all three.

The operators pillar carries the same claim in the opposite direction and it went uncorrected, because that change deliberately scoped itself to the analyst capabilities. Three live sites justify the operators' unscoped `edit: allow` by asserting that a path-scoped rule *would* be enforced somewhere:

- `openspec/specs/operator-agent-roster/spec.md` line 72 — "a scoped rule would be enforced in opencode and silently absent in omp"
- `CLAUDE.md` line 103 — "a scoped rule would hold in opencode and silently evaporate in omp"
- `docs/agents-skills-extension-workbook.md` lines 646–648 — "a scoped rule would hold in opencode and silently evaporate in omp"

All three are false in effect for exactly the reason the analyst change established. Every operator agent sets `bash: allow` (with per-pattern denies that omp and Claude Code do not enforce either), so a hypothetical path-scoped `edit` on an operator would be defeated by a shell redirection in opencode too. The asymmetry the three sites describe — enforced in one harness, absent in another — does not exist.

A fourth site states the right conclusion from a narrower reason. `openspec/specs/harness-tool-translation/spec.md` line 34 requires the `.acordia/ops/` journal to be "described in prompts as discipline, not enforced as a permission scope, **because omp cannot scope a tool to a path**". The requirement is correct; the causal clause credits the gap to omp alone, which is the framing being retired.

The decision these sites defend is untouched and remains right: operators keep `edit: allow`, unscoped, and the journal stays prose discipline. Only the argument for it is wrong, and a wrong argument in a normative spec propagates — `2026-07-31-aleph-data-access` already reasoned from it by analogy when placing the Aleph read-only boundary upstream.

**Current behaviour:** three live artifacts justify the operators' unscoped write posture with a harness asymmetry that does not exist, and a fourth attributes universal non-enforcement to omp specifically. The analyst pillar now says the opposite of its sibling about the same mechanism.

**Desired behaviour:** every live site gives the same reason the analyst capabilities now give — a path-scoped `edit` rule is unenforceable in every harness because `bash` writes anywhere, so the operators' `edit: allow` is honest rather than a concession to omp. The `.acordia/ops/` journal remains discipline, for the correct reason.

## What Changes

No permission changes. No agent prompt changes. Every operator keeps `edit: allow` unscoped, keeps its `bash` denies, and keeps its `## Operation journal` section verbatim. This change edits four sentences of justification.

### Specs

`operator-agent-roster` line 72 restates the no-path-scoped-writes requirement with the universal reason. `harness-tool-translation` line 34 keeps its requirement and replaces its causal clause.

### Documentation

`CLAUDE.md` line 103 and `docs/agents-skills-extension-workbook.md` lines 646–648 adopt the same reason. The workbook passage is the mechanism reference new pillars are told to read before authoring, so a wrong reason there is the one most likely to be copied into a future pillar.

### Deliberately not changed

- **Archived changes stay as written.** `2026-07-29-operators-pillar` (design.md line 47, and its own delta spec) and `2026-07-31-aleph-data-access` (proposal line 34, design line 24) carry the retired framing. Archives are the historical record of what was decided and why at the time; rewriting them would falsify that record. The live specs they fed are the artifacts that govern.
- **The Aleph upstream boundary is unaffected.** `2026-07-31-aleph-data-access` reasoned from the flawed analogy but reached the correct conclusion for an independent reason — an API key whose collection ACL is `read=true, write=false` is refused server-side regardless of harness, tool, or shell. That decision needs no revisiting.
- **No permission, prompt, or generator change.** Nothing regenerates, so no plugin tree moves.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `operator-agent-roster` — the requirement forbidding path-scoped writes keeps its normative force and gains the correct reason: unenforceable everywhere, not absent in omp only.
- `harness-tool-translation` — the `.acordia/ops/` journal requirement keeps its normative force; its causal clause stops attributing universal non-enforcement to omp.

## Impact

- **Modified — specs:** `openspec/specs/operator-agent-roster/spec.md`, `openspec/specs/harness-tool-translation/spec.md`.
- **Modified — docs:** `CLAUDE.md` line 103, `docs/agents-skills-extension-workbook.md` lines 646–648.
- **Unchanged:** every agent prompt, every permission map, every skill, every command wrapper, `tools/build-plugins.py`, and both plugin trees. `VERSION` does **not** move — nothing reaching a user changes, and the generated output is byte-identical.
- **Verification:** `tools/build-plugins.py --check` still clean with no rebuild; a repository grep for the retired phrasing returns only the archived changes.
