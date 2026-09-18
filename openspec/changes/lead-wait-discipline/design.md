## Context

Three defects, one surface. All three live in the orchestrator's prompt body, which is carried byte-identically in three artifacts and sits close to the ceiling the repository's own gate enforces. The design question is therefore not *what to say* — the proposal settles that from selected passages — but whether the sentences fit, and if not, which **existing** prose earns its place less.

### The measurement, corrected

An earlier draft of this design claimed the body was 10,810 characters and therefore 310 over the ceiling. That was `wc -c` on the whole file. **The gate does not measure that.** Check 8 measures `len(parts[2].strip())` — the body after the frontmatter delimiter:

| Agent | File bytes | Gate body | Headroom |
|---|---|---|---|
| `cyber-analyst` | 10,738 | **10,391** | **109** |
| `mission-analyst` | 8,838 | 8,443 | 2,057 |
| `terrain-analyst` | 8,780 | 8,423 | 2,077 |
| `overwatch-analyst` | 8,550 | 8,270 | 2,230 |
| `collection-analyst` | 8,813 | 8,432 | 2,068 |

So the body is **under** the ceiling, and the gate passing was never in contradiction with anything. But 109 characters is not enough for three clauses, so a relocation is still required — just a smaller and more precisely targeted one than the earlier draft assumed.

## Goals

- The lead has a named alternative to waiting, and waiting is the residual case.
- No dispatched leg's work is lost to a lifecycle boundary without a record.
- Every assignment names its agent, positively.
- The orchestrator body ends **at or below the spec's 10,500-character ceiling**, which is the only acceptance criterion the repository actually enforces. **Measured result: 266 characters freed, a 375-character budget, 368 used, final body 10,493 with 7 characters of margin.** "No net growth against 10,391" was an invented stricter bar and is withdrawn — it would have capped the clauses at 266 and contradicted the budget used everywhere else.

## Non-goals

- Changing fan-out doctrine. `Orchestrator fan-out follows real dependencies` already covers dispatching independent questions without waiting and already retains fusion as the lead's duty.
- Adding a drift test or a shared/generated prompt source. Check 7 already asserts orchestrator-body identity across the agent and both wrappers; a generated source would change the distribution's shape and require a MAJOR bump and a different change.
- A `plugin-distribution` delta. This change adds no packaging mechanism and no new check, so `agent-roster` alone is the natural capability for three lead-behaviour requirements.
- Touching `task.maxConcurrency`. Operator configuration, and the evidence argues against raising it.

## Decisions

### What is relocated, named exactly

The earlier draft proposed moving "the interstitial-work enumeration" out of the orchestrator. **No such enumeration exists there** — it is prose this change introduces, so it cannot be the thing that frees space. That plan was circular and is withdrawn.

The real slack is a genuine duplication. The credential brief's required contents are enumerated **twice** in the same body:

1. Under `## You direct four specialists` — "Briefs require corpus state, assets, provenance, observed/inferred status, freshness, confidence, credential forms, mission/value gaps, exposure, and omissions." (161 chars)
2. Under `## Credential harvest` — "The credential brief carries the scoped collections, asset classes, non-secret fingerprints, expected credential forms, planned specialist owners and named gaps." (162 chars)

Both are technique detail for one procedure, and `credential-harvest-triage` — already named in that same section, already `procedural: true` — owns it. The two raw lists total 323 characters. Stating the packet once, in the skill, also removes a latent drift bug: two lists of what a credential brief must carry, which did not agree.

**Forecast working budget: 109 + 323 = 432 characters.** *Measured on implementation: only 266 were freed, because each removed enumeration left a short routing pointer behind, giving a real budget of 375. The three clauses used 368; the final body is 10,493, with 7 characters of margin.* The forecast is kept here beside the measurement because the gap between them is the lesson: raw sentence length is not freed length when the sentence is replaced rather than deleted.

### Where each sentence lives

