## ADDED Requirements

### Requirement: The plugin version derives from source content

The version SHALL be `<epoch>-<hash>`, where the epoch is a hand-kept `MAJOR.MINOR` bumped when the roster changes — an agent or pillar added or removed — and the hash is the leading hex characters of a sha256 over the content of the two pillars, `commands/acordia/`, and `tools/build-plugins.py`.

The generator SHALL be hashed alongside the sources, because a change to what it emits must reach installed users and hashing only the sources would not detect one.

The version SHALL NOT derive from a git revision. It is written into the committed catalogs and plugin manifests, so a revision-derived version would be invalidated by the very commit that lands the rebuild carrying it, and the drift check would fail on every push in perpetuity. Content hashing has no such fixpoint, and additionally succeeds where git cannot answer: a dirty working tree, a shallow clone, or an exported tree with no repository metadata.

The derivation SHALL be deterministic: inputs traversed in sorted order, hashing each file's repository-relative path as well as its bytes, so that renaming an artifact changes the version even when its content does not.

#### Scenario: Rebuilding twice is byte-identical

- **WHEN** the generator runs twice with no intervening source change
- **THEN** the emitted version is identical
- **AND** the drift check passes

#### Scenario: A source edit changes the version

- **WHEN** any file under a pillar or `commands/acordia/` is modified and the version is derived again
- **THEN** the hash differs from before the edit

#### Scenario: A generator edit changes the version

- **WHEN** `tools/build-plugins.py` is modified and the version is derived again
- **THEN** the hash differs from before the edit

#### Scenario: Landing a rebuild does not invalidate it

- **WHEN** a rebuild is committed and the generator runs again with no source change
- **THEN** the emitted version is unchanged
- **AND** the drift check passes

### Requirement: The version is deliberately not semantic versioning

The emitted version SHALL NOT be valid semver, because the harness that consumes it for upgrade detection compares non-semver versions by inequality and semver versions by precedence.

Verified against omp 17.1.8, on the upgrade-all path — the only path that compares versions at all: two unequal non-semver versions reinstall in either direction, so a content hash propagates regardless of hex ordering; two semver versions differing only in build metadata compare equal and never reinstall, so a `MAJOR.MINOR.PATCH+<hash>` form would be a silent no-op and strictly worse than a frozen version.

A targeted upgrade naming one plugin reinstalls unconditionally and compares nothing. It SHALL NOT be used as evidence of version semantics.

The consuming harnesses' acceptance of a non-semver string SHALL be recorded honestly: omp compares it as described, and Claude Code accepts and displays it, while Claude Code's own upgrade behaviour for such a string is unverified because a directory-sourced marketplace is read live there.

#### Scenario: Unequal hashes propagate

- **WHEN** the catalog version changes from one hash to a different hash
- **AND** the upgrade-all path runs
- **THEN** the plugin is reinstalled at the new version

#### Scenario: An unchanged version is a no-op

- **WHEN** the catalog version equals the installed version
- **AND** the upgrade-all path runs
- **THEN** nothing is reinstalled

#### Scenario: Build-metadata versioning is rejected as a design

- **WHEN** the version scheme is inspected
- **THEN** it does not emit a semver string carrying the hash as build metadata
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
