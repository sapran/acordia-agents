---
name: target-friction-susceptibility
description: Establish how much friction a target organisation absorbs before its performance degrades — SOP rigidity, redundancy, whether its culture surfaces problems — when the end is disruption.
metadata:
  acordia:
    family: target-modelling
    grid_row: target-friction-susceptibility
    grid_deep_in: [Mission]
    grid_working_in: []
    row: target-friction-susceptibility
    source: docs/roles/operational-analyst.md
    doctrine_source: [Rovner#three-propositions, Sand#weaponization-of-friction]
---

# Target Friction Susceptibility

## Objective

Predict whether degrading a target's systems will degrade the target, by reading the organisation
rather than the estate. Two organisations on identical infrastructure absorb the same disruption
very differently, and the difference is bureaucratic, not technical.

## When to use

- When the operation's end is disruption, degradation or delay rather than collection, and someone
  must say whether the effect will propagate past the machine it lands on.
- When choosing between candidate targets whose technical exposure is comparable.
- When judging, after an action, why an effect that clearly landed technically produced no
  organisational consequence.

## Method

- Establish the **process rigidity**: does the organisation run one operating model applied to the
  letter, or does it improvise? Strict adherence maximises efficiency unstressed and becomes the
  vulnerability when the model itself is attacked. Look for single documented procedures, mandated
  tooling, and change control that admits no exception.
- Inventory **redundancy in all three forms**, because resilience is their combination and not any
  one alone: backup systems, diverse processes that reach the same outcome by different means, and
  **personnel trained and willing to switch to them**. An organisation with warm standby hardware and
  nobody drilled on it is not redundant.
- Read the **reporting culture**, which governs whether friction compounds or gets caught. Two ideal
  types bracket the range. Where personnel are expected to resolve problems alone — reporting reads
  as professional failure, asking for help as waste — faults stay local, causes go unfound, and
  nobody connects two symptoms in different departments. Where disclosure is immediate and expected,
  practical effects resolve faster, but the same norms invite blame-shifting and the damage lands on
  morale and mutual trust instead.
- Therefore score the two effects separately. A disclosure culture is **resistant to practical
  degradation and exposed to psychological degradation**; a silence culture is the reverse. Naming
  which one is being pursued is part of the judgement, not a detail.
- Identify the **load-bearing routines** rather than the load-bearing servers: the recurring work
  whose delay is felt elsewhere — shift handover, reconciliation, dispatch, approval chains,
  procurement. Friction injected into a routine radiates; friction injected into an idle system does
  not.
- Estimate the **absorption horizon**: how long the organisation continues to function while
  degraded, and whether the operation's timescale is shorter than that. Friction accumulates slowly,
  so an effect that would tell over months is worthless against a deadline of days.
- Degradation: where the target's internal procedures are not observable, substitute regulated or
  published analogues — sector rules, audit findings, filings, job advertisements naming tooling and
  shift patterns — and record the substitution rather than presenting the inference as observed.

## Signals / outputs

- A susceptibility read per candidate effect: would this degrade the organisation, or only the host.
- Separate practical and psychological effect estimates, with the culture type each rests on.
- The named routines whose disruption propagates, and the ones that would be absorbed unnoticed.
- An absorption horizon, stated against the operation's own timescale.
- Explicit flags where the read is inferred from external analogues rather than observed.
