## MODIFIED Requirements

### Requirement: Credential-harvest dispatch section in every agent prompt

Every analyst agent prompt SHALL carry a named `## Credential harvest` H2 section containing a one-line reference to the `credential-harvest-triage` skill, so that collected material is inventoried and classified before deeper analysis.

The section MAY additionally name the credential-adjacent skills that agent applies, and MAY carry one domain-specific lens that belongs to the agent rather than to the triage procedure (for `defender-detection-analyst`, the distinction between operation-owned and target-owned credentials). The section SHALL NOT restate the triage skill's classification schema, bucket-partition step, priority bins, or routing table — `analysts/skills/credential-harvest-triage/SKILL.md` is the single source for those, and a second copy in four prompt bodies drifts from it.

The section SHALL remain additive — existing sections (defining spine, baseline, dispatch topology, tool discipline, guardrails) are not rewritten — and SHALL continue to report classifications rather than raw credential values. No permission change SHALL result.

#### Scenario: Section present in all four agents

- **WHEN** any of the four analyst agent files is inspected
- **THEN** it contains a `## Credential harvest` H2 section

#### Scenario: Primary names the triage skill

- **WHEN** `operational-analyst`'s credential-harvest section is read
- **THEN** it names `credential-harvest-triage` as what to apply when collected material lands, without restating that skill's procedure

#### Scenario: Each leg names the triage skill

- **WHEN** any leg agent's credential-harvest section is read
- **THEN** it names `credential-harvest-triage`, and where it names credential-adjacent skills those are drawn from that leg's grid column

#### Scenario: Procedure is not duplicated

- **WHEN** any agent's credential-harvest section is compared with `credential-harvest-triage`
- **THEN** the section does not reproduce the bucket partition, the classification schema, or the priority bins

#### Scenario: Permissions unchanged

- **WHEN** the frontmatter of any analyst agent is compared before and after the amendment
- **THEN** `edit`, `bash`, and `task` permission blocks are unchanged

### Requirement: Leg subagents declare what they return

Each of the three leg subagent prompts (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) SHALL carry a named `## What to return` H2 section stating, in advisory prose, the compact surface the leg emits back to the orchestrator. The section SHALL name three elements: (a) the hypothesis or judgement the leg produces, (b) the confidence attached to it, and (c) the gaps that bound it together with what would close them.

Credential findings are covered by the agent's `## Credential harvest` reference to `credential-harvest-triage` and SHALL NOT need restating here, though a leg MAY note that classified findings come back with their source paths.

The section SHALL be additive — existing sections are not rewritten. The section SHALL NOT be a JSON schema, a typed block, or a structured-output contract; it is prose, and it prescribes no template. `description` frontmatter SHALL remain the italic operating question of the leg, unchanged.

#### Scenario: Section present in each leg

- **WHEN** any leg subagent prompt is inspected
- **THEN** it contains a `## What to return` H2 section

#### Scenario: Section names the three elements

- **WHEN** a leg's `## What to return` section is read
- **THEN** it describes (a) the hypothesis or judgement, (b) confidence, and (c) the gaps and what would close them

#### Scenario: Section prescribes no return template

- **WHEN** a leg's `## What to return` section is read
- **THEN** it is prose stating what the return is about, not a field list, schema, or fixed format the leg must fill in

#### Scenario: `description` frontmatter unchanged

- **WHEN** a leg's `description` is compared before and after the amendment
- **THEN** it remains the italic operating question, verbatim

#### Scenario: Permissions unchanged

- **WHEN** a leg's `edit`, `bash`, `task` permission blocks are compared before and after the amendment
- **THEN** they are unchanged

### Requirement: Primary declares output discipline

The primary orchestrator prompt (`operational-analyst`) SHALL carry a named `## Output discipline` H2 section stating, in advisory prose, the principle by which it turns the legs' returns into one operator-facing recommendation: fuse the reads into a single recommended course of action, attribute claims to the leg that made them, carry each leg's confidence through rather than averaging it away, surface disagreement between legs instead of silently picking a side, and be brief when the picture is clear.

The section SHALL NOT prescribe an aggregation template, a fixed ordering of elements, or a return schema. It SHALL be additive, and SHALL NOT alter the orchestrator's dispatch topology or the three-leg `task` whitelist.

#### Scenario: Section present in the primary

- **WHEN** `operational-analyst.md` is inspected
- **THEN** it contains a `## Output discipline` H2 section

#### Scenario: Section states the fusion principle

- **WHEN** the section is read
- **THEN** it states that the legs' reads are fused into one recommendation with claims attributed to their source leg, confidence carried through, and disagreement surfaced

#### Scenario: Section prescribes no aggregation template

- **WHEN** the section is read
- **THEN** it does not enumerate a mandatory set of aggregation steps the orchestrator must perform in order

