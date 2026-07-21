## Why

The analyst stack (4 agents + 39 skills derived from `docs/roles/operational-analyst.md`) is decision-support — analysts that read, model, and judge. When an operation produces file dumps, memory captures, or configuration archives, no analyst skill says what to do with the credential material inside them. Seven grid rows touch credentials (`identity-directory-trust`, `disk-memory-forensics`, `os-host-internals`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `log-artefact-interpretation`, `implant-payload-re`) but their bodies carry no extraction procedures, no classification schema, and no triage workflow. A collected LSASS dump or `.env` archive sits until an operator manually asks the right questions.

The original proposal (`openspec/changes/archive/2026-07-22-credential-harvest-capability/proposal.md`) named four layers. Layer 4 (repo split) shipped as a side effect of relocating the analyst pillar into this repo. **Layers 1-3 were never authored.** This change delivers them.

## What Changes

### Layer 1: Enrich seven existing skill bodies with credential-extraction procedures

No new skills; the grid rows already cover the competencies. What's missing is depth. Each skill gains a credential-extraction section listing artefact locations, extraction tools, and portable patterns for its domain.

- `disk-memory-forensics` — LSASS dump parsing (Mimikatz, pypykatz), SAM/SECURITY hive extraction (secretsdump.py), cached logon data, memory string-scan patterns.
- `identity-directory-trust` — NTDS.dit hash extraction, Kerberos ticket parsing (.kirbi/.ccache), LAPS/gMSA credential harvesting, ADCS certificate material (PFX/PEM).
- `log-artefact-interpretation` — Credential patterns in debug/application/CI logs, connection strings, API key leakage in request logs.
- `cloud-controlplane-analysis` — Instance metadata credential extraction, service account key file analysis (GCP JSON, Azure SP certs), Terraform/CloudFormation state file secrets.
- `web-api-authflow-analysis` — JWT decode and claim extraction, OAuth token analysis, API key pattern library by provider, session cookie assessment.
- `os-host-internals` — Per-OS credential stores: Windows (SAM, DPAPI, Credential Manager, browser saved passwords), Linux (shadow, SSH keys, GNOME Keyring, bash_history), macOS (Keychain, SSH agent).
- `implant-payload-re` — Hardcoded credentials in malware configs, embedded API keys in binaries, credential extraction from packed payloads.

### Layer 2: Add `credential-harvest-triage` skill

One new cross-cutting procedural skill (does not change the grid — it is not a competency row) that provides:

- A **classification schema** for credential findings (type, subtype, status, scope, source, reuse potential, priority).
- A **triage procedure** — inventory → first-pass scan → deep-pass per category → classify → correlate → prioritise → report.
- A **pattern library** — portable regex patterns for API keys by provider, auth material formats, password hash types, connection strings, private key markers.

Fires when any analyst encounters file dumps or collection archives. Complements each specialist skill's "where to find" with a shared "how to triage".

### Layer 3: Amend four agent prompts to wire triage dispatch

Small paragraph additions, no permission changes:

- `operational-analyst` — dispatch credential-harvest triage when file dumps arrive; route findings to appropriate specialist.
- `target-network-analyst` — apply credential extraction from identity/OS/cloud/web skills; classify using triage schema; assess reuse against target model.
- `defender-detection-analyst` — extract from memory dumps and forensic artefacts; distinguish operation-owned vs target-owned credentials; assess detection risk of extraction.
- `fusion-analyst` — correlate credential findings across sources; assess take value; maintain credential inventory in operating picture.

### Layer 4: Repository split — **already done**

The analyst pillar lives in this repo. Retained here only to make the delta from the archived proposal explicit.

## Capabilities

### New Capabilities

None. The new `credential-harvest-triage` skill lands inside the existing `analyst-skill-library` capability as a cross-cutting procedural addition, not a separate capability.

### Modified Capabilities

- `analyst-skill-library`: Seven existing skill bodies gain credential-extraction sections; skill count changes from 39 to 40 with the addition of `credential-harvest-triage`. Skill count invariants in the current spec change accordingly.
- `analyst-agent-roster`: Four agent prompts gain a credential-harvest dispatch/handling paragraph. No new agents; no permission changes; existing invariants (four agents, primary + three legs, read-only, prompt-named skill sets) preserved.

## Impact

- **Modified files:** 7 existing `analysts/skills/*/SKILL.md` bodies (additive sections); 4 `analysts/agents/*.md` prompts (one paragraph each).
- **New file:** `analysts/skills/credential-harvest-triage/SKILL.md`.
- **Referenced source of truth:** `docs/roles/operational-analyst.md` appendix grid — read, not modified. The new triage skill is explicitly marked as procedural/cross-cutting, not a grid row.
- **No install script change.** The install script globs `skills/*` and picks up the new skill automatically; no wiring needed.
- **No permission change.** Analyst permissions (`edit: deny`, bash-substitute gating, leg `task: deny`) unchanged.
- **Passive analysis only.** All credential extraction is performed on already-collected data. Analysts never interact with targets. No active validation of discovered credentials.
- **No credential storage.** Analysts describe and classify findings; they never store raw credential values in skill output. The operational security boundary is the analyst's reporting.
