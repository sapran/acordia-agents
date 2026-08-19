---
name: briefing-reporting
description: Use when you must hand the current picture and a recommended course of action to a decision-maker or teammate and it has to land fast, unambiguous, and act-on-able.
metadata:
  acordia:
    family: analytic-spine
    grid_row: briefing-reporting
    grid_deep_in: [Core]
    grid_working_in: [Fus]
    source: docs/roles/operational-analyst.md#L76
---

# Briefing & Written Reporting

## Objective
Communicate the operational picture and the recommended course of action crisply, so the recipient can decide and act without reconstructing your analysis or misreading your confidence.

## When to use
- Handing off a judgement, a target read, or a recommended move to a decision-maker or the next operator.
- Producing a written product (spot report, target package, after-action) others will act on.

## Method
- Lead with the bottom line: the judgement and the recommended action, before any supporting detail.
- Separate fact from inference from recommendation, and mark the confidence on each (see calibrated-confidence).
- Give only the evidence that changes the decision; push the rest to an annex, and name the key gaps and risks plainly.
- Match depth to the audience and the clock — a two-line spot report and a full target package are different products.
- State what you need from the reader: a decision, a resource, or an acknowledgement, with the deadline.

## Signals / outputs
- A bottom-line-up-front judgement and recommendation.
- Confidence, key assumptions, and gaps flagged inline.
- An explicit ask: the decision or action required, by when.
- When the product is written to disk it lands in `.acordia/reports/`, the convention every analyst follows; returning it in-message instead is equally correct when the caller only needs the judgement.
