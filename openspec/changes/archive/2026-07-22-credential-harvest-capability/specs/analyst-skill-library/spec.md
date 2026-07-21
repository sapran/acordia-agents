## MODIFIED Requirements

### Requirement: One skill per competency-grid row

The library SHALL contain exactly one `SKILL.md` file for each skill row of the appendix grid in `docs/roles/operational-analyst.md`, and SHALL NOT merge, split, or omit rows. Section-header rows (the italic group labels) are not skills and SHALL NOT produce files. The library MAY additionally contain **procedural cross-cutting skills** that reuse multiple grid rows and would violate the one-competency-per-row invariant if added as rows themselves; each such skill SHALL declare its cross-cutting nature explicitly in its own body and SHALL NOT appear in the grid.

#### Scenario: Row count matches file count for competency skills
- **WHEN** the grid lists N skill rows (excluding italic section headers)
- **THEN** the library contains at least N `SKILL.md` files, one traceable to each row

#### Scenario: Header rows produce no skill
- **WHEN** a grid line is an italic section label (e.g. *Analytic spine*)
- **THEN** no `SKILL.md` is created for it

#### Scenario: Procedural skill declares its non-grid status
- **WHEN** a procedural cross-cutting skill is inspected
- **THEN** its body states it is procedural/cross-cutting and does not correspond to a grid row

## ADDED Requirements

### Requirement: Credential-extraction sections in credential-adjacent skills

Seven skills SHALL each carry a named `## Credential extraction` section covering, for that skill's domain: artefact locations, canonical extraction tools, and portable extraction patterns. The seven are `disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, and `implant-payload-re`. The section SHALL be additive — it does not replace the existing `Objective`, `When to use`, `Method`, or `Signals / outputs` sections.

#### Scenario: Section present in each credential-adjacent skill
- **WHEN** any of the seven skills' `SKILL.md` is inspected
- **THEN** it contains a `## Credential extraction` H2 section with domain-specific artefact locations, tools, and patterns

#### Scenario: Enrichment is additive, not a rewrite
- **WHEN** an enriched skill is compared against its pre-enrichment content
- **THEN** the existing sections are unchanged and only the new `## Credential extraction` section is added

#### Scenario: Passive posture preserved
- **WHEN** a credential-extraction section is read
- **THEN** it describes analysis of already-collected material only, references no active credential validation, and stores no raw credential values in its examples

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (type, subtype, status, scope, source, reuse potential, priority), (b) a triage procedure (inventory → first-pass scan → deep-pass per category → classify → correlate → prioritise → report), and (c) an inline pattern library for common credential material (API-key prefixes by provider, auth-material formats, password-hash types, connection-string shapes, private-key markers). It SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

#### Scenario: Triage skill loads from opencode
- **WHEN** opencode starts
- **THEN** `credential-harvest-triage` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library
- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a numbered triage procedure, and an inline pattern library

#### Scenario: Not a grid row
- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`
