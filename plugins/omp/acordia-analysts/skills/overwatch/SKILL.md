---
name: overwatch
description: Use during a live operation to read the defender's own security-operations data plus external signals and judge whether or when they are onto you — driving the go-quiet, move, or pull-out decision.
metadata:
  acordia:
    grid_row: overwatch
    grid_deep_in: [Def]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L96
---

# Overwatch (Live "Are We Detected?")

## Objective
Maintain a live read on whether the defender has detected the operation by fusing data pulled from their own security operations with external signals, and convert that read into a timely go-quiet / move / pull-out call.

## When to use
- Continuously throughout an active engagement, especially after any action flagged as detectable.
- The moment any anomaly on the blue side or in your own channels suggests attention.

## Method
- Collect from inside where you have reach: SIEM/EDR consoles, alert queues, ticketing/SOAR, analyst chat, email — and read what the defender knows and is doing.
- Fuse with external signals: sudden credential/token invalidation, blocked C2, sinkholed domains, new EDR pushes, threat-intel or vendor chatter, staff behavior changes.
- Correlate blue activity to your own timeline — did an alert or investigation follow a specific action of yours? — to gauge whether they are onto the operation vs. routine noise.
- Track dwell indicators: is the response widening, targeting your artifacts, or preparing containment (isolation, resets, forensics collection).
- Produce a standing detection-likelihood estimate and a trigger threshold for each response option; never let the estimate go stale.

## Signals / outputs
- A live detection-likelihood read with the evidence behind it and its confidence.
- A recommended posture — continue / go quiet / relocate infrastructure / exit — with the trigger that would change it.
- Early-warning indicators queued for continuous monitoring and handoff.
