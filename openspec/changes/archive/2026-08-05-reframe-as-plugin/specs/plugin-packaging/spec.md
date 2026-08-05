## ADDED Requirements

### Requirement: The repository root is a plugin marketplace

The repository SHALL publish itself as a plugin marketplace carrying exactly two plugins, so that a harness with a plugin system installs the distribution through its own mechanism rather than through a bespoke shell installer. The marketplace SHALL be named `acordia`, and the plugins SHALL be `acordia-analysts` and `acordia-operators`, one per pillar.

The two plugins SHALL be independently installable, because the pillars carry opposite postures: the analysts are read-only decision support and the operators are write-capable offensive tooling. Installing the analytic library SHALL NOT imply installing the offensive one.

#### Scenario: Both plugins are offered separately

- **WHEN** either marketplace catalog is read
- **THEN** it lists exactly the two plugin entries `acordia-analysts` and `acordia-operators`
- **AND** each entry carries its own `source`, `version`, `description`, `category`, and `keywords`

#### Scenario: The analysis pillar installs alone

- **WHEN** `acordia-analysts@acordia` is installed and `acordia-operators@acordia` is not
- **THEN** the four analyst agents, the analyst skill library, and the eight analyst command wrappers are available
- **AND** no operator agent, skill, or command wrapper is installed

#### Scenario: Plugin contents are fixed by pillar

- **WHEN** an installed plugin is inspected
- **THEN** `acordia-analysts` carries the four agents and the skill library of `analysts/`, and `acordia-operators` carries the five agents and the skill library of `operators/`
- **AND** each carries exactly the command wrappers that dispatch its own agents

### Requirement: Two plugin trees, because one agent file cannot serve both harnesses

The distribution SHALL materialise a Claude-shaped tree at `plugins/claude/<plugin>/` and an omp-shaped tree at `plugins/omp/<plugin>/`, both generated from the single opencode-format source under `<pillar>/agents/`, `<pillar>/skills/`, and `commands/acordia/`.

Two trees are required rather than preferred. Both harnesses discover plugin agents at the fixed path `<plugin-root>/agents/`; Claude Code expects a capitalised Claude tool vocabulary while omp expects lowercase omp tool names and additionally requires `spawns` for the orchestrators' delegation allowlists; and Claude Code's manifest `agents` path field supplements the `./agents` default rather than replacing it, so the two harnesses cannot be pointed at different directories inside one plugin. Emitting no tool field at all SHALL NOT be used as an escape, because both harnesses would then inherit every tool and the analysts' read-only posture would be lost in both.

Skills and command wrappers SHALL be byte-identical between the two trees, so that `agents/` is the only directory in which they can differ.

#### Scenario: Only the agent directory differs

- **WHEN** the Claude tree and the omp tree of the same plugin are compared
- **THEN** their `skills/` directories are identical
- **AND** their `commands/` directories are identical
- **AND** their `agents/` directories differ

#### Scenario: Each tree speaks its harness's vocabulary

- **WHEN** an agent file from each tree is read
- **THEN** the omp file carries a lowercase `tools` allowlist, and `spawns` when the source allows dispatch
- **AND** the Claude file carries no `tools` allowlist and no `spawns`

### Requirement: Two marketplace catalogs, one per harness

The repository root SHALL carry `.omp-plugin/marketplace.json` and `.claude-plugin/marketplace.json`. omp reads the former in preference to the latter and falls back only when it is absent, and Claude Code reads the latter, so shipping both is what hands each harness its own tree from one checkout.

The two catalogs SHALL be identical except for the `source` values, which SHALL point at `./plugins/omp/<plugin>` and `./plugins/claude/<plugin>` respectively. Each SHALL carry only keys both catalog schemas document — `name`, `owner`, `metadata`, and per entry `name`, `source`, `version`, `description`, `category`, `keywords` — because omp logs and skips a plugin entry it considers invalid, so a speculative field risks silently dropping a plugin.

#### Scenario: Catalogs differ only in their sources

- **WHEN** the two catalogs are compared
- **THEN** every field is equal except the two `source` values
- **AND** the omp catalog's sources name `./plugins/omp/…` while the Claude catalog's name `./plugins/claude/…`

#### Scenario: Each plugin directory carries a manifest

- **WHEN** a plugin directory in either tree is inspected
- **THEN** it carries `.claude-plugin/plugin.json` naming the plugin, its version, description, author, repository, and keywords
- **AND** the manifest declares no `commands`, `agents`, or `skills` path key, because the defaults are exactly what the tree uses and the fields supplement rather than replace

### Requirement: Generated trees are committed and gate-checked

Everything under `plugins/`, `.claude-plugin/`, and `.omp-plugin/` SHALL be build output produced by `tools/build-plugins.py` from the opencode-native sources, and SHALL be committed, because a marketplace install clones the repository and performs no build on the installing machine.

