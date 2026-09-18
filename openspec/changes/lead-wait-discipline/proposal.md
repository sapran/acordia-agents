## Why

The orchestrator has no doctrine for the time it spends waiting, and no doctrine for ending a session while its legs are still running. Both gaps are measured, not suspected.

A seven-day audit of the omp `opwe` profile on `mini` (2026-09-12 → 2026-09-18, 49 lead sessions, 48 analyst legs, 4,083 executed tool calls, frozen snapshot) found:

- **`cyber-analyst` spent 21.2 hours blocked in `hub wait`** across 434 wait calls, median 144 s, maximum 600 s. **202 of those 434 (47%) ran their full window and returned nothing.** In the largest runs this was 62–78% of active lead time, measured with idle gaps over 30 minutes excluded from both sides of the ratio. The lead was not thinking; it was parked.
- **Four legs were disposed mid-work when their lead exited.** `CorpusDomain` (47 tool calls), `LogisticsEstate` (36) and `MissionProd` (33) all terminated at `2026-09-18T00:03:00`, the same second as their lead's exit, plus `IdRecoveryLeg` (31). Every `session_exit` in the corpus reads `reason: dispose, kind: normal`, so nothing crashed — the lead simply ended first and the work went with it.
- **Eight dispatches omitted the `agent:` field**, silently producing persona-less generic workers rather than analysts. One run dispatched `MissionThread`, `TakeDeps` and `LogisticsMovement` twice — once naming the specialist and once omitting it. An omitted field defaults quietly; a wrong value errors loudly, and that asymmetry is why this went unnoticed for a week.

The existing requirement *Orchestrator fan-out follows real dependencies* already covers dispatching independent questions without waiting, and already retains fusion as the lead's own duty. Neither addresses what the lead does **while already-dispatched legs run**, nor the **lifecycle boundary** at session end. This change is narrowly those two things, plus the positive dispatch field.

The canon treats idle analysis as a first-order failure rather than an inefficiency. The Analysis pillar is defined as "real-time decision support during operations: target understanding …, pattern recognition …, and operational planning (selecting methods, timing actions, assessing risk)" (`ACORDIA`, p. 21). A lead parked in a wait window is not directing any step. The same paper prices the failure: "Overinvestment in supporting functions … at the expense of core functions (particularly analysis) produces capability without effectiveness" (p. 23). Its Organization pillar names "doctrine, mission planning, inter-agency cooperation, and **deconfliction**" as the institutional enablers that determine "whether technical capabilities translate into operational outcomes" (p. 22) — losing a leg's completed work to a lifecycle boundary is exactly that translation failing. Monte identifies the mechanism: among the consequences of splitting work into specialist units, "**the communication between units is a potential weak point**", because "the different tempos, risk tolerances, tools, expertise, and leadership of the units will inevitably lead to miscommunication and potential mistakes" (`Monte`, p. 63).

On the dispatch field specifically: Monte describes the attacker's structure as a split into *named* functional units, each with its own driver and mission (p. 61). That grounds naming the specialist, but **no registered work prescribes an API field name**, so the requirement below rests on the measured silent-default defect and carries no literature attribution for the mechanism itself.

## What Changes

- Add doctrine for **productive work while legs run**: before re-entering a wait, the orchestrator performs the analysis it can do without a pending return — verifying returns already in hand, sizing the corpus, naming gaps, revising the operating picture — and waiting is what it does when no such work remains, not its default posture.
- Add a **join-before-exit** lifecycle rule: the orchestrator does not end a session while a dispatched leg is still running. It collects the return, or cancels the leg explicitly and records what was lost.
- Make the dispatch field **positive**: every specialist assignment names its agent. An assignment that does not name one is not dispatched.
- Free the characters the three clauses need by relocating a **duplicated** enumeration. The orchestrator body was **10,391 characters against the 10,500 ceiling — 109 characters of headroom**, measured the way the gate measures it (`len(parts[2].strip())` after the frontmatter, not `wc -c` on the file). Three clauses do not fit in 109. The credential brief's required contents were enumerated twice in that body, so both moved to `credential-harvest-triage`, which owns the procedure. **Measured outcome: 266 characters freed rather than the 323 the raw sentence lengths suggested, because each removal left a short routing pointer behind; the clauses used 371 of the resulting 375; final body 10,496, with 4 characters of margin.** This is the remedy the ceiling requirement prescribes — reduce by moving technique detail to the skill that owns it — applied to prose that already existed rather than to prose this change introduces.
- Update `docs/roles/operational-analyst.md` in the same change, per the source-of-truth rule. No grid row is added, moved or removed; the prose above the table gains the interstitial-work competency for the Core column, and `maintaining-operating-picture`'s row is unchanged.
- Version `6.19.1` → `6.20.0` (three-file lockstep).

## Impact

