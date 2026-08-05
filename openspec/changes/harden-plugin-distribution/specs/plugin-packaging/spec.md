## ADDED Requirements

### Requirement: The plugin version is hand-maintained and bumped on every change

The catalogs and plugin manifests SHALL carry a hand-maintained `MAJOR.MINOR.PATCH` version, declared once in the generator, and it SHALL be bumped by whoever changes a source artifact. MINOR SHALL move for any change that reaches a user — an agent prompt, a skill body, a command wrapper, or the generator's emitted output. MAJOR SHALL move for a change to the roster, to a pillar, or to the shape of the distribution.

The version is the only update signal either plugin harness has. omp compares the catalog version against the installed one and skips when they match, so an unbumped version means an edited artifact never reaches an already-installed user, and it fails silently — no error and no warning distinguishes it from being up to date. The obligation to bump therefore SHALL be stated as a rule in the repository's own contributor guidance, not left implicit in the generator.

The version SHALL be real semantic versioning and SHALL increase monotonically, because a hand-maintained version can be ordered and both harnesses then compare it by precedence. Verified against omp 17.1.8: a newer semver reinstalls and an older one is skipped.

The version SHALL NOT be derived from source content or from a git revision, and SHALL NOT carry semver build metadata. Two versions differing only in build metadata compare **equal** and never upgrade, so a `MAJOR.MINOR.PATCH+<hash>` form would be a silent no-op — accepted by both harnesses and propagating to neither.

A targeted upgrade naming one plugin reinstalls unconditionally and compares nothing. It SHALL NOT be used as evidence of version semantics.

#### Scenario: A newer version propagates

- **WHEN** the catalog version is bumped above the installed version
- **AND** the upgrade-all path runs
- **THEN** the plugin is reinstalled at the new version

#### Scenario: An unchanged version is a no-op

- **WHEN** the catalog version equals the installed version
- **AND** the upgrade-all path runs
- **THEN** nothing is reinstalled

#### Scenario: The bump obligation is written down

- **WHEN** the repository's contributor guidance is read
- **THEN** it states that a source change without a version bump is a release bug
- **AND** it gives the MINOR and MAJOR criteria

#### Scenario: Build-metadata versioning is rejected as a design

- **WHEN** the version scheme is inspected
- **THEN** it carries no hash and no build metadata
- **AND** the reason is recorded, because that form is accepted by both harnesses yet never upgrades

### Requirement: Agent-name resolution differs by harness and is documented

A plugin agent's dispatch handle SHALL be documented per harness, because the harnesses disagree and a single documented form would be wrong for one of them. Verified against Claude Code 2.1.220: plugin agents are namespaced there, so the dispatch name is `<plugin>:<agent>` and the bare agent name fails as an unrecognised type. omp and opencode register agents flat, by bare name.

The command wrappers SHALL remain the portable entry point, naming their agent in prose so each harness resolves it in its own idiom.

#### Scenario: Claude Code requires the namespaced handle

- **WHEN** a plugin agent is dispatched in Claude Code by its bare name
- **THEN** the dispatch fails as an unrecognised agent type
- **AND** the same dispatch succeeds as `<plugin>:<agent>`

#### Scenario: Documentation states both forms

- **WHEN** the install documentation is read
- **THEN** it states the namespaced form for Claude Code and the bare form for omp and opencode
