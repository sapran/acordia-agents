## ADDED Requirements

### Requirement: The repository root is a plugin marketplace with one pillar

The repository SHALL publish itself as a marketplace named `acordia` carrying exactly one plugin,
`acordia-analysts`. There SHALL be no second plugin entry, no second authored tree, and no catalog
`source` pointing anywhere but `./acordia-analysts`.

This requirement replaces *The repository root is a plugin marketplace with two pillars*, which this
delta removes rather than modifies. A `## MODIFIED Requirements` block matches an existing requirement
by its title, so it cannot carry a retitle: the old title asserts the very thing this change deletes,
and leaving it in place while rewriting its body would leave the published spec claiming two pillars in
its own heading. Removing the false title and adding the true one is the honest form.

An installed user of the retired `acordia-operators` plugin SHALL be told to uninstall it. Its final
published version is 4.2.0; because its catalog entry no longer exists, the upgrade path cannot remove
it and it will remain installed and dispatchable at that version until the user removes it by hand. A
harness that cannot resolve an installed plugin's entry does not uninstall it.

#### Scenario: One plugin is offered

- **WHEN** either marketplace catalog is read
- **THEN** it lists exactly one plugin entry, `acordia-analysts`
- **AND** that entry carries its own `source`, `version`, `description`, `category` and `keywords`

#### Scenario: The analysis pillar is the whole distribution

- **WHEN** `acordia-analysts@acordia` is installed
- **THEN** the five analyst agents, the analyst skill library and the ten analyst command wrappers are available
- **AND** nothing else is installed, because nothing else is published

#### Scenario: The operations pillar is gone from the live tree

- **WHEN** the live tree, both catalogs and both manifests are searched for `acordia-operators`
- **THEN** no match is found, and no `acordia-operators/` directory exists

#### Scenario: A stranded install is called out, not silently upgraded

- **WHEN** the change's release note is read by a user who has `acordia-operators` installed
- **THEN** it tells them to uninstall it, and states that no upgrade will do it for them

## MODIFIED Requirements

### Requirement: One authored tree per pillar serves every harness

The plugin SHALL be a single authored directory at the repository root — `acordia-analysts/` —
containing `.claude-plugin/plugin.json`, `agents/`, `commands/` and `skills/`. The same directory
SHALL serve every target harness: there SHALL be no per-harness tree, no generated or translated copy
of any agent, skill or command, and no build step between the checkout and an install. A harness
install SHALL therefore consist of resolving the catalog and copying the plugin directory.

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
the latter. Both SHALL point at the same single source, `./acordia-analysts`, and SHALL therefore be
byte-identical. Each SHALL carry only keys both catalog schemas document — `name`, `owner`,
`metadata`, and per entry `name`, `source`, `version`, `description`, `category`, `keywords` —
because a harness that considers an entry invalid logs and skips it, so a speculative field risks
silently dropping a plugin. Both files are authored by hand; no tool generates or checks them.

Dropping to one entry SHALL NOT collapse the pair into one file. Two harnesses still read two
filenames, and the reason both exist is unchanged by how many plugins each lists.

#### Scenario: Catalogs are identical

- **WHEN** the two catalogs are compared
- **THEN** every byte is equal, and both name `./acordia-analysts` as their only source

#### Scenario: Catalog parses and resolves

- **WHEN** a harness resolves the marketplace from a fresh clone
- **THEN** both catalog files parse as JSON and each `source` path exists in the checkout

#### Scenario: Drift between the two is visible by inspection

- **WHEN** one catalog is edited and the other is not
- **THEN** the two files differ, and a diff of the pair shows it — there is no gate, and the pair is short enough to compare by eye

#### Scenario: Both filenames survive the collapse to one plugin

- **WHEN** the repository root is inspected after the operations pillar is removed
- **THEN** both `.omp-plugin/marketplace.json` and `.claude-plugin/marketplace.json` are still present

### Requirement: Each pillar carries its own manifest

The plugin directory SHALL carry `.claude-plugin/plugin.json` naming the plugin, its version,
description, author, repository and keywords. The manifest SHALL declare no `commands`, `agents` or
`skills` path key, because the default locations are exactly the ones the tree uses. Exactly one such
manifest SHALL exist in the repository.

