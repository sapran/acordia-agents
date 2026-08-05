## REMOVED Requirements

### Requirement: Harness selector on install and uninstall

**Reason**: omp is no longer served by the shell installer. It installs the distribution as a plugin from `.omp-plugin/marketplace.json`, so `install.sh` and `uninstall.sh` have exactly one destination and a selector would name a harness they can no longer reach.

**Migration**: `./install.sh --harness omp` and `--harness both` are gone; `--harness` is rejected as an unknown flag. Replace them with `omp plugin marketplace add <repo>` followed by `omp plugin install acordia-analysts@acordia` (and `acordia-operators@acordia` for the offensive pillar). `./install.sh` with no selector is unchanged and still deploys to opencode. The refusal-to-overwrite, `--force`, `--dry-run`, `--pillar`, `--target`, and command-deployment behaviours are unaffected.

### Requirement: Translated agents are materialised, never symlinked

**Reason**: Nothing is translated at install time any more. The omp agent tree is generated ahead of time by `tools/build-plugins.py` and committed under `plugins/omp/`, and omp's own plugin installer places it — the shell installer never writes an omp-form file, so there is no link-versus-copy decision left to make.

**Migration**: None for users. The property the requirement protected — that an omp agent file is a real file carrying its generated provenance, not a link into a transient build directory — now holds by construction, and is covered by the `plugin-packaging` capability's committed-and-gate-checked requirement.

## MODIFIED Requirements

### Requirement: Source artifacts stay opencode-native

The files under `<pillar>/agents/` and `<pillar>/skills/` SHALL remain written to the opencode contract and SHALL be the only editable source for every harness. Distribution to omp SHALL be produced by translating those files, never by maintaining a parallel set.

The translated form is no longer transient. It is generated into the committed plugin tree at `plugins/omp/<plugin>/agents/`, because a marketplace install clones the repository and performs no build on the installing machine. That tree is build output all the same: it is regenerated wholesale on every build and gated by `tools/build-plugins.py --check`, so editing it is a drift bug rather than a change.

#### Scenario: Committed omp agent copies are generated, never authored

- **WHEN** the repository is inspected for tracked agent files
- **THEN** the only editable agent prompts are `<pillar>/agents/*.md` in opencode frontmatter form
- **AND** every omp-form agent file lives under `plugins/omp/`, is committed, and declares in its generated metadata the source path it came from
- **AND** `tools/build-plugins.py --check` reproduces every one of them byte-for-byte

#### Scenario: Source edit reaches every harness

- **WHEN** a prompt body in `<pillar>/agents/*.md` is edited
- **THEN** rebuilding the plugin trees carries the edited body into both the omp and the Claude agent files
- **AND** reinstalling for opencode carries it into the opencode deployment

#### Scenario: Editing the generated tree is caught

- **WHEN** a file under `plugins/omp/` is edited without editing its source
- **THEN** `tools/build-plugins.py --check` exits non-zero naming that path

### Requirement: Skill autoloading is opt-in

omp can inject named skill bodies into a subagent at start via `autoloadSkills`. Because opencode has no equivalent and binds skills by prose reference, the generated omp agent files SHALL leave `autoloadSkills` unset, so that every harness behaves alike. There is no flag to enable it: a prebuilt plugin is installed by the harness rather than by a user-invoked command, so there is no invocation to carry one.

The `(deep)` skill heading in each prompt SHALL nonetheless still be parsed on every build, and a heading that is missing or names no skills SHALL fail the build, because the one-line shape remains normative in the roster specifications.

#### Scenario: Generated agents declare no autoloading

- **WHEN** any agent is generated for the omp tree
- **THEN** the output frontmatter declares no `autoloadSkills`

#### Scenario: A broken deep heading still fails the build

- **WHEN** an agent prompt's `(deep)` heading is followed by a blank line, or is absent
- **THEN** the generator exits non-zero naming that source file

### Requirement: Ownership evidence is defined once for install and uninstall

