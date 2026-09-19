---
name: maintaining-operating-picture
description: Keep a fused picture current while the operation runs — timestamping updates, decaying perishable facts, and doing the analysis that needs no pending return while legs are still out.
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

### While dispatched legs are still out

**Lead only.** This subsection applies to the orchestrator that dispatched the legs; a leg dispatches
no legs of its own, and updates and returns its own slice instead.

Waiting on a return is not a pause in the analysis; it is an interval with its own work. Before
re-entering a wait, establish what does not depend on a pending return:

- Verify the returns already in hand — read the notes each leg named rather than its summary, and
  reconcile them against the standing picture while the detail is still addressable.
- Establish the size and shape of the corpus where no dispatched leg owns that question — what the
  denominator is, and whether a coverage claim could yet be stated honestly;
  `exhaustive-data-processing` carries the method.
- Name the gaps the dispatched legs are **not** covering. A leg's assignment bounds what it can
  find, so the uncovered remainder is visible only from the lead's seat and only while the legs run.
- Re-verify the perishable facts the next decision will rest on, rather than after the return lands.

Waiting is what remains when that work is exhausted. A picture that did not move while its legs
ran is a picture nobody was keeping.

## Signals / outputs

- A continuously updated operating picture with change-log of deltas.
- Freshness/decay markers separating durable facts from perishable ones.
- Early-warning flags where the environment has shifted enough to invalidate a plan.
