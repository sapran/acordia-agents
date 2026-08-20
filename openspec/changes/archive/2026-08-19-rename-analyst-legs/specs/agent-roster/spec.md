# agent-roster

## MODIFIED Requirements

### Requirement: Nine agents, two pillars, one authored file each

The distribution SHALL ship exactly nine agent files, four under `acordia-analysts/agents/` and five
under `acordia-operators/agents/`, each the single editable source for every harness. The analyst
files SHALL be `cyber-analyst.md`, `target-analyst.md`,
`overwatch-analyst.md`, `fusion-analyst.md`; the operations files SHALL be `cyber-operator.md`,
`web-application.md`, `mobile-application.md`, `cloud-security.md`, `internal-network.md`. Filename
stem SHALL equal frontmatter `name`. No generated or translated copy of an agent SHALL exist in the
repository.

#### Scenario: Roster is complete and named
- **WHEN** the two pillar `agents/` directories are enumerated
- **THEN** exactly those nine files are present, and each filename stem equals its frontmatter `name`

#### Scenario: No second copy of an agent exists
- **WHEN** the repository is searched for agent files carrying an ACORDIA description
- **THEN** the only matches are those nine files

## ADDED Requirements

### Requirement: A leg agent is named for the question it answers

Each analyst leg SHALL be named for the work its prompt leads with, not for the competency-grid
column it was derived from. The legs SHALL be `target-analyst`, `overwatch-analyst` and
`fusion-analyst`. A leg name SHALL NOT carry a term that describes only the secondary half of its
prompt, and SHALL NOT stack two near-synonyms.

The competency grid in `docs/roles/operational-analyst.md` SHALL keep its column letters **T&N**,
**Def** and **Fus**. A column labels a leg of the role that document describes; it does not name the
agent file that implements the leg. The mapping between the two SHALL be recorded in that document,
appended after the grid so that no skill anchor shifts.

Short command aliases SHALL survive a leg rename under their existing filenames, so that an
invocation that worked before the rename still resolves.

#### Scenario: No leg is named after a grid column
- **WHEN** the analyst `agents/` directory is enumerated
- **THEN** no filename contains `network` or `detection`, and each name states the leg's own question

#### Scenario: Old leg names are gone from the live tree
- **WHEN** the live tree is searched for `target-network-analyst` or `defender-detection-analyst`
- **THEN** no match is found outside `openspec/changes/archive/`

#### Scenario: Short alias still resolves after a rename
- **WHEN** `/target` or `/defender` is invoked
- **THEN** the wrapper names the renamed agent, and the alias filename is unchanged
