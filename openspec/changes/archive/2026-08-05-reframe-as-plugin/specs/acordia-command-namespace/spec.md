## MODIFIED Requirements

### Requirement: Namespace shape is per harness, because discovery differs

The namespace SHALL never be realised by renaming an artifact. Because the three target harnesses discover commands differently, one source tree SHALL produce three deployed shapes, two of which are supplied by the harness itself:

- **omp**, via `plugins/omp/<plugin>/commands/<stem>.md`, yields `/<plugin>:<stem>` — for example `/acordia-analysts:fusion`. The prefix comes from the plugin name, applied by the harness.
- **Claude Code**, via `plugins/claude/<plugin>/commands/<stem>.md`, yields the same `/<plugin>:<stem>`, by the same rule. The two plugin harnesses therefore agree without any per-harness placement decision.
- **opencode** receives `<opencode-root>/commands/acordia-<stem>.md`, yielding `/acordia-<stem>`, because opencode command discovery is flat and it has no plugin system to supply a prefix. This matches the convention this repository already uses for its own OpenSpec commands (`.opencode/commands/opsx-apply.md` beside `.claude/commands/opsx/apply.md`).

Within a plugin the command directory SHALL be flat, because omp's plugin command provider scans `<plugin-root>/commands/*.md` non-recursively and a subdirectory would be invisible to it. The source tree SHALL keep its `commands/acordia/` directory, which is now purely the opencode-facing layout.

#### Scenario: Plugin harnesses namespace by plugin name

- **WHEN** a plugin is installed in omp or in Claude Code
- **THEN** each of its wrappers is invocable as `<plugin>:<stem>`
- **AND** the two harnesses expose the same handle for the same wrapper

#### Scenario: Plugin command directories are flat

- **WHEN** a generated plugin tree is inspected
- **THEN** every wrapper sits directly in `<plugin-root>/commands/`
- **AND** no subdirectory is created there

#### Scenario: opencode carries the flat namespace

- **WHEN** the command set is deployed for the opencode harness
- **THEN** each wrapper lands at `<opencode-root>/commands/acordia-<stem>.md`
- **AND** no subdirectory is created, because opencode command discovery is flat

### Requirement: Commands deploy under the same guarantees as agents and skills

For the opencode install path, `install.sh` and `uninstall.sh` SHALL carry the command set by default, and SHALL apply to it the guarantees they already apply to agents and skills: ownership evidence before overwrite or removal, preflight abort before anything is written, `--dry-run` that writes nothing, and idempotent re-invocation.

The scripts SHALL accept `--no-commands` to skip the step and `--commands-target DIR` to place the tree explicitly. Because a command root cannot be inferred from an overridden harness root, a run that overrides the root without naming a command target SHALL skip the command step with an explanatory message rather than guess.

Ownership evidence for a command SHALL be defined in the same shared file as the existing evidence, as a symlink resolving inside this repository or a byte-identical copy, so the installer and uninstaller cannot drift.

These guarantees are specific to the opencode filesystem deployment. In omp and Claude Code the wrappers arrive as part of a plugin directory the harness installs and removes itself, so overwrite refusal, ownership evidence, and the dry run have no counterpart and no need of one — a plugin's files are attributable to the plugin by construction.

#### Scenario: Foreign command file is refused

- **WHEN** a file this repository did not deploy occupies an opencode command destination
- **AND** `./install.sh` runs
- **THEN** the run exits non-zero naming the conflicting path
- **AND** the foreign file is left byte-for-byte unchanged

#### Scenario: Commands can be skipped

- **WHEN** `./install.sh --no-commands` runs
- **THEN** agents and skills are deployed
- **AND** no command file is written

#### Scenario: Dry run writes no command

- **WHEN** `./install.sh --dry-run` runs
- **THEN** the intended command actions are printed
- **AND** no command file is created, removed, or modified

#### Scenario: Uninstall removes owned commands only

- **WHEN** `./uninstall.sh` runs after an install
- **THEN** the command files this repository deployed are removed
- **AND** a name-matching command file it did not deploy is left in place and reported

#### Scenario: Plugin harnesses need no ownership protocol

- **WHEN** a plugin is uninstalled in omp or Claude Code
- **THEN** the harness removes the plugin's own directory
- **AND** neither `install.sh` nor `tools/ownership.sh` participates
