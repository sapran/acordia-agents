---
name: credential-harvest-triage
description: Use when a collected file dump, memory capture, configuration archive, or log bundle lands and you need to inventory, classify, and prioritise the credential material inside it without knowing yet what is there.
metadata:
  acordia:
    grid_row: null
    procedural: true
    source: openspec/changes/archive/2026-07-22-credential-harvest-capability/proposal.md
---

# Credential Harvest Triage

## Cross-cutting notice

This skill is **procedural and cross-cutting**. It does not correspond to a row in the competency-grid appendix of `docs/roles/operational-analyst.md`. It reuses the credential-extraction procedures embedded in seven grid-row skills (`disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`) and imposes one shared triage flow across them. Adding it as a grid row would inflate the competency map with a workflow, not a competency.

## Objective

Turn a pile of collected material into a ranked, classified inventory of credential findings — with source, scope, reuse potential, and priority attached to each — so the operation can act on the best material first and set the rest aside without losing it.

## When to use

- A collection archive arrives (LSASS dump, disk image, cloud state export, log bundle, config directory, backup, browser profile) and no one has looked inside yet.
- Multiple specialist analysts have surfaced credential candidates and someone needs to fuse them into one prioritised list without double-counting.
- The operation is deciding whether to move on a specific credential and needs a defensible read on its type, scope, and freshness first.

## Classification schema

Every credential finding SHALL be classified along these axes. Analysts record the classification, never the raw value.

| Field | Values (examples) |
|-------|-------------------|
| `type` | password, hash, key, token, certificate, cookie, ticket, seed |
| `subtype` | NTLM, Kerberos TGT, AWS access key, JWT (HS256), OAuth refresh, SSH RSA-2048, DPAPI blob, browser saved password |
| `status` | plaintext, hashed, encrypted-at-rest, encrypted-in-transit, revoked-suspected |
| `scope` | account, service, host, tenant, domain, cross-tenant |
| `source` | absolute path or artefact identifier (redact home dir / user) |
| `provenance` | in-memory, file-on-disk, log-line, config-value, network-capture |
| `reuse-potential` | high (broad scope, likely valid), medium (narrow scope or unknown freshness), low (revoked-likely, single-use), unknown |
| `freshness` | timestamp of the source artefact or "unknown" |
| `priority` | P0/P1/P2/P3 — derived from scope × reuse-potential × freshness |
| `next-action` | who owns follow-up (specialist name), or "hold" |

## Triage procedure

1. **Inventory** the archive: list every file, size, mtime, MIME/file-type. Note directory shape (single dump vs. multi-user backup vs. cloud state export). Output: an inventory table.
2. **Bucket partition**: split the inventory by material class into leg-owned buckets, so that the per-category scan and deep-pass below run in parallel — the orchestrator dispatches each slice to its handling leg with **only that slice**, not the whole archive. Current mapping:
   - **Bucket A — identity / directory / cloud control-plane** (AD exports, NTDS, Kerberos, LAPS/gMSA, ADCS, IMDS captures, service-account keys, IaC state) → `target-network-analyst`
   - **Bucket B — host-forensic** (memory captures, SAM/SECURITY hives, DPAPI, Keychain, `shadow`, SSH agent) → whichever leg holds the host under analysis
   - **Bucket C — web / API auth** (JWTs, OAuth tokens, session cookies, provider API keys) → `target-network-analyst`
   - **Bucket D — log-artefact** (application / CI / system logs, connection strings leaked in logs) → `defender-detection-analyst`
   - **Bucket E — implant / payload RE** (malware configs, embedded keys in binaries) → cross-cutting via `implant-payload-re`, findings reported to `fusion-analyst`
   Buckets route to legs, not to skills; a leg applies its own specialist skills (step 4) to its slice. The mapping is fixed by domain — reclassify a bucket only through an openspec change, not an in-file edit.
3. **First-pass scan**: run the pattern library (see `references/credential-patterns.md`) across text-decodable artefacts (`grep -rHnE`, `rg`, or equivalent). Record hits with path + line, not the matched string. Flag binary artefacts for deep-pass.
4. **Deep-pass per category**: dispatch to the matching specialist skill:
   - Memory / disk images → `disk-memory-forensics`
   - AD / NTDS / Kerberos / LAPS / ADCS → `identity-directory-trust`
   - Debug / application / CI logs → `log-artefact-interpretation`
   - Cloud state / metadata / service-account keys → `cloud-controlplane-analysis`
   - JWT / OAuth / API keys / session cookies → `web-api-authflow-analysis`
   - OS credential stores (SAM, DPAPI, Keychain, shadow, SSH agent) → `os-host-internals`
   - Malware / binary configs → `implant-payload-re`
5. **Classify** each finding into the schema. Redact source paths that reveal analyst home dirs or workstation identity.
6. **Correlate** across findings: same account across sources, same key in multiple archives, one credential unlocking another (e.g. DPAPI master key → browser passwords). Because the buckets were analysed by different legs, this is where their classifications re-merge — hand the per-leg findings to `fusion-analyst`, which runs `multi-source-fusion` to resolve cross-leg linkages. Merge duplicates; note the correlation in `provenance`.
7. **Prioritise**: rank by scope × reuse-potential × freshness. Break ties by ease-of-use (plaintext > hash > encrypted). Assign P0/P1/P2/P3.
8. **Report**: emit the classified inventory. Do not include raw credential values. For each P0/P1, name the specialist owner and the reuse hypothesis to validate operationally.

## Pattern library

The pattern library lives in [`references/credential-patterns.md`](references/credential-patterns.md) alongside this skill — provider API-key prefixes, auth-material shapes, password-hash markers, connection-string DSNs, private-key PEM markers, and cloud/k8s secret-file patterns, grouped by class. It is the single source of truth for detection patterns: add a new provider prefix there once and every consumer (this skill's first-pass scan, and the pattern-citing `## Credential extraction` sections in `log-artefact-interpretation`, `web-api-authflow-analysis`, and `implant-payload-re`) inherits it. Anchor detection on the prefix; verify the current format at the provider's docs before acting.

## Signals / outputs

- A classified inventory table (findings × schema fields), no raw values.
- Ranked P0/P1/P2/P3 buckets with the reuse hypothesis attached to each P0 and P1.
- A named specialist owner for every finding that requires deep analysis.
- An audit trail: source path (redacted), pattern that matched, timestamp, and analyst confidence.

## Guardrails

- **Passive only.** Never attempt to validate a credential (no login attempt, no API probe, no key-fingerprint lookup against the live provider).
- **No raw values in output.** Report classification, source path, and hash-of-value if disambiguation is needed — never the credential itself.
- **Redact analyst-identifying paths** (`/Users/<name>/`, workstation hostnames) from the source field.
- **Do not persist raw values** in analyst working files. If deep-pass requires holding the value in memory (e.g. to compute a fingerprint), discard after use and record only the fingerprint.
- **Escalate on discovery of high-scope material** (domain admin hash, root cloud key, signing keys) — do not sit on it in the inventory.
