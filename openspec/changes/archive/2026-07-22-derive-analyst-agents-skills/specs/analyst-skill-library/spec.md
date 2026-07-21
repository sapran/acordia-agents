## ADDED Requirements

### Requirement: One skill per competency-grid row

The library SHALL contain exactly one `SKILL.md` file for each skill row of the appendix grid in `docs/roles/operational-analyst.md`, and SHALL NOT merge, split, or omit rows. Section-header rows (the italic group labels) are not skills and SHALL NOT produce files.

#### Scenario: Row count matches file count
- **WHEN** the grid lists N skill rows (excluding italic section headers)
- **THEN** the library contains exactly N `SKILL.md` files, one traceable to each row

#### Scenario: Header rows produce no skill
- **WHEN** a grid line is an italic section label (e.g. *Analytic spine*)
- **THEN** no `SKILL.md` is created for it

### Requirement: opencode-native location, plain slugs

Each skill SHALL live at `~/.config/opencode/skills/<slug>/SKILL.md`. The slug SHALL be kebab-case with **no prefix** and SHALL equal the frontmatter `name`.

#### Scenario: Loaded by opencode
- **WHEN** opencode starts
- **THEN** the skill is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Slug and name agree, no prefix
- **WHEN** a skill folder is named `<slug>`
- **THEN** its `SKILL.md` frontmatter `name` equals `<slug>` and neither carries an `oa-` or other prefix

### Requirement: opencode frontmatter contract

Each `SKILL.md` SHALL declare the opencode-required fields `name` (lowercase-hyphen, 1–64 chars) and `description` (1–1024 chars). It MAY declare opencode's optional `metadata`. It SHALL NOT rely on CyberStrike-only fields (`category`, `cwe_ids`, `chains_with`, `severity_boost`) for behaviour, and SHALL NOT include `sha256`/`signature`.

#### Scenario: Required fields present and valid
- **WHEN** any library `SKILL.md` is inspected
- **THEN** `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$` and is ≤64 chars, `description` is 1–1024 chars, and the body is non-empty

### Requirement: Triggering-quality descriptions

Because opencode attaches skills by description (there is no per-agent binding), each `description` SHALL state WHEN the skill applies in one sharp sentence, sufficient to trigger the skill for the right task.

#### Scenario: Description drives selection
- **WHEN** opencode evaluates the skill against a matching analytic task
- **THEN** the `description` alone is specific enough to select it

### Requirement: Cross-cutting deep skills are ordinary skills

The two cross-cutting deep skills — reverse-engineering (implant/payload behaviour) and operational-technology/embedded — SHALL be authored as ordinary `SKILL.md` files, not agents. Their relationship to the legs that draw on them SHALL be stated in prose (skill body / agent prompt), not via a `chains_with` frontmatter edge.

#### Scenario: RE and OT are plain skills
- **WHEN** the reverse-engineering and operational-technology skills are inspected
- **THEN** each is a `SKILL.md` with opencode frontmatter, no `chains_with` field, and neither has its own agent file
