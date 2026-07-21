## ADDED Requirements

### Requirement: Four analyst agents mirroring the role model

The roster SHALL contain exactly four agent files under `~/.config/opencode/agents/`: `operational-analyst.md`, `target-network-analyst.md`, `defender-detection-analyst.md`, and `fusion-analyst.md` — one general role plus the three specialisations named in `docs/roles/operational-analyst.md`.

#### Scenario: Roster is complete and named
- **WHEN** opencode lists agents
- **THEN** exactly those four appear (filename = agent name)

### Requirement: Primary orchestrator, subagent legs

`operational-analyst` SHALL be `mode: primary` and act as the senior orchestrator that dispatches the specialists. The three leg agents SHALL be `mode: subagent`.

#### Scenario: Modes assigned per role
- **WHEN** the four agents are loaded
- **THEN** `operational-analyst` is `primary` and the three legs are `subagent`

#### Scenario: Orchestrator dispatches a leg
- **WHEN** the primary needs a deep technical read for a specialist question
- **THEN** it can dispatch the matching leg subagent

### Requirement: Dispatch descriptions are the role doc's leg questions

Each subagent's `description` SHALL be the italic operating question of its leg from `docs/roles/operational-analyst.md`, because a subagent's `description` is its routing signal.

#### Scenario: Description matches the leg question
- **WHEN** `target-network-analyst` is inspected
- **THEN** its `description` conveys "what is the target for, what does it depend on, where can we move, when will it change — and did our action land on it?"

### Requirement: Portable prompt bodies

Each agent's prompt body SHALL be authored from the corresponding prose in the role doc (the spine paragraph for the primary; the leg paragraphs for the specialists).

#### Scenario: Body traces to the role doc
- **WHEN** an agent body is compared to its source paragraph in `docs/roles/operational-analyst.md`
- **THEN** the body conveys that paragraph's content

### Requirement: Read-only file access via `edit: deny`

opencode's permission default is **allow**, and the `edit` permission governs the edit, write, and patch tools collectively (there is no separate `write` key; a top-level `"*": deny` is accepted but overridden by per-tool built-in defaults, so it does not produce a deny-default). Every analyst agent SHALL therefore set `edit: deny`, so no analyst can modify files with the built-in tools. Analysis capability (read, grep, glob, bash, webfetch, websearch, skill) remains allowed by opencode's default. Each leg subagent SHALL additionally set `task: deny` (leaf specialist — does not dispatch).

#### Scenario: File modification denied
- **WHEN** an analyst agent attempts to edit, write, or patch a file
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: Analysis allowed by default
- **WHEN** an analyst agent reads a file or fetches a web resource
- **THEN** the action is allowed (opencode default)

#### Scenario: Legs do not dispatch
- **WHEN** a leg subagent is inspected
- **THEN** its resolved `task` permission is `deny`

### Requirement: Prompt names the skill set from the grid column

Because opencode has no per-agent `skills:` field, each agent's **prompt** SHALL name the set of skills it draws on — exactly the skills marked (● deep or ○ working) in that agent's grid column (Core for the primary, T&N/Def/Fus for the legs).

#### Scenario: Column marks become the named set
- **WHEN** a skill row carries a mark in the `Def` column
- **THEN** that skill name appears in `defender-detection-analyst`'s prompt skill set

### Requirement: Shared spine named in all four agents

The analytic-spine skills (the `Core ●` rows) SHALL be named in the prompt of all four agents, realising the shared spine by prompt reference (there is no inheritance and no `skills:` binding).

#### Scenario: Spine present everywhere
- **WHEN** any of the four agents is inspected
- **THEN** every `Core ●` spine skill is named in its prompt skill set
