---
name: evasion-antianalysis
description: Use when you know what the defender can see and must decide how to shape an action to avoid detection and frustrate later analysis — timing, obfuscation, living-off-the-land, and anti-forensic choices.
---

# Evasion & Anti-Analysis Reasoning

## Objective
Given a model of the defender's visibility, reason about how to shape actions so they evade real-time detection and impede after-the-fact analysis — without the evasion itself becoming the loudest signal.

## When to use
- After detection-capability, EDR, or cloud-log analysis has told you what would be seen and you need a concrete evasion plan.
- When an action cannot be made invisible and you must trade fidelity of evidence against operational cost.

## Method
- Take the forecasted signals as input and choose the cheapest reduction per signal: blend-in (LOLBins, legit tooling, normal hours), suppression (unhook, log-tamper), or avoidance (different primitive).
- Weigh anti-analysis tactics (obfuscation, packing, in-memory-only, encrypted staging) against the meta-signal they create — many tamper/evasion actions are themselves high-confidence detections.
- Time and pace actions to defeat correlation and baselining; avoid bursty or novel sequences that stand out from environment norms.
- Plan the forensic aftermath: what artifacts remain, what can be minimized, and what a responder would reconstruct if they arrive later.
- Keep every evasion reversible/deniable where possible; never trade a quiet action for a loud cover-up.

## Signals / outputs
- A per-action evasion plan mapping each expected signal to a mitigation and its residual risk.
- Explicit call-outs where evasion is louder than the action and should be dropped.
- Forensic-footprint notes for own-footprint and disk/memory self-checks.
