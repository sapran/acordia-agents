---
name: analytic-tooling-scripting
description: Use when manual analysis won't scale or repeat cleanly — script your own parsers, extractors, and transforms to turn raw take into answers instead of grinding it by hand.
metadata:
  acordia:
    grid_row: analytic-tooling-scripting
    grid_deep_in: [Core]
    grid_working_in: ['T&N', Def, Fus]
    source: docs/roles/operational-analyst.md#L108
---

# Analytic Tooling & Scripting

## Objective
Build and wield your own scripts and tools to process, transform, and interrogate collected data — the cross-cutting baseline that lets an analyst move faster than the take piles up.

## When to use
- When analysis is repetitive, large, or format-specific enough that a script beats manual work.
- When no off-the-shelf tool fits the data or the question, and you must make one.

## Method
- Reach for the right tool: shell and pipes for quick triage, a scripting language (Python) for structured parsing, transformation, and joins.
- Write parsers/extractors for the take's real format — decode, deserialise, and flatten proprietary or nested structures into something queryable.
- Automate the repeatable: encode recurring correlation, enrichment, and filtering as reusable scripts, not one-off keystrokes.
- Validate your tooling against known-good samples so a parsing bug doesn't silently manufacture a false conclusion.
- Keep tradecraft on the tools themselves — mind where they run, what they touch, and what traces the analysis environment leaves.

## Signals / outputs
- Reusable scripts/tools that convert raw take into structured, queryable answers.
- Automated pipelines for recurring parse-enrich-correlate work.
- Validated transforms with confidence that outputs reflect the source, not a bug.
