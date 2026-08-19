---
name: overwatch
description: Hold a live read on whether the defender has noticed, by working your reach into their own security operations — SIEM and EDR consoles, alert queues, SOAR tickets, analyst chat, mailboxes — alongside external tells such as credential invalidation, blocked C2, sinkholed domains and fresh agent pushes, and convert it into a timely go-quiet, move or pull-out call.
metadata:
  acordia:
    family: defender-reading
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
- Inventory your reach into the defender's surfaces first — which SIEM/EDR consoles, alert queues, ticketing/SOAR boards, analyst chat channels, and mailboxes you can actually see — and export what you rely on to files, enumerating those captures with `ls`/`glob` so coverage is known rather than assumed.
- Collect from inside with bounded, exhaustive queries: scope each console read to a time window or a rule/host filter rather than scrolling the whole feed, but process every alert and ticket that window returns, not just the first screenful — a missed alert in the tail is the one that ends the operation.
- Fuse with external signals: sudden credential/token invalidation, blocked C2, sinkholed domains, new EDR pushes, threat-intel or vendor chatter, staff behavior changes.
- Correlate blue activity to your own timeline — did an alert or investigation follow a specific action of yours? — to gauge whether they are onto the operation vs. routine noise, and cite each corroborating observation against its capture as `<export>:<alert-id>` or `<export>@L<line>`, so a live view that has since scrolled away stays reproducible evidence.
- Track dwell indicators: is the response widening, targeting your artifacts, or preparing containment (isolation, resets, forensics collection).
- Produce a standing detection-likelihood estimate and a trigger threshold for each response option; never let the estimate go stale.
- Degradation: if a console or queue is unreachable, fall back to the external signals and say plainly which internal source is dark and how much that widens the uncertainty; if you have no blue-side visibility at all, flag the blind spot rather than reporting a false all-clear.

## Signals / outputs
- A live detection-likelihood read with the evidence behind it and its confidence.
- A recommended posture — continue / go quiet / relocate infrastructure / exit — with the trigger that would change it.
- Early-warning indicators queued for continuous monitoring and handoff.
