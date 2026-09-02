---
name: method-timing-risk-decision
description: Choose the method, the moment and the exposure by pricing each option's gain, detection risk and reversibility against stated risk appetite, when a window is closing.
metadata:
  acordia:
    family: analytic-spine
    grid_row: method-timing-risk-decision
    grid_deep_in: [Core]
    grid_working_in: [Mission, Terrain, Def, Coll]
    row: method-timing-risk-decision
    source: docs/roles/operational-analyst.md
    doctrine_source: [ACORDIA#exploit-contingency]
---

# Method / Timing / Risk Decision

## Objective

Choose the method to use, the moment to move, and the exposure to accept, by comparing the live options against the objective and the operation's risk tolerance rather than defaulting to the most familiar tool.

## When to use

- Multiple viable methods exist and they trade off effect, stealth, and reversibility differently.
- Timing matters — a window is opening or closing on the target.

## Method

- Restate the objective and the hard constraints (stealth required, deadline, no-go effects) the choice must respect.
- Lay out each option's expected gain, its exposure/detection risk, and its reversibility side by side.
- Price timing explicitly: what a window opening or closing does to each option's risk and payoff.
- Weigh options against the operation's stated risk appetite, not the analyst's; flag any option that exceeds it.
- Recommend one course with its trigger to execute, and keep a named fallback if the window or the picture shifts.

## When an exploit is the right method

An exploit is one method among several, chosen on the same terms as any other and not because it is the most familiar instrument. Used selectively, not reflexively.

**Reach for one** against a hardened perimeter with no alternative, under time pressure, or to escalate on a well-configured system.

**Leave it** when detection risk exceeds its value, when stability matters, when a zero-day is worth preserving, or when a credential, an administrative tool or a native protocol would do the same work. Most of what sustains access after entry is not exploitation at all, so price the quiet path before the loud one and say plainly when the quiet path wins.

## Signals / outputs

- A recommended method, timing, and accepted risk level, with the reasoning.
- A comparison of the rejected options and why they lost.
- The execute-trigger and the fallback branch.
