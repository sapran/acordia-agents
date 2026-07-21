## Why

The analyst agents and skills (derived from `docs/roles/operational-analyst.md` via `openspec/changes/archive/2026-07-22-derive-analyst-agents-skills/`) give the operation decision-support capability — analysts that read, model, and judge. But when the operation produces file dumps, memory captures, or configuration archives, no analyst skill says what to do with the credential material inside them. The grid rows name competencies that touch credentials (identity-directory-trust, disk-memory-forensics, os-host-internals, cloud-controlplane-analysis, web-api-authflow-analysis, log-artefact-interpretation, implant-payload-re) but the skill bodies carry no extraction procedures, no classification schema, and no triage workflow. A collected LSASS dump or `.env` archive sits there until an operator manually asks the right questions.

This is a gap in the analyst stack's ability to perform one of the most operationally valuable post-collection tasks: systematically extracting, classifying, and prioritising credential material from collected data for reuse. The gap is purely analytical — the analysts already have read-only permissions and bash for inspection; what's missing is the knowledge and coordination to apply them to credential material.

Separately, the analyst agents and skills are opencode-native artifacts that live in `~/.config/opencode/` and have no code dependency on this repository. They should move to their own repo. This change is the natural point to make that split: the credential-harvest capability is the first significant addition to the analyst stack, and it should land in the right place from the start.

## What Changes

### Layer 1: Enrich existing skill bodies with credential-extraction procedures

Seven existing skills gain credential-specific sections — extraction techniques, tool commands, and patterns tailored to each skill's data domain. No new skills; the grid rows already cover the competencies. What's missing is depth.

- **`disk-memory-forensics`** — LSASS dump parsing (Mimikatz, pypykatz), SAM/SECURITY hive extraction (secretsdump.py), cached logon data, string scanning patterns for memory dumps.
- **`identity-directory-trust`** — NTDS.dit hash extraction, Kerberos ticket parsing (.kirbi/.ccache), LAPS/gMSA credential harvesting, ADCS certificate material (PFX/PEM).
- **`log-artefact-interpretation`** — Credential patterns in debug/application/CI logs, connection strings, API key leakage in request logs.
- **`cloud-controlplane-analysis`** — Instance metadata credential extraction, service account key file analysis (GCP JSON, Azure SP certs), Terraform/CloudFormation state file secrets.
- **`web-api-authflow-analysis`** — JWT decode and claim extraction, OAuth token analysis, API key pattern library by provider, session cookie assessment.
- **`os-host-internals`** — Per-OS credential stores: Windows (SAM, DPAPI, Credential Manager, browser saved passwords), Linux (shadow, SSH keys, GNOME Keyring, bash_history), macOS (Keychain, SSH agent).
- **`implant-payload-re`** — Hardcoded credentials in malware configs, embedded API keys in binaries, credential extraction from packed payloads.

### Layer 2: New skill — `credential-harvest-triage`

One new skill (skill #40, does not change the grid — it's a cross-cutting procedural skill, not a competency row) that provides:
- A **classification schema** for credential findings (type, subtype, status, scope, source, reuse potential, priority).
- A **triage procedure** — inventory → first-pass scan → deep-pass per category → classify → correlate → prioritise → report.
- A **pattern library** — portable regex patterns for API keys by provider, auth material formats, password hash types, connection strings, private key markers.

This skill fires when any analyst encounters file dumps or collection archives. It is the "how to triage" complement to each specialist skill's "where to find".

### Layer 3: Agent prompt amendments

Four one-paragraph amendments to existing agent prompts wiring credential harvest into the dispatch flow:
- **`operational-analyst`** — dispatch credential-harvest triage when file dumps arrive; route findings to appropriate specialist.
- **`target-network-analyst`** — apply credential extraction from identity/OS/cloud/web skills; classify using triage schema; assess reuse against target model.
- **`defender-detection-analyst`** — extract from memory dumps and forensic artifacts; distinguish operation-owned vs target-owned credentials; assess detection risk of extraction.
- **`fusion-analyst`** — correlate credential findings across sources; assess take value; maintain credential inventory in operating picture.

### Layer 4: Repository split

Move the analyst agents and skills to a dedicated repository (e.g., `operational-analysts` or `acordia-analysts`). This repo becomes the canonical source for:
- The 4 agent markdown files.
- The 39 existing + 1 new skill `SKILL.md` files.
- An install script that links or copies to `~/.config/opencode/`.

The competency map (`docs/roles/operational-analyst.md`) and OpenSpec specs stay in CyberStrike — they are part of the ACORDIA framework. The new repo holds the compiled artifacts, with a README tracing each artifact back to its source in the grid.

## Capabilities

### New Capabilities

- `credential-harvest-triage`: Cross-cutting triage skill for systematic credential extraction from file dumps. Classification schema, triage procedure, pattern library. Fires on analyst encounter with collected data archives.

### Modified Capabilities

- `analyst-skill-library`: Seven existing skill bodies enriched with credential-extraction sections (procedures, tool commands, patterns). Skill count changes from 39 to 40 with the addition of credential-harvest-triage.
- `analyst-agent-roster`: Four agent prompts amended with credential-harvest dispatch logic. No new agents; no permission changes.

## Impact

- **Modified files (analyst repo):** 7 existing `SKILL.md` bodies (additive sections), 4 agent `.md` prompts (one paragraph each).
- **New file (analyst repo):** 1 `credential-harvest-triage/SKILL.md`.
- **New repository:** Analyst agents + skills split from CyberStrike personal config into a standalone repo.
- **Referenced source of truth:** `docs/roles/operational-analyst.md` appendix grid — read, not modified. The new triage skill is explicitly marked as procedural/cross-cutting, not a grid row.
- **No application code, no TypeScript, no rebuild.** Markdown extension path only.
- **Passive analysis only.** All credential extraction is performed on already-collected data. Analysts never interact with targets. No active validation of discovered credentials.
- **No credential storage.** Analysts describe and classify findings; they never store raw credential values in skill output. The operational security boundary is the analyst's reporting.
