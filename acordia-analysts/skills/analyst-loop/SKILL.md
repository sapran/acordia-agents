---
name: analyst-loop
description: Run one full analytic round over a live operation — target read, defender read, fusion, outcome judgement, next move — and close it on the operation's dual end of effect or intel, whenever fresh material lands or a decision point is reached and a single narrow read will not do.
metadata:
  acordia:
    family: analytic-spine
    grid_row: null
    procedural: true
    source: openspec/changes/archive/2026-07-22-analyst-loop-skill/proposal.md
---

# Analyst Loop

## Cross-cutting notice

This skill is **procedural and cross-cutting**. It does not correspond to a row in the competency-grid appendix of `docs/roles/operational-analyst.md` — it names the *workflow* that composes the grid's competencies, not a competency of its own. It reuses the analytic-spine skills (`reasoning-under-uncertainty`, `hypothesis-testing`, `key-assumptions-check`, `calibrated-confidence`, `naming-the-gaps`, `outcome-judgement`, `gain-loss-calculus`) and the three legs' specialist reads. Adding it as a grid row would inflate the competency map with a loop, not a competency; it lands under the same procedural-skill exception that `credential-harvest-triage` uses.

## Objective

Turn the current state of an operation into a recommended course of action by running one full analytic round — target read, defender read, fusion, judgement, next move — and closing the loop on the operation's dual end: an **effect** (break, deny, manipulate) or **intel** (collect). The same access often serves either; the loop is end-neutral and drives toward whichever end is in play.

## When to use

- New material has landed (collection, a completed action, fresh defender signal) and the picture needs a fresh pass.
- The operation is between decision points and the operator wants a full round rather than a single narrow read.
- An action has just been taken and the question is *did we get there, and what now?*

## Loop shape

Five steps, each dispatching to the analyst who owns it:

1. **Target read** — through `target-network-analyst`: what the target is for, what it depends on, where movement is possible, when it will change, and — after an action — whether the target actually changed (effect-on-target verification).
2. **Defender read** — through `defender-detection-analyst`: will this be seen, is it being seen right now, is the operation still clean, and what does our own footprint reveal (the are-we-seen half of "did it land").
3. **Fusion** — through `fusion-analyst`: what all of it together means, how good the take is, and — for a collection end — whether the take is real and worth having (the value-of-the-take half of "did it land").
4. **Judgement** — the orchestrator's own: fuse the three reads into one calibrated call using the analytic spine (`reasoning-under-uncertainty`, `hypothesis-testing`, `key-assumptions-check`, `outcome-judgement`, `gain-loss-calculus`), attributing each hypothesis to the leg that raised it.
5. **Next move** — name the recommended action and the end it serves: continue, pivot, go quiet, move, or pull out. End-neutral: whichever of effect or intel is in play, say whether it was met and what follows.

## Loop invariants

- **End-neutral closure.** Every pass reaches a judgement *and* a next move. "Insufficient information" is not a stopping point — it is a gap to name and a collection task to hand back.
- **Gap-naming on every judgement.** Run `naming-the-gaps`: state the specific reads you do not yet have and what would close them. The loop's output includes the gaps that bound it.
- **Calibrated confidence on every judgement.** Run `calibrated-confidence`: attach a confidence band to each claim; where the legs disagree, surface the disagreement rather than averaging it away.
- **Passive posture.** The loop reads, models, and judges. It never acts — no file edits, no payloads, no credential validation. Execution belongs to the operators the analyst advises.

## Where this runs

This is the **orchestrator's** loop — `cyber-analyst` runs it, dispatching the three legs and fusing their reads into one judgement. A leg subagent is a leaf specialist that answers its own scoped question; if a leg session matches this skill, it should **surface the need for a full pass back to the orchestrator** rather than attempt the loop itself (a leg cannot dispatch other legs). Future pillars (Collection, Operations, Reflection, Direction, Independent action) can model their own end-neutral loop on this one, or define a `<pillar>-loop` sibling and cite this skill as prior art.

## Signals / outputs

- A single recommended course of action tied to the operation's end (effect or intel).
- Per-hypothesis attribution to the leg that raised it, each with a calibrated-confidence band.
- The named gaps that bound the judgement and the next collection or method that would close each.
- A next-move call: continue / pivot / go quiet / move / pull out.
