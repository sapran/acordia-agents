## 1. Author the triage skill

- [x] 1.1 Create `analysts/skills/credential-harvest-triage/SKILL.md` with opencode frontmatter (`name`, `description`), a `## Cross-cutting notice` paragraph declaring the skill is procedural and not a grid row, a `## Classification schema` section, a `## Triage procedure` section, and an inline `## Pattern library` section
- [x] 1.2 Verify frontmatter validates against opencode contract (`name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars; `description` 1–1024 chars)

## 2. Enrich the seven credential-adjacent skills

- [x] 2.1 Append `## Credential extraction` section to `analysts/skills/disk-memory-forensics/SKILL.md` — LSASS dumps (Mimikatz, pypykatz), SAM/SECURITY hive extraction (secretsdump.py), cached logon data, memory string-scan patterns
- [x] 2.2 Append `## Credential extraction` section to `analysts/skills/identity-directory-trust/SKILL.md` — NTDS.dit hash extraction, Kerberos ticket parsing (.kirbi/.ccache), LAPS/gMSA, ADCS PFX/PEM material
- [x] 2.3 Append `## Credential extraction` section to `analysts/skills/log-artefact-interpretation/SKILL.md` — credentials in debug/application/CI logs, connection strings, API keys leaked in request logs
- [x] 2.4 Append `## Credential extraction` section to `analysts/skills/cloud-controlplane-analysis/SKILL.md` — instance-metadata credentials, service-account key files (GCP JSON, Azure SP certs), Terraform/CloudFormation state secrets
- [x] 2.5 Append `## Credential extraction` section to `analysts/skills/web-api-authflow-analysis/SKILL.md` — JWT decode and claims, OAuth token analysis, provider API-key patterns, session cookie assessment
- [x] 2.6 Append `## Credential extraction` section to `analysts/skills/os-host-internals/SKILL.md` — Windows (SAM, DPAPI, Credential Manager, browser saved passwords), Linux (shadow, SSH keys, GNOME Keyring, bash_history), macOS (Keychain, SSH agent)
- [x] 2.7 Append `## Credential extraction` section to `analysts/skills/implant-payload-re/SKILL.md` — hardcoded credentials in malware configs, embedded API keys in binaries, extraction from packed payloads
- [x] 2.8 Cross-check: each section is additive, existing `Objective`/`When to use`/`Method`/`Signals` sections unchanged, no raw credential values in examples, no active-validation references

## 3. Amend the four agent prompts

- [x] 3.1 Add `## Credential harvest` section to `analysts/agents/operational-analyst.md` — dispatch triage on file dumps, route findings to appropriate leg, names `credential-harvest-triage`
- [x] 3.2 Add `## Credential harvest` section to `analysts/agents/target-network-analyst.md` — apply credential extraction from identity/OS/cloud/web skills, classify with triage schema, assess reuse against target model
- [x] 3.3 Add `## Credential harvest` section to `analysts/agents/defender-detection-analyst.md` — extract from memory dumps and forensic artefacts, distinguish operation-owned vs target-owned credentials, assess detection risk of extraction
- [x] 3.4 Add `## Credential harvest` section to `analysts/agents/fusion-analyst.md` — correlate credential findings across sources, assess take value, maintain credential inventory in operating picture
- [x] 3.5 Verify frontmatter permission blocks (`edit`, `bash`, `task`) are unchanged in each agent

## 4. Validate

- [x] 4.1 `openspec validate --all --strict` passes
- [x] 4.2 grep `## Credential harvest` in `analysts/agents/*.md` returns 4 matches
- [x] 4.3 grep `## Credential extraction` in `analysts/skills/*/SKILL.md` returns 7 matches
- [x] 4.4 `analysts/skills/credential-harvest-triage/SKILL.md` exists and its frontmatter parses
