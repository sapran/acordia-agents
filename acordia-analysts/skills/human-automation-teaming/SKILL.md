---
name: human-automation-teaming
description: Divide a workflow between analyst judgement and automation, setting an autonomy level per task and designing against automation bias, when a filter decides what the analyst ever sees.
metadata:
  acordia:
    family: analytic-spine
    grid_row: human-automation-teaming
    grid_deep_in: [Core]
    grid_working_in: []
    row: human-automation-teaming
    source: docs/roles/operational-analyst.md
---

# Human–Automation Teaming

## Objective

Divide the work between analyst judgement and automation so machines carry scale, speed, and recall while the analyst owns the judgement calls, keeping the operation both fast and accountable.

## When to use

- Standing up or tuning a workflow where tooling triages, scores, or filters what the analyst sees.
- Deciding whether to let automation act, recommend, or merely surface.

## Method

- Split by strength: give automation volume, correlation, and monitoring; keep intent, ambiguity, deception, and irreversible calls with the human.
- Set the autonomy level per task — automate-and-act, recommend-and-confirm, or surface-only — matched to the cost of a wrong move.
- Design against automation bias: the analyst must be able to see the evidence and overrule the machine, not rubber-stamp it.
- Watch for the failure modes automation hides — silent misses, stale models, adversary gaming the filter — and sample its output by hand.
- Keep a human in the loop for any effect or targeting decision that is irreversible or attributable.

## Signals / outputs

- A task split with an autonomy level assigned to each step.
- The override points and evidence the analyst must retain visibility of.
- A list of automation failure modes to sample against.
