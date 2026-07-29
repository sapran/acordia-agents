## ADDED Requirements

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
