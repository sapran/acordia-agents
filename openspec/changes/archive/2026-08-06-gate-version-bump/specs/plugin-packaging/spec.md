## MODIFIED Requirements

### Requirement: The plugin version is hand-maintained and bumped on every change

The catalogs and plugin manifests SHALL carry a hand-maintained `MAJOR.MINOR.PATCH` version, declared once in the generator, and it SHALL be bumped by whoever changes a source artifact. MINOR SHALL move for any change that reaches a user — an agent prompt, a skill body, a command wrapper, or the generator's emitted output. MAJOR SHALL move for a change to the roster, to a pillar, or to the shape of the distribution.

The version is the only update signal either plugin harness has. omp compares the catalog version against the installed one and skips when they match, so an unbumped version means an edited artifact never reaches an already-installed user, and it fails silently — no error and no warning distinguishes it from being up to date. The obligation to bump therefore SHALL be stated as a rule in the repository's own contributor guidance, not left implicit in the generator.

The version SHALL be real semantic versioning and SHALL increase monotonically, because a hand-maintained version can be ordered and both harnesses then compare it by precedence. Verified against omp 17.1.8: a newer semver reinstalls and an older one is skipped.

The version SHALL NOT be derived from source content or from a git revision, and SHALL NOT carry semver build metadata. Two versions differing only in build metadata compare **equal** and never upgrade, so a `MAJOR.MINOR.PATCH+<hash>` form would be a silent no-op — accepted by both harnesses and propagating to neither.

A targeted upgrade naming one plugin reinstalls unconditionally and compares nothing. It SHALL NOT be used as evidence of version semantics.

The obligation SHALL additionally be gate-checked, because stating it in contributor guidance did not prevent a source artifact from being committed without a bump. `tools/build-plugins.py --check` SHALL compare the working tree against a git base and SHALL exit non-zero when any tracked file under `analysts/`, `operators/`, or `commands/acordia/` differs from that base while the declared version does not exceed the base's version, compared as a semver tuple.

The base SHALL be the merge base with the integration branch, so the obligation is one bump per release rather than one per commit; a branch that bumps once and then edits further sources SHALL pass. When git is unavailable, the tree is not a git checkout, or no base branch resolves, the check SHALL report that the version gate was skipped and SHALL NOT fail — an unresolvable base is not evidence of a missing bump.

The gate SHALL apply to `--check` only and SHALL NOT apply to a plain build, because a plain build runs continuously while editing and failing it on an unbumped version would make the generator unusable for its primary purpose.

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

#### Scenario: A source change with no bump fails the check

- **WHEN** a tracked file under `analysts/`, `operators/`, or `commands/acordia/` differs from the base and the declared version equals the base's version
- **THEN** `tools/build-plugins.py --check` exits non-zero naming the changed source paths and both versions

#### Scenario: A source change with a bump passes

- **WHEN** source artifacts differ from the base and the declared version is strictly greater than the base's version
- **THEN** the version gate passes and `--check` reports only whatever generated-tree drift it finds independently

#### Scenario: One bump covers a whole branch

- **WHEN** a branch has already bumped the version above the base and then changes further source artifacts without bumping again
- **THEN** the version gate passes, because the obligation is one bump per release rather than one per commit

#### Scenario: A change touching no source artifact needs no bump

- **WHEN** the only differences from the base lie outside `analysts/`, `operators/`, and `commands/acordia/` — documentation or planning artifacts, for example
- **THEN** the version gate passes with the version unchanged

#### Scenario: An unresolvable base skips rather than fails

- **WHEN** git is unavailable, the tree is not a git checkout, or no integration branch resolves
- **THEN** `--check` reports that the version gate was skipped
- **AND** the absence of a base does not by itself fail the check

#### Scenario: A plain build is never blocked by the version gate

- **WHEN** source artifacts have changed with no version bump and `tools/build-plugins.py` runs without `--check`
- **THEN** the build succeeds, because the gate is scoped to the check path
