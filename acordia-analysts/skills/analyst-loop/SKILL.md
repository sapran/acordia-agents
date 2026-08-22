---
name: analyst-loop
description: Run one full analytic round over a live operation — mission, terrain, defender and take reads, then judgement and next move — when fresh material lands or a decision point is reached.
metadata:
  acordia:
    family: analytic-spine
    grid_row: null
    procedural: true
    source: openspec/changes/archive/2026-07-22-analyst-loop-skill/proposal.md
---

# Analyst Loop

## Cross-cutting notice

This skill is **procedural and cross-cutting**. It does not correspond to a row in the competency-grid appendix of `docs/roles/operational-analyst.md` — it names the *workflow* that composes the grid's competencies, not a competency of its own. It reuses the analytic-spine skills (`reasoning-under-uncertainty`, `hypothesis-testing`, `key-assumptions-check`, `calibrated-confidence`, `naming-the-gaps`, `outcome-judgement`, `gain-loss-calculus`) and the four legs' specialist reads. Adding it as a grid row would inflate the competency map with a loop, not a competency; it lands under the same procedural-skill exception that `credential-harvest-triage` uses.

## Objective

Turn the current state of an operation into a recommended course of action by running one full analytic round — mission read, terrain read, defender read, take read, judgement, next move — and closing the loop on whichever of the operation's three ends is in play: an **effect** (break, deny, manipulate), **intelligence** (collect), or **access** held because it may become useful later. The same access often serves more than one, so the loop is end-neutral; it is not end-agnostic, because collection and effect compete for that access and pull in opposite directions.

## When to use

- New material has landed (collection, a completed action, fresh defender signal) and the picture needs a fresh pass.
- The operation is between decision points and the operator wants a full round rather than a single narrow read.
- An action has just been taken and the question is *did we get there, and what now?*

## Loop shape

Six steps. Four dispatch to the leg that owns them; the last two are the orchestrator's own.

1. **Mission read** — through `mission-analyst`: what the target is for, what it depends on, how it behaves, when it will change, how much friction it would absorb — and, after an action, whether the *organisation* changed.
2. **Terrain read** — through `terrain-analyst`: what the estate is made of, where movement opens and closes, what the trust between systems allows — and, after an action, whether the *system* changed, as distinct from whether the payload ran.
3. **Defender read** — through `overwatch-analyst`: will this be seen, is it being seen right now, is the operation still clean, and what does our own footprint reveal (the are-we-seen half of "did it land").
4. **Take read** — through `collection-analyst`: is the material real, what does it say in its own domain and language, is it worth what it cost, and what does the operation already know (the value-of-the-take half of "did it land").
5. **Judgement** — the orchestrator's own, and **not delegated**: hold the fused picture and reach one calibrated call using the analytic spine (`reasoning-under-uncertainty`, `hypothesis-testing`, `key-assumptions-check`, `outcome-judgement`, `gain-loss-calculus`), attributing each hypothesis to the leg that raised it. There is no fusion step in this loop because fusing is the orchestrator's work: a picture assembled in a leg and passed back arrives stripped of the detail that made it a judgement.
6. **Next move** — name the recommended action and the end it serves: continue, pivot, go quiet, move, or pull out. End-neutral across all three ends — effect, intelligence, or access held for later use — say which was in play, whether it was met, and what follows. Because the analyst does not execute, the move is a recommendation handed to a human operator.

## Loop invariants

- **End-neutral closure.** Every pass reaches a judgement *and* a next move. "Insufficient information" is not a stopping point — it is a gap to name and a collection task to hand back.
- **Gap-naming on every judgement.** Run `naming-the-gaps`: state the specific reads you do not yet have and what would close them. The loop's output includes the gaps that bound it.
- **Calibrated confidence on every judgement.** Run `calibrated-confidence`: attach a confidence band to each claim; where the legs disagree, surface the disagreement rather than averaging it away.
- **Passive posture.** The loop reads, models, and judges. It never acts — no file edits, no payloads, no credential validation. Execution belongs to the human operator the analyst advises, so the loop's outcome judgement rests on evidence reported back rather than observed first-hand; say which is which.
- **Handoff discipline.** Each dispatch carries the objective, the operating logic, the stage, the tempo, the risk tolerance, what is already established, and what must not be touched; each return carries what was done, what was learned, its confidence, the exposure it incurred, and what was deliberately not done. The boundary between units is where mistakes enter, and this is what keeps them out.

## Where this runs

This is the **orchestrator's** loop — `cyber-analyst` runs it, dispatching the four legs and fusing their reads into one judgement itself. A leg subagent is a leaf specialist that answers its own scoped question; if a leg session matches this skill, it should **surface the need for a full pass back to the orchestrator** rather than attempt the loop itself (a leg cannot dispatch other legs). A future pillar — Research is the ACORDIA-aligned next one — can model its own end-neutral loop on this one, or define a `<pillar>-loop` sibling and cite this skill as prior art.

## Signals / outputs

- A single recommended course of action tied to the end in play — effect, intelligence, or access held for later use — addressed to the human operator who will act on it.
- Per-hypothesis attribution to the leg that raised it, each with a calibrated-confidence band.
- The named gaps that bound the judgement and the next collection or method that would close each.
- A next-move call: continue / pivot / go quiet / move / pull out.
