---
name: change-cycle-forecasting
description: Use when an operation's window depends on target change — forecast if and when the target will patch, upgrade, migrate, or rotate, so you can time access before it closes or exploit the churn while it's open.
metadata:
  acordia:
    grid_row: change-cycle-forecasting
    grid_deep_in: ['T&N']
    grid_working_in: []
    source: docs/roles/operational-analyst.md#L81
---

# Change-Cycle Forecasting

## Objective
Predict the timing of target-side change — patches, version upgrades, migrations, credential/key rotation, decommissions — to answer "if and when will the target change?" and set the operational clock accordingly.

## When to use
- When an access or exploit depends on a version/config that may soon disappear (or appear).
- When deciding whether to move now or wait for change-induced exposure (migration windows, fresh deployments, transition states).

## Method
- Identify the target's change drivers: vendor patch cadence, compliance deadlines, contract/renewal cycles, fiscal timing, EOL/support dates.
- Read observable change signals — job postings, tender notices, changelog/version drift, cert renewals, new subdomains/hosts appearing.
- Model the maintenance rhythm: change windows, freeze periods, who approves, how slow they historically are to patch.
- Forecast the specific transition and its exposure: what is briefly weaker during a migration or rollout, and for how long.
- Convert to an operational timeline — act-before-close vs exploit-the-churn — with confidence and refresh triggers.

## Signals / outputs
- Forecast of likely patch/upgrade/rotation dates with confidence and the evidence behind each.
- Named exposure windows created by transitions.
- Go/wait recommendation tied to the closing or opening of the window.
