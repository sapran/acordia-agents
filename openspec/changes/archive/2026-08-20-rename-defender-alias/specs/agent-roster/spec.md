# agent-roster

## MODIFIED Requirements

### Requirement: A leg agent is named for the question it answers

Each analyst leg SHALL be named for the work its prompt leads with, not for the competency-grid
column it was derived from. The legs SHALL be `target-analyst`, `overwatch-analyst` and
`fusion-analyst`. A leg name SHALL NOT carry a term that describes only the secondary half of its
prompt, and SHALL NOT stack two near-synonyms.

The competency grid in `docs/roles/operational-analyst.md` SHALL keep its column letters **T&N**,
**Def** and **Fus**. A column labels a leg of the role that document describes; it does not name the
agent file that implements the leg. The mapping between the two SHALL be recorded in that document,
appended after the grid so that no skill anchor shifts.

A short alias SHALL be formed from its own agent's name — a word of that name, or a legible
contraction of it. An alias SHALL NOT outlive the name it was formed from: when an agent is renamed
and its alias no longer derives from the new name, the alias SHALL be renamed with it rather than
retained as a handle for vocabulary the roster has dropped.

#### Scenario: No leg is named after a grid column
- **WHEN** the analyst `agents/` directory is enumerated
- **THEN** no filename contains `network` or `detection`, and each name states the leg's own question

#### Scenario: Old leg names are gone from the live tree
- **WHEN** the live tree is searched for `target-network-analyst` or `defender-detection-analyst`
- **THEN** no match is found outside `openspec/changes/archive/`

#### Scenario: Every alias derives from its own agent
- **WHEN** the nine short aliases are compared with the agents they dispatch
- **THEN** each alias is a word of its agent's name or a legible contraction of it, and none names a
  term absent from that agent's name