#### Scenario: Dispatch topology unchanged

- **WHEN** the primary's `task` block is compared before and after the amendment
- **THEN** the three-leg whitelist (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is unchanged

### Requirement: Exhaustive-processing section in every agent prompt

Every analyst agent prompt SHALL carry a named `## Exhaustive data processing` H2 section stating the principle — process all of a handed slice before concluding, never sample its opening portion — and SHALL name the `exhaustive-data-processing` skill, which carries the method. The section SHALL be additive and SHALL cause no permission change.

The primary orchestrator's section SHALL state exhaustive processing as the default before judgement, and that partial coverage returned by a leg is re-dispatched or sub-partitioned rather than compiled into a sampled result.

Each leg's section SHALL state that the leg never samples its assigned slice and — because a leg is `task: deny` and cannot fan out — surfaces any un-processable remainder back to the orchestrator.

The section SHALL NOT mandate a coverage-receipt format, a declared-to-covered reconciliation protocol, or any other artifact whose shape no skill or harness defines; the coverage ledger belongs to `exhaustive-data-processing`.

#### Scenario: Section present in all four agents

- **WHEN** any of the four analyst agent files is inspected
- **THEN** it contains a `## Exhaustive data processing` H2 section that names `exhaustive-data-processing`

#### Scenario: Primary states exhaustive processing as the default before judgement

- **WHEN** `operational-analyst`'s exhaustive-processing section is read
- **THEN** it states that all of a handed slice is processed before judgement and that partial coverage from a leg is re-dispatched or sub-partitioned

#### Scenario: Each leg never samples and surfaces overflow

- **WHEN** any leg agent's exhaustive-processing section is read
- **THEN** it states that the leg never samples its slice and surfaces the un-processable remainder back to the orchestrator

#### Scenario: No receipt format is mandated

- **WHEN** any agent's exhaustive-processing section is read
- **THEN** it does not require a coverage receipt in a prescribed form, nor a reconciliation protocol between declared and covered scope

#### Scenario: Permissions unchanged

- **WHEN** the frontmatter of any analyst agent is compared before and after the amendment
- **THEN** `edit`, `bash`, and `task` permission blocks are unchanged, and the orchestrator's three-leg `task` whitelist is intact

### Requirement: Primary prompt defaults to leg dispatch

The role model defines the orchestrator's recommended course of action as **"three technical reads feeding one analytic judgement"** (`docs/roles/operational-analyst.md` L52; "How the pieces fit" L48–52). To encode that without forcing a round trip on work that does not need one, the `operational-analyst` prompt **body** SHALL state leg dispatch as the **default** path to a recommended course of action: the orchestrator SHOULD dispatch the leg that owns the question, and SHOULD fan out to several legs when the task spans their domains, because the deep technical read is what the legs exist to produce.

The prompt body SHALL present **self-service** — the orchestrator using its own `read` / `grep` / `glob` / `bash` in place of a leg — as the alternative for scoped work: appropriate when no leg's operating question applies, and when the task is a focused single-artefact read. It SHALL NOT frame dispatch as a precondition of every recommendation, and SHALL NOT frame self-service as a narrow exception.

This SHALL be realised in the **prompt body only**. It SHALL NOT alter the `task` whitelist, the `edit` / `bash` permission blocks, `mode`, or any leg `description`; it SHALL add no grid row and no new skill. It complements — does not replace — the existing "Primary orchestrator, subagent legs" requirement.

#### Scenario: Dispatch stated as the default

- **WHEN** the `operational-analyst.md` prompt body is inspected
- **THEN** it states that dispatching the leg owning the question is the default, and that fan-out is appropriate when the task spans several legs' domains

#### Scenario: Self-service is an alternative, not an exception

- **WHEN** the prompt body's self-service clause is read
- **THEN** it presents working the material directly as appropriate when no leg's question applies or the task is a focused single-artefact read, rather than as a narrow exception to a mandatory dispatch

#### Scenario: Dispatch is not stated as a precondition

- **WHEN** the prompt body is searched for a precondition framing
- **THEN** it does not require every leg whose question the task touches to be dispatched before any recommended course of action is delivered

#### Scenario: Dispatch topology and permissions unchanged

- **WHEN** `operational-analyst`'s `task`, `edit`, and `bash` permission blocks and `mode` are compared before and after the amendment
- **THEN** they are unchanged — the three-leg `task` whitelist (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is intact and `mode` remains `primary`

#### Scenario: Leg descriptions unchanged

- **WHEN** each leg subagent's `description` is compared before and after the amendment
- **THEN** it remains the italic operating question of that leg (the routing signal surfaced to the model is untouched)

## RENAMED Requirements

- FROM: `### Requirement: Primary prompt compels leg dispatch before a course of action`
- TO: `### Requirement: Primary prompt defaults to leg dispatch`
