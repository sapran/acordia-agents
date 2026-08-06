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

**The report sink is a convention, not a boundary, in every harness including opencode.** Because every analyst carries `bash: allow` (`analysts/agents/*.md`), file creation via scripting (`python`, `jq`, a shell redirection) is permitted at any path, and the path-scoped `edit` rule does not constrain it. `edit: deny` therefore expresses read-only **posture** — the agent holds no file-editing tool — and the scoped rule **declares** the one sanctioned report destination rather than enforcing it. The scoped rule is retained because it is the clearest available expression of that convention in opencode's vocabulary, not because it confines anything.

Documentation, generated notes, and prompt guardrails SHALL NOT describe the sink as enforced in opencode and unenforced elsewhere. The non-enforcement is universal and follows from `bash: allow`, which is retained because `analytic-tooling-scripting` and `exhaustive-data-processing` depend on it.

#### Scenario: File modification denied
- **WHEN** an analyst agent attempts to edit, write, or patch a file outside its sanctioned report sink
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: Reporting agents may write to the report sink
- **WHEN** `operational-analyst` or `fusion-analyst` writes or edits a file under `.acordia/reports/`
- **THEN** the resolved `edit` permission is `allow` (last-match-wins on the `.acordia/reports/**` rule) and the write proceeds

#### Scenario: Non-reporting legs are fully read-only
- **WHEN** `target-network-analyst` or `defender-detection-analyst` attempts to edit, write, or patch any file
- **THEN** the resolved `edit` permission is `deny` and the action is refused

#### Scenario: A scripted write outside the sink is refused by no harness
- **WHEN** any analyst agent writes a file outside `.acordia/reports/` using `bash`
- **THEN** the write succeeds, in opencode as in omp and Claude Code
- **AND** the scoped `edit` rule does not apply to it, because `bash: allow` is a separate and unrestricted write channel

#### Scenario: The sink is documented as a convention
- **WHEN** the repository's documentation, the generated agent notes, or an analyst's guardrails describe the report sink
- **THEN** the confinement is stated as prompt discipline holding in every harness
- **AND** no harness is credited with enforcing it

#### Scenario: Analysis allowed by default
- **WHEN** an analyst agent reads a file or fetches a web resource
- **THEN** the action is allowed (opencode default)

#### Scenario: Legs do not dispatch
- **WHEN** a leg subagent is inspected
- **THEN** its resolved `task` permission is `deny`

### Requirement: Analyst guardrails state the product destination uniformly

Each analyst's `## Guardrails` section SHALL state, in wording consistent across all four agents, where that agent's written product goes and that the destination is prompt discipline rather than an enforced scope.

The two reporting analysts (`operational-analyst`, `fusion-analyst`) SHALL name `.acordia/reports/` as the sink. The two non-reporting legs (`target-network-analyst`, `defender-detection-analyst`) SHALL state that they return their product in-message, because they hold no write tool — a fact their guardrails previously omitted entirely, leaving the destination unstated.

The guardrails SHALL NOT attribute the non-enforcement to a specific harness. The prior per-agent divergence — `defender-detection-analyst` and `target-network-analyst` naming only "Under OMP, write access is prompt-level only", against `operational-analyst` and `fusion-analyst` naming "Under OMP … confine writes to `.acordia/reports/`" — is the drift this requirement removes.

#### Scenario: All four guardrails share one wording
- **WHEN** the `## Guardrails` sections of the four analyst agents are compared
- **THEN** each states the sink or the in-message destination in the same form
- **AND** none names a single harness as the reason the confinement is prompt-level

#### Scenario: Read-only legs state where the product goes
- **WHEN** `target-network-analyst` or `defender-detection-analyst` guardrails are read
- **THEN** they state that the product is returned in-message

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

### Requirement: Triage skill named in agent prompts that draw on it

Every analyst agent prompt that references credential handling SHALL name `credential-harvest-triage` in its prompt skill set, realising the triage skill's binding by prompt reference (there is no `skills:` field). At minimum this SHALL include the primary orchestrator and any leg whose grid column touches a credential-adjacent skill.

#### Scenario: Triage skill named where used
- **WHEN** an agent's `## Credential harvest` section is present
- **THEN** the string `credential-harvest-triage` appears in the agent's prompt (either in the credential-harvest section itself or in the agent's named skill set)

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

### Requirement: Bash analysis fully allowed; read-only CLI tools ungated

Every analyst agent SHALL set `bash: allow`, granting every shell command — including the read-only CLI tools used for file and data analysis (`cat`, `head`, `tail`, `less`, `more`, `ls`, `grep`, `egrep`, `rg`, `find`, `fd`) — the `allow` resolution. No read-only CLI tool SHALL be gated with `deny` or `ask`.