| Doctrine | Surface | Why there |
|---|---|---|
| "Waiting is the residual case", naming `maintaining-operating-picture` | orchestrator body (×3) | A posture the model must hold before it reaches for a tool cannot live in a skill it may not read. |
| *What* interstitial work to do | `maintaining-operating-picture` | Technique detail, and that skill owns keeping a fused picture current while an operation runs. Its existing method covers only freshness, deltas and decay, so it takes a bounded lead-only subsection as well as the routing. |
| Join-before-exit, with the record obligation | orchestrator body (×3) | A lifecycle boundary is not a technique; it fires at session end whether or not a skill was read. |
| "Every assignment names its agent" | orchestrator body (×3) | It governs the shape of a `task` call, which is prompt-level. One clause. |
| Credential brief contents | `credential-harvest-triage` | Relocated, not new. Stated once instead of twice. |

### `maintaining-operating-picture` takes a bounded addition

The skill's `## Method` covers freshness of an existing picture — living state, timestamping, deltas, decay on perishable facts, reconciling new take, pushing the picture out. It does not cover **sizing a corpus** or **naming the gaps the dispatched legs are not covering**, which are two of the three interstitial activities this requirement promises. Naming the skill without adding that text would route the lead somewhere that does not carry the method, so it takes a bounded "while legs are still out" subsection.

**It takes no `doctrine_source`.** `doctrinal-provenance` states that technique detail SHALL NOT be attributed to the literature — a procedure "traces to its grid row through the `row` / `source` anchor … and adding a literature citation to it would falsely imply a work prescribes it" — with a scenario that a Method section describing a procedure "carries no literature attribution". A Method subsection is technique by that definition, and ACORDIA did not supply this method. The ACORDIA pages ground the **normative posture** — that a lead which stops directing has hollowed out a core pillar — so they are cited in `proposal.md` and the grid prose, and nowhere in the skill's metadata.

No ceiling applies to skill bodies, so this costs the orchestrator's character budget nothing. The skill's grid row and its `grid_deep_in: [Core]` / `grid_working_in: [Coll]` marks are unchanged, so the competency grid does not move for it. Because `Coll` carries the skill too, the new subsection opens with an explicit **lead-only** scope guard: a leg has no legs of its own and updates its own slice instead.

The skill was **invoked zero times** in the audited week, consistent with nothing routing the lead to it. Content and routing were both missing.

### Why the dispatch field is stated positively

The repository has already learned this once. The entry guard was phrased as the absence of a tool and never fired, because a model does not notice an absence it was not asked to look for; the `positive-dispatch-guard` change replaced it with an enumerate-and-report determination. "Do not omit `agent:`" is a prohibition on an absence. "Every assignment names the agent it is for" is a positive property checkable against what is about to be sent.

### Why join-before-exit is a record, not a prohibition

Cancelling a leg is legitimate — 6 of the 16 non-yielding legs in the window were cancelled deliberately, and that is the lead exercising judgement. The defect is the *silent* case: 4 legs whose work vanished with no decision and no note. The rule permits both endings and requires only that the second be recorded.

## Risks

- **The budget may not be enough.** *Resolved on implementation: 368 of 375 used, 7 characters of margin. No second relocation was needed.* Had it been, the `## A directory per task` section restates hand-back shape that `briefing-reporting` owns and was the next candidate. The margin is thin: the next addition to this prompt must relocate something first.
- **The relocated enumerations disagree with each other.** Merging two non-identical lists into one is a content decision, not a move. It must be done deliberately and noted in the task, not silently resolved in favour of whichever was copied last.
- **The moved detail may not be read.** A skill is selected by description match. Mitigation: `credential-harvest-triage` is already named explicitly in the section losing the text, so the routing already exists.
- **No behavioural proof.** Prompt changes are not self-verifying: the 21.2 idle hours are the defect, not evidence that new prose cures it. Crediting this change requires a fresh A/B of print-mode sessions scored from session JSONL, not a re-read of the motivating corpus.

## Migration

None. Prompt and skill prose only, picked up by a version bump. No install route, frontmatter contract or grid row changes.
