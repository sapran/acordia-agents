---
name: detection-capability-analysis
description: Model the defender's detection surface before you act, separating what their sensors can collect from what is collected and what is analysed into an alert.
metadata:
  acordia:
    family: defender-reading
    grid_row: detection-capability-analysis
    grid_deep_in: [Def]
    grid_working_in: [Core]
    row: detection-capability-analysis
    source: docs/roles/operational-analyst.md
---

# Detection-Capability Analysis

## Objective

Model the defender's detection surface in principle — sensors, log sources, coverage, and analytic maturity — so each planned action can be scored for how likely it is to generate an alert before it is taken.

## When to use

- Pre-op planning of a technique or kill-chain step, when you need to predict detectability rather than react to it.
- Anytime new environment recon reveals a security product, log pipeline, or SOC capability you had not accounted for.

## Method

- Enumerate the defender's likely sensor and log sources (EDR, network, identity, cloud, SIEM) from recon, vendor fingerprints, and environment class.
- Map each planned technique to the data source that would witness it, then to whether an analytic plausibly exists for it (MITRE ATT&CK data-source and detection coverage as a baseline).
- Separate "can be collected" from "is collected" from "is analyzed/alerted" — coverage gaps live between those layers.
- Rank techniques by residual detection risk; prefer actions witnessed only by sources the target does not collect or correlate.
- Flag high-confidence tripwires (canaries, honeytokens, signatured behaviors) as no-go without mitigation.

## Signals / outputs

- A per-technique detectability score with the specific log/sensor that would catch it.
- A ranked list of low-visibility paths and an explicit list of tripwires to avoid.
- Assumptions and unknowns that Overwatch and recon should resolve.
