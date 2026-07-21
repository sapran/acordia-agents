---
name: protocol-routing-architecture
description: Use when you need the shape of the target network — reconstruct how it is built, routed, and segmented so you can find the paths between where you are and where you want to be.
---

# Protocol, Routing & Network Architecture

## Objective
Reconstruct the target's network architecture — topology, routing, segmentation, and protocol boundaries — to reveal reachable paths, trust zones, and the controls that stand between access and objective.

## When to use
- When planning movement across a network and needing to know what can reach what.
- When you must locate segmentation, chokepoints, and egress/ingress paths before touching them.

## Method
- Map layers: L2/L3 topology, VLANs, subnets, routing domains, VPNs/tunnels, and the gateways/firewalls that join or divide them.
- Identify segmentation and trust zones — DMZ, corp, OT/ICS, management, cloud interconnect — and the exact crossing points.
- Trace routing and reachability: default routes, NAT, proxies, split-tunnel, and what a packet from your foothold can actually reach.
- Profile protocols in play (routing protocols, tunneling, management planes) and their weaknesses or misconfigurations.
- Derive attack paths: which segment boundary to cross, via which host/rule/protocol, and where egress for C2 or exfil exists.

## Signals / outputs
- Segmentation and trust-zone map with named crossing points.
- Reachability matrix from likely footholds to objectives.
- Ingress/egress and C2 path candidates, with the controls on each.
