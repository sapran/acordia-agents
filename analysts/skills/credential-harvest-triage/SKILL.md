---
name: credential-harvest-triage
description: Use when a collected file dump, memory capture, configuration archive, or log bundle lands and you need to inventory, classify, and prioritise the credential material inside it without knowing yet what is there.
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
2. **First-pass scan**: run the pattern library (below) across text-decodable artefacts (`grep -rHnE`, `rg`, or equivalent). Record hits with path + line, not the matched string. Flag binary artefacts for deep-pass.
3. **Deep-pass per category**: dispatch to the matching specialist skill:
   - Memory / disk images → `disk-memory-forensics`
   - AD / NTDS / Kerberos / LAPS / ADCS → `identity-directory-trust`
   - Debug / application / CI logs → `log-artefact-interpretation`
   - Cloud state / metadata / service-account keys → `cloud-controlplane-analysis`
   - JWT / OAuth / API keys / session cookies → `web-api-authflow-analysis`
   - OS credential stores (SAM, DPAPI, Keychain, shadow, SSH agent) → `os-host-internals`
   - Malware / binary configs → `implant-payload-re`
4. **Classify** each finding into the schema. Redact source paths that reveal analyst home dirs or workstation identity.
5. **Correlate** across findings: same account across sources, same key in multiple archives, one credential unlocking another (e.g. DPAPI master key → browser passwords). Merge duplicates; note the correlation in `provenance`.
6. **Prioritise**: rank by scope × reuse-potential × freshness. Break ties by ease-of-use (plaintext > hash > encrypted). Assign P0/P1/P2/P3.
7. **Report**: emit the classified inventory. Do not include raw credential values. For each P0/P1, name the specialist owner and the reuse hypothesis to validate operationally.

## Pattern library

Portable prefixes and shapes that survive most provider rotations. Anchor detection on the prefix; verify current format at the provider's docs before acting.

```text
# API keys (prefix anchored)
AKIA[0-9A-Z]{16}                              # AWS access key ID (long-term)
ASIA[0-9A-Z]{16}                              # AWS temp session
AIza[0-9A-Za-z_\-]{35}                        # Google API key
AGQ[A-Za-z0-9_-]{20,}                         # GitHub app installation token (recent)
ghp_[A-Za-z0-9]{36}                           # GitHub personal token
gho_[A-Za-z0-9]{36}                           # GitHub OAuth token
ghs_[A-Za-z0-9]{36}                           # GitHub server-to-server
ghu_[A-Za-z0-9]{36}                           # GitHub user-to-server
glpat-[A-Za-z0-9_\-]{20}                      # GitLab personal token
xox[baprs]-[A-Za-z0-9-]{10,}                  # Slack bot/app/refresh tokens
sk-[A-Za-z0-9]{20,}                           # OpenAI-style secret key
sk-ant-[A-Za-z0-9\-_]{80,}                    # Anthropic API key
npm_[A-Za-z0-9]{36}                           # npm token
pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]+           # PyPI token (macaroon)
dckr_pat_[A-Za-z0-9_\-]{27,}                  # Docker Hub PAT

# Auth material shapes
eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+   # JWT (base64 header.payload.signature)
Bearer\s+[A-Za-z0-9_\-\.=]+                    # HTTP bearer header
Authorization:\s*Basic\s+[A-Za-z0-9+/=]+       # HTTP basic (base64 user:pass)

# Password hashes
\$1\$[./A-Za-z0-9]{8}\$[./A-Za-z0-9]{22}                # MD5 crypt
\$2[abxy]?\$[0-9]{2}\$[./A-Za-z0-9]{53}                 # bcrypt
\$5\$(rounds=[0-9]+\$)?[./A-Za-z0-9]{16}\$[./A-Za-z0-9]{43}  # SHA-256 crypt
\$6\$(rounds=[0-9]+\$)?[./A-Za-z0-9]{16}\$[./A-Za-z0-9]{86}  # SHA-512 crypt
[a-fA-F0-9]{32}                                          # NTLM / LM (also MD5; disambiguate by source)
[^:]+::[^:]+:[a-fA-F0-9]{16}:[a-fA-F0-9]{32}:[a-fA-F0-9]{32,}  # NetNTLMv2

# Connection strings
(mongodb|postgres|mysql|redis)(\+srv)?://[^:@\s]+:[^@\s]+@[^\s/]+  # user:pass DSN
Server=[^;]+;.*Password=[^;]+;                                     # SQL Server ADO
DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[^;]+  # Azure Storage

# Private keys (PEM markers)
-----BEGIN (RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY(\s+BLOCK)?-----
-----BEGIN ENCRYPTED PRIVATE KEY-----

# Cloud service accounts
"type":\s*"service_account"                    # GCP JSON key file marker
"private_key":\s*"-----BEGIN                   # GCP JSON key (embedded PEM)
"clientSecret":\s*"[A-Za-z0-9_\-\.~]+"          # Azure SP JSON
aws_access_key_id\s*=\s*AKIA[0-9A-Z]{16}       # ~/.aws/credentials line
aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40} # ~/.aws/credentials line

# Kubernetes / secret files
apiVersion:\s*v1[\s\S]*?kind:\s*Secret         # k8s Secret manifest
kubeconfig[\s\S]*?client-key-data:             # kubeconfig with embedded key
```

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