This supersedes the prior tool-steering block (which denied `cat`/`head`/`tail`/`less`/`more`/`ls` and prompted on `grep`/`egrep`/`rg`/`find`/`fd` while leaving `"*": allow`). Removing those overrides grants no new command class: `bash: "*": allow` already permitted every non-read-only command, so `bash: allow` only lifts the gate on the read-only tools. The preference for opencode-native `read`/`grep`/`glob` is retained as prompt-level advice, not as a permission gate.

This requirement governs only the `bash` permission. It does not alter `edit` (read-only file-modification posture: `edit: deny`, plus the `.acordia/reports/**` scoped-write exception on the two reporting agents) or `task` (leg `task: deny`; the orchestrator's three-leg dispatch whitelist).

#### Scenario: Read-only CLI tools resolve to allow

- **WHEN** any analyst agent runs a read-only CLI command (`cat`, `head`, `tail`, `less`, `more`, `ls`, `grep`, `egrep`, `rg`, `find`, or `fd`)
- **THEN** its resolved `bash` permission is `allow` and the command runs without a prompt or denial

#### Scenario: Bash block is a single allow

- **WHEN** any analyst agent's frontmatter is inspected
- **THEN** its `bash` permission is `bash: allow` with no per-command `deny` or `ask` overrides

#### Scenario: edit and task posture unchanged

- **WHEN** an analyst agent's `edit` and `task` blocks are compared before and after this change
- **THEN** they are unchanged — file-modification stays denied outside the sanctioned report sink, legs still set `task: deny`, and the orchestrator still whitelists only its three legs

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

### Requirement: Aleph-corpora section in every agent prompt

Every analyst agent prompt SHALL carry a named `## Aleph corpora` H2 section containing a one-line reference to the `aleph-entity-graph` skill, so that take which has already been ingested into an Aleph instance is worked as an entity graph rather than re-ground as a pile of documents.

This exists because the skill is non-grid and therefore appears in no agent's compiled skill set: with no prompt reference at all, selection depends entirely on opencode's description-match, and the capability is reachable only by accident. A prose H2 section is the mechanism this repository already uses for exactly that problem — `## Credential harvest` and `## Exhaustive data processing` are both required in all four prompts for the same reason — and it does not touch the grid-derived list, so the bijection between grid column and prompt skill set is unaffected.

The section MAY carry one agent-specific lens that belongs to the agent rather than to the corpus procedure: for `operational-analyst`, routing corpus work to a leg; for `fusion-analyst`, correlation across collections; for `target-network-analyst`, reading ownership and address edges as target structure; for `defender-detection-analyst`, operation-owned exposure surfacing in an indexed collection as an own-footprint finding.

The section SHALL NOT restate the skill's method, its tool list, or its ceilings — `analysts/skills/aleph-entity-graph/SKILL.md` is the single source for the inventory-first and facet-first method, the 9999 search window, the per-property expansion cap and the `_stream` WRITE requirement, and a second copy in four prompt bodies drifts from it. In particular a prompt SHALL NOT name individual MCP tools, because the skill states that the harness decides what those are called.

The section SHALL remain additive — existing sections (defining spine, baseline, dispatch topology, tool discipline, credential harvest, exhaustive data processing, guardrails) are not rewritten — and SHALL NOT add `aleph-entity-graph` to any agent's grid-derived skill set. No permission change SHALL result.

#### Scenario: Section present in all four agents

- **WHEN** any of the four analyst agent files is inspected
- **THEN** it contains an `## Aleph corpora` H2 section naming `aleph-entity-graph`

#### Scenario: Primary routes corpus work

- **WHEN** `operational-analyst`'s Aleph-corpora section is read
- **THEN** it names `aleph-entity-graph` as what carries the method, routes corpus work to a leg by default, and requires a coverage claim over a corpus to name which collections were searched

#### Scenario: Each leg carries its own lens

- **WHEN** any leg agent's Aleph-corpora section is read
- **THEN** it names `aleph-entity-graph`, and any lens it adds is that leg's own analytic angle rather than a restatement of the corpus procedure

#### Scenario: Method is not duplicated

- **WHEN** any agent's Aleph-corpora section is compared with `aleph-entity-graph`
- **THEN** the section does not reproduce the facet-first method, the tool names, the 9999 window, or the expansion cap

#### Scenario: Grid-derived skill set is unchanged

- **WHEN** each agent's compiled skill set is compared with its column in the competency grid
- **THEN** the two still correspond exactly, and `aleph-entity-graph` appears in no agent's skill set

#### Scenario: Permissions unchanged

- **WHEN** the frontmatter of any analyst agent is compared before and after the amendment
- **THEN** `edit`, `bash`, and `task` permission blocks are unchanged

