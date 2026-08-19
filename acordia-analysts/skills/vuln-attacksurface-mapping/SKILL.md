---
name: vuln-attacksurface-mapping
description: Use when you need to consolidate everything reachable into a ranked attack surface — where the target is weakest, prioritised by exploitability and by what it actually gets you toward the mission.
metadata:
  acordia:
    family: target-modelling
    grid_row: vuln-attacksurface-mapping
    grid_deep_in: ['T&N']
    grid_working_in: [Core, Def]
    source: docs/roles/operational-analyst.md#L89
---

# Vulnerability & Attack-Surface Mapping

## Objective
Build and prioritize the target's attack surface — every reachable entry point and its weaknesses — ranked not by CVSS but by exploitability times proximity to the crown jewels.

## When to use
- When terrain and mission analysis must converge into a decision on where to strike first.
- When there are more findings than time, and prioritization must reflect mission value.

## Method
- Inventory the reachable recon feeds with `glob` / `find` / `list`: external scan outputs, internal Nmap results, cloud-asset inventories, identity enumeration dumps, application/API catalogues, and human-surface OSINT.
- Read in bounded, context-scoped slices per source — one scanner report, one cloud-asset export, one identity slice — rather than concatenating every feed into a single wall of text in context; drive coverage with an exhaustive `grep`/parser pass over the whole feed to locate every candidate finding, then read the scoped range around each — every hit, not just the first.
- Aggregate the surface: external and internal exposure, services, apps/APIs, cloud, identity, and human entry points from all recon feeds.
- Assess each element for weakness — known vulns, misconfig, weak auth, exposure — and, critically, whether it is actually reachable and exploitable; cite each weakness by `<path>:<offset>` (byte) or `<path>@L<line>` (line) back to the scan or config line that grounds it.
- Weight by mission proximity: how close a foothold there sits to a crown jewel or mission choke point.
- Rank by exploitability x impact x cost/risk to use; prefer reliable, quiet paths over flashy ones.
- Keep it live — re-map as the target changes (see change-cycle forecasting) and as access alters what is reachable.
- If a scanner-output parser (e.g. an `nmap` XML reader, a cloud CSPM export tool) is unavailable, fall back to raw `grep` over the report files; if the underlying scan or asset feed was never produced, flag the gap and refuse to rank a surface you cannot see.

## Signals / outputs
- Consolidated attack-surface inventory with exploitability assessed.
- Prioritized target list ranked by mission-weighted value, not raw severity.
- Recommended initial and follow-on entry points with the path each opens toward the objective.
