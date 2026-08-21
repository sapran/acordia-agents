---
name: identity-directory-trust
description: Map the target's identity fabric from directory artefacts such as BloodHound exports, LDAP dumps and NTDS extractions — privileged principals, constrained, unconstrained and resource-based delegation, ADCS, LAPS and gMSA material, domain and tenant trust — to find the shortest identity path from a foothold to control of a Windows AD or Entra-backed enterprise.
metadata:
  acordia:
    family: target-modelling
    grid_row: identity-directory-trust
    grid_deep_in: [Terrain]
    grid_working_in: [Def]
    row: identity-directory-trust
    source: docs/roles/operational-analyst.md
---

# Identity & Directory (AD/Entra) & Trust

## Objective

Map the target's identity fabric — Active Directory / Entra ID structure, privileged principals, and domain/tenant trust — to find the shortest identity path to control of the environment.

## When to use

- When the target is a Windows/AD or Entra-backed enterprise and identity is the real terrain.
- When you need to convert a foothold into domain/tenant dominance via identity, not exploits.

## Method

- Inventory the collected directory artefacts with `ls` / `find` / `glob` — SharpHound / BloodHound JSON exports, ADExplorer snapshots, NTDS.dit + SYSTEM hive dumps, LDAP dumps, ticket caches, LAPS/gMSA/ADCS material — and record what each covers (domain, tenant, time window).
- Enumerate the directory from those artefacts, bounded: query BloodHound JSON via `jq`; grep LDIF / CSV exports for privileged group memberships, delegation attributes (`msDS-AllowedToActOnBehalfOfOtherIdentity`, `TrustedForDelegation`), and trust records rather than reading multi-megabyte dumps wholesale. For NTDS, use `impacket-secretsdump` targeted extractions, not raw hive reads.
- Map privilege: who is effectively Domain/Enterprise/Global Admin, delegation (constrained/unconstrained/RBCD), and shadow-admin paths.
- Analyze trust relationships — inter-forest/domain trusts, hybrid sync (AD<->Entra), federation, and where trust is transitive or over-broad.
- Trace identity attack paths (Kerberos abuse, ACL/ADCS misconfig, token/PRT theft, sync-account leverage) toward tier-0 assets.
- Identify the crown-jewel identities and choke points whose control equals control of the mission. Cite each finding as `<artefact>@L<line>` for text/LDIF exports or `<artefact>:<offset>` for binary hive/database evidence; reference the BloodHound node/edge id when routing through graph data.
- Degradation: if BloodHound / SharpHound output is unavailable, fall back to raw LDAP dump grep + hand-drawn privilege map and flag reduced completeness; if `impacket-secretsdump` / `impacket-dpapi` are unavailable for hive/DPAPI parsing, flag the gap and stop — do not improvise credential extraction from unfamiliar formats.

## Signals / outputs

- Directory and privilege map with tier-0 principals identified.
- Trust and hybrid-sync edges, including transitive and over-broad grants.
- Shortest identity attack paths from foothold to domain/tenant control.

## Credential extraction

Passive extraction from directory-service artefacts already in hand (NTDS dumps, ticket caches, LAPS exports, ADCS material). Never queries the live directory to validate.

**Active Directory database**

- `NTDS.dit` + `SYSTEM` hive — `impacket-secretsdump -ntds NTDS.dit -system SYSTEM LOCAL`. Yields all domain account NTLM hashes plus `krbtgt` (golden-ticket material — highest scope, flag P0 automatically). Kerberos AES keys are extracted with `-just-dc` mode.
- `DPAPI_SYSTEM` LSA secret + user DPAPI master keys — chained decrypt with `impacket-dpapi` yields service account plaintexts, scheduled-task credentials, saved browser passwords.

**Kerberos tickets**

- Windows `.kirbi` files — parse with `KrbRelay`, `Rubeus describe /ticket:<file>` (analysis only, not renewal). Yields service, client, renew-till, encryption type, target SPN. TGTs (`krbtgt/<domain>`) mark broadest scope.
- MIT `.ccache` files (`/tmp/krb5cc_*`, `KRB5CCNAME` env var target) — parse with `klist -c` or `impacket-ticketConverter`. Same fields.

**LAPS / gMSA / ADCS**

- Legacy LAPS (`ms-Mcs-AdmPwd`) and Windows LAPS (`msLAPS-Password`, `msLAPS-EncryptedPassword`) — plaintext or encrypted local-admin passwords. When collected from AD replication metadata or an LDAP dump, decode per attribute type.
- gMSA (`msDS-ManagedPassword`) — 240-byte blob; parse with `gMSADumper.py`-style logic against the raw blob you already collected. Yields NTLM + Kerberos keys for the gMSA identity.
- ADCS artefacts — `.pfx`/`.p12` (private key + cert; may be passphrase-protected — dictionary attack offline only, not online), `.pem` with `-----BEGIN` headers, template-vulnerable enrolments identifiable in AD-DUMP JSON exports.

**Cross-cutting**

- Directory-derived credentials classify as `scope: domain` or higher; `krbtgt`, tier-0 accounts, and enterprise-CA private keys always mark `priority: P0`. All output flows through [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); no raw hashes or keys in reports.
