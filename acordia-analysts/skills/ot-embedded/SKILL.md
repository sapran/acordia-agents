---
name: ot-embedded
description: Analyse an industrial or embedded target on its own terms — controllers, buses, proprietary protocols, carved firmware — where downtime is physical and fragility is the constraint.
metadata:
  acordia:
    family: target-modelling
    grid_row: ot-embedded
    grid_deep_in: []
    grid_working_in: [Terrain, Def]
    row: ot-embedded
    source: docs/roles/operational-analyst.md
---

# Operational-Technology / Embedded

## Objective

Analyse operational-technology and embedded environments — ICS/SCADA, PLCs, controllers, and firmware — on their own terms. This is a cross-cutting deep skill that attaches to whichever analytic leg (targeting, mapping, effects, verification) the operation puts against an OT/embedded target.

## When to use

- When the target crosses from IT into OT/embedded: industrial control, building systems, medical, automotive, or bespoke hardware.
- When IT assumptions break — where downtime is physical, protocols are proprietary, and a wrong move has kinetic consequences.

## Method

- Inventory the collected OT evidence first with `ls`/`find`/`glob` and a file-typing pass — firmware images, HMI project files, ladder-logic exports, historian dumps, PCAPs of industrial protocols — recording device, vendor, and firmware version per artefact before any read.
- Learn the specific environment: identify controllers, buses, and industrial protocols (Modbus, DNP3, S7, EtherNet/IP) and how the process actually maps to the equipment.
- Analyse firmware and embedded logic with bounded reads over exhaustive coverage: carve and enumerate the image with `binwalk`/`strings` across 100% of its bytes, then read only the located regions (offsets, function bounds) into context rather than loading a multi-megabyte image; reason about memory and I/O without the safety net of a normal OS.
- Respect the physics: model the process the OT controls, so effects and side-effects are understood before, not after, they manifest in the real world.
- Read OT-specific engineering artefacts (HMI projects, ladder logic, historian data) for state, intent, and safety interlocks, processing every located hit rather than the first, and cite each finding as `<artefact>:<offset>` for binary evidence or `<artefact>@L<line>` for text/project exports.
- Weight fragility and consequence heavily — legacy, unpatched, safety-critical systems fail hard, and detection and damage both differ from IT.
- Degradation: if a firmware image is encrypted or a proprietary project format has no available parser, fall back to protocol capture and observable process behaviour and flag the reduced confidence; if a vendor's format is entirely opaque with no tool to read it, flag the gap and stop rather than guessing.

## Signals / outputs

- A model of the OT/embedded target: devices, protocols, process, and controlling logic.
- Firmware/embedded behaviour analysis with I/O and memory understanding.
- Consequence and safety assessment tying any action to its physical effect.
