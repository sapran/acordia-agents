---
name: packet-traffic-analysis
description: Use when you have pcap or netflow from a target and need to read the wire — infer terrain, live services, trust relationships, and behavioural opportunity from what actually moves across the network.
metadata:
  acordia:
    grid_row: packet-traffic-analysis
    grid_deep_in: ['T&N', Def]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L83
---

# Packet & Traffic Analysis

## Objective
Turn captured packets or flow records into an operational picture of the target: who talks to whom, over what, when, and where the exploitable gaps and blend-in paths are.

## When to use
- When you have a capture (pcap/pcapng) or flow data (NetFlow/IPFIX/sFlow) from inside or adjacent to the target.
- When you need ground-truth on live hosts, services, and trust that scanning would miss or that would be too noisy to probe.

## Method
- Inventory the capture set with `ls` / `find` / `glob` (pcap/pcapng files, netflow/IPFIX/sFlow exports); note per-file capture point, timespan, byte size, and truncation (`capinfos`) before opening anything.
- Read bounded slices — never load a multi-gigabyte pcap wholesale. Drive with `tshark -Y <bpf-or-display-filter>` per conversation, `zeek -r` for typed logs (`conn.log`, `dns.log`, `http.log`, `ssl.log`, `kerberos.log`, `smb_files.log`), and `mergecap`/`editcap` slices when scoping to a time window. Map the conversation graph from Zeek `conn.log` aggregates rather than per-packet reads.
- Fingerprint services and stacks from real traffic (banners, TLS/JA3, DNS, SMB/Kerberos, DHCP) rather than active probing, extracting via the Zeek log field of interest or a scoped `tshark -T fields` query.
- Extract credentials, tokens, and cleartext where protocols leak them; note where auth and encryption are weak or absent. Never quote raw credential values — cite location only.
- Read behaviour and timing — beacon-like periodicity, backup/replication flows, admin sessions, trust and dependency edges — from flow aggregates.
- Locate opportunity: unsegmented paths, chatty services, exfil-friendly channels, and where your traffic would look native. Cite each finding as `<pcap>:<packet-number>` (or `<pcap>:<frame-offset>`) for packet-level evidence and `<log>@L<line>` for Zeek/flow log lines.
- Degradation: if `tshark`/Wireshark is unavailable, fall back to Zeek logs alone (or `tcpdump -r ... -nn`) and flag reduced protocol-decoder coverage; if Zeek is unavailable, fall back to `tshark -T fields` extraction and flag missing typed-log fidelity; if only netflow is on hand (no payload), flag the gap for any signature that requires payload inspection.

## Signals / outputs
- Host/service inventory and conversation graph derived from real traffic.
- Extracted secrets, weak-auth findings, and trust edges.
- Candidate movement paths and covert channels with timing to blend into.
