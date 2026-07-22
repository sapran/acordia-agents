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

opencode's permission default is **allow**, and the `edit` permission governs the edit, write, and patch tools collectively (there is no separate `write` key; a top-level `"*": deny` is accepted but overridden by per-tool built-in defaults, so it does not produce a deny-default). The `edit` permission additionally accepts **path-scoped rules with last-match-wins precedence**, exactly like `bash` (documented in `docs/agents-skills-extension-workbook.md` §6).

Every analyst agent SHALL deny file modification by default. The two analysts that hold the **Briefing & written reporting** competency in the role grid (`docs/roles/operational-analyst.md` L76 — `●` Core `operational-analyst`, `○` Fus `fusion-analyst`) SHALL set a path-scoped `edit` permission that denies every path except a single report sink:

```yaml
edit:
  "*": deny
  ".acordia/reports/**": allow
```

Every other analyst — `target-network-analyst` and `defender-detection-analyst`, which carry no reporting competency in the grid — SHALL set a blanket `edit: deny`. Analysis capability (read, grep, glob, bash, webfetch, websearch, skill) remains allowed by opencode's default. Each leg subagent SHALL additionally set `task: deny` (leaf specialist — does not dispatch).

Because `bash: "*": allow` already permits file creation via scripting (`python`, `jq`), `edit: deny` expresses read-only **posture**, not a hard sandbox; the path-scoped exception declares the one sanctioned report destination for the reporting agents rather than granting a new capability class.

#### Scenario: File modification denied
- **WHEN** an analyst agent attempts to edit, write, or patch a file outside its sanctioned report sink
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: Reporting agents may write to the report sink
- **WHEN** `operational-analyst` or `fusion-analyst` writes or edits a file under `.acordia/reports/`
- **THEN** the resolved `edit` permission is `allow` (last-match-wins on the `.acordia/reports/**` rule) and the write proceeds

#### Scenario: Non-reporting legs are fully read-only
- **WHEN** `target-network-analyst` or `defender-detection-analyst` attempts to edit, write, or patch any file
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

### Requirement: Primary prompt compels leg dispatch before a course of action

The role model defines the orchestrator's recommended course of action as **"three technical reads feeding one analytic judgement"** (`docs/roles/operational-analyst.md` L52; "How the pieces fit" L48–52). To encode that faithfully, the `operational-analyst` prompt **body** SHALL compel dispatch of every leg subagent whose operating question the task touches **before** the orchestrator delivers a recommended course of action — not merely state that it *can* dispatch (which the existing "Orchestrator dispatches a leg" scenario already establishes at the permission level).

The prompt body SHALL bound **self-service** — the orchestrator using its own `read` / `grep` / `glob` / `list` / `bash` in place of a leg — to work that matches **no** leg's operating question, plus trivial single-artefact lookups. It SHALL NOT present self-service as a co-equal alternative to dispatch for questions that fall to a specialist.

This mandate SHALL be realised in the **prompt body only**. It SHALL NOT alter the `task` whitelist, the `edit` / `bash` permission blocks, `mode`, or any leg `description`; it SHALL add no grid row and no new skill. It complements — does not replace — the existing "Primary orchestrator, subagent legs" requirement.

#### Scenario: Dispatch stated as a precondition, not an option

- **WHEN** the `operational-analyst.md` prompt body is inspected
- **THEN** it states that the legs whose operating question the task touches are dispatched **before** a recommended course of action is delivered, rather than presenting dispatch as one option among several

#### Scenario: Self-service is bounded to no-leg work

- **WHEN** the prompt body's self-service clause is read
- **THEN** it limits the orchestrator's own `read`/`grep`/`glob`/`list`/`bash` reads to work matching no leg's operating question (and trivial single-artefact lookups), rather than offering self-service as a co-equal path for specialist questions

#### Scenario: Dispatch topology and permissions unchanged

- **WHEN** `operational-analyst`'s `task`, `edit`, and `bash` permission blocks and `mode` are compared before and after the amendment
- **THEN** they are unchanged — the three-leg `task` whitelist (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is intact and `mode` remains `primary`

#### Scenario: Leg descriptions unchanged

- **WHEN** each leg subagent's `description` is compared before and after the amendment
- **THEN** it remains the italic operating question of that leg (the routing signal surfaced to the model is untouched)

