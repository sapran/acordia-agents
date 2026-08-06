---
name: effect-on-target-verification
description: Use after an action to confirm the target system actually changed — read the effects side of "did it land," distinguishing real effect from delivery success, cover story, or defender illusion.
metadata:
  acordia:
    grid_row: effect-on-target-verification
    grid_deep_in: ['T&N']
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L82
---

# Effect-on-Target Verification

## Objective
After an operational action, determine whether the target system genuinely changed in the intended way — separating "the payload ran" from "the effect occurred," and both from what the target may be showing you deliberately.

## When to use
- Immediately after any action intended to produce an effect (access gained, service disrupted, data altered, persistence set).
- When success indicators are ambiguous, delayed, or could be spoofed by the defender.

## Method
- Define the expected effect concretely before acting: what state must be true on the target if it worked.
- Inventory the observable channels before reading them — command return, target-side logs, downstream service signals, out-of-band indicators — and record which are first-party (the tool's own report) and which are independent, because the split decides how much each is worth.
- Gather independent observables with bounded, exhaustive reads: scope each source to the action's time window, but process every matching record in that window rather than the first hit, so a delayed or buffered effect is not missed; never rest a verdict on the tool's own success return alone.
- Distinguish delivery success from effect: code executed vs objective achieved vs objective persisted, and cite each supporting observable as `<source>:<offset>` or `<log>@L<line>` (or source-plus-timestamp for a console signal) so the verdict is auditable back to evidence.
- Watch for deception and honeypot tells — effects that are too clean, mirrored responses, or verification channels the defender controls.
- Judge landed / partial / failed / uncertain, and decide whether to re-attempt, wait, or back off to avoid burning access.
- Degradation: if only the first-party return is available and no independent channel can be read, cap the verdict at "delivered, effect unconfirmed" and say so rather than reporting success; if a verification channel is one the defender may control, treat it as untrusted and flag the gap.

## Signals / outputs
- Verdict on effect with the independent evidence supporting it.
- Explicit separation of delivery vs effect vs persistence.
- Deception-risk note and a next-action recommendation (confirm, retry, hold, withdraw).