The evidence that this repository deployed a given artifact SHALL be defined in exactly one place, sourced by both `install.sh` and `uninstall.sh`, because a destination the uninstaller declines to remove is by definition a destination the installer must decline to overwrite. The evidence SHALL be: a symlink resolving inside this repository, a copied file byte-identical to its source, or a copied skill whose `SKILL.md` is byte-identical to its source's.

The translated-agent branch is gone. It existed because `install.sh` deployed generated omp agents, which differ from their source by construction and so could only be recognised by the provenance line naming that source. No opencode deployment is ever a translated file — the plugin trees are the only generated form, and the harnesses' own plugin machinery installs them — so byte-identity is now the whole agent test.

#### Scenario: Both scripts consult the same definition

- **WHEN** `install.sh` and `uninstall.sh` are inspected
- **THEN** neither defines its own ownership test
- **AND** both obtain it from a single shared shell file under `tools/`

#### Scenario: Shared file is not a distributable artifact

- **WHEN** `./install.sh` runs with pillars auto-discovered
- **THEN** the shared ownership file is not deployed to any harness root

#### Scenario: A generated agent is not recognised by provenance

- **WHEN** a file carrying a generated provenance line occupies an opencode agent destination but is not byte-identical to its source
- **THEN** `install.sh` refuses to overwrite it and `uninstall.sh` declines to remove it

### Requirement: Installation is idempotent and inspectable

`install.sh` SHALL support repeated invocation without accumulating state, and SHALL support previewing an invocation without touching the filesystem. Because it now serves opencode alone, the guarantee is stated for one destination rather than for a harness selector.

The dry run no longer exercises a translator: nothing is translated at install time, so a dry run's fidelity is the destination list it prints, not a parse it performs. Translation failures surface at build time instead, where `tools/build-plugins.py` fails the build.

#### Scenario: Re-running changes nothing

- **WHEN** `./install.sh` runs twice in succession
- **THEN** the second run leaves the same set of deployed files as the first

#### Scenario: Dry run writes nothing

- **WHEN** `./install.sh --dry-run` runs
- **THEN** the intended actions are printed
- **AND** no file is created, removed, or modified anywhere on disk

#### Scenario: The dry run names only opencode destinations

- **WHEN** `./install.sh --dry-run` runs
- **THEN** every destination printed lies under the opencode root or the command target
- **AND** no path under `~/.omp/` is named

### Requirement: Installation refuses to overwrite an artifact it does not own

`install.sh` SHALL, before removing or replacing any destination path, require ownership evidence for that path, and SHALL exit non-zero naming the path when the evidence is absent, because the opencode root is a flat namespace shared with the harness's built-ins and with the user's own artifacts.

A destination deployed by a previous run SHALL still test as owned after its source is edited, on the strength of the symlink resolving into this repository or of byte-identity in copy mode. The generated-provenance route to ownership is gone with the translated agents it existed for.

#### Scenario: Foreign agent file of the same name is refused

- **WHEN** an agent file this repository did not deploy already occupies a destination agent path
- **AND** `./install.sh` runs for the pillar containing that name
- **THEN** the run exits non-zero naming the path
- **AND** the foreign file is left byte-for-byte unchanged

#### Scenario: A refused run deploys nothing at all

- **WHEN** a foreign artifact occupies one destination path among many
- **AND** `./install.sh` runs for the pillar containing that name
- **THEN** every destination is checked before any file is written
- **AND** no artifact of any pillar is deployed, including those whose destinations were free

#### Scenario: A previous deployment is owned and is replaced

- **WHEN** `./install.sh` runs twice in succession in any mode
- **THEN** the second run replaces its own artifacts without error
- **AND** the deployed set is the same as after the first run

#### Scenario: Dry run detects the collision

- **WHEN** a foreign artifact occupies a destination path
- **AND** `./install.sh --dry-run` runs
- **THEN** the run exits non-zero
- **AND** no file is created, removed, or modified anywhere on disk
