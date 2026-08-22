---
name: key-assumptions-check
description: Surface the assumptions a plan silently rests on, mark the load-bearing ones and stress each for evidence and freshness, when success depends on expected behaviour.
metadata:
  acordia:
    family: analytic-spine
    grid_row: key-assumptions-check
    grid_deep_in: [Core]
    grid_working_in: [Mission, Terrain, Def, Coll]
    row: key-assumptions-check
    source: docs/roles/operational-analyst.md
---

# Key-Assumptions Check & Debiasing

## Objective

Surface the assumptions the operational judgement silently rests on, mark which ones are load-bearing, and stress them — while countering the analyst's own biases — so the plan does not collapse when an unexamined premise turns out wrong.

## When to use

- Before acting on a plan whose success depends on the target or defender behaving "as expected".
- When the team has converged fast and confidently on one read.

## Method

- List every assumption behind the judgement, including the ones stated as fact ("this box is internet-reachable", "no EDR here").
- Tag each as load-bearing or minor: would the plan break if it were false?
- For each load-bearing assumption, ask what evidence supports it, how recent it is, and what would falsify it.
- Name the biases in play — confirmation, anchoring on first access, mirror-imaging the defender, sunk-cost on burned effort — and correct for each.
- Convert fragile assumptions into gaps to collect against or contingencies to pre-plan.

## Signals / outputs

- A list of load-bearing assumptions, each rated supported / stale / unfounded.
- The named biases and the specific correction applied.
- Assumptions promoted to collection gaps or branch-plan triggers.
