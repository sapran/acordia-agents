## ADDED Requirements

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
