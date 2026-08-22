---
name: hypothesis-testing
description: Hold every plausible explanation at once and score evidence against each, weighting what discriminates and hunting what would kill the leader, when several readings fit.
metadata:
  acordia:
    family: analytic-spine
    grid_row: hypothesis-testing
    grid_deep_in: [Core]
    grid_working_in: [Mission, Terrain, Def, Coll]
    row: hypothesis-testing
    source: docs/roles/operational-analyst.md
---

# Hypothesis Testing (Competing Hypotheses)

## Objective

Hold every plausible explanation of the target situation at once and test each against the evidence together, so the surviving judgement is the one least contradicted rather than the one you liked first.

## When to use

- The evidence admits several readings (attribution, target function, detection status, intent).
- You notice yourself building a case for a single explanation instead of comparing.

## Method

- Enumerate the full set of hypotheses up front, including the uncomfortable ones (you are burned; the target is a decoy/honeypot).
- Build an evidence-by-hypothesis matrix; score each item for consistency with each hypothesis, not just the favoured one.
- Weight diagnostic evidence — items that discriminate between hypotheses — and discount evidence consistent with all of them.
- Try to disconfirm: seek the observation that would kill the leading hypothesis, and task collection for it.
- Rank by fewest inconsistencies; carry the runner-up forward rather than discarding it.

## Signals / outputs

- A ranked set of hypotheses with the evidence that supports and undercuts each.
- The most diagnostic missing observation, handed to collection.
- A lead judgement plus the surviving alternative you keep watching.
