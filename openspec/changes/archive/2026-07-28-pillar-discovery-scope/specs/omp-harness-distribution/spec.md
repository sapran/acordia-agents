## ADDED Requirements

### Requirement: Pillar auto-discovery is limited to distributable directories

When no pillar is named explicitly, `install.sh` and `uninstall.sh` SHALL treat a top-level directory as a pillar only if it is not dot-prefixed and carries an `agents/` or `skills/` subdirectory. Dot-prefixed directories hold tooling configuration for this repository rather than distributable artifacts, and SHALL NOT be swept into a default install.

#### Scenario: Repository tooling is not published

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** the OpenSpec workflow skills under `.opencode/skills/` and `.claude/skills/` are not deployed
- **AND** no dot-prefixed directory contributes artifacts to the deployment

#### Scenario: Non-artifact directories are still skipped

- **WHEN** pillar auto-discovery runs
- **THEN** a visible top-level directory carrying neither `agents/` nor `skills/` is not treated as a pillar

#### Scenario: Analyst pillar is unaffected

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** every agent under `analysts/agents/` and every skill under `analysts/skills/` is deployed

#### Scenario: Explicit selection overrides the filter

- **WHEN** a dot-prefixed directory carrying artifacts is named with `--pillar`
- **THEN** its artifacts are deployed
- **AND** the same holds for `uninstall.sh`, so an already-published dot-directory pillar can still be removed
