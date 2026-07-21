---
name: c2-beacon-exfil-analysis
description: Use to analyze your own command-and-control, beaconing, and exfiltration traffic for the signatures a network defender could detect — before the channel gets you caught.
---

# C2 / Beacon / Exfil-Signal Analysis

## Objective
Examine the operation's own C2, beacon, and exfiltration behavior from the network defender's viewpoint to identify detectable signatures — protocol, timing, volume, and reputation — and tune the channel to stay below their thresholds.

## When to use
- When standing up, tuning, or migrating a C2 channel or exfil path.
- After a network-detection capability (NDR, proxy, DNS analytics, NetFlow, TLS inspection) is discovered in the environment.

## Method
- Characterize the channel's observable fingerprint: JA3/JARM, TLS cert and SNI, domain/IP reputation, HTTP headers/URIs, DNS query patterns, protocol anomalies.
- Analyze beacon behavior a defender baselines against: interval regularity, jitter, packet sizing, connection frequency, and long-lived or off-hours sessions.
- Model exfil detectability: volume vs. baseline, destination reputation, timing, and DLP content triggers; prefer low-and-slow or blend-with-normal egress.
- Map each signature to the specific network sensor that would catch it and estimate alert likelihood.
- Recommend tuning — domain fronting/redirectors, malleable profiles, jitter, protocol choice, chunking — weighed against the cost and the risk the tuning itself is anomalous.

## Signals / outputs
- A signature inventory of the current C2/exfil channel with per-signature detection risk.
- Concrete tuning recommendations and the residual risk after each.
- Egress and beacon indicators handed to Overwatch and the own-footprint ledger.
