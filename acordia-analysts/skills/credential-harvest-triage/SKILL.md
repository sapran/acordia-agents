---
name: credential-harvest-triage
description: Inventory and rank credential material inside collected data — an LSASS dump, disk image, browser profile — by type, scope, freshness and reuse, so the best is acted on first.
metadata:
  acordia:
    family: take-handling
    grid_row: null
    procedural: true
    source: openspec/changes/archive/2026-07-22-credential-harvest-capability/proposal.md
    doctrine_source: [Monte#operational-security, Heuer#information-quantity]
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

Every credential finding SHALL be classified along these axes. `ownership` is settled first, because it decides what may be written down at all — see Guardrails.

| Field | Values (examples) |
|-------|-------------------|
| `ownership` | target, operation, third-party, unknown — `unknown` is handled as `operation` until adjudicated |
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
   - **Bucket A — identity / directory / cloud control-plane** (AD exports, NTDS, Kerberos, LAPS/gMSA, ADCS, IMDS captures, service-account keys, IaC state) → `terrain-analyst`
   - **Bucket B — host-forensic** (memory captures, SAM/SECURITY hives, DPAPI, Keychain, `shadow`, SSH agent) → whichever leg holds the host under analysis
   - **Bucket C — web / API auth** (JWTs, OAuth tokens, session cookies, provider API keys) → `terrain-analyst`
   - **Bucket D — log-artefact** (application / CI / system logs, connection strings leaked in logs) → `overwatch-analyst`
   - **Bucket E — implant / payload RE** (malware configs, embedded keys in binaries) → cross-cutting via `implant-payload-re`, findings reported to `cyber-analyst`, which holds the fused picture itself
   Buckets route to legs, not to skills. Each leg then runs steps 3–5 (first-pass scan, deep-pass, classify) on its own slice, applying its own specialist skills; the legs work in parallel, and step 6 re-merges their classifications. Each leg returns a **coverage receipt** for its bucket — declared scope reconciled to covered scope — per `exhaustive-data-processing`; the orchestrator rejects any bucket whose scan did not cover its whole slice and re-dispatches it. The mapping is fixed by domain — reclassify a bucket only through an openspec change, not an in-file edit.
3. **First-pass scan**: run the pattern library (see `references/credential-patterns.md`) across text-decodable artefacts (`grep -rHnE`, `rg`, or equivalent). The scan SHALL cover 100% of each bucket's text-decodable bytes and record *every* hit — never a sample — with path + line, not the matched string (see `exhaustive-data-processing`). Flag binary artefacts for deep-pass.
4. **Deep-pass per category**: dispatch to the matching specialist skill:
   - Memory / disk images → `disk-memory-forensics`
   - AD / NTDS / Kerberos / LAPS / ADCS → `identity-directory-trust`
   - Debug / application / CI logs → `log-artefact-interpretation`
   - Cloud state / metadata / service-account keys → `cloud-controlplane-analysis`
   - JWT / OAuth / API keys / session cookies → `web-api-authflow-analysis`
   - OS credential stores (SAM, DPAPI, Keychain, shadow, SSH agent) → `os-host-internals`
   - Malware / binary configs → `implant-payload-re`
5. **Classify** each finding into the schema, settling `ownership` first because it governs whether the value may be recorded at all, then purge from the extraction file every value ownership refused — steps 3 and 4 ran before this question was asked, so that file holds your own material too. Redact source paths that reveal analyst home dirs or workstation identity.
6. **Correlate** across findings: same account across sources, same key in multiple archives, one credential unlocking another (e.g. DPAPI master key → browser passwords). Because the buckets were analysed by different legs, this is where their classifications re-merge — hand the per-leg findings to `cyber-analyst`, which holds `multi-source-fusion` itself and resolves cross-leg linkages there. Merge duplicates; note the correlation in `provenance`.
7. **Prioritise**: rank by scope × reuse-potential × freshness. Break ties by ease-of-use (plaintext > hash > encrypted). Assign P0/P1/P2/P3.
8. **Report**: emit the classified inventory. State total coverage — buckets scanned, artefacts parsed, any deferred remainder named — so a sampled pass cannot masquerade as a complete one. Target-owned values belong in the product, as does a corporate third-party one; operation-owned, unadjudicated and personal ones appear as classification only, whatever the reader would find useful. A product carrying values is written to disk rather than returned in a reply. For each P0/P1, name the specialist owner and the reuse hypothesis to validate operationally.

## Pattern library

The pattern library lives in [`references/credential-patterns.md`](references/credential-patterns.md) alongside this skill — provider API-key prefixes, auth-material shapes, password-hash markers, connection-string DSNs, private-key PEM markers, and cloud/k8s secret-file patterns, grouped by class. It is the single source of truth for detection patterns: add a new provider prefix there once and every consumer (this skill's first-pass scan, and the pattern-citing `## Credential extraction` sections in `log-artefact-interpretation`, `web-api-authflow-analysis`, and `implant-payload-re`) inherits it. Anchor detection on the prefix; verify the current format at the provider's docs before acting.

## Signals / outputs

- A classified inventory table (findings × schema fields), ownership settled on every row.
- Ranked P0/P1/P2/P3 buckets with the reuse hypothesis attached to each P0 and P1.
- A named specialist owner for every finding that requires deep analysis.
- An audit trail: source path (redacted), pattern that matched, timestamp, and analyst confidence.

## Guardrails

- **Passive only.** Never attempt to validate a credential (no login attempt, no API probe, no key-fingerprint lookup against the live provider). This is unchanged by everything below: recording a value is not permission to try it.

**Ownership decides what may be written down.** Settle it before anything else.

- **Target-owned** — the finding. Its value belongs in your credential file and in the finished product: the recipient owns the credential and cannot remediate from `type: password, scope: domain, priority: P0` alone.
- **Operation-owned** — your own tooling, C2 authentication, staging accounts. Kept nowhere at all: extraction has usually written it to a file before you could know it was yours, so settling that it is yours is what obliges you to purge it. This is not a stricter version of the target case but a different one: protecting your own material is operational security, minimising exposure of the operation's existence, and a product leaves your control the moment you hand it over.
- **Third-party** — neither the target's nor yours. A corporate one is recorded and disclosed exactly as a target-owned one is, so the target can revoke the trust; a personal one is carried by classification alone, because disclosing an individual's own credential to their employer harms someone who is not party to the operation.
- **Unknown** — handled as operation-owned until adjudicated. One memory capture holds both kinds, and the errors are not symmetric: over-protecting a target credential costs a re-run, under-protecting your own burns infrastructure still in use.

**Six rules, at every ownership.**

- **Do not print.** A command reading credential-bearing material ends in a file write, not on standard output, and you work from the receipt — type, count, source location. One act feeds three places at once: what is displayed, what enters your context, and what the session records. A redirected value reaches none of them, so this is the whole of the difference and it costs nothing.
- **Look deliberately.** Read a value when a judgement needs it — is this reused, is it strong, does it match one seen elsewhere — not as the ordinary way of handling material. Acquiring awareness is itself exposure, and information past what the judgement needs raises your confidence without raising your accuracy.
- **Files, not messages.** A value reaches another reader only as a file that reader opens — never in a reply, a dispatch, a hand-back or a summary, and never quoted into prose you are composing in-session. This is the rule that lets a product disclose what its recipient owns: a product written to disk is a file, the same product returned in-message is not, so a product carrying credential values is always written rather than returned. A value in a file sits in one place; a value quoted travels into every summary downstream of it.
- **A credential file, separate from your notes.** Values go in a file of their own, beside the notes in the working directory the brief names and named in them; the notes carry the classification and that pointer, never the value — nor a command with a value in its arguments, which records the value just as surely. Your notes exist to be read by whoever fuses your work, and that read must not be the thing that spreads what every other rule contained. Because this doctrine gathers into one named file what used to sit scattered, the file needs an end as well as a place: it is destroyed when the engagement closes, and it is named in the hand-off so the person who inherits it knows it exists.
- **Purge what ownership refused.** Extraction runs before classification, so every file steps 3 and 4 wrote — raw tool output included, one per tool and per slice — holds all four ownerships at once, your own among them. Once you settle ownership at step 5, go back over each of those files and delete the values ownership did not permit: the classified inventory keeps the finding, the raw file loses the value. A file written before the question was asked is not a file the answer may be skipped for.
- **And nowhere else.** Values live in the credential file and in the product, and nowhere besides: not in `operational-memory`, which is durable and read by everyone who comes next; not in a commit; and never upstream — no network call, no API argument, no target-owned system, no third-party service. The upstream exclusion admits no ownership exception.

- **Redact analyst-identifying paths** (`/Users/<name>/`, workstation hostnames) from the source field.
- **Escalate on discovery of high-scope material** (domain admin hash, root cloud key, signing keys) — do not sit on it in the inventory.

None of this is enforced. These are instructions you follow, not a control something applies to you.
