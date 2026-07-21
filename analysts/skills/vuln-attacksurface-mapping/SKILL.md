---
name: vuln-attacksurface-mapping
description: Use when you need to consolidate everything reachable into a ranked attack surface — where the target is weakest, prioritised by exploitability and by what it actually gets you toward the mission.
---

# Vulnerability & Attack-Surface Mapping

## Objective
Build and prioritize the target's attack surface — every reachable entry point and its weaknesses — ranked not by CVSS but by exploitability times proximity to the crown jewels.

## When to use
- When terrain and mission analysis must converge into a decision on where to strike first.
- When there are more findings than time, and prioritization must reflect mission value.

## Method
- Aggregate the surface: external and internal exposure, services, apps/APIs, cloud, identity, and human entry points from all recon feeds.
- Assess each element for weakness — known vulns, misconfig, weak auth, exposure — and, critically, whether it is actually reachable and exploitable.
- Weight by mission proximity: how close a foothold there sits to a crown jewel or mission choke point.
- Rank by exploitability x impact x cost/risk to use; prefer reliable, quiet paths over flashy ones.
- Keep it live — re-map as the target changes (see change-cycle forecasting) and as access alters what is reachable.

## Signals / outputs
- Consolidated attack-surface inventory with exploitability assessed.
- Prioritized target list ranked by mission-weighted value, not raw severity.
- Recommended initial and follow-on entry points with the path each opens toward the objective.