- `acordia-analysts/agents/cyber-analyst.md`, and **both** wrappers that carry its body byte-identically — `acordia-analysts/commands/cyber-analyst.md` and `acordia-analysts/commands/analyst.md`. All three are edits; `tools/check-acordia.sh` check 7 already enforces their identity, so no new drift test is proposed.
- `acordia-analysts/skills/credential-harvest-triage/SKILL.md` — receives the brief-contents enumeration, stated once rather than twice; its grid row and `procedural: true` anchor are unchanged.
- `acordia-analysts/skills/maintaining-operating-picture/SKILL.md` — gains a bounded "while legs are still out" subsection under `## Method`. Its current method covers freshness, deltas and decay only, so naming it from the orchestrator without adding this text would route the lead to a skill that does not carry the promised technique. It carries **no** `doctrine_source`: `doctrinal-provenance` requires that technique detail trace to its grid row and carry no literature attribution, and a Method subsection is technique. Its `row` / `source` anchor and grid marks are unchanged, and no ceiling applies to skill bodies.
- `openspec/specs/agent-roster/spec.md` — one requirement **added** (the lead's waiting and join-before-exit doctrine) and one **modified**. `Directed credential collection requires orientation first` owns the packet contract normatively, so changing the packet requires a `MODIFIED` block carrying that requirement whole, all its scenarios restated. `skill-library` needs no delta: its `credential-harvest-triage` requirement does impose an orientation-packet input contract — the triage procedure "first validates a lead-supplied orientation packet" and reconciles material to its asset classes — but it fixes no field list, so widening the packet leaves that requirement true as written.
- `docs/roles/operational-analyst.md` — prose only.
- No new agent, skill, competency-grid row, command wrapper, permission boundary or install route.

## The credential brief packet — settled here, not at apply time

The packet was enumerated in **four** places, and no two agreed: twice in the orchestrator body, once normatively in `agent-roster`'s scenario *"Orientation packet reaches the credential brief"*, and once inside `credential-harvest-triage` itself — the fourth surfaced only during implementation, which is itself evidence of how far the drift had spread. A reader reaching any one of them held an incomplete contract. Merging is a content decision, so it is fixed here rather than left to an implementer.

| Source | Items |
|---|---|
| Prompt A — `## You direct four specialists` | corpus state, assets, provenance, observed/inferred status, freshness, confidence, credential forms, mission/value gaps, exposure, omissions |
| Prompt B — `## Credential harvest` | scoped collections, asset classes, non-secret fingerprints, expected credential forms, planned specialist owners, named gaps |
| Spec — `agent-roster` scenario (normative) | scoped collections, asset/system classes, evidence and provenance, freshness, confidence, mission relevance, expected credential forms, planned specialist owners, named gaps |
| Skill's own prior list — `credential-harvest-triage` triage procedure | asset register, mission relevance, system fingerprints, expected credential forms, planned bucket owners, named gaps |

The canonical packet is the **union of all four**, collapsing only clear synonyms and preferring the spec's wording where it is broader (`asset/system classes` over `asset classes`). Ordered scope-first, judgement-last — **14 items**:

> scoped collections · corpus state · asset/system classes · non-secret fingerprints · evidence and provenance · observed/inferred status · freshness · confidence · mission relevance · expected credential forms · planned specialist owners · named mission/value gaps · exposure · omissions

Four pairs deliberately survive as distinct rather than collapsing:

- **`corpus state` / `scoped collections`** — the condition of the corpus (size, coverage, ingestion state) is not which collections are in scope.
- **`omissions` / `named mission/value gaps`** — a gap is something unknown; an omission is something deliberately not covered. Collapsing loses the deliberate-choice signal, which is what a lead most needs when reading a return.
- **`mission relevance` / `named mission/value gaps`** — how an asset matters is not the same as what is unknown about it.
- **`evidence` / `provenance`** — kept as the spec's paired phrase; what was observed and where it came from.

`exposure` comes only from prompt A, and is retained deliberately: the orchestrator's handoff section already requires every leg to report "what exposure it incurred", so dropping it here would contradict a live instruction in the same prompt.

**One item is relocated rather than merged, and this distinction must survive future cleanup.** The skill's own prior list required the *packet* to contain `the asset register`. In the canonical packet the asset register **is field 3** (`asset/system classes`), which is also the artefact triage step 7 extends. Separately, the *asset-and-credential hypothesis register* the lead fuses is **not** a packet field: the MODIFIED requirement already obliges the lead to "include the resulting asset-and-credential hypothesis register in the credential brief", so it travels in the brief beside the packet. Two different registers, two different homes — a later tidy-up that collapsed them would silently drop one.

With that distinction stated, no obligation from any of the four sources is lost.

## Out of scope

Parked rather than fixed here, with evidence recorded in `docs/implementation-notes.md`:

- `task.maxConcurrency: 4` in the profile forces batches into waves. That is operator configuration, not distribution prose, and raising it is **not** recommended — 33 upstream `SERVICE_UNAVAILABLE` and 17 transport timeouts in the same window show the backing service under strain.
- The 8 `skill://…/references/…` reads that failed for skills which are shipped. That is a harness resolver or install-state fault; the agent asked correctly.
- Aleph-side error ergonomics, sent to the aleph-mcp maintainer as a separate field report.