A plain build SHALL stage the whole tree in a temporary directory and swap it into place only on success, replacing each generated path wholesale, so that a renamed or removed source artifact cannot leave an orphan behind and a failed build cannot leave the committed tree deleted or half-written. `tools/build-plugins.py --check` SHALL build into a temporary directory, diff against the committed tree, name every missing, extra, and differing path, and exit non-zero on any mismatch, without writing anything outside that temporary directory. Editing a file under `plugins/` SHALL be treated as a drift bug rather than as a change.

#### Scenario: The generator is deterministic

- **WHEN** `tools/build-plugins.py` runs twice in succession
- **THEN** the second run leaves the tree byte-identical to the first

#### Scenario: Drift is reported and fails

- **WHEN** a file under `plugins/` is edited by hand and `tools/build-plugins.py --check` runs
- **THEN** the command exits non-zero naming that path as differing
- **AND** no file outside the temporary build directory is modified

#### Scenario: A removed source artifact leaves no orphan

- **WHEN** a skill directory is deleted from a pillar and the generator runs
- **THEN** the corresponding directory is absent from both plugin trees

#### Scenario: A failed build leaves the committed tree intact

- **WHEN** a source artifact is malformed and the generator runs
- **THEN** it exits non-zero naming that source file
- **AND** the previously committed trees are unchanged, because the build is staged and swapped rather than written in place

### Requirement: Claude Code posture is expressed as a denylist

A Claude Code plugin agent SHALL carry `disallowedTools`, never a `tools` allowlist, because an allowlist would have to enumerate the harness's whole tool vocabulary and would silently strip tools this repository never audited. The denylist SHALL be derived from the same source signals the omp emitter reads:

| source signal | contributes to `disallowedTools` |
| --- | --- |
| `permission.edit` denies writing outright | `Edit`, `Write`, `NotebookEdit` |
| `permission.edit` is path-scoped | `Edit`, `NotebookEdit` — `Write` is retained |
| `permission.edit: allow` | nothing |
| `permission.task` allows no agent | `Task` |

`disallowedTools` SHALL be omitted entirely when the derived list is empty.

The path-scoped row deliberately diverges from the omp emitter, which drops the tool. opencode confines the two reporting analysts' writes to `.acordia/reports/**`; Claude Code cannot express a path scope in plugin-agent frontmatter, and denying `Write` outright would leave those agents unable to produce the reports the competency grid assigns them. `Write` is therefore granted and the confinement is recorded as prompt-level.

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

#### Scenario: Provenance is always present

- **WHEN** any Claude plugin agent file is read
- **THEN** its first comment line names the repo-relative source path and `tools/build-plugins.py`, and states that the file is not to be edited

#### Scenario: Spawn allowlist gap recorded

- **WHEN** an agent whose source allows dispatch to named agents is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express a spawn allowlist and that the prompt names the agents this one dispatches

#### Scenario: Path scope gap recorded

- **WHEN** an agent whose source scopes writes to a report path is emitted for Claude Code
- **THEN** a comment states that the harness cannot express a path scope and that the confinement is prompt-level

#### Scenario: Bash deny gap recorded

- **WHEN** an agent whose source carries per-pattern bash denies is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express per-command bash rules and that those denies are prompt-level

### Requirement: Command wrappers are routed by the agent they name

Each `commands/acordia/<stem>.md` SHALL be placed in whichever plugin owns the agent its body names. The agent SHALL be read from the wrapper's opening sentence, which is one of two shapes — a dispatch sentence for a leaf agent, or a hand-the-work sentence for an orchestrator, which must additionally name a session-switch fallback. A wrapper matching neither shape, or naming an agent belonging to no pillar, SHALL fail the build naming that wrapper rather than being guessed at.

The emitted wrapper SHALL carry `description` and `argument-hint` only, preserving their values verbatim along with any trailing comment line, and SHALL drop `name` (the handle is now supplied by the plugin prefix) and `category` (a key in neither plugin schema). The body SHALL be copied unchanged, including `$ARGUMENTS`.

Wrappers SHALL be emitted flat at `<plugin-root>/commands/<stem>.md`, because omp's plugin command provider scans that directory non-recursively and a subdirectory would be invisible to it.

#### Scenario: Wrappers follow their agent's pillar

- **WHEN** the plugin trees are generated
- **THEN** every wrapper naming an analyst agent is in `acordia-analysts` and every wrapper naming an operator agent is in `acordia-operators`

#### Scenario: An unroutable wrapper fails the build

- **WHEN** a wrapper's body names no agent, or names an agent in no pillar
- **THEN** the generator exits non-zero naming that wrapper
- **AND** no plugin tree is left partially written in the repository

#### Scenario: Frontmatter is reduced, not rewritten

- **WHEN** a generated wrapper is compared with its source
- **THEN** its `description` and `argument-hint` values are unchanged, and any trailing comment line is preserved
- **AND** it carries no `name` and no `category`
- **AND** its body is byte-identical to the source body
