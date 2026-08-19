---
name: cloud-identity-log-analysis
description: Use when the operation moves through cloud or identity infrastructure and you must predict what the audit and sign-in logs record about your authentication, API calls, and resource access.
metadata:
  acordia:
    family: defender-reading
    grid_row: cloud-identity-log-analysis
    grid_deep_in: [Def]
    grid_working_in: ['T&N', Fus]
    source: docs/roles/operational-analyst.md#L93
---

# Cloud & Identity Log Analysis

## Objective
Reason about what cloud control-plane and identity providers log about activity — sign-ins, token issuance, consent, API/audit events, and their conditional-access signals — so identity and cloud actions are taken in ways that blend with legitimate activity.

## When to use
- Operating against cloud tenants (Entra ID/Azure, AWS, GCP, Okta, Workspace) or using stolen tokens, service principals, or federated identities.
- Planning cloud persistence, privilege escalation, or data access where control-plane logging is the primary witness.

## Method
- Enumerate the relevant log sources (sign-in and audit logs, CloudTrail, Admin/Workspace logs, unified audit) and what fields each captures — IP, device, UA, MFA method, token type, risk score.
- Map each planned action to the events it generates and to the risk/anomaly signals it trips (impossible travel, new device, unusual client, MFA anomalies, consent grants).
- Distinguish control-plane events (usually logged) from data-plane access (often unlogged or off by default) and prefer paths that leave the thinner trail.
- Shape identity context to match the victim's baseline — source geography/ASN, device compliance, client app — to avoid risk-based detection.
- Note logs that are delayed, sampled, or not retained, and events that survive session teardown (token/refresh, app registrations).

## Signals / outputs
- A per-action forecast of cloud/identity log events and the risk signals each triggers.
- Recommended identity-context shaping to stay under anomaly thresholds.
- A list of low-logging access paths and persistence artifacts Overwatch should track.
