## ADDED Requirements

### Requirement: Leg subagents declare what they return

Each of the three leg subagent prompts (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) SHALL carry a named `## What to return` H2 section stating, in advisory prose, the compact surface the leg emits back to the orchestrator. The section SHALL name: (a) the hypothesis or judgement the leg produces, (b) a calibrated confidence expression, (c) the gaps the leg has named (`naming-the-gaps`), (d) the recommended next collection or method, and (e) how credential findings are routed via `credential-harvest-triage` bins (P0–P3) with source paths.

The section SHALL be additive — existing sections (defining spine, baseline, tool discipline, guardrails, credential-harvest) are not rewritten. The section SHALL NOT be a JSON schema, a typed block, or a structured-output contract; it is prose. `description` frontmatter SHALL remain the italic operating question of the leg, unchanged.

#### Scenario: Section present in each leg

- **WHEN** any leg subagent prompt is inspected
- **THEN** it contains a `## What to return` H2 section

#### Scenario: Section describes the five named elements

- **WHEN** a leg's `## What to return` section is read
- **THEN** it describes (a) hypothesis/judgement, (b) confidence expression, (c) gaps named, (d) next collection/method, and (e) credential-finding routing to triage bins with source paths

#### Scenario: `description` frontmatter unchanged

- **WHEN** a leg's `description` is compared before and after the amendment
- **THEN** it remains the italic operating question, verbatim

#### Scenario: Permissions unchanged

- **WHEN** a leg's `edit`, `bash`, `task` permission blocks are compared before and after the amendment
- **THEN** they are unchanged

### Requirement: Primary declares output discipline

The primary orchestrator prompt (`operational-analyst`) SHALL carry a named `## Output discipline` H2 section stating, in advisory prose, how it aggregates the three legs' returns into the operator-facing picture: (a) hypothesis attribution to leg source, (b) union of named gaps across legs, (c) prioritisation of next-collection recommendations across legs, and (d) de-duplication of credential findings across legs before routing through `credential-harvest-triage`.

The section SHALL be additive. It SHALL NOT introduce a return schema, alter the orchestrator's dispatch topology, or change the three-leg `task` whitelist.

#### Scenario: Section present in the primary

- **WHEN** `operational-analyst.md` is inspected
- **THEN** it contains a `## Output discipline` H2 section

#### Scenario: Section names the four aggregation elements

- **WHEN** the section is read
- **THEN** it describes (a) hypothesis attribution, (b) gap union, (c) next-collection prioritisation, and (d) credential-finding de-duplication

#### Scenario: Dispatch topology unchanged

- **WHEN** the primary's `task` block is compared before and after the amendment
- **THEN** the three-leg whitelist (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is unchanged
