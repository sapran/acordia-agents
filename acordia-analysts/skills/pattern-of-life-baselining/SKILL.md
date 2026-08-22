---
name: pattern-of-life-baselining
description: Baseline the target's normal rhythms from authentication, telemetry and calendar sources — working hours, admin windows, batch jobs — so activity can be timed into the routine.
metadata:
  acordia:
    family: target-modelling
    grid_row: pattern-of-life-baselining
    grid_deep_in: [Mission]
    grid_working_in: [Core, Terrain]
    row: pattern-of-life-baselining
    source: docs/roles/operational-analyst.md
---

# Pattern-of-Life / Behavioural Baselining

## Objective

Establish the target's baseline behaviour across people and machines so operational activity can be timed to blend in, and so deviations (yours or the defender's) stand out on demand.

## When to use

- Before acting inside a target, to schedule activity into normal rhythm and avoid tripping behavioural detection.
- When you need to distinguish routine noise from meaningful change (admin logon, a new tool, a hunt in progress).

## Method

- Inventory the temporal data sources with `glob` / `find` / `list`: authentication logs, EDR process telemetry, mail/calendar exports, scheduled-task dumps, and any prior baseline artefacts.
- Read in bounded, context-scoped slices per source — one week of logon events, one admin's process tree, one service account's scheduled runs — rather than ingesting months of raw log into context wholesale; drive coverage with an exhaustive `grep`/parser pass over the whole source to isolate every actor or time window in scope, then read the scoped line range around each — every hit, not just the first.
- Collect temporal data: logon times, working hours, timezone, admin windows, backup/patch jobs, batch runs, beacon-friendly idle periods.
- Profile per-actor patterns — a given admin's hosts, tools, and cadence; a service account's fixed behaviour; a system's periodic traffic; cite each pattern claim by `<path>:<offset>` (byte) or `<path>@L<line>` (line) back to the log line that supports it.
- Separate human rhythm from automation rhythm; automation is regular and forgeable, humans are irregular and observant.
- Derive blend-in windows and cover: when your action looks like theirs, and which identity/host makes it plausible.
- Re-baseline periodically — normal drifts, and a stale baseline turns your cover into an anomaly.
- If a log-parsing helper (e.g. `evtx_dump`, `chainsaw`, a SIEM export tool) is unavailable, fall back to raw `grep` over the collected exports; if the collection itself is missing the relevant time window, flag the gap and mark the baseline partial rather than extrapolate.

## Signals / outputs

- Baseline profiles per user/admin/system with active hours and typical actions.
- Quiet windows and high-cover windows for operational timing.
- Anomaly triggers that flag defender activity or environment change.
