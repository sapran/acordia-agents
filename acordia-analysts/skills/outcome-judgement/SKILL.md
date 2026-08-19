---
name: outcome-judgement
description: Call whether an action achieved the operation's intended end — the effect took hold on the target, or the intelligence was genuinely collected — by inventorying first-party against independent observable channels and separating 'the payload ran' from 'the system actually changed', immediately after any action whose success indicators are ambiguous, delayed or spoofable.
metadata:
  acordia:
    family: analytic-spine
    grid_row: outcome-judgement
    grid_deep_in: [Core, 'T&N']
    grid_working_in: [Fus]
    source: docs/roles/operational-analyst.md#L74
---

# Outcome Judgement (End Achieved)

## Objective
After an action, judge whether the operation's intended end was actually achieved — the effect (break / deny / manipulate) took hold, or the intelligence was genuinely collected — and decide what happens next. This includes verifying that the target system genuinely changed in the intended way, separating "the payload ran" from "the effect occurred," and both from what the target may be showing you deliberately.

## When to use
- An action has fired and you must call success or failure against the objective.
- The technique "worked" but it is unclear whether it produced the intended operational end.
- Immediately after any action intended to produce an effect (access gained, service disrupted, data altered, persistence set), especially when success indicators are ambiguous, delayed, or could be spoofed by the defender.

## Method
- Restate the intended end in observable terms before acting: what state must be true on the target if it worked. Judge against that — not against "did the tool run".
- **Inventory the observable channels before reading them** — command return, target-side logs, downstream service signals, out-of-band indicators — and record which are **first-party** (the tool's own report) and which are **independent**, because the split decides how much each is worth. Never rest a verdict on the tool's own success return alone.
- Gather independent observables with bounded, exhaustive reads: scope each source to the action's time window, but process every matching record in that window rather than the first hit, so a delayed or buffered effect is not missed.
- **Distinguish delivery from effect from persistence**: code executed vs objective achieved vs objective held under the target's response and not silently reverted or contained. Cite each supporting observable as `<log>:<offset>` or `<log>@L<line>`, capturing any transient downstream or out-of-band signal to a file first so the verdict stays auditable back to evidence.
- For collection specifically: confirm the data is genuine, complete enough, and not planted or partial (see `deception-detection`).
- **Watch for deception and honeypot tells** — effects that are too clean, mirrored responses, or verification channels the defender controls; treat a channel the defender may control as untrusted and flag the gap.
- Weigh cost paid: what the action cost in exposure, access, or attribution, and whether that changes the win.
- Classify: end achieved / partial / failed / unknown-pending-confirmation, and derive the next move — exploit, re-attempt, collect more, or withdraw.
- **Degradation**: if only the first-party return is available and no independent channel can be read, cap the verdict at "delivered, effect unconfirmed" and say so rather than reporting success.

## Signals / outputs
- A verdict on whether the operational end was met, with the confirming independent observation, and the explicit separation of delivery vs effect vs persistence.
- The residual cost/exposure the action incurred, and a deception-risk note.
- A next-move recommendation: exploit, re-attack, collect more, or disengage.
