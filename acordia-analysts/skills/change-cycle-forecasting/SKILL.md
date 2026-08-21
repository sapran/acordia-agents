---
name: change-cycle-forecasting
description: Forecast when the target will patch, upgrade, migrate, rotate credentials or decommission, dating every change-evidence source and reading the drivers behind it — vendor cadence, compliance deadlines, contract and fiscal cycles, EOL dates — to set the operational clock when an access depends on a version or config that may soon vanish, or on the exposure that churn opens.
metadata:
  acordia:
    family: target-modelling
    grid_row: change-cycle-forecasting
    grid_deep_in: [Mission]
    grid_working_in: [Terrain]
    row: change-cycle-forecasting
    source: docs/roles/operational-analyst.md
---

# Change-Cycle Forecasting

## Objective

Predict the timing of target-side change — patches, version upgrades, migrations, credential/key rotation, decommissions — to answer "if and when will the target change?" and set the operational clock accordingly.

## When to use

- When an access or exploit depends on a version/config that may soon disappear (or appear).
- When deciding whether to move now or wait for change-induced exposure (migration windows, fresh deployments, transition states).

## Method

- Inventory the change evidence before forecasting: enumerate the sources you hold — changelogs, version banners, cert transparency records, tender notices, job postings, DNS/host snapshots — with `ls`/`find`/`glob` or a saved-query list, and record each with its capture date, since a forecast is only as fresh as its stalest input.
- Identify the target's change drivers: vendor patch cadence, compliance deadlines, contract/renewal cycles, fiscal timing, EOL/support dates.
- Read observable change signals over exhaustive coverage — scan the full changelog or cert history rather than the latest entry, process every version string and host record a query returns, and read only the located deltas into context; a rotation cadence inferred from the most recent entry alone is a head sample.
- Model the maintenance rhythm: change windows, freeze periods, who approves, how slow they historically are to patch.
- Forecast the specific transition and its exposure: what is briefly weaker during a migration or rollout, and for how long, citing the evidence behind each predicted date as `<source>:<offset>` or `<source>@L<line>` (or source-plus-capture-date for a live-queried signal).
- Convert to an operational timeline — act-before-close vs exploit-the-churn — with confidence and refresh triggers.
- Degradation: if a changelog or release feed is unavailable, fall back to observable drift (banners, cert dates, host churn) and lower the forecast's confidence explicitly; if no change evidence is obtainable at all, say the timing is unknown rather than anchoring on cadence priors.

## Signals / outputs

- Forecast of likely patch/upgrade/rotation dates with confidence and the evidence behind each.
- Named exposure windows created by transitions.
- Go/wait recommendation tied to the closing or opening of the window.
