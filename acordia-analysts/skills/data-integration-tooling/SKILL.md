---
name: data-integration-tooling
description: Join heterogeneous take into one queryable corpus — normalising identities, timestamps, IPs and hosts into a common schema, picking a relational, graph or time-series join model to fit the question, then resolving, deduplicating and enriching entities across datasets — when repeated correlation on the same keys justifies a pipeline over one-off inspection.
metadata:
  acordia:
    family: take-handling
    grid_row: data-integration-tooling
    grid_deep_in: [Fus]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L104
---

# Data Integration & Correlation Tooling

## Objective
Provide the data-handling muscle behind fusion: ingest, normalise, and correlate large, mixed datasets so that patterns and links surface which no manual review would find.

## When to use
- When the collected take exceeds what you can read by hand, or spans formats (logs, dumps, captures, exports) that must be joined.
- When repeated correlation on the same keys justifies a pipeline over one-off inspection.

## Method
- Inventory the sources before joining: enumerate each input with `ls`/`find`/`glob`, type it, and record its expected record count, so the pipeline reconciles against a known denominator rather than absorbing a truncated feed silently.
- Ingest and normalise over exhaustive coverage: parse each source in full into a common schema — standardising identities, timestamps, IPs, and hosts — and assert the ingested row count against the inventory, never sampling the head of a large export as a stand-in for the whole.
- Choose the join model — relational, graph, or time-series — that fits the question; graph for relationships, time-series for sequence and cadence.
- Correlate at scale: link entities across datasets, deduplicate, and enrich with reference data to turn raw records into resolved objects.
- Query for the analytic question, not the data — build repeatable queries/pipelines that answer "who touched what, when, from where."
- Guard data integrity: track provenance so every resolved object carries its source rows as `<source-path>:<offset>` or `<source>@L<line>`, preserve originals, and keep transformations reversible so a conclusion can be audited back to source.
- Degradation: if a source cannot be parsed into the schema, hold it out of the join explicitly and report the coverage gap and its effect on any conclusion, rather than joining the parseable remainder and presenting it as complete.

## Signals / outputs
- A normalised, correlatable dataset with entities resolved across sources.
- Repeatable queries/pipelines that answer recurring fusion questions at scale.
- Provenance trail linking every derived link back to its raw records.
