# plugin-distribution Specification

## Purpose

Defines how the distribution reaches a harness: the repository root is a plugin marketplace carrying
two independently installable pillars, each an authored plugin directory with its own manifest, and
the hand-maintained version that is the only upgrade signal either harness has.

## Requirements

### Requirement: The repository root is a plugin marketplace with two pillars

The repository SHALL publish itself as a marketplace named `acordia` carrying exactly two plugins,
`acordia-analysts` and `acordia-operators`, one per pillar. The two SHALL be independently
installable: installing the analytic library SHALL NOT install the offensive one.

#### Scenario: Both plugins are offered separately

- **WHEN** either marketplace catalog is read
- **THEN** it lists exactly the two plugin entries `acordia-analysts` and `acordia-operators`
- **AND** each entry carries its own `source`, `version`, `description`, `category` and `keywords`

#### Scenario: The analysis pillar installs alone

- **WHEN** `acordia-analysts@acordia` is installed and `acordia-operators@acordia` is not
- **THEN** the four analyst agents, the analyst skill library and the eight analyst command wrappers are available
- **AND** no operations agent, skill or command wrapper is installed

### Requirement: One authored tree per pillar serves every harness

Each plugin SHALL be a single authored directory at the repository root —
`acordia-analysts/` and `acordia-operators/` — containing `.claude-plugin/plugin.json`, `agents/`,
`commands/` and `skills/`. The same directory SHALL serve every target harness: there SHALL be no
per-harness tree, no generated or translated copy of any agent, skill or command, and no build step
between the checkout and an install. A harness install SHALL therefore consist of resolving the
catalog and copying the plugin directory.

#### Scenario: Plugin layout is the authored layout

- **WHEN** a plugin directory is inspected
- **THEN** it contains `.claude-plugin/plugin.json`, `agents/`, `commands/` and `skills/`, and nothing declares itself generated

#### Scenario: No second tree exists

- **WHEN** the repository is searched for a per-harness plugin tree or a generator that would emit one
- **THEN** none is found

#### Scenario: One tree loads in both harnesses

- **WHEN** the same plugin directory is installed in omp and in Claude Code
- **THEN** both discover the pillar's agents, commands and skills from it

### Requirement: Two marketplace catalogs, hand-maintained and identical

The repository root SHALL carry both `.omp-plugin/marketplace.json` and
`.claude-plugin/marketplace.json`, because omp reads the former in preference and Claude Code reads
the latter. Both SHALL point at the same two sources, `./acordia-analysts` and
`./acordia-operators`, and SHALL therefore be byte-identical. Each SHALL carry only keys both catalog
schemas document — `name`, `owner`, `metadata`, and per entry `name`, `source`, `version`,
`description`, `category`, `keywords` — because a harness that considers an entry invalid logs and
skips it, so a speculative field risks silently dropping a plugin. Both files are authored by hand;
no tool generates or checks them.

#### Scenario: Catalogs are identical

- **WHEN** the two catalogs are compared
- **THEN** every byte is equal, and both name `./acordia-analysts` and `./acordia-operators` as sources

#### Scenario: Catalog parses and resolves

- **WHEN** a harness resolves the marketplace from a fresh clone
- **THEN** both catalog files parse as JSON and each `source` path exists in the checkout

#### Scenario: Drift between the two is visible by inspection

- **WHEN** one catalog is edited and the other is not
- **THEN** the two files differ, and a diff of the pair shows it — there is no gate, and the pair is short enough to compare by eye

### Requirement: Each pillar carries its own manifest

Each plugin directory SHALL carry `.claude-plugin/plugin.json` naming the plugin, its version,
description, author, repository and keywords. The manifest SHALL declare no `commands`, `agents` or
`skills` path key, because the default locations are exactly the ones the tree uses.

#### Scenario: Manifest present and minimal

- **WHEN** a plugin directory is inspected
- **THEN** `.claude-plugin/plugin.json` parses, names the plugin and its version, and declares no path-remapping key

#### Scenario: Manifest name matches the directory

- **WHEN** the manifest's `name` is compared with its directory name
- **THEN** they are identical

### Requirement: The version is hand-maintained, semver, and bumped on every user-visible change

The two catalogs and the two manifests SHALL carry the same `MAJOR.MINOR.PATCH` version, and it SHALL
be bumped by whoever changes an artifact a user receives — an agent prompt, a skill body, a command
wrapper, a manifest or a catalog. MINOR SHALL move for any such change; MAJOR SHALL move for a change
to the roster, to a pillar, or to the shape of the distribution, including a change to an install
source path.

