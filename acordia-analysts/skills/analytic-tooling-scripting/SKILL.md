---
name: analytic-tooling-scripting
description: Script your own parser or transform for the take's format, reconciling output records against an inventory denominator so a silent parse failure cannot hide, when no tool fits.
metadata:
  acordia:
    family: analytic-spine
    grid_row: analytic-tooling-scripting
    grid_deep_in: [Core]
    grid_working_in: [Mission, Terrain, Def, Coll]
    row: analytic-tooling-scripting
    source: docs/roles/operational-analyst.md
---

# Analytic Tooling & Scripting

## Objective

Build and wield your own scripts and tools to process, transform, and interrogate collected data — the cross-cutting baseline that lets an analyst move faster than the take piles up.

## When to use

- When analysis is repetitive, large, or format-specific enough that a script beats manual work.
- When no off-the-shelf tool fits the data or the question, and you must make one.

## Method

- Inventory the take before writing anything: enumerate the inputs with `ls`/`find`/`glob` and a file-typing pass, and record the record or byte count each input should yield, so the tool has a denominator to reconcile against.
- Reach for the right tool: shell and pipes for quick triage, a scripting language (Python) for structured parsing, transformation, and joins.
- Write parsers/extractors for the take's real format — decode, deserialise, and flatten proprietary or nested structures into something queryable — and run them over 100% of the records, never against the opening sample alone: a parser validated on the first rows and let loose on the rest is how a head sample masquerades as full coverage.
- Reconcile coverage explicitly: assert the output record count against the inventory denominator and account for every dropped or unparsed record, so a silent parse failure cannot shrink the dataset unnoticed.
- Automate the repeatable: encode recurring correlation, enrichment, and filtering as reusable scripts, not one-off keystrokes, and carry each derived row's provenance (`<source-path>:<offset>` or `<source>@L<line>`) so a conclusion can be traced back to the source record.
- Validate your tooling against known-good samples so a parsing bug doesn't silently manufacture a false conclusion.
- Keep tradecraft on the tools themselves — mind where they run, what they touch, and what traces the analysis environment leaves.
- Degradation: if no parser exists for a format and one cannot be written in the time available, process what is parseable, quarantine the remainder, and report the uncovered fraction rather than treating the parsed subset as the whole.

## Signals / outputs

- Reusable scripts/tools that convert raw take into structured, queryable answers.
- Automated pipelines for recurring parse-enrich-correlate work.
- Validated transforms with confidence that outputs reflect the source, not a bug.