#### Scenario: Manifest present and minimal

- **WHEN** a plugin directory is inspected
- **THEN** `.claude-plugin/plugin.json` parses, names the plugin and its version, and declares no path-remapping key

#### Scenario: Manifest name matches the directory

- **WHEN** the manifest's `name` is compared with its directory name
- **THEN** they are identical

#### Scenario: Only one manifest exists

- **WHEN** the repository is searched for `*/.claude-plugin/plugin.json`
- **THEN** the only match is `acordia-analysts/.claude-plugin/plugin.json`

### Requirement: The version is hand-maintained, semver, and bumped on every user-visible change

The one manifest and the one entry in each of the two catalogs SHALL carry the same
`MAJOR.MINOR.PATCH` version — three occurrences across three JSON files — and it SHALL be bumped by
whoever changes an artifact a user receives: an agent prompt, a skill body, a command wrapper, a
manifest or a catalog. MINOR SHALL move for any such change; MAJOR SHALL move for a change to the
roster, to a pillar, or to the shape of the distribution, including a change to an install source
path.

Removing a pillar is the clearest MAJOR case there is: it deletes agents, skills and commands a user
already has. This change SHALL therefore release 4.2.0 → 5.0.0.

The version is the only update signal either harness has: a harness compares the catalog version
against the installed one and skips when they match, silently, so an unbumped version means an edited
artifact never reaches an already-installed user. The version SHALL be real semantic versioning,
SHALL increase monotonically, SHALL NOT be derived from source content or a git revision, and SHALL
NOT carry semver build metadata — two versions differing only in build metadata compare equal and
never upgrade.

The count of version occurrences is asserted outside this repository. The external drift check
`~/ai/checks/check-acordia.sh` requires the version to appear six times across four JSON files —
two `plugin.json` files and two entries in each of two catalogs — and fails when the total is anything
else. Dropping to three occurrences across three files makes that check fail on a correct tree, so
this change updates the script in lockstep with the deletion. This is an obligation on the change, not
a requirement this specification places on a file it does not ship.

The scenario below is still titled *All four version declarations agree* although only three now
exist. The title is retained deliberately: OpenSpec matches scenarios between a `## MODIFIED`
block and the published spec by title, reports any title it cannot find as a dropped scenario at
`ERROR` level, and refuses to archive the change. Retitling it to name three would therefore fail
validation for a spec that is otherwise correct. It SHALL be read as an identifier, not as a count,
and SHALL NOT be renamed except in a change that also removes the published title.

#### Scenario: All four version declarations agree

- **WHEN** every JSON file in the repository that declares a plugin version is read
- **THEN** there are three such declarations rather than four, the fourth having been deleted with the operations manifest, and all three carry the same version string

#### Scenario: No fourth declaration survives the deletion

- **WHEN** the repository is searched for a second `plugin.json` or a second catalog entry
- **THEN** neither exists, so three is the complete count and a check expecting four is stale

#### Scenario: Removing a pillar is released as MAJOR

- **WHEN** this change is released
- **THEN** the version moves 4.2.0 → 5.0.0 in all three places, because a pillar was deleted

#### Scenario: A newer version propagates

- **WHEN** the catalog version is bumped above the installed version and the upgrade path runs
- **THEN** the plugin is reinstalled at the new version

#### Scenario: An unchanged version is a silent no-op

- **WHEN** the catalog version equals the installed version and the upgrade path runs
- **THEN** nothing is reinstalled and no warning distinguishes that from being up to date

#### Scenario: The bump obligation is written down

- **WHEN** the repository's contributor guidance is read
- **THEN** it states that a user-visible change without a version bump is a release bug, and gives the MINOR and MAJOR criteria

#### Scenario: Build-metadata versioning is rejected

- **WHEN** the version scheme is inspected
- **THEN** it carries no hash and no build metadata

## REMOVED Requirements

### Requirement: The repository root is a plugin marketplace with two pillars

**Reason**: The operations pillar is deleted, so both the requirement and its own title are false; it is replaced by *The repository root is a plugin marketplace with one pillar* as a REMOVE-plus-ADD pair, because a MODIFIED block matches on title and cannot retitle a requirement.
