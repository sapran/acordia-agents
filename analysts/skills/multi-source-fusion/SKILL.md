---
name: multi-source-fusion
description: Use when you hold fragments from several sources — your own implant take, passive collection, OSINT, and non-technical context — and need one coherent target picture instead of a pile of disconnected observations.
---

# Multi-Source Fusion & Correlation

## Objective
Consolidate every strand of intelligence — your own take, collection feeds, open sources, and non-technical context — into a single coherent picture of the target that is greater than the sum of its sources.

## When to use
- When multiple sources touch the same target and no single one gives you the full answer, so the truth lives in the correlation.
- Before a decision that depends on a unified read (where to move, what to trust, when to act) rather than on any one feed.

## Method
- Inventory every strand: on-box take, passive/network collection, OSINT, prior operations, and human/business context — tag each with source, reliability, and timestamp.
- Resolve entities across sources — reconcile hostnames, IPs, identities, and accounts so the same object is one object, not several.
- Correlate on shared keys (identity, host, time, infrastructure) and look for convergence (independent sources agreeing) and contradiction (sources that cannot both be true).
- Weight by source reliability and independence; corroboration from genuinely independent sources beats volume from one echoing feed.
- State the fused picture as a judgement, not a data dump: what is known, what is inferred, what remains a gap.

## Signals / outputs
- A single fused target picture with entities resolved and sources cross-referenced.
- Convergence points (high-confidence facts) and contradictions flagged for resolution.
- A source-reliability trail so any conclusion can be walked back to its evidence.
