---
name: human-automation-teaming
description: Use when deciding what the tooling should do versus what the analyst must judge — before you let automation drive a targeting, triage, or movement decision on the operation.
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
