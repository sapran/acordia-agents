# omp-harness-distribution Specification

## Purpose

How the opencode-native source artifacts under `<pillar>/` reach a second harness, omp (`oh-my-pi`): the agent frontmatter translation contract, the deployment locations and selector, the rule that translated agents are build output rather than tracked files, and the permission-model gaps that translation cannot close.

## Requirements

### Requirement: Source artifacts stay opencode-native

The files under `<pillar>/agents/` and `<pillar>/skills/` SHALL remain written to the opencode contract and SHALL be the only editable source for both harnesses. Deployment to omp SHALL be produced by translating those files, never by maintaining a parallel set.

#### Scenario: No committed omp agent copies

- **WHEN** the repository is inspected for tracked agent files
- **THEN** the only tracked agent prompts are `<pillar>/agents/*.md` in opencode frontmatter form
- **AND** any omp-form agent file present on disk lives under a gitignored build directory

#### Scenario: Source edit reaches both harnesses

- **WHEN** a prompt body in `<pillar>/agents/*.md` is edited and both harnesses are reinstalled
- **THEN** the opencode deployment and the omp deployment both carry the edited body

### Requirement: Harness selector on install and uninstall

`install.sh` and `uninstall.sh` SHALL accept `--harness opencode|omp|both`. The default SHALL be `opencode`, so that an invocation with no harness argument behaves as it did before this capability existed.

#### Scenario: Default is unchanged behaviour

- **WHEN** `./install.sh` runs with no `--harness` argument
- **THEN** artifacts are deployed only under `~/.config/opencode/`
- **AND** nothing is written under `~/.omp/`

#### Scenario: omp harness selected

- **WHEN** `./install.sh --harness omp` runs
- **THEN** translated agent files are deployed to `~/.omp/agent/agents/`
- **AND** skill directories are deployed to `~/.omp/agent/skills/`
- **AND** nothing is written under `~/.config/opencode/`

#### Scenario: Both harnesses selected

- **WHEN** `./install.sh --harness both` runs
- **THEN** both deployments described above are performed in one invocation

#### Scenario: Unknown harness rejected

- **WHEN** `--harness` is given a value other than `opencode`, `omp`, or `both`
- **THEN** the script exits non-zero with a message naming the accepted values
- **AND** no files are deployed

#### Scenario: Uninstall is scoped to the harness

- **WHEN** `./uninstall.sh --harness omp` runs after an omp install
- **THEN** the agent files and skill entries this repository deployed under `~/.omp/agent/` are removed
- **AND** files under `~/.omp/agent/` that this repository did not deploy are left in place

#### Scenario: A name match alone is not grounds for removal

- **WHEN** a harness config holds an agent file or skill directory whose name matches a repository artifact but whose content this repository did not deploy
- **THEN** `uninstall.sh` leaves it in place
- **AND** reports how many name-matching artifacts it declined to remove

#### Scenario: Ownership is established by deployment evidence

- **WHEN** `uninstall.sh` considers a deployed artifact
- **THEN** it removes a symlink only if the link resolves inside this repository
- **AND** removes a copied agent only if it is byte-identical to its source or carries generated provenance naming that source
- **AND** removes a copied skill only if its `SKILL.md` is byte-identical to the source's

### Requirement: Frontmatter translation contract

The translator SHALL convert one opencode agent file into one omp task-agent file according to a fixed mapping. The generated file SHALL carry a `name` field equal to the source filename stem and SHALL preserve the source `description` verbatim, because omp skips any agent file lacking either field.

#### Scenario: Required fields emitted

- **WHEN** any `<pillar>/agents/<stem>.md` is translated
- **THEN** the output frontmatter contains `name: <stem>`
- **AND** the output frontmatter contains the source `description` unchanged

#### Scenario: Read-only posture becomes an absent tool

- **WHEN** a source agent carries `permission.edit` denying `"*"`
- **THEN** the output `tools` allowlist contains neither `edit` nor `write`
- **AND** the running agent has no `edit` tool

#### Scenario: Analysis shell preserved

- **WHEN** a source agent carries `permission.bash: allow`
- **THEN** the output `tools` allowlist contains `bash`

#### Scenario: Leaf specialist cannot dispatch

- **WHEN** a source agent carries `mode: subagent` and `permission.task: deny`
- **THEN** the output `tools` allowlist does not contain `task`
- **AND** the output frontmatter declares no `spawns`

#### Scenario: Orchestrator dispatches exactly its named legs

