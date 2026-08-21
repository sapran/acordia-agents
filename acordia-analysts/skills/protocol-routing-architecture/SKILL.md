---
name: protocol-routing-architecture
description: Reconstruct the target network's shape from device configs, routing tables, firewall rulesets and VPN definitions — L2 and L3 topology, VLANs and subnets, routing domains, tunnels, trust zones, chokepoints and egress paths — to establish what can reach what before planning movement or touching a control that divides two segments.
metadata:
  acordia:
    family: target-modelling
    grid_row: protocol-routing-architecture
    grid_deep_in: [Terrain]
    grid_working_in: [Def]
    row: protocol-routing-architecture
    source: docs/roles/operational-analyst.md
---

# Protocol, Routing & Network Architecture

## Objective

Reconstruct the target's network architecture — topology, routing, segmentation, and protocol boundaries — to reveal reachable paths, trust zones, and the controls that stand between access and objective.

## When to use

- When planning movement across a network and needing to know what can reach what.
- When you must locate segmentation, chokepoints, and egress/ingress paths before touching them.

## Method

- Inventory the collected network artefacts with `glob` / `find` / `list`: config exports (Cisco/Juniper/Palo Alto), routing tables, firewall rulesets, VPN configs, network diagrams, and any topology dumps.
- Read in bounded, context-scoped slices by interface block, VLAN definition, or ACL rule set rather than pulling multi-megabyte show-tech dumps wholesale into context; drive coverage with an exhaustive `grep`/parser pass over the whole export to locate every segment boundary, then read the scoped line range around each hit — every hit, not just the first.
- Map layers from those reads: L2/L3 topology, VLANs, subnets, routing domains, VPNs/tunnels, and the gateways/firewalls that join or divide them.
- Identify segmentation and trust zones — DMZ, corp, OT/ICS, management, cloud interconnect — and the exact crossing points; cite each boundary by `<path>:<offset>` (byte) or `<path>@L<line>` (line) back to the config line that proves the claim.
- Trace routing and reachability: default routes, NAT, proxies, split-tunnel, and what a packet from your foothold can actually reach.
- Profile protocols in play (routing protocols, tunneling, management planes) and their weaknesses or misconfigurations.
- Derive attack paths: which segment boundary to cross, via which host/rule/protocol, and where egress for C2 or exfil exists.
- If a vendor-specific parser (e.g. `ciscoconfparse`, offline `netmiko` helpers) is unavailable, fall back to manual `grep`-driven reads of the raw config; if the raw config itself is missing, flag the gap and stop rather than infer topology from screenshots or memory.

## Signals / outputs

- Segmentation and trust-zone map with named crossing points.
- Reachability matrix from likely footholds to objectives.
- Ingress/egress and C2 path candidates, with the controls on each.
