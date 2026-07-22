## MODIFIED Requirements

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (type, subtype, status, scope, source, reuse potential, priority), (b) a triage procedure that begins with **inventory**, then performs a **bucket partition** step assigning material to a leg-owned bucket, then scans, classifies, correlates, prioritises, and reports, and (c) a **pointer** to a co-located pattern-library reference file for common credential material. It SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The **bucket partition** step SHALL enumerate five buckets and their target legs:

- Bucket A — identity / directory / cloud-controlplane material → `target-network-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `target-network-analyst`
- Bucket D — log-artefact material → `defender-detection-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `fusion-analyst`

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation.

#### Scenario: Triage skill loads from opencode

- **WHEN** opencode starts
- **THEN** `credential-harvest-triage` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries schema, bucket-partition step, procedure, and pattern pointer

- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a bucket-partition step, a numbered triage procedure downstream of the partition, and a pointer to `references/credential-patterns.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

## ADDED Requirements

### Requirement: Procedural skills MAY co-locate reference files

A procedural cross-cutting skill MAY ship supplementary content in a `references/` subdirectory alongside its `SKILL.md`. When it does, the skill body SHALL contain a naming pointer to each reference file, so a session that reads only `SKILL.md` knows the reference exists and what class of content lives there. `install.sh` symlinks the whole skill directory; sibling reference files SHALL therefore land alongside `SKILL.md` at deploy time without an install-script change.

Reference files SHALL be markdown. Structured formats (YAML, JSON) SHALL NOT be used unless a consumer exists in the repo — this repo has no code path that loads structured references.

#### Scenario: Reference file colocated with skill

- **WHEN** a procedural skill declares a reference file
- **THEN** the file lives at `analysts/skills/<slug>/references/<name>.md`

#### Scenario: Skill body names each reference file

- **WHEN** a procedural skill's `SKILL.md` is inspected
- **THEN** for every reference file present, the body contains a naming pointer stating the file's path relative to `SKILL.md` and what class of content it holds

#### Scenario: `credential-harvest-triage` carries `credential-patterns.md`

- **WHEN** `analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `SKILL.md` and `references/credential-patterns.md`, and `SKILL.md` names the reference file

#### Scenario: Reference file is markdown

- **WHEN** any reference file under a procedural skill is inspected
- **THEN** it is a `.md` file
