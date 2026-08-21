---
name: endpoint-telemetry-edr
description: Reason about what a host sensor genuinely captures and by which mechanism — kernel callbacks, ETW providers, user-mode hooks, minifilters, AMSI, the deployed Sysmon configuration — and where that instrumentation goes blind, so you can choose between execution, injection or persistence primitives when one writes far richer endpoint telemetry than another.
metadata:
  acordia:
    family: defender-reading
    grid_row: endpoint-telemetry-edr
    grid_deep_in: [Def]
    grid_working_in: [Terrain]
    row: endpoint-telemetry-edr
    source: docs/roles/operational-analyst.md
---

# Endpoint Telemetry & EDR Internals

## Objective

Reason about what endpoint and EDR sensors actually capture — process, thread, image-load, registry, file, and network events — how they capture it, and where the instrumentation goes blind, so on-host actions are chosen to minimize recorded evidence.

## When to use

- Planning or executing any on-host action (execution, injection, persistence, credential access) on an endpoint that runs an EDR or host sensor.
- Deciding between execution primitives when one leaves richer telemetry than another.

## Method

- Inventory the collected endpoint evidence with `ls` / `find` / `glob` — sensor config exports, ETW provider manifests, EDR agent driver binaries, Sysmon config, exported event archives, and any SIEM extract for the host — and record sensor product + version per artefact.
- Identify the sensor and its collection mechanism (kernel callbacks, ETW providers, user-mode hooks, minifilter, AMSI) and enumerate the event types each produces. Read with bounded context, exhaustive coverage: `grep`/`rg` provider GUIDs and hooked-syscall lists across the whole driver/manifest slice; filter event archives with time-window or event-id queries (`Get-WinEvent -FilterHashtable`, targeted `evtx` queries) rather than dumping full channels into context — scope the query to the analytic question, then process every event it matches, not the first screenful.
- Trace your planned action through those hooks: which callbacks fire, what fields are populated, what gets shipped to the SIEM vs. held locally.
- Locate blind spots — unhooked syscalls, ETW providers that can be tampered/disabled, direct/indirect syscall paths, sensor coverage gaps for a given OS or agent version.
- Prefer primitives that touch the fewest high-fidelity providers; treat tamper actions themselves as loud events that may be watched.
- Account for local buffering and delayed upload — evidence can surface after the fact even if no real-time alert fired. Cite each finding as `<artefact>@L<line>` for text/config/manifest evidence or `<evtx-or-archive>:<record-id>` (or `:<offset>`) for event-log evidence.
- Degradation: if the sensor's driver/manifest is opaque or unavailable, fall back to observed telemetry (event archives, SIEM extracts) and public provider documentation; if event archives are unavailable, restrict to config-only reasoning and flag the reduced confidence; if neither is available for the specific agent version in play, flag the gap and stop.

## Signals / outputs

- An event-by-event forecast of the telemetry a planned action emits, per provider.
- A shortlist of lower-telemetry execution paths and the blind spots they exploit.
- Notes on tamper-detection risk and post-hoc evidence that Overwatch must monitor.
