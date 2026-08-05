## Context

Five changes landed H2 sections in all four analyst prompts between 2026-07-22 and 2026-07-31. Each was individually justified and each was written defensively — the way to make a model actually do a thing is to spell the thing out. Cumulatively they produced prompts in which the protocol outweighs the identity: `operational-analyst`'s body is ~1,650 words, of which ~950 describe how to talk to the other three agents and how to format what comes back.

Three specific over-specifications drive this change.

**Duplicated procedure.** `credential-harvest-triage` is an 8.3 KB skill carrying a classification schema, a five-bucket partition, and a routing table. All four prompts restate parts of it, and the orchestrator's section reproduces the entire bucket-to-leg mapping inline. The skill fires on description match; the prompt reference is what binds it. Everything past the reference is a second copy that can drift.

**Unenforceable protocol.** The exhaustive-processing requirement mandates a "coverage receipt — declared scope reconciled to covered scope" and makes the orchestrator reject returns whose receipt does not reconcile. No artifact defines the receipt's format, and no harness validates it. A leg can satisfy the letter by emitting the phrase. What actually prevents head-sampling is the principle plus the skill's script-first method, not the receipt ceremony.

**Precondition dispatch.** `analyst-delegation-forcing` made leg dispatch a precondition of any recommended course of action, with self-service as a "narrow exception" for trivial single-artefact lookups. It fixed a real failure (the orchestrator answering specialist questions itself), but it overshot: a user who asks the orchestrator to read one log file now gets a subagent round trip, and the prompt explicitly forbids treating self-service as co-equal even where it plainly is.

## Goals

- Cut cross-agent boilerplate by ~40–50% without removing a single required section.
- Move procedure to the skill that owns it; leave the principle and the skill name in the prompt.
- Restore the orchestrator's judgement about when to dispatch, without reverting to the pre-`delegation-forcing` failure mode.
- Keep every mechanical contract the tooling depends on byte-stable.
- Close the two known omp gaps (`color`, Tool-discipline rewrite honesty) while the prompts are open.

Non-goals: touching `operators/` (different source-of-truth chain), resizing any skill, changing any permission, changing the competency grid.

## Decisions

**Relax the spec first, then the prompts.** The chain is `docs/roles/ → openspec/specs/ → analysts/`. Editing a prompt to violate a published SHALL and fixing the spec afterwards is the drift bug CLAUDE.md names. The five requirements are amended and synced into `openspec/specs/analyst-agent-roster/spec.md` before any prompt is opened.

**Soften, never delete.** Every section stays mandatory. A deleted requirement would let a future prompt drop `## What to return` entirely, and the reason those sections exist — a leg that returns a reading log instead of a judgement — has not gone away. The mandate moves from *how much* to *that it exists and what it is about*.

**Dispatch becomes the default, not the precondition.** "Default" keeps the forcing function that `analyst-delegation-forcing` was after: a specialist question goes to the specialist, and the orchestrator's recommendation is still a fusion of technical reads. It drops the part that produced ceremony — mandatory fan-out on a focused single-artefact read. Rejected alternative: keep the precondition and carve out more exceptions; that is the same rigidity with more words.

**Keep the skill names in the trimmed sections.** The plan's trimmed exhaustive-processing text dropped `exhaustive-data-processing`. Skills bind by prompt reference plus description match, so dropping the only mention from all four prompts would silently unbind the skill from the roster — a functional regression rather than a trim. Both trimmed sections keep their skill name; the amended spec keeps the naming clause and drops only the protocol clauses.

**Keep the defender leg's own-footprint lens.** The one part of a credential-harvest section that is not a copy of the skill is `defender-detection-analyst`'s operation-owned vs. target-owned distinction — that lens belongs to the leg, not the triage procedure. It survives the trim.

**`color` is derived, not authored.** The value comes from the `metadata.acordia` block every agent already declares and `competency-map-derivation` already governs — `leg: orchestrator` in the analyst pillar, `role: orchestrator` in the operators pillar. Hardcoding a per-filename table would be a second source of truth for the same fact. `cyan` for the orchestrator, `blue` for the three legs: two families that read apart in the omp picker without claiming a semantic the source does not carry.

**Fix the translator scenario rather than the translator.** `omp-harness-distribution` publishes "Unrecognised paragraph aborts translation", which the translator has never implemented — it aborts only on a surviving `list` token. The trim makes the divergence observable, so the scenario is corrected to the enforced behaviour. Per `openspec/config.yaml`, specs state the actual behaviour; the ideal (a hard match on the Tool-discipline paragraph) is recorded here and not implemented, because after this change no shipped prompt carries the legacy paragraph and a hard match would abort on every future author's wording.

## Risks

- **Under-specification rebound.** A model given "state your hypothesis, confidence, and gaps" may return less structure than one given a five-element list. Mitigated by keeping the sections mandatory and the verbs concrete; if leg returns degrade in practice, the fix is a sharper sentence, not a restored schema.
- **Sampling regression.** Dropping the coverage-receipt mandate could let a leg quietly head-sample. Mitigated by keeping "never sample" and the `exhaustive-data-processing` reference in every prompt — the skill still carries the coverage ledger, which is where a reconciliation format belongs if one is ever formalised.
- **Dispatch regression.** Relaxing precondition to default could return the orchestrator to answering specialist questions itself. Mitigated by stating the default in the same breath as the reason ("that is how you get the deep technical read") rather than as a bare permission.
- **Autoload breakage.** The `·`-separated skill lines under the `(deep)` headings are parsed positionally — the line immediately after the heading, no blank line. Any body rewrite risks disturbing them. Mitigated by leaving all four skill-set blocks untouched and verifying the translator's `autoloadSkills` output is identical before and after.
- **`color` unsupported by an older omp.** An unknown frontmatter key is ignored rather than fatal, so the downside is cosmetic.
