---
name: data-integration-tooling
description: Use when the take is too big or too mixed to correlate by hand — build the data-handling pipeline that ingests, normalises, and joins large heterogeneous datasets so fusion can happen at scale.
metadata:
  acordia:
    grid_row: data-integration-tooling
    grid_deep_in: [Fus]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L105
---

# Data Integration & Correlation Tooling

## Objective
Provide the data-handling muscle behind fusion: ingest, normalise, and correlate large, mixed datasets so that patterns and links surface which no manual review would find.

## When to use
- When the collected take exceeds what you can read by hand, or spans formats (logs, dumps, captures, exports) that must be joined.
- When repeated correlation on the same keys justifies a pipeline over one-off inspection.

## Method
- Ingest and normalise: parse each source into a common schema, standardising identities, timestamps, IPs, and hosts so cross-source joins are possible.
- Choose the join model — relational, graph, or time-series — that fits the question; graph for relationships, time-series for sequence and cadence.
- Correlate at scale: link entities across datasets, deduplicate, and enrich with reference data to turn raw records into resolved objects.
- Query for the analytic question, not the data — build repeatable queries/pipelines that answer "who touched what, when, from where."
- Guard data integrity: track provenance, preserve originals, and keep transformations reversible so a conclusion can be audited back to source.

## Signals / outputs
- A normalised, correlatable dataset with entities resolved across sources.
- Repeatable queries/pipelines that answer recurring fusion questions at scale.
- Provenance trail linking every derived link back to its raw records.
