## MODIFIED Requirements

### Requirement: One authored tree per pillar serves every harness

The plugin SHALL be a single authored directory at the repository root — `acordia-analysts/` —
containing `.claude-plugin/plugin.json`, `agents/`, `commands/`, `skills/` and `skill-sets.json`. The
same directory SHALL serve every target harness: there SHALL be no per-harness tree, no generated or
translated copy of any agent, skill or command, and no build step between the checkout and an install.

`skill-sets.json` declares each agent's skill set so a host can render a catalogue for one analyst
rather than for the whole library. It ships inside the pillar rather than beside it in `docs/`
precisely because its consumer is the host that installed the pillar, and it is hand-maintained like
the catalogs: nothing emits it, and a script that did would be the generated tree this requirement
forbids. It carries no version, so the three-occurrence version count is unaffected by its presence.

An install SHALL be one of exactly two routes into that one directory, and both SHALL read the
authored files rather than a copy of them. The marketplace route resolves the catalog and copies the
plugin directory, and is the documented default for both harnesses. The script route, specified below,
symlinks the pillar's agents and skills into omp's native roots, and exists only because a marketplace
install is inert when the `claude-plugins` discovery provider is disabled. Neither route SHALL generate,
translate or restructure an artifact, so the one-tree guarantee holds under both: what a user receives
is the authored file, reached either by copy of the authored directory or by symlink to it.

#### Scenario: Plugin layout is the authored layout

- **WHEN** a plugin directory is inspected
- **THEN** it contains `.claude-plugin/plugin.json`, `agents/`, `commands/`, `skills/` and `skill-sets.json`, and nothing declares itself generated

#### Scenario: No second tree exists

- **WHEN** the repository is searched for a per-harness plugin tree or a generator that would emit one
- **THEN** none is found

#### Scenario: One tree loads in both harnesses

- **WHEN** the same plugin directory is installed in omp and in Claude Code
- **THEN** both discover the pillar's agents, commands and skills from it

#### Scenario: Both install routes read the authored files

- **WHEN** the marketplace route and the script route are compared
- **THEN** each resolves to files inside `acordia-analysts/`, and neither produces a generated or translated artifact

#### Scenario: The declaration does not join the version count

- **WHEN** the repository's version occurrences are counted
- **THEN** there are exactly three, across `plugin.json` and the two catalogs, and `skill-sets.json` carries none
