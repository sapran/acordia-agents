---
name: packet-traffic-analysis
description: Use when you have pcap or netflow from a target and need to read the wire — infer terrain, live services, trust relationships, and behavioural opportunity from what actually moves across the network.
---

# Packet & Traffic Analysis

## Objective
Turn captured packets or flow records into an operational picture of the target: who talks to whom, over what, when, and where the exploitable gaps and blend-in paths are.

## When to use
- When you have a capture (pcap/pcapng) or flow data (NetFlow/IPFIX/sFlow) from inside or adjacent to the target.
- When you need ground-truth on live hosts, services, and trust that scanning would miss or that would be too noisy to probe.

## Method
- Map the conversation graph: endpoints, ports, protocols, volumes, and direction — who initiates, who serves, who is central.
- Fingerprint services and stacks from real traffic (banners, TLS/JA3, DNS, SMB/Kerberos, DHCP) rather than active probing.
- Extract credentials, tokens, and cleartext where protocols leak them; note where auth and encryption are weak or absent.
- Read behaviour and timing — beacon-like periodicity, backup/replication flows, admin sessions, trust and dependency edges.
- Locate opportunity: unsegmented paths, chatty services, exfil-friendly channels, and where your traffic would look native.

## Signals / outputs
- Host/service inventory and conversation graph derived from real traffic.
- Extracted secrets, weak-auth findings, and trust edges.
- Candidate movement paths and covert channels with timing to blend into.