The version is the only update signal either harness has: a harness compares the catalog version
against the installed one and skips when they match, silently, so an unbumped version means an edited
artifact never reaches an already-installed user. The version SHALL be real semantic versioning,
SHALL increase monotonically, SHALL NOT be derived from source content or a git revision, and SHALL
NOT carry semver build metadata — two versions differing only in build metadata compare equal and
never upgrade.

#### Scenario: All four version declarations agree

- **WHEN** the two catalogs and the two manifests are read
- **THEN** all four declare the same version string

#### Scenario: A newer version propagates

- **WHEN** the catalog version is bumped above the installed version and the upgrade path runs
- **THEN** both plugins are reinstalled at the new version

#### Scenario: An unchanged version is a silent no-op

- **WHEN** the catalog version equals the installed version and the upgrade path runs
- **THEN** nothing is reinstalled and no warning distinguishes that from being up to date

#### Scenario: The bump obligation is written down

- **WHEN** the repository's contributor guidance is read
- **THEN** it states that a user-visible change without a version bump is a release bug, and gives the MINOR and MAJOR criteria

#### Scenario: Build-metadata versioning is rejected

- **WHEN** the version scheme is inspected
- **THEN** it carries no hash and no build metadata

### Requirement: Changing the install source path is a major version

Moving the directory a catalog `source` points at SHALL be a MAJOR bump, and the change SHALL state
that an installed user must re-resolve the marketplace before upgrading, because a catalog entry whose
source no longer exists fails to install rather than upgrading in place.

#### Scenario: Source move is released as major

- **WHEN** a release moves a plugin's `source` path
- **THEN** its MAJOR component increases and the change records the re-resolve step users must run

### Requirement: A committed lint policy governs the authored markdown

The repository SHALL carry a `.markdownlint-cli2.jsonc` at its root declaring which markdownlint rules
apply to its own markdown and which paths are out of scope. Applying it to every file it does not
exclude SHALL report zero violations.

The file SHALL be `.markdownlint-cli2.jsonc` and exclusions SHALL live in its `ignores` array. A
`.markdownlintignore` SHALL NOT be used: neither markdownlint-cli2 nor the
`DavidAnson.vscode-markdownlint` extension reads that filename — only the legacy markdownlint-cli v1
does, and nothing here invokes it — so exclusions placed there are silently inert.

A rule this repository violates by intent SHALL be disabled with its reason recorded beside it, rather
than left firing. An editor reporting thousands of violations teaches its reader to ignore the report,
which costs more than the rules were worth: the failure this guards against is an author correcting
what the editor flagged and disturbing a convention the editor knew nothing about.

`openspec/changes/` SHALL be excluded. OpenSpec mandates that a delta spec opens with
`## ADDED Requirements` or `## MODIFIED Requirements`, which can never satisfy a first-line-heading
rule, and archived changes are immutable by contract so a violation there could not be fixed anyway. Vendored tooling under `.claude/` and `.codex/` SHALL be excluded, because it is not
part of the distribution and its upstream owns its formatting.

Because the rule set grows between markdownlint releases, the policy SHALL record the version it was
verified against, and a change that adopts a newer version SHALL re-verify the zero.

The policy SHALL NOT be enforced by a build step or a hook. This repository ships no build, and a lint
gate would be the first. It is an authoring convention.

An automated fix SHALL NOT be trusted without inspecting every line it changed. Verified 2026-08-21:
markdownlint's own `--fix` read the JavaScript property `__proto__` in `attack-prototype-pollution` as
strong emphasis and rewrote it to `**proto**`, destroying the literal payload the skill exists to
document. Emphasis-normalising rules are unsafe next to identifiers that carry underscores.

#### Scenario: The committed tree is clean under its own policy

- **WHEN** the rule set in `.markdownlint-cli2.jsonc` is applied to every file its `ignores` array does not exclude
- **THEN** no violation is reported

#### Scenario: A disabled rule carries its reason

- **WHEN** `.markdownlint-cli2.jsonc` disables a rule
- **THEN** a comment beside it records why this repository violates that rule by intent

#### Scenario: Exclusions live where a tool will read them

- **WHEN** the repository is searched for a `.markdownlintignore`
- **THEN** none exists, and the exclusions are in the `ignores` array of `.markdownlint-cli2.jsonc`

#### Scenario: OpenSpec changes and vendored tooling are out of scope

- **WHEN** the `ignores` array is read
- **THEN** it excludes `openspec/changes/`, `.claude/` and `.codex/`

#### Scenario: The verified tool version is recorded

- **WHEN** the lint policy is read
- **THEN** it names the markdownlint version its zero was verified against

#### Scenario: No gate is introduced

- **WHEN** the repository is searched for a lint invocation in a build script, hook or workflow
- **THEN** none exists
