---
name: identity-directory-trust
description: Use when Active Directory or Entra ID underpins the target — map the directory, its privileged identities, and the trust relationships that let one compromise reach everything.
---

# Identity & Directory (AD/Entra) & Trust

## Objective
Map the target's identity fabric — Active Directory / Entra ID structure, privileged principals, and domain/tenant trust — to find the shortest identity path to control of the environment.

## When to use
- When the target is a Windows/AD or Entra-backed enterprise and identity is the real terrain.
- When you need to convert a foothold into domain/tenant dominance via identity, not exploits.

## Method
- Enumerate the directory: domains/forests/tenants, OUs, groups, privileged roles, service accounts, and trust links.
- Map privilege: who is effectively Domain/Enterprise/Global Admin, delegation (constrained/unconstrained/RBCD), and shadow-admin paths.
- Analyze trust relationships — inter-forest/domain trusts, hybrid sync (AD<->Entra), federation, and where trust is transitive or over-broad.
- Trace identity attack paths (Kerberos abuse, ACL/ADCS misconfig, token/PRT theft, sync-account leverage) toward tier-0 assets.
- Identify the crown-jewel identities and choke points whose control equals control of the mission.

## Signals / outputs
- Directory and privilege map with tier-0 principals identified.
- Trust and hybrid-sync edges, including transitive and over-broad grants.
- Shortest identity attack paths from foothold to domain/tenant control.
