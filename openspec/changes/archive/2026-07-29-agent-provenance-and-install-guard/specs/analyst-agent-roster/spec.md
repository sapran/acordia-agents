## MODIFIED Requirements

### Requirement: Dispatch descriptions are the role doc's leg questions

Each subagent's `description` SHALL be the italic operating question of its leg from `docs/roles/operational-analyst.md`, because a subagent's `description` is its routing signal. Each agent's `description` SHALL additionally open with the pillar provenance tag `ACORDIA Analysis — `, ahead of the routing sentence and without altering it, because a harness renders the description beside a bare slug in a namespace shared with its own built-in agents, and the user needs to see which agents this distribution supplied.

#### Scenario: Description matches the leg question
- **WHEN** `target-network-analyst` is inspected
- **THEN** its `description` conveys "what is the target for, what does it depend on, where can we move, when will it change — and did our action land on it?"

#### Scenario: Description carries the pillar tag
- **WHEN** any agent under `analysts/agents/` is inspected
- **THEN** its `description` begins with `ACORDIA Analysis — `
- **AND** the routing sentence following the tag is unchanged in meaning

#### Scenario: Provenance is carried by the description, not the name
- **WHEN** the agent files, the orchestrator's `task` whitelist, and the skill slugs are inspected
- **THEN** no agent filename, agent name, or skill slug carries a distribution prefix
