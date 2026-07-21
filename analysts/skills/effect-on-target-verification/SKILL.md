---
name: effect-on-target-verification
description: Use after an action to confirm the target system actually changed — read the effects side of "did it land," distinguishing real effect from delivery success, cover story, or defender illusion.
---

# Effect-on-Target Verification

## Objective
After an operational action, determine whether the target system genuinely changed in the intended way — separating "the payload ran" from "the effect occurred," and both from what the target may be showing you deliberately.

## When to use
- Immediately after any action intended to produce an effect (access gained, service disrupted, data altered, persistence set).
- When success indicators are ambiguous, delayed, or could be spoofed by the defender.

## Method
- Define the expected effect concretely before acting: what state must be true on the target if it worked.
- Gather independent observables — not just the tool's own success return, but second-source confirmation (behaviour change, downstream signal, out-of-band indicator).
- Distinguish delivery success from effect: code executed vs objective achieved vs objective persisted.
- Watch for deception and honeypot tells — effects that are too clean, mirrored responses, or verification channels the defender controls.
- Judge landed / partial / failed / uncertain, and decide whether to re-attempt, wait, or back off to avoid burning access.

## Signals / outputs
- Verdict on effect with the independent evidence supporting it.
- Explicit separation of delivery vs effect vs persistence.
- Deception-risk note and a next-action recommendation (confirm, retry, hold, withdraw).
