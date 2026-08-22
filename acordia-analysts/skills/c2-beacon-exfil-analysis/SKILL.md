---
name: c2-beacon-exfil-analysis
description: Examine the operation's own C2, beacon and exfiltration traffic as a network defender would — fingerprints, certificates, interval regularity — and tune it below their thresholds.
metadata:
  acordia:
    family: defender-reading
    grid_row: c2-beacon-exfil-analysis
    grid_deep_in: [Def]
    grid_working_in: [Coll]
    row: c2-beacon-exfil-analysis
    source: docs/roles/operational-analyst.md
---

# C2 / Beacon / Exfil-Signal Analysis

## Objective

Examine the operation's own C2, beacon, and exfiltration behavior from the network defender's viewpoint to identify detectable signatures — protocol, timing, volume, and reputation — and tune the channel to stay below their thresholds.

## When to use

- When standing up, tuning, or migrating a C2 channel or exfil path.
- After a network-detection capability (NDR, proxy, DNS analytics, NetFlow, TLS inspection) is discovered in the environment.

## Method

- Inventory the channel-evidence set with `ls` / `find` / `glob` — own-side pcap of the beacon, Zeek/flow exports of the exfil path, profile files (malleable C2, redirector config), proxy/DNS logs from the environment — and note capture point, timespan, and byte size per artefact before opening.
- Characterize the channel's observable fingerprint from bounded reads: JA3/JARM via `tshark -Y tls.handshake.type==1 -T fields ...` or `zeek -r`'s `ssl.log`; TLS cert and SNI, domain/IP reputation, HTTP headers/URIs, DNS query patterns, protocol anomalies — pulled per conversation, not per full capture.
- Analyze beacon behavior a defender baselines against from Zeek `conn.log` aggregates: interval regularity, jitter, packet sizing, connection frequency, and long-lived or off-hours sessions.
- Model exfil detectability: volume vs. baseline (flow aggregates), destination reputation, timing, and DLP content triggers; prefer low-and-slow or blend-with-normal egress.
- Map each signature to the specific network sensor that would catch it and estimate alert likelihood. Cite each finding as `<pcap>:<packet-number>` for packet-level evidence, `<log>@L<line>` for Zeek / proxy / DNS log lines, and `<profile>@L<line>` for malleable / redirector config anchors.
- Recommend tuning — domain fronting/redirectors, malleable profiles, jitter, protocol choice, chunking — weighed against the cost and the risk the tuning itself is anomalous.
- Degradation: if `tshark`/Wireshark is unavailable, fall back to Zeek logs (or `tcpdump -r ... -nn`) and flag reduced fingerprint fidelity (JA3/JARM may be missing); if Zeek is unavailable, drive from `tshark -T fields` extraction and flag missing typed-log aggregation; if only netflow is on hand, flag the gap for any payload-dependent signature (JA3, SNI, URI) and constrain analysis to volume/timing.

## Signals / outputs

- A signature inventory of the current C2/exfil channel with per-signature detection risk.
- Concrete tuning recommendations and the residual risk after each.
- Egress and beacon indicators handed to Overwatch and the own-footprint ledger.
