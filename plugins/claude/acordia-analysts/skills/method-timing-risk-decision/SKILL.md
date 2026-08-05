---
name: method-timing-risk-decision
description: Use when several ways to reach the objective are on the table and you must choose which method, at what moment, and at what exposure — before committing the operation to one of them.
metadata:
  acordia:
    grid_row: method-timing-risk-decision
    grid_deep_in: [Core]
    grid_working_in: ['T&N', Def, Fus]
    source: docs/roles/operational-analyst.md#L73
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

## Signals / outputs
- A recommended method, timing, and accepted risk level, with the reasoning.
- A comparison of the rejected options and why they lost.
- The execute-trigger and the fallback branch.
