---
name: evasion-antianalysis
description: Shape a planned action against an already-established visibility model, taking each forecast signal and buying the cheapest reduction for it — blending in with LOLBins, legitimate tooling and normal hours, suppression, timing, obfuscation, anti-forensic handling — without the evasion itself becoming the loudest signal on the wire or the host.
metadata:
  acordia:
    family: defender-reading
    grid_row: evasion-antianalysis
    grid_deep_in: [Def]
    grid_working_in: ['T&N']
    source: docs/roles/operational-analyst.md#L93
---

# Evasion & Anti-Analysis Reasoning

## Objective
Given a model of the defender's visibility, reason about how to shape actions so they evade real-time detection and impede after-the-fact analysis — without the evasion itself becoming the loudest signal.

## When to use
- After detection-capability, EDR, or cloud-log analysis has told you what would be seen and you need a concrete evasion plan.
- When an action cannot be made invisible and you must trade fidelity of evidence against operational cost.

## Method
- Inventory the defender-visibility inputs feeding this decision with `glob` / `find` / `list`: the detection-capability write-up, EDR telemetry samples, cloud log excerpts, and any own-footprint ledger already produced.
- Read in bounded, context-scoped slices — the specific rule, the specific event window, the specific artefact — rather than loading whole detection catalogues into context; drive coverage with an exhaustive `grep`/parser pass over the whole catalogue to locate every relevant signal, then read the scoped line range around each — every hit, not just the first.
- Take the forecasted signals as input and choose the cheapest reduction per signal: blend-in (LOLBins, legit tooling, normal hours), suppression (unhook, log-tamper), or avoidance (different primitive).
- Weigh anti-analysis tactics (obfuscation, packing, in-memory-only, encrypted staging) against the meta-signal they create — many tamper/evasion actions are themselves high-confidence detections.
- Time and pace actions to defeat correlation and baselining; avoid bursty or novel sequences that stand out from environment norms.
- Plan the forensic aftermath: what artifacts remain, what can be minimized, and what a responder would reconstruct if they arrive later; cite each expected-signal-to-mitigation pairing by `<path>:<offset>` (byte) or `<path>@L<line>` (line) back to the detection or telemetry line that predicts it.
- Keep every evasion reversible/deniable where possible; never trade a quiet action for a loud cover-up.
- If a detection-rule parser or EDR-log decoder is unavailable, fall back to raw-string `grep` over the exports; if the visibility model itself is absent, flag the gap and stop rather than plan evasion against assumed sensors.

## Signals / outputs
- A per-action evasion plan mapping each expected signal to a mitigation and its residual risk.
- Explicit call-outs where evasion is louder than the action and should be dropped.
- Forensic-footprint notes for own-footprint and disk/memory self-checks.
