## Context

See `proposal.md` — Why. The design question is narrow: this is a four-sentence prose correction with no behavioural surface, so the only real decisions are **which sites to touch** and **what the replacement reason is**.

Site inventory, from a repository grep for the retired phrasings (`enforced in opencode`, `hold in opencode`, `would be enforced`, `silently evaporate`, `silently absent`):

| site | status | action |
| --- | --- | --- |
| `openspec/specs/operator-agent-roster/spec.md:72` | live, normative | correct |
| `CLAUDE.md:103` | live, contributor guidance | correct |
| `docs/agents-skills-extension-workbook.md:646-648` | live, mechanism reference for new pillars | correct |
| `openspec/specs/harness-tool-translation/spec.md:34` | live, normative — right conclusion, narrow reason | correct the causal clause only |
| `openspec/changes/archive/2026-07-29-operators-pillar/design.md:47` + its delta spec | archived | leave |
| `openspec/changes/archive/2026-07-31-aleph-data-access/proposal.md:34`, `design.md:24` | archived | leave |

`reframe-report-sink-convention` already fixed the analyst-side sites; nothing here overlaps it.

## Goals / Non-Goals

**Goals:**

- Every live artifact gives the same reason for the same mechanism, matching the analyst capabilities.
- The workbook passage is corrected, because it is the reference a future pillar author reads first.
- The normative force of both modified requirements is preserved exactly — this must not become a licence to add path-scoped rules.

**Non-Goals:**

- No permission change, no prompt change, no generator change, no rebuild.
- No rewriting of archived changes.
- No revisiting of the Aleph upstream-boundary decision.
- No `VERSION` bump.

## Decisions

### Keep `edit: allow` unscoped and keep the requirement forbidding path scopes

The requirement survives intact, only better argued. The correction makes the prohibition *stronger*, not weaker: previously a path-scoped rule was avoided because one harness would ignore it, which invites "then scope it anyway, opencode users benefit." Once the rule is unenforceable everywhere, scoping buys nothing but a false impression. Both modified requirements gain a scenario pinning the reason so the old phrasing cannot drift back.

### Do not rewrite archived changes

**Considered:** correct all six sites including the two archived changes, for a clean grep.

**Rejected.** An archive records what was decided and on what basis at the time; editing it would make the repository's history claim a reasoning nobody had. The live specs are what govern, and `2026-07-29-operators-pillar`'s delta was already superseded by the main spec it fed. The cost is that a grep for the retired phrasing still returns archive hits — accepted, and stated in the proposal so it does not read as an oversight.

### Do not bump `VERSION`

`plugin-packaging` fixes MINOR as "any change that reaches a user — an agent prompt, a skill body, a command wrapper, or the generator's emitted output". This change touches none of those: two OpenSpec specs, one contributor-guidance file, one internal mechanism document. Generated output is byte-identical, so a bump would ship an upgrade carrying nothing and burn the signal that a version change is meaningful. `--check` is still run to prove the trees did not move.

### `harness-tool-translation` keeps its conclusion, changes its clause

Its requirement already lands correctly — the journal is discipline. Only the trailing `because omp cannot scope a tool to a path` is wrong, in that it makes a universal fact sound like an omp defect. Minimal edit: keep the sentence, replace the clause, keep omp's real limitation as a secondary note. This is why the change modifies two capabilities rather than one; leaving it would have the operators' two governing specs disagree about the reason.

### Not folded into `reframe-report-sink-convention`

That change is applied, validated, and awaiting archive. Reopening it to widen scope would invalidate its own "Unchanged: the operators pillar" claim and its verification record. A separate change keeps both auditable.

## Risks / Trade-offs

**Grep still returns the archived hits.** Anyone auditing the phrasing must know to exclude `openspec/changes/archive/`. Mitigated by naming the archived sites explicitly in the proposal and in this table, so the residue is documented rather than discovered.

**Two open changes touch `openspec/specs/`.** `reframe-report-sink-convention` has delta specs for `analyst-agent-roster`, `plugin-packaging`, and `omp-harness-distribution`; this one for `operator-agent-roster` and `harness-tool-translation`. The sets are disjoint, so the syncs commute and either may archive first. `extend-aleph-analyst-capability` is also in flight against `analyst-agent-roster` and `analyst-skill-library` — disjoint from this change, though not from its sibling.

**A reader may over-read the correction as loosening the rule.** The added scenarios and the explicit "makes the prohibition stronger" framing in the modified requirement guard against a future author concluding that path scopes are now merely discouraged.
