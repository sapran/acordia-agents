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

### Requirement: Pillar auto-discovery is limited to distributable directories

When no pillar is named explicitly, `install.sh` and `uninstall.sh` SHALL treat a top-level directory as a pillar only if it is not dot-prefixed and carries an `agents/` or `skills/` subdirectory. Dot-prefixed directories hold tooling configuration for this repository rather than distributable artifacts, and SHALL NOT be swept into a default install.

#### Scenario: Repository tooling is not published

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** the OpenSpec workflow skills under `.opencode/skills/` and `.claude/skills/` are not deployed
- **AND** no dot-prefixed directory contributes artifacts to the deployment

#### Scenario: Non-artifact directories are still skipped

- **WHEN** pillar auto-discovery runs
- **THEN** a visible top-level directory carrying neither `agents/` nor `skills/` is not treated as a pillar

#### Scenario: Analyst pillar is unaffected

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** every agent under `analysts/agents/` and every skill under `analysts/skills/` is deployed

#### Scenario: Explicit selection overrides the filter

- **WHEN** a dot-prefixed directory carrying artifacts is named with `--pillar`
- **THEN** its artifacts are deployed
- **AND** the same holds for `uninstall.sh`, so an already-published dot-directory pillar can still be removed

### Requirement: Write-capable pillars are translated without a false read-only claim

Because omp cannot deny `write` while `tools.xdev` is on, the generated metadata note about write access SHALL distinguish three source postures: a blanket denial, a path-scoped exception, and an outright `allow`. A write-capable source SHALL NOT be stamped with the read-only note.

#### Scenario: Write-capable source stamped accurately

- **WHEN** an agent whose source grants `edit: allow` is translated
- **THEN** the generated metadata states that the source granted write access and that the allowlist carries `edit` and `write`
- **AND** it does not claim a read-only posture

#### Scenario: Read-only sources keep their existing note

- **WHEN** an analyst agent is translated after this change
- **THEN** its generated write-access note is unchanged from before the change

### Requirement: Ownership evidence is defined once for install and uninstall

The evidence that this repository deployed a given artifact SHALL be defined in exactly one place, sourced by both `install.sh` and `uninstall.sh`, because a destination the uninstaller declines to remove is by definition a destination the installer must decline to overwrite. The evidence SHALL be: a symlink resolving inside this repository, a copied file byte-identical to its source, a copied skill whose `SKILL.md` is byte-identical to its source's, or a translated agent whose generated provenance names its source path.

#### Scenario: Both scripts consult the same definition

- **WHEN** `install.sh` and `uninstall.sh` are inspected
- **THEN** neither defines its own ownership test
- **AND** both obtain it from a single shared shell file under `tools/`

#### Scenario: Shared file is not a distributable artifact

- **WHEN** `./install.sh` runs with pillars auto-discovered
- **THEN** the shared ownership file is not deployed to any harness root

### Requirement: Installation refuses to overwrite an artifact it does not own

`install.sh` SHALL, before removing or replacing any destination path, require ownership evidence for that path, and SHALL exit non-zero naming the path when the evidence is absent, because both harness roots are flat namespaces shared with harness built-ins and with the user's own artifacts.

#### Scenario: Foreign agent of the same name is refused

- **WHEN** an agent file this repository did not deploy already occupies a destination agent path
- **AND** `./install.sh` runs for the pillar containing that agent name
- **THEN** the run exits non-zero
- **AND** the message names the conflicting destination path
- **AND** the foreign file is left byte-for-byte unchanged

#### Scenario: Foreign skill directory of the same slug is refused

- **WHEN** a skill directory this repository did not deploy already occupies a destination skill path
- **AND** `./install.sh` runs for the pillar containing that slug
- **THEN** the run exits non-zero
- **AND** the foreign directory is left in place

#### Scenario: A refused run deploys nothing at all

- **WHEN** a foreign artifact occupies one destination path among many
- **AND** `./install.sh` runs for the pillar containing that name
- **THEN** every destination is checked before any file is written
- **AND** no artifact of any pillar is deployed, including those whose destinations were free

#### Scenario: A previous deployment is owned and is replaced

- **WHEN** `./install.sh` runs twice in succession in any mode, for either harness
- **THEN** the second run replaces its own artifacts without error
- **AND** the deployed set is the same as after the first run

#### Scenario: A translated agent whose source changed is still owned

- **WHEN** an omp agent was deployed by a previous run and its source agent has since been edited
- **AND** `./install.sh --harness omp` runs again
- **THEN** the destination tests as owned on the strength of its generated provenance
- **AND** the run replaces it without error

#### Scenario: Dry run detects the collision

- **WHEN** a foreign artifact occupies a destination path
- **AND** `./install.sh --dry-run` runs
- **THEN** the run exits non-zero
- **AND** no file is created, removed, or modified anywhere on disk

### Requirement: Overwriting an unowned artifact requires an explicit flag

`install.sh` SHALL accept `--force`, which replaces unowned destinations instead of refusing them, because a user who deliberately keeps a modified copy of a shipped artifact must retain a way to return to the shipped one.

#### Scenario: Forced install replaces the foreign artifact

- **WHEN** a foreign artifact occupies a destination path
- **AND** `./install.sh --force` runs
- **THEN** the destination is replaced with this repository's artifact
- **AND** the run exits zero

#### Scenario: Force is announced

- **WHEN** `./install.sh --force` replaces an unowned destination
- **THEN** the run reports each unowned path it overwrote
