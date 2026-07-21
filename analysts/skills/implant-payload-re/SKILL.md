---
name: implant-payload-re
description: Use to reverse-engineer an implant or payload's real behavior — ours, a competitor's, or a captured sample — to understand exactly what it does, what it emits, and how it would be detected.
---

# Implant/Payload Behaviour & Reverse-Engineering

## Objective
Reverse-engineer implant/payload behavior to ground-truth what it actually does on a host and over the wire. This is a CROSS-CUTTING deep skill: it attaches to whichever leg needs it — Target & Network (understanding a target's malware or a tool you'll deploy) or Defender & Detection (predicting the artifacts and signatures a payload emits) — for a given operation.

## When to use
- Validating your own tooling's real footprint before deployment, or triaging unexpected behavior in the field.
- Analyzing a captured, third-party, or competitor sample to understand capability, indicators, and attribution.

## Method
- Triage statically first: file type, packing, imports, strings, embedded config, and signing — cheap signal before you run anything.
- Analyze safely in an isolated, instrumented environment; assume anti-analysis and sandbox-evasion and account for it.
- Recover behavior dynamically: process/thread activity, injection, persistence, file/registry changes, and full network/C2 behavior.
- Extract config and IOCs — keys, domains, mutexes, campaign markers — and map behavior to ATT&CK techniques and the telemetry each would produce.
- Feed findings to the leg that needs them: detection-signature prediction for blue-side reasoning, or capability/attribution for target work.

## Signals / outputs
- A behavior profile: what it does on host and network, plus its anti-analysis tricks.
- Extracted config, IOCs, and an emitted-signature map tied to detection sources.
- Attribution and capability notes routed to the relevant operational leg.
