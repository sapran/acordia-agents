## Context

An analyst handed a large collected artefact reads the opening window and concludes from it. The cause is mechanical: the `read` tool returns a bounded slice of a file, and nothing in the framework requires the rest to be processed. Fanning out subagents — the operator's first instinct — does not fix this by itself: if each leaf still reads a head, the sampling is merely distributed across more agents.

Two layers produce the behaviour:

1. **No artefact mandates exhaustive coverage.** `analytic-tooling-scripting` names scripting as a competency but not as a *coverage guarantee*; `credential-harvest-triage` scans with `grep -rHnE` but never asserts the scan covered 100% or that every hit was classified.
2. **The spec licenses sampling.** The `analyst-skill-library` "Method contract for evidence-reading skills" requirement frames read discipline as a "bounded sampling discipline" whose sole test is "not wholesale." An analyst that samples the head and stops passes that test. Seven evidence-reading skills inherit the "Sample bounded reads" framing.

This repo is markdown-only opencode agents and skills — there is no runtime, so "ensure" can only mean a triggering skill plus a precondition forcing-function in the prompt, the same mechanism already used for dispatch discipline (`analyst-delegation-forcing`) and credential harvest. There is no hard gate; this design does not pretend otherwise.

## Goals / Non-Goals

**Goals:**
- Make exhaustive coverage a discoverable, triggerable discipline that fires on any bulk-data-analysis session.
- Guarantee completeness through a *tool pass over 100% of the input*, not through reading raw bytes into model context.
- Make sampling structurally visible via a coverage ledger the orchestrator reconciles and can reject.
- Close the spec-level licensing gap so "bounded" governs context size and "exhaustive" governs coverage — two orthogonal axes, no longer conflated.
- Remove the "sample" trap word from the seven skills that carry it, without changing their sound grep-first method.

**Non-Goals:**
- Not a runtime enforcement mechanism — none exists in a markdown distribution.
- Not a grid row — the skill is a workflow, not a competency (procedural-skill exception).
- Not a new agent, and no change to dispatch topology or the three-leg whitelist.
- Not a permission change — no `edit`/`bash`/`task` block is touched.
- Not a rewrite of the evidence-reading skills' substance — only the read-discipline bullet, and only where it uses the "sample" verb.

## Decisions

### Script-first exhaustion is the engine; fan-out is for judgement only

**Choice:** The default is a tool pass (`rg`/`grep -c`/`awk`/`jq`/parser) over 100% of the bytes or records, returning aggregates and located hits (`path:line`). The model reads results, then reads only the located regions into context. Fan-out over bounded slices is reserved for judgement a script cannot make.

**Rationale:** Completeness comes from the tool, which processes every byte cheaply, not from loading raw material into a context window that cannot hold it. This is the only mechanism that is *both* exhaustive and affordable at scale. Fan-out-full-read alone is expensive and re-samples whenever a slice exceeds a leaf's window.

**Alternative considered:** Fan-out full-read as the primary. Rejected — it distributes sampling rather than eliminating it unless every slice is bounded, and it is costly. It survives here only as the judgement path, under the coverage ledger.

### Strict coverage ledger with orchestrator-owned reconciliation

**Choice:** Declare input scope up front as a denominator (files × bytes, or record/line counts). Every processing step accounts for its scope (scanned / parsed / deferred-with-reason). A leaf emits a coverage receipt — `{scope declared, scope covered, method, deferred + why}`. The orchestrator reconciles each leg receipt against the slice it dispatched and **rejects** any receipt that does not cover its slice, re-dispatching or sub-partitioning. Compilation draws only from reconciled receipts; the final output states total coverage or names the deferred remainder.

**Rationale:** Without a reconciled denominator, "I processed the data" is unfalsifiable. The ledger turns a short return into a visible failure the orchestrator can catch, which is the only teeth available absent a runtime.

**Alternative considered:** Advisory "be exhaustive" language with no receipt. Rejected — it cannot catch a leg that quietly sampled; it re-creates the trust-the-model failure this change exists to remove.

### The skill is procedural and non-grid

**Choice:** Author `exhaustive-data-processing` as a procedural cross-cutting skill under the same exception clause as `credential-harvest-triage` and `analyst-loop`. Do not add a grid row.

