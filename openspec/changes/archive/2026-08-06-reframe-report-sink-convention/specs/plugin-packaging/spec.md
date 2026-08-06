## MODIFIED Requirements

### Requirement: Claude Code posture is expressed as a denylist

A Claude Code plugin agent SHALL carry `disallowedTools`, never a `tools` allowlist, because an allowlist would have to enumerate the harness's whole tool vocabulary and would silently strip tools this repository never audited. The denylist SHALL be derived from the same source signals the omp emitter reads:

| source signal | contributes to `disallowedTools` |
| --- | --- |
| `permission.edit` denies writing outright | `Edit`, `Write`, `NotebookEdit` |
| `permission.edit` is path-scoped | `Edit`, `NotebookEdit` — `Write` is retained |
| `permission.edit: allow` | nothing |
| `permission.task` allows no agent | `Task` |

`disallowedTools` SHALL be omitted entirely when the derived list is empty.

The path-scoped row deliberately diverges from the omp emitter, which drops the tool. `Write` is retained because denying it outright would leave the two reporting analysts unable to produce the reports the competency grid assigns them, and the report sink they write into is a prompt-level convention rather than an enforced scope — in opencode as much as here, since `bash: allow` is an unrestricted write channel in every harness (see `analyst-agent-roster`). The rationale SHALL be stated in those terms and SHALL NOT read as opencode confining the writes while Claude Code fails to.

#### Scenario: Read-only analyst is denied every write tool

- **WHEN** an agent whose source denies `edit` outright and allows no dispatch is emitted for Claude Code
- **THEN** its `disallowedTools` names `Edit`, `Write`, `NotebookEdit`, and `Task`

#### Scenario: Scoped reporting analyst keeps Write

- **WHEN** an agent whose source scopes `edit` to a report path and allows no dispatch is emitted for Claude Code
- **THEN** its `disallowedTools` names `Edit`, `NotebookEdit`, and `Task`
- **AND** it does not name `Write`

#### Scenario: Write-capable orchestrator is denied nothing

- **WHEN** an agent whose source grants `edit: allow` and allows dispatch is emitted for Claude Code
- **THEN** its frontmatter carries no `disallowedTools` key

### Requirement: Postures Claude Code cannot express are recorded in the generated file

Claude Code plugin agents silently ignore `metadata`, `hooks`, `mcpServers`, and `permissionMode`, so the provenance and permission-gap record the omp emitter places in `metadata.generated` has no frontmatter home. The Claude emitter SHALL therefore write comment lines above the frontmatter keys: always the generating tool and the repo-relative source path, and conditionally one note per posture the harness cannot express — the spawn allowlist, the path-scoped write, and the per-command bash denies.

The path-scoped-write note SHALL describe the report sink as a convention no harness enforces, on the same grounds as the omp emitter's note. It SHALL NOT state or imply that the confinement is prompt-level *here* in contrast to being enforced in the source harness.

#### Scenario: Provenance is always present

- **WHEN** any agent is emitted for Claude Code
- **THEN** a comment names the generating tool and the repo-relative source path

#### Scenario: Path scope gap recorded as a universal convention

- **WHEN** an agent whose source scopes writes to a report path is emitted for Claude Code
- **THEN** a comment states that the sink is a prompt-level convention enforced by no harness
- **AND** the comment does not contrast Claude Code against the source harness

#### Scenario: Bash deny gap recorded

- **WHEN** an agent whose source carries per-pattern bash denies is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express per-command bash rules and that those denies are prompt-level
