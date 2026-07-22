## Context

The analytic loop — target-read → defender-read → fusion → judgement → next-move — is the shape of an analyst pass. It appears in the orchestrator's prompt body as prose derived from the spine paragraph in `docs/roles/operational-analyst.md`. Nothing else in the repo names it as a first-class thing.

Two forces argue for naming it as a skill:

- **Reusability across entry points.** A session may enter through the primary or a leg. Naming the loop as a skill makes it invokable from either.
- **Future-pillar template.** The pillar list in `openspec/config.yaml` names five more pillars (Collection, Operations, Reflection, Direction, Independent action). Each will need its own end-neutral loop. A named `analyst-loop` skill gives future pillars a concrete artifact to model against.

Two forces argue against:

- **Prose-in-prompt is already how the loop reaches the model.** Adding a skill duplicates content.
- **Skills-as-pipelines are less trigger-friendly than skills-as-knowledge** in opencode's description-match model. If the description doesn't read as "when to run this loop", it may never fire.

The proposal accepts both tensions: the skill is prose (short — the loop's shape is not long), and its `description` is authored specifically to trigger on the right situation ("when the operator asks for a fresh end-neutral pass").

## Goals / Non-Goals

**Goals:**
- Name the end-neutral loop as a discoverable skill.
- Make the loop reusable across future pillars via prior-art reference.
- Keep the orchestrator's existing loop prose intact — add a pointer, don't rewrite.
- Do not authorise the legs to run the loop (they are leaf specialists).

**Non-Goals:**
- Not adding a grid row for the loop — it is procedural.
- Not adding a new agent.
- Not changing dispatch topology or the three-leg whitelist.
- Not authoring pillar-specific loops for Collection/Operations/etc. — those are their own future changes.
- Not embedding a full replay of every spine skill inside `analyst-loop` — the loop names the shape, not the competencies.

## Decisions

### The loop is a procedural skill, not a competency row

**Choice:** Author as a procedural cross-cutting skill under the same exception clause used by `credential-harvest-triage`. Do not add a row to the grid.

**Rationale:** The grid is a competency map. The loop is a workflow that composes multiple competencies (spine skills). Adding it as a row would violate one-competency-per-row.

**Alternative considered:** Add a row `analytic-loop` to the grid. Rejected — inflates the grid with workflow-shaped content that isn't a competency.

### Skill body is short — names the loop, not the competencies

**Choice:** The skill body describes the five steps in one sentence each, states the invariants (end-neutral, gap-naming, calibrated confidence, passive), and stops. It does not reproduce content from spine skills.

**Rationale:** Spine skills (`reasoning-under-uncertainty`, `calibrated-confidence`, `naming-the-gaps`, `hypothesis-testing`, etc.) each carry their own content. `analyst-loop` names them as the components of each step, not their internals. This keeps the loop skill readable and prevents drift with the underlying spine.

**Alternative considered:** Long body reproducing each spine skill's content in loop context. Rejected — creates duplication that will drift.

### Only the orchestrator prompt references `analyst-loop`

**Choice:** Add a pointer to `operational-analyst.md`'s existing loop paragraph. Do not reference from any leg.

**Rationale:** Legs are leaf specialists that answer a leg-scoped question. Running the full loop is the orchestrator's job. Reference-from-legs would blur the topology and invite legs to imitate the orchestrator.

**Alternative considered:** Reference from all four agents. Rejected — violates leg-specialist posture and confuses which agent runs the loop.

### `description` is trigger-facing, not descriptive

**Choice:** The `description` says WHEN to run the loop, not WHAT it is.

**Rationale:** opencode selects skills by description match. A description that reads "the end-neutral analytic loop" is what-facing and won't trigger cleanly on operator prompts. A description that reads "when the operator asks for a fresh analytic round" is when-facing and matches actual sessions.

**Alternative considered:** Descriptive `description`. Rejected — matches the `analyst-skill-library` requirement to author descriptions for triggering quality.

### No `## Method` contract (from the verifiability change)

**Choice:** `analyst-loop` is not an evidence-reading skill; it has no file inventory, no sampling, no citation, no tool degradation. It is exempt from the `## Method` contract added by `2026-07-22-analyst-verifiability-anchors`.

**Rationale:** Same rationale as analytic-spine skills. The loop reasons; it does not read files.

## Risks / Trade-offs

- **[Skill may never fire]** — opencode's description match is prose-based; if the description doesn't align with how sessions phrase requests, the loop never triggers. Mitigation: description is authored explicitly for trigger quality; can be refined by iterating on real sessions.

- **[Duplication with orchestrator prompt]** — Both name the loop. Mitigation: orchestrator carries the loop *as its own workflow*; the skill carries the loop *as a template*. Wording deliberately differs — one is instructional (do this), the other is definitional (this is the loop). Duplication is minimal by construction.

- **[Legs may attempt the loop despite the topology]** — A leg session with `analyst-loop` in its description-match pool may attempt to run the loop. Mitigation: the skill body itself states "this skill runs from the orchestrator; a leg session that matches this skill should surface the need for a full pass back to the orchestrator, not attempt the loop itself".

- **[Cross-cutting procedural skill count creeps up]** — Two procedural skills after this change (`credential-harvest-triage`, `analyst-loop`). Future changes may add more. Mitigation: `analyst-skill-library` already contains the escape clause; but future proposals adding procedural skills should justify why the addition is genuinely cross-cutting rather than a hidden competency.
