---
name: naming-the-gaps
description: Convert a vague sense of knowing too little into ranked intelligence gaps, each an answerable question with a collection route and an owner, when collection has no stated question.
metadata:
  acordia:
    family: analytic-spine
    grid_row: naming-the-gaps
    grid_deep_in: [Core]
    grid_working_in: [Coll]
    row: naming-the-gaps
    source: docs/roles/operational-analyst.md
---

# Naming the Gaps

## Objective

Convert a vague sense of "we don't know enough" into an explicit, prioritised list of intelligence gaps, each tied to a way to close it, so collection is aimed instead of opportunistic.

## When to use

- Before committing a method, timing, or targeting decision that rests on assumed facts.
- When collection is running but nobody can say what it is actually meant to answer.

## Method

- Restate the decision the picture must support; every gap is judged by whether it changes that decision.
- Walk the target model deliberately (access, structure, defences, people, timing) and mark each element as observed, inferred, or blank.
- For each blank, name the specific question in answerable form, not a topic ("does host X reboot nightly?" not "patching").
- Rank gaps by leverage over the decision times feasibility of closing them; drop the merely-interesting.
- Assign each priority gap a collection route (existing access, new access needed, or open-source) and an owner.

## Signals / outputs

- A ranked gap list, each item phrased as an answerable question.
- A collection tasking: what to look at, through which access, and by when.
- A "decide anyway" line marking which gaps you will accept as open risk.
