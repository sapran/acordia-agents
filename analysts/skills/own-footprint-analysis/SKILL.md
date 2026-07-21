---
name: own-footprint-analysis
description: Use to enumerate every indicator your own operation emits — host, network, identity, and infrastructure artifacts — so you know exactly what a defender or responder could find and attribute.
---

# Own-Footprint / Emitted-Indicator Analysis

## Objective
Systematically enumerate the indicators the operation itself generates across every layer, producing the attacker's-eye inventory of "what we leave behind" that feeds evasion, Overwatch, and cleanup decisions.

## When to use
- Before, during, and after any phase, to keep a running ledger of emitted indicators.
- When preparing to go quiet, hand off, or exit, and you need to know what remains for a responder to find.

## Method
- Walk each layer and list artifacts: host (files, registry, services, prefetch, logs), network (C2 domains/IPs, JA3/JARM, TLS certs, User-Agents), identity (accounts, tokens, consent), and infrastructure (redirectors, VPS, registrant/OSINT leakage).
- For each indicator, record its fidelity (how uniquely it points to us), persistence (how long it survives), and observability (who can see it).
- Distinguish transient indicators (in-memory, session-scoped) from durable ones (on-disk, logged, registered) and flag the durable, high-fidelity ones as priority risk.
- Cross-check against the defender's known collection to see which emitted indicators are actually within their reach.
- Maintain the ledger as a living artifact; update it every time a new tool, host, or channel is introduced.

## Signals / outputs
- A layered indicator ledger with fidelity/persistence/observability per item.
- A prioritized list of durable, attributable artifacts requiring cleanup or avoidance.
- Inputs for Overwatch (what to watch for on the blue side) and for exit/cleanup planning.
