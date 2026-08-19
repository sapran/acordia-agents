---
name: own-footprint-analysis
description: Use to enumerate every indicator your own operation emits — host, network, identity, and infrastructure artifacts — so you know exactly what a defender or responder could find and attribute.
metadata:
  acordia:
    family: defender-reading
    grid_row: own-footprint-analysis
    grid_deep_in: [Def]
    grid_working_in: []
    source: docs/roles/operational-analyst.md#L95
---

# Own-Footprint / Emitted-Indicator Analysis

## Objective
Systematically enumerate the indicators the operation itself generates across every layer, producing the attacker's-eye inventory of "what we leave behind" that feeds evasion, Overwatch, and cleanup decisions.

## When to use
- Before, during, and after any phase, to keep a running ledger of emitted indicators.
- When preparing to go quiet, hand off, or exit, and you need to know what remains for a responder to find.

## Method
- Inventory the operation's own emitted-artefact set with `glob` / `find` / `list`: staging logs, C2 configs, tooling manifests, redirector/VPS records, and any collection our own dry-runs produced.
- Read in bounded, context-scoped slices — a single log day, a single host's exported registry hive, a single beacon PCAP window — rather than dumping the entire operation's ledger into context at once; drive coverage with an exhaustive `grep`/parser pass over the whole source to isolate every indicator, then read the scoped line range around each — every hit, not just the first.
- Walk each layer and list artifacts: host (files, registry, services, prefetch, logs), network (C2 domains/IPs, JA3/JARM, TLS certs, User-Agents), identity (accounts, tokens, consent), and infrastructure (redirectors, VPS, registrant/OSINT leakage).
- For each indicator, record its fidelity (how uniquely it points to us), persistence (how long it survives), and observability (who can see it); cite each ledger entry by `<path>:<offset>` (byte) or `<path>@L<line>` (line) back to the source artefact so the ledger stays auditable.
- Distinguish transient indicators (in-memory, session-scoped) from durable ones (on-disk, logged, registered) and flag the durable, high-fidelity ones as priority risk.
- Cross-check against the defender's known collection to see which emitted indicators are actually within their reach.
- Maintain the ledger as a living artifact; update it every time a new tool, host, or channel is introduced.
- If a specialised triage helper (e.g. `KAPE`-style timelining, JA3/JARM extractor, prefetch parser) is unavailable, fall back to manual `grep`-driven reads of the raw exports; if the operational logs themselves were never collected, flag the gap and mark the ledger incomplete rather than infer emissions from memory.

## Signals / outputs
- A layered indicator ledger with fidelity/persistence/observability per item.
- A prioritized list of durable, attributable artifacts requiring cleanup or avoidance.
- Inputs for Overwatch (what to watch for on the blue side) and for exit/cleanup planning.
