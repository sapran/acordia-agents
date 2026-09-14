## MODIFIED Requirements

### Requirement: Procedural skills MAY co-locate reference files

A procedural cross-cutting skill MAY ship supplementary content in a `references/` subdirectory alongside its `SKILL.md`. When it does, the skill body SHALL contain a naming pointer to each reference file, so a session that reads only `SKILL.md` knows the reference exists and what class of content lives there. A harness installs the whole skill directory, so sibling reference files land alongside `SKILL.md` with no packaging step.

Every naming pointer SHALL give an address a reading session can open without reconstructing one: the file named relative to the `SKILL.md` that owns it, **and** the `skill://<owning-slug>/references/<name>.md` URI. This binds every body that points at a reference file, including a body in a skill that does not own it. A path relative to a sibling skill directory (`../<slug>/references/<name>.md`) SHALL NOT be a pointer's only address, because no harness read tool resolves a path relative to a skill body.

The skill that owns a reference file SHALL state that a path into a harness skills directory is never to be reconstructed, because a guessed absolute path is how a reference file gets reported missing while being installed and current.

No requirement here SHALL credit a named harness with resolving the `skill://` form. The URI is recorded as the address the pointer gives, and the relative filename remains stated for any harness that reads a sibling file by relative path.

Reference files SHALL be markdown. Structured formats (YAML, JSON) SHALL NOT be used unless a consumer exists in the repo — this repo has no code path that loads structured references.

A skill MAY carry more than one reference file. Where it does, the body SHALL carry a separate naming pointer for each, rather than one pointer to the directory, because a session that reads only `SKILL.md` learns of a reference file solely from the pointer that names it.

#### Scenario: Reference file colocated with skill

- **WHEN** a procedural skill declares a reference file
- **THEN** the file lives at `acordia-analysts/skills/<slug>/references/<name>.md`

#### Scenario: Skill body names each reference file

- **WHEN** a procedural skill's `SKILL.md` is inspected
- **THEN** for every reference file present, the body contains a naming pointer stating the file's path relative to `SKILL.md`, the `skill://<owning-slug>/references/<name>.md` URI, and what class of content it holds

#### Scenario: A pointer from another skill's body carries the URI

- **WHEN** a skill body points at a reference file owned by a different skill
- **THEN** the pointer gives the `skill://<owning-slug>/references/<name>.md` URI
- **AND** it does not rely on a path relative to a sibling skill directory as its only address

#### Scenario: The owning skill refuses a reconstructed path

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/SKILL.md` is read
- **THEN** it states that its reference files ship inside its own directory and names the two addresses that open them
- **AND** it states that a path into a harness skills directory is never reconstructed

#### Scenario: `credential-harvest-triage` carries `credential-patterns.md`

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `SKILL.md` and `references/credential-patterns.md`, and `SKILL.md` names the reference file

#### Scenario: `credential-harvest-triage` carries `report-layout.md`

- **WHEN** `acordia-analysts/skills/credential-harvest-triage/` is inspected
- **THEN** it contains `references/report-layout.md` alongside `references/credential-patterns.md`, and `SKILL.md` carries a naming pointer to each of the two files rather than a single pointer to the `references/` directory

#### Scenario: Reference file is markdown

- **WHEN** any reference file under a procedural skill is inspected
- **THEN** it is a `.md` file
