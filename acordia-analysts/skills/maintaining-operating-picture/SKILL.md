---
name: maintaining-operating-picture
description: Stop an already-fused picture from rotting while the operation runs — timestamping updates, setting decay on perishable facts and re-verifying them before reliance.
metadata:
  acordia:
    family: take-handling
    grid_row: maintaining-operating-picture
    grid_deep_in: [Core]
    grid_working_in: [Coll]
    row: maintaining-operating-picture
    source: docs/roles/operational-analyst.md
---

# Maintaining the Operating Picture

## Objective

Keep the fused operating picture current and trustworthy as the operation runs and the target changes, so decisions are made against reality rather than a stale snapshot.

## When to use

- During any live operation where access, infrastructure, defenders, or the environment drift over time.
- When a plan or judgement rests on facts collected earlier that may no longer hold.

## Method

- Treat the picture as a living state, not a one-off product: every new observation updates it, and every update is timestamped.
- Track deltas explicitly — what changed since last read (new hosts, revoked access, patched paths, a hunt starting) and what that change implies.
- Set decay on facts: mark which elements are durable and which are perishable, and re-verify perishable ones before relying on them.
- Reconcile new take against the standing picture; when they conflict, trust fresh observation and retire the stale entry.
- Push the current picture to whoever acts on it, so operators are never steering on a picture the analyst already knows is dead.

## Signals / outputs

- A continuously updated operating picture with change-log of deltas.
- Freshness/decay markers separating durable facts from perishable ones.
- Early-warning flags where the environment has shifted enough to invalidate a plan.
