---
name: ot-embedded
description: Use when the target includes ICS/SCADA, PLCs, or embedded devices — analyse OT and embedded environments where protocols, physics, and fragility differ sharply from IT.
metadata:
  acordia:
    grid_row: ot-embedded
    grid_deep_in: []
    grid_working_in: ['T&N', Def]
    source: docs/roles/operational-analyst.md#L109
---

# Operational-Technology / Embedded

## Objective
Analyse operational-technology and embedded environments — ICS/SCADA, PLCs, controllers, and firmware — on their own terms. This is a cross-cutting deep skill that attaches to whichever analytic leg (targeting, mapping, effects, verification) the operation puts against an OT/embedded target.

## When to use
- When the target crosses from IT into OT/embedded: industrial control, building systems, medical, automotive, or bespoke hardware.
- When IT assumptions break — where downtime is physical, protocols are proprietary, and a wrong move has kinetic consequences.

## Method
- Learn the specific environment: identify controllers, buses, and industrial protocols (Modbus, DNP3, S7, EtherNet/IP) and how the process actually maps to the equipment.
- Analyse firmware and embedded logic — extract, understand memory and I/O, and reason about behaviour without the safety net of a normal OS.
- Respect the physics: model the process the OT controls, so effects and side-effects are understood before, not after, they manifest in the real world.
- Read OT-specific telemetry and engineering artefacts (HMI projects, ladder logic, historian data) for state, intent, and safety interlocks.
- Weight fragility and consequence heavily — legacy, unpatched, safety-critical systems fail hard, and detection and damage both differ from IT.

## Signals / outputs
- A model of the OT/embedded target: devices, protocols, process, and controlling logic.
- Firmware/embedded behaviour analysis with I/O and memory understanding.
- Consequence and safety assessment tying any action to its physical effect.
