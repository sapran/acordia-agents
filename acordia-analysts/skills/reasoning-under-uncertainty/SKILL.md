---
name: reasoning-under-uncertainty
description: Reach a defensible provisional judgement when the picture is too thin or too noisy to read cleanly, fixing the decision and its deadline first and triaging knowns from unknowables.
metadata:
  acordia:
    family: analytic-spine
    grid_row: reasoning-under-uncertainty
    grid_deep_in: [Core]
    grid_working_in: []
    row: reasoning-under-uncertainty
    source: docs/roles/operational-analyst.md
---

# Reasoning Under Uncertainty & Overload

## Objective

Produce a defensible operational judgement when information is scarce, contradictory, or overwhelming, so the operation keeps moving instead of stalling on a picture that will never be complete.

## When to use

- You are starved of data on a target and pressured to decide anyway (move / hold / abort).
- You are drowning in collection and cannot see which signals actually bear on the decision.

## Method

- Fix the decision first, not the data: state the exact call you owe and the deadline, then reason backward to only the facts that would change it.
- Triage the picture into knowns, unknowns, and unknowables; refuse to spend effort resolving what is unknowable in the available window.
- Under scarcity, reason from the target's structure and incentives (what a system/operator of this type must do) to bridge missing observations.
- Under overload, filter by decision-relevance and source diversity; discount volume, weight independent corroboration.
- Decide provisionally, mark the judgement as revisable, and set the trigger that would force reconsideration.

## Signals / outputs

- A stated operational judgement with the minimum evidence it rests on.
- A short list of what would flip the call (the reconsider triggers).
- A confidence band and an explicit note of what remains unknown or unknowable.
