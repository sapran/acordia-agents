# analyst-agent-roster Specification

## Purpose
Defines the four opencode analyst agents derived from the role model in `docs/roles/operational-analyst.md` — one primary orchestrator plus three subagent legs — including their modes, dispatch descriptions, prompt bodies, read-only permissions, and the prompt-named skill sets that realise the shared analytic spine.

## Requirements
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

### Requirement: Credential-harvest dispatch section in every agent prompt

Every analyst agent prompt SHALL carry a named `## Credential harvest` H2 section describing that agent's role in the credential-harvest triage flow. The primary orchestrator SHALL describe when to dispatch triage and how to route findings to the specialist legs. Each leg SHALL describe how its domain-specific credential extraction plugs into the shared triage schema. The section SHALL be additive — existing sections (defining spine, baseline, dispatch topology, tool discipline, guardrails) are not rewritten. No permission change SHALL result from this addition.

#### Scenario: Section present in all four agents
- **WHEN** any of the four analyst agent files is inspected
- **THEN** it contains a `## Credential harvest` H2 section

#### Scenario: Primary describes dispatch
- **WHEN** `operational-analyst`'s credential-harvest section is read
- **THEN** it names `credential-harvest-triage` and describes when to dispatch it and how to route findings to the appropriate leg

#### Scenario: Each leg describes domain plug-in
- **WHEN** any leg agent's credential-harvest section is read
- **THEN** it names the credential-adjacent skills from that leg's grid column and describes how their extractions feed the triage schema

#### Scenario: Permissions unchanged
- **WHEN** the frontmatter of any analyst agent is compared before and after the amendment
- **THEN** `edit`, `bash`, and `task` permission blocks are unchanged

### Requirement: Triage skill named in agent prompts that draw on it

Every analyst agent prompt that references credential handling SHALL name `credential-harvest-triage` in its prompt skill set, realising the triage skill's binding by prompt reference (there is no `skills:` field). At minimum this SHALL include the primary orchestrator and any leg whose grid column touches a credential-adjacent skill.

#### Scenario: Triage skill named where used
- **WHEN** an agent's `## Credential harvest` section is present
- **THEN** the string `credential-harvest-triage` appears in the agent's prompt (either in the credential-harvest section itself or in the agent's named skill set)