- **WHEN** a source agent carries `mode: primary` and a `permission.task` map allowing three named agents
- **THEN** the output `tools` allowlist contains `task`
- **AND** the output `spawns` lists exactly those three names

#### Scenario: Provenance metadata preserved

- **WHEN** a source agent carries a `metadata.acordia` block
- **THEN** the output frontmatter carries that block unchanged
- **AND** the output frontmatter records that the file is generated, naming its source path

### Requirement: Prompt text corrected for omp's tool set

omp provides no `list` tool; a directory path given to `read` enumerates it. The translator SHALL replace the shared "Tool discipline" paragraph with an omp-correct version and SHALL fail rather than emit a prompt that instructs the agent to use a tool the harness does not provide.

#### Scenario: Paragraph rewritten

- **WHEN** an agent file whose Tool-discipline paragraph names `list` is translated
- **THEN** the emitted paragraph does not name a `list` tool
- **AND** the emitted paragraph states that `read` on a directory path lists its entries

#### Scenario: Unrecognised paragraph aborts translation

- **WHEN** the expected Tool-discipline paragraph is not found in a source agent file
- **THEN** the translator exits non-zero naming the offending file
- **AND** no output file is written for it

### Requirement: Unmappable permissions are surfaced, not silently resolved

omp allowlists whole tools, cannot scope a tool to a path, and cannot remove `write` at all while its `tools.xdev` setting is on, because `read` and `write` are the transport for every `xd://` device. The source files' `".acordia/reports/**": allow` write exception therefore has no faithful translation, and neither does a blanket write denial. The translator SHALL emit the narrower allowlist regardless and SHALL record in the generated file that the harness does not enforce it.

#### Scenario: Write access is never silently claimed

- **WHEN** any agent is translated
- **THEN** the output frontmatter records, under generated metadata, that omp exposes `write` as an `xd://` transport tool irrespective of the allowlist

#### Scenario: Scoped report sink is reported as unenforceable

- **WHEN** an agent carrying the scoped report-sink exception is translated
- **THEN** the output frontmatter records that omp cannot express the path scope
- **AND** the record states that the agent can write anywhere

#### Scenario: Dispatch denial is enforced

- **WHEN** a translated leaf agent runs in omp
- **THEN** it has no `task` tool and cannot dispatch any agent

### Requirement: Skill autoloading is opt-in

omp can inject named skill bodies into a subagent at start via `autoloadSkills`. Because opencode has no equivalent and binds skills by prose reference, the translator SHALL leave `autoloadSkills` unset by default so that both harnesses behave alike.

#### Scenario: Default omits autoloading

- **WHEN** an agent is translated with no autoload flag
- **THEN** the output frontmatter declares no `autoloadSkills`

#### Scenario: Deep skills autoloaded on request

- **WHEN** the translator is invoked with the deep-autoload flag
- **THEN** the output `autoloadSkills` lists exactly the skills named in the source prompt's `(deep)` heading

### Requirement: Translated agents are materialised, never symlinked

Because translated agents are build output that is regenerated on each install, the omp harness SHALL deploy them as real files. A request to symlink SHALL not silently produce a link into the build directory.

#### Scenario: Copy regardless of link mode

- **WHEN** `./install.sh --harness omp --link` runs
- **THEN** the files under `~/.omp/agent/agents/` are regular files, not symlinks
- **AND** the script reports that link mode does not apply to translated agents

#### Scenario: Skills still honour link mode

- **WHEN** `./install.sh --harness omp --link` runs
- **THEN** the entries under `~/.omp/agent/skills/` are symlinks into the repository

### Requirement: Installation is idempotent and inspectable

Both harnesses SHALL support repeated invocation without accumulating state, and SHALL support previewing an invocation without touching the filesystem.

#### Scenario: Re-running changes nothing

- **WHEN** `./install.sh --harness both` runs twice in succession
- **THEN** the second run leaves the same set of deployed files as the first

#### Scenario: Dry run writes nothing

- **WHEN** `./install.sh --harness omp --dry-run` runs
- **THEN** the intended actions are printed
- **AND** no file is created, removed, or modified anywhere on disk

#### Scenario: A clean dry run predicts a clean install

- **WHEN** `./install.sh --harness omp --dry-run` runs
- **THEN** the translator is exercised in a mode that parses every source agent without writing output
- **AND** a source file that would fail translation makes the dry run exit non-zero
- **AND** the printed plan names the translated build path as each agent's source, matching what a real run copies

