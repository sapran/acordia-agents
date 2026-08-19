---
name: assessing-take-value
description: Judge whether collected take is genuine, complete, current and worth having — the real thing rather than truncated, corrupted, wrongly decrypted or a deception feed planted for you to find — measured against an expected record count and against the requirement it was meant to answer, right after collection and before anything is built on it.
metadata:
  acordia:
    family: take-handling
    grid_row: assessing-take-value
    grid_deep_in: [Fus]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L103
---

# Assessing Value/Quality of the Collected Take

## Objective
Judge whether the collected take is real, reliable, and operationally valuable — the collection half of "did it land" — so downstream analysis is not built on noise, decoys, or worthless data.

## When to use
- Right after a collection action, before the take is fused or acted on.
- When deciding whether a source or feed is earning its risk and effort, or should be dropped.

## Method
- Inventory the delivered take before judging it: enumerate the files, records, or streams with `ls`/`find`/`glob` and a file-typing pass, and record the expected size or record count so completeness can be measured against a denominator rather than a feeling.
- Verify authenticity first, over exhaustive coverage: is this the real thing, or truncated, corrupted, decrypted-wrong, or a deception feed placed for you to find? Run a tool pass (`grep`/`rg`/a parser) across 100% of the bytes or records — a truncation or corruption verdict read off the opening portion is exactly the failure this discipline exists to prevent — and read only the located anomalies into context.
- Assess completeness and freshness — how much of the intended target did you actually get against the inventory count, and is it current or already superseded.
- Test relevance against the requirement: does this take answer a real question, or is it volume that merely feels like progress; cite the evidence behind each verdict as `<path>:<offset>` or `<path>@L<line>`.
- Estimate value against cost and exposure: what the take is worth versus the risk, time, and access burned to obtain it.
- Grade the source's track record — does this feed reliably produce, and does its output corroborate against independent strands.
- Degradation: if a parser for the take's format is unavailable, fall back to `strings` and structural sampling for an authenticity read and flag that completeness is unverified; if the take is encrypted and no key is at hand, record what can and cannot be judged rather than passing it as sound.

## Signals / outputs
- A take-quality verdict: authentic/complete/fresh/relevant, with each dimension scored.
- Value-versus-cost judgement on whether to keep, re-collect, or abandon the source.
- Flags for suspected deception, staleness, or partial collection that must caveat any downstream use.
