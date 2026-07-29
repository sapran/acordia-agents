## MODIFIED Requirements

### Requirement: Frontmatter translation contract

The translator SHALL convert one opencode agent file into one omp task-agent file according to a fixed mapping. The generated file SHALL carry a `name` field equal to the source filename stem and SHALL preserve the source `description` verbatim, because omp skips any agent file lacking either field.

The emitted `tools` allowlist SHALL be derived from the source `permission` map rather than from a fixed list, so that a write-capable pillar translates as faithfully as a read-only one. The derivation is:

- always present: `read`, `grep`, `glob`, `bash`, `web_search`, `todo`, and `yield` (omp appends `yield` itself; naming it keeps the generated file honest)
- `edit` and `write` are present when the source `permission.edit` is not a denial — that is, when it is `allow`, or a path map with at least one `allow`
- `browser` is present when the source `permission.browser` is `allow`
- `task` is present, and `spawns` lists the allowed agent names, when the source `permission.task` map names at least one allowed agent

#### Scenario: Required fields emitted

- **WHEN** any `<pillar>/agents/<stem>.md` is translated
- **THEN** the output frontmatter contains `name: <stem>`
- **AND** the output frontmatter contains the source `description` unchanged

#### Scenario: Read-only posture becomes an absent tool

- **WHEN** a source agent carries `permission.edit` denying `"*"`
- **THEN** the output `tools` allowlist contains neither `edit` nor `write`
- **AND** the running agent has no `edit` tool

#### Scenario: Write-capable posture becomes present tools

- **WHEN** a source agent carries `permission.edit: allow`
- **THEN** the output `tools` allowlist contains both `edit` and `write`

#### Scenario: Browser capability carried over

- **WHEN** a source agent carries `permission.browser: allow`
- **THEN** the output `tools` allowlist contains `browser`

#### Scenario: Analysis shell preserved

- **WHEN** a source agent carries `permission.bash: allow`
- **THEN** the output `tools` allowlist contains `bash`

#### Scenario: Per-command bash denies do not remove the shell

- **WHEN** a source agent carries `bash: allow` together with per-pattern `deny` rules
- **THEN** the output `tools` allowlist still contains `bash`
- **AND** the generated metadata records that omp has no per-command equivalent, so those denies are prompt-level under omp

#### Scenario: Leaf specialist cannot dispatch

- **WHEN** a source agent carries `mode: subagent` and `permission.task: deny`
- **THEN** the output `tools` allowlist does not contain `task`
- **AND** the output frontmatter declares no `spawns`

#### Scenario: Orchestrator dispatches exactly its named legs

- **WHEN** a source agent carries `mode: primary` and a `permission.task` map allowing named agents
- **THEN** the output `tools` allowlist contains `task`
- **AND** the output `spawns` lists exactly those names

#### Scenario: Provenance metadata preserved

- **WHEN** a source agent carries a `metadata.acordia` or `metadata.cyberstrike` block
- **THEN** the output frontmatter carries that block unchanged
- **AND** the output frontmatter records that the file is generated, naming its source path

### Requirement: Prompt text corrected for omp's tool set

omp provides no `list` tool; a directory path given to `read` enumerates it. Where a source prompt carries the shared "Tool discipline" paragraph, the translator SHALL replace it with an omp-correct version. Prompts that do not carry that paragraph SHALL translate unchanged in that respect — its absence is not an error, because it is an analyst-pillar convention rather than a repository-wide one.

Regardless of which pillar a prompt comes from, the translator SHALL fail rather than emit a prompt that names a `list` tool.

#### Scenario: Paragraph rewritten

- **WHEN** an agent file whose Tool-discipline paragraph names `list` is translated
- **THEN** the emitted paragraph does not name a `list` tool
- **AND** the emitted paragraph states that `read` on a directory path lists its entries

#### Scenario: Prompt without the paragraph translates cleanly

- **WHEN** an agent file carrying no Tool-discipline paragraph and no `list` reference is translated
- **THEN** translation succeeds and the body is emitted unchanged

#### Scenario: Surviving `list` reference aborts translation

- **WHEN** a source prompt names a `list` tool in wording the translator cannot rewrite
- **THEN** the translator exits non-zero naming the offending file
- **AND** no output file is written for it

#### Scenario: Unrecognised paragraph aborts translation

- **WHEN** a source agent file carries the Tool-discipline paragraph but in wording that differs from the expected text
- **THEN** the translator exits non-zero naming the offending file
- **AND** no output file is written for it

## ADDED Requirements

### Requirement: Write-capable pillars are translated without a false read-only claim

Because omp cannot deny `write` while `tools.xdev` is on, the generated metadata note about write access SHALL distinguish three source postures: a blanket denial, a path-scoped exception, and an outright `allow`. A write-capable source SHALL NOT be stamped with the read-only note.

#### Scenario: Write-capable source stamped accurately

- **WHEN** an agent whose source grants `edit: allow` is translated
- **THEN** the generated metadata states that the source granted write access and that the allowlist carries `edit` and `write`
- **AND** it does not claim a read-only posture

#### Scenario: Read-only sources keep their existing note

- **WHEN** an analyst agent is translated after this change
- **THEN** its generated write-access note is unchanged from before the change
