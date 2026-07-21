---
name: endpoint-telemetry-edr
description: Use when an operation touches a monitored endpoint and you must predict what the EDR/host sensor records about your actions and which execution paths slip past its instrumentation.
---

# Endpoint Telemetry & EDR Internals

## Objective
Reason about what endpoint and EDR sensors actually capture — process, thread, image-load, registry, file, and network events — how they capture it, and where the instrumentation goes blind, so on-host actions are chosen to minimize recorded evidence.

## When to use
- Planning or executing any on-host action (execution, injection, persistence, credential access) on an endpoint that runs an EDR or host sensor.
- Deciding between execution primitives when one leaves richer telemetry than another.

## Method
- Identify the sensor and its collection mechanism (kernel callbacks, ETW providers, user-mode hooks, minifilter, AMSI) and enumerate the event types each produces.
- Trace your planned action through those hooks: which callbacks fire, what fields are populated, what gets shipped to the SIEM vs. held locally.
- Locate blind spots — unhooked syscalls, ETW providers that can be tampered/disabled, direct/indirect syscall paths, sensor coverage gaps for a given OS or agent version.
- Prefer primitives that touch the fewest high-fidelity providers; treat tamper actions themselves as loud events that may be watched.
- Account for local buffering and delayed upload — evidence can surface after the fact even if no real-time alert fired.

## Signals / outputs
- An event-by-event forecast of the telemetry a planned action emits, per provider.
- A shortlist of lower-telemetry execution paths and the blind spots they exploit.
- Notes on tamper-detection risk and post-hoc evidence that Overwatch must monitor.