**Rationale:** The grid maps competencies. Exhaustive processing is a *workflow* that composes `analytic-tooling-scripting` and the legs' reads. A row would inflate the grid with a workflow.

**Alternative considered:** Add a grid row `exhaustive-data-processing`. Rejected — violates one-competency-per-row.

### Strengthen the Method contract rather than layer over it

**Choice:** MODIFY the existing "Method contract for evidence-reading skills" requirement so element (b) reads *bounded-context, exhaustive-coverage* and split its scenario into a context-bound scenario and an exhaustive-coverage scenario — instead of adding a new, competing requirement.

**Rationale:** The old requirement is the spec-level root cause. Leaving it in place and adding a contradicting "never sample" requirement would leave the framework asserting both. Fixing the requirement at its origin (choose the fix point carefully) removes the contradiction and gives the new skill a coherent normative anchor. The two intents are orthogonal: bounded governs how much enters context; exhaustive governs how much of the input is covered — both now stated.

**Alternative considered:** Leave the Method contract untouched and rely solely on the new skill. Rejected — leaves a live licensing gap and a spec that both permits and forbids sampling.

### Rewording the seven skills traces to the Method contract, not the grid

**Choice:** Reword only the read-discipline bullet, only in the seven skills that use "sample" as a read verb, and treat the strengthened Method-contract requirement as the normative anchor for that edit.

**Rationale:** Editing artefacts under `analysts/` requires an upstream normative source or it is source-of-truth drift. The Method contract (introduced by `analyst-verifiability-anchors`, not the competency grid) is exactly that source for Method-section wording. So the edits are anchored without any grid change. The other evidence-reading skills use "bounded" without "sample" and are already substantively conformant — touching them would be churn beyond the fix.

**Alternative considered:** Rewrite the read-discipline bullet across all fifteen evidence-reading skills. Rejected — the non-"sample" skills already grep-first and carry no trap word; uniform rewriting adds diff without removing risk.

### Legs cannot fan out — they surface overflow back

**Choice:** A leg whose slice still exceeds full processing script-exhausts what it can and surfaces the un-processable remainder back to the orchestrator for sub-partition; it does not sample and does not fan out.

**Rationale:** Legs are `task: deny` leaf specialists. This mirrors `analyst-loop`'s "a leg surfaces the need for a full pass back to the orchestrator" and keeps the fan-out authority solely with the primary.

**Alternative considered:** Grant legs `task` to self-partition. Rejected — breaks the leaf-specialist topology and the three-leg whitelist.

### The new skill is exempt from the four-element Method contract

**Choice:** `exhaustive-data-processing` is procedural and not one of the fifteen evidence-reading skills; it *defines* the strengthened discipline rather than being audited against the four-element `## Method` contract.

**Rationale:** Same treatment `analyst-loop` received — a procedural skill names a workflow. Here the workflow *is* the reading discipline, so subjecting it to the contract would be circular.

## Risks / Trade-offs

- **[Skill may never fire]** — opencode selects by `description` match; a poorly-phrased description means the discipline never triggers. Mitigation: the description is authored for trigger quality (bulk material / dump / archive / dataset / whole-file), and the four agent prompts carry the precondition independently, so the orchestrator enforces it even if the skill does not surface.

- **[Ledger theatre]** — a leg could emit a receipt that claims full coverage without achieving it. Mitigation: the receipt names the *method* (which tool, which pass); a receipt whose method is "read the file" over a multi-megabyte artefact is self-evidently a sample and is rejected. The ledger reduces, not eliminates, trust — honestly stated as the ceiling of a no-runtime framework.

- **[Fan-out cost]** — full-read fan-out is expensive. Mitigation: script-first is the default and keeps fan-out rare (judgement only); most exhaustion is a cheap tool pass whose results, not raw bytes, reach context.

- **[Overflow ping-pong]** — a leg surfacing overflow back, the orchestrator re-dispatching a still-too-large slice, repeat. Mitigation: the orchestrator sub-partitions deterministically (by file, then by byte/line range) so each round strictly shrinks the slice.

- **[Strengthened contract exposes latent non-conformance]** — the MODIFY makes exhaustive coverage normative for all fifteen evidence-reading skills, and the repo has no CI that audits skill bodies against it. Mitigation: the seven trap-word skills are fixed in this change; the remainder are substantively conformant (grep-first covers the input); any future audit gap is a documentation concern, not a behavioural regression.
