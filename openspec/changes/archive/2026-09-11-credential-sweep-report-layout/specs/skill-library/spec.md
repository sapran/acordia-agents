## MODIFIED Requirements

### Requirement: Procedural skills MAY co-locate reference files

A procedural cross-cutting skill MAY ship supplementary content in a `references/` subdirectory alongside its `SKILL.md`. When it does, the skill body SHALL contain a naming pointer to each reference file, so a session that reads only `SKILL.md` knows the reference exists and what class of content lives there. A harness installs the whole skill directory, so sibling reference files land alongside `SKILL.md` with no packaging step.

Reference files SHALL be markdown. Structured formats (YAML, JSON) SHALL NOT be used unless a consumer exists in the repo — this repo has no code path that loads structured references.

A skill MAY carry more than one reference file. Where it does, the body SHALL carry a separate naming pointer for each, rather than one pointer to the directory, because a session that reads only `SKILL.md` learns of a reference file solely from the pointer that names it.

#### Scenario: Reference file colocated with skill

- **WHEN** a procedural skill declares a reference file
- **THEN** the file lives at `acordia-analysts/skills/<slug>/references/<name>.md`

#### Scenario: Skill body names each reference file

- **WHEN** a procedural skill's `SKILL.md` is inspected
- **THEN** for every reference file present, the body contains a naming pointer stating the file's path relative to `SKILL.md` and what class of content it holds

#### Scenario: `credential-harvest-triage` carries `credential-patterns.md`

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `SKILL.md` and `references/credential-patterns.md`, and `SKILL.md` names the reference file

#### Scenario: `credential-harvest-triage` carries `report-layout.md`

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `references/report-layout.md` alongside `references/credential-patterns.md`, and `SKILL.md` carries a naming pointer to each of the two files rather than a single pointer to the `references/` directory

#### Scenario: Reference file is markdown

- **WHEN** any reference file under a procedural skill is inspected
- **THEN** it is a `.md` file

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `acordia-analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (ownership, type, subtype, status, scope, source, reuse potential, priority), (b) a triage procedure that begins with **inventory**, then performs a **bucket partition** step assigning material to a leg-owned bucket, then scans, classifies, correlates, prioritises, and reports, (c) a **pointer** to a co-located pattern-library reference file for common credential material, and (d) a **pointer** to a co-located report-layout reference file fixing the shape of the HTML sweep product — one that organises by the system each credential opens, holds every credential value inside a collapsed disclosure element, and carries a self-check reporting a verdict rather than content. It SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The **bucket partition** step SHALL enumerate five buckets and their target legs:

- Bucket A — identity / directory / cloud-controlplane material → `terrain-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `terrain-analyst`
- Bucket D — log-artefact material → `overwatch-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `cyber-analyst`, which holds the fused picture itself

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation.

#### Scenario: Triage skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `credential-harvest-triage` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library

- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a bucket-partition step, a numbered triage procedure downstream of the partition, a pointer to the pattern library at `references/credential-patterns.md`, and a pointer to the report layout at `references/report-layout.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `terrain-analyst`, `overwatch-analyst`, `cyber-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: No bucket names a retired leg

- **WHEN** the bucket-partition step is searched for `target-analyst` or `fusion-analyst`
- **THEN** neither is found, because neither agent exists

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

#### Scenario: Schema carries ownership

- **WHEN** the triage skill's classification schema is inspected
- **THEN** `ownership` is one of its fields

#### Scenario: The report layout fixes presentation without widening disclosure

- **WHEN** `references/report-layout.md` is read
- **THEN** it organises the product by the system each credential opens, requires every credential
  value to sit inside a collapsed disclosure element rather than in a heading, dateline, banner,
  field cell or summary, requires an evidence link to carry the whole identifier with only the
  displayed text shortened, and states that it decides presentation only while `SKILL.md`'s
  guardrails decide what may be disclosed
