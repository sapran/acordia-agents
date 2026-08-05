## Why

The four analyst prompts have accreted interagent protocol. Successive changes (`credential-harvest-capability`, `credential-harvest-reshape`, `analyst-verifiability-anchors`, `analyst-delegation-forcing`, `exhaustive-data-processing`) each added an H2 to every agent, and each H2 restated a procedure that already lives in a skill. The result is ~1,380 words of cross-agent boilerplate: the credential-harvest sections re-derive `credential-harvest-triage`'s bucket partition and routing table in four places; the exhaustive-processing sections mandate a coverage-receipt/reconciliation protocol that no artifact defines a format for; `## What to return` enumerates a five-element surface that reads as a schema in prose clothing; and the orchestrator's dispatch prose makes delegation a **precondition**, which forbids the orchestrator from reading a single artefact without a round trip.

Two costs. First, tokens: the boilerplate is paid on every dispatch of every agent, and duplicated procedure drifts from the skill it duplicates. Second, judgement: a prompt that mandates a protocol the harness cannot check produces theatre — a leg that emits the words "coverage receipt" rather than one that actually covered its slice. The skills carry the real procedure and fire on description match; the agent prompt only needs to name them and state the principle.

Current behaviour: five requirements in `analyst-agent-roster` mandate protocol-level detail in prompt bodies. Desired behaviour: the same five sections remain mandatory as *sections*, but state principles and defaults and point at the skill, leaving procedure to the skill that owns it.

A second, unrelated gap is closed in the same change because Step 3 trips it: the omp translator's Tool-discipline rewrite is keyed to a byte-exact legacy paragraph that the trimmed prompts no longer carry, and one published scenario claims the translator aborts on a differing paragraph — it does not, and never did. The translator also emits no `color`, so all five ACORDIA agents render identically in the omp picker.

## What Changes

### Relax five `analyst-agent-roster` requirements (prompt-body normative language only)

No requirement is deleted, no requirement is added, and no frontmatter contract moves. Each amendment softens normative language while keeping the section mandatory:

- **Credential-harvest dispatch section** — a one-line reference to `credential-harvest-triage` replaces the duplicated dispatch/routing/bucket-partition description. An agent MAY name its credential-adjacent skills and one domain-specific lens; it SHALL NOT restate the skill's procedure.
- **Exhaustive-processing section** — states the principle (process all of a handed slice, never sample; legs surface overflow) and names `exhaustive-data-processing`. The coverage-receipt format and the orchestrator's receipt-reconciliation protocol stop being mandated.
- **Leg subagents declare what they return** — three elements (hypothesis, confidence, gaps and next step) instead of five. Credential routing is covered by the credential-harvest reference and need not be restated.
- **Primary declares output discipline** — states the aggregation principle (fuse, attribute, surface disagreement, be brief) instead of prescribing a four-element template.
- **Primary prompt defaults to leg dispatch** (renamed from "…compels leg dispatch before a course of action") — dispatch is the **default**, not a precondition. Self-service is the alternative for scoped work, not a narrow exception.

### Rewrite the four agent prompt bodies against the relaxed spec

Every H2 the spec requires stays; the prose inside is cut to the principle. Frontmatter, identity paragraphs, and the four skill-set headings with their `·`-separated lines are untouched — `tools/translate-omp.py --autoload deep` parses those lines and breaking their shape breaks the flag. Each agent's `## Guardrails` gains the one-line omp write-surface note (under omp, read-only is prompt-level for `write`).

### Relax the matching CLAUDE.md format contract

The `## Credential harvest` bullet is restated as a one-line skill reference, and a note records that `## Exhaustive data processing`, `## What to return`, and `## Output discipline` are advisory prose, not schemas.

### Patch two omp-harness gaps

- The translator emits `color` — `cyan` for the orchestrator, `blue` for the three legs, keyed off the `metadata.acordia` orchestrator declaration (`leg` for analysts, `role` for operators) — so the pillar is distinguishable from the harness's own agents in a shared namespace, the same problem the `ACORDIA <pillar> — ` description tag solves for text.
- The Tool-discipline rewrite is restated as a legacy-wording fallback and the false "Unrecognised paragraph aborts translation" scenario is replaced by what the translator actually enforces: a surviving `list` token aborts; a paragraph the rewrite does not recognise is not itself an error.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `analyst-agent-roster` — five **MODIFIED** requirements (one of them also **RENAMED**). No requirement added or removed.
- `omp-harness-distribution` — two **MODIFIED** requirements: the frontmatter translation contract gains the `color` derivation; the prompt-text correction requirement is restated to match enforced behaviour.

## Impact

- **Modified agent files (4):** `analysts/agents/{operational-analyst,target-network-analyst,defender-detection-analyst,fusion-analyst}.md` — bodies only. No `edit`/`bash`/`task` permission block, no `mode`, no `description`, no `metadata` block is touched.
- **Modified tooling (1):** `tools/translate-omp.py` — `color` in the emitted frontmatter; comment correction on the legacy Tool-discipline constants.
- **Modified docs (1):** `CLAUDE.md` format contracts.
- **Unchanged:** every skill body (the 39-skill library is correctly sized; `credential-harvest-triage` and `exhaustive-data-processing` become the single source for the procedures the prompts stop duplicating), the competency grid in `docs/roles/operational-analyst.md`, `install.sh`/`uninstall.sh`, and the whole `operators/` pillar.
- **No source-of-truth drift.** The prompt edits trace to the amended openspec requirements, which are applied before the prompts change. No grid row moves, so `competency-map-derivation` is untouched.
- **Analyst posture preserved.** Read-only, no raw credential values, three-leg dispatch whitelist, `task: deny` on the legs — all intact. Relaxing prompt prose grants no new capability.
