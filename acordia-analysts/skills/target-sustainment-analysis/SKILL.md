---
name: target-sustainment-analysis
description: Model whether a target can keep its mission running through suppliers, spares, transport, repair, people and external services, when continuity or recovery is in question.
metadata:
  acordia:
    family: target-modelling
    grid_row: target-sustainment-analysis
    grid_deep_in: [Mission]
    grid_working_in: []
    row: target-sustainment-analysis
    source: docs/roles/operational-analyst.md
    doctrine_source: [ACORDIA#analysis, MTA#mission-process-thread, Sand#weaponization-of-friction, Rovner#three-propositions, CCH2#resilience, Orye-Maennel#effect-assessment]
---

# Target Sustainment Analysis

## Objective

Establish whether a target organisation can continue its mission when the suppliers, stock and spares, transport, maintenance, trained people, contractors, or external services that sustain it are constrained.

## When to use

- When a mission thread is known but the conditions that keep it running are not.
- When continuity, recovery, redundancy, or the organisational consequence of a disruption must be judged.

## Method

- Start with `target-mission-analysis`: state the mission process and the output it must continue to produce. Map the target-side dependencies that sustain each step — supplier or contractor, stock or spare, transport or distribution, maintenance or repair, trained person, or external service.
- For every dependency, record its mission role, owner or provider, evidence and confidence, cadence or capacity constraint, alternative, and recovery implication. Keep observed relationships separate from inference; a missing stock level, contract, route, or service arrangement is a named gap, not an assumed link.
- Use `nontechnical-context-integration` for supplier, contractor, finance, procurement, and organisational context; use `change-cycle-forecasting` for replenishment, maintenance, replacement, and change timing. Digital supply-chain analysis — software components, CI/CD, package registries, cloud-service dependency graphs, and equivalent ecosystems — is out of scope.
- Use `target-friction-susceptibility` to assess redundancy, trained alternatives, process rigidity, reporting culture, and the absorption horizon. State what degrades first, what alternative keeps the mission moving, and what recovery depends on.
- Use `outcome-judgement` to plan independent first-, second-, and third-order observables that would show whether mission capability changed rather than only a supporting system state.

## Signals / outputs

- Sustainment model: mission steps and their target-side sustaining dependencies.
- Critical-dependency register: role, evidence, uncertainty, alternatives, cadence/capacity constraint, and recovery condition.
- Resilience assessment: redundancy, trained alternatives, absorption horizon, and recovery constraints.
- Effect-assessment plan: first-, second-, and third-order observables that would distinguish system disturbance from mission consequence.

## Boundary

This is an organisational analysis for a human operator. It does not rank intervention points, recommend action, model the analyst’s own operation, or cover digital supply chains. The full evidence and reasoning belong in the task notes; hand back the judgement, confidence, gaps, and notes-file location.