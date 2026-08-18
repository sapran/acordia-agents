## ADDED Requirements

### Requirement: Analyst agents carry the pillar and role anchor

Every analyst agent's `metadata.acordia` block SHALL declare `pillar: analysts` and `role` (`orchestrator` for the primary, `specialist` for the three legs), in addition to the grid anchors `column` and `source_paragraph`. The former `leg` key SHALL NOT be present: it carried an identity — `fusion`, `target-network` — that the filename already establishes, and the filename is the dispatch handle.

#### Scenario: The anchor is uniform across pillars

- **WHEN** an analyst agent and an operator agent are compared
- **THEN** both declare `pillar` and `role` under `metadata.acordia`, with no key that exists in only one pillar for the same purpose

## MODIFIED Requirements

### Requirement: Prompt names the skill set from the grid column

Because opencode has no per-agent `skills:` field, each agent's **prompt** SHALL name the set of skills it draws on — exactly the skills marked (● deep or ○ working) in that agent's grid column (Core for the primary, T&N/Def/Fus for the legs).

A prompt's skill lines MAY additionally name a procedural cross-cutting skill that corresponds to no grid row, where that skill is the agent's own declared method rather than a competency it exercises. The primary orchestrator SHALL name `analyst-loop` on its defining-spine line, first, because the spine skills the line goes on to name are steps inside that loop; naming the loop in prose alone left the one skill that defines the orchestrator's cycle as the only referenced skill in the file that was not list-declared. The three legs SHALL NOT name it: they are `task: deny` leaves and do not run the loop.

Every slug named on a skill line SHALL resolve to a skill in the agent's own pillar, which the generator enforces.

#### Scenario: Grid marks appear in the prompt

- **WHEN** a skill is marked ● or ○ in an agent's grid column
- **THEN** that skill's slug appears on one of that agent's skill lines

#### Scenario: The orchestrator declares its own loop

- **WHEN** `operational-analyst`'s defining-spine line is read
- **THEN** `analyst-loop` is its first slug

#### Scenario: A leg does not declare the loop

- **WHEN** any of the three leg prompts is read
- **THEN** `analyst-loop` does not appear on its skill lines

#### Scenario: Column marks become the named set
- **WHEN** a skill row carries a mark in the `Def` column
- **THEN** that skill name appears in `defender-detection-analyst`'s prompt skill set
