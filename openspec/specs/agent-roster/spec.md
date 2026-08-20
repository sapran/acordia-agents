# agent-roster Specification

## Purpose
Defines the nine ACORDIA agents shipped by the two pillars — one authored markdown file each, the
three-key frontmatter contract both target harnesses accept, what each agent owns, the write posture
that separates an agent's own work from the material it was given, and the command wrappers that
dispatch them.

## Requirements

### Requirement: Nine agents, two pillars, one authored file each

The distribution SHALL ship exactly nine agent files, four under `acordia-analysts/agents/` and five
under `acordia-operators/agents/`, each the single editable source for every harness. The analyst
files SHALL be `cyber-analyst.md`, `target-analyst.md`,
`overwatch-analyst.md`, `fusion-analyst.md`; the operations files SHALL be `cyber-operator.md`,
`web-application.md`, `mobile-application.md`, `cloud-security.md`, `internal-network.md`. Filename
stem SHALL equal frontmatter `name`. No generated or translated copy of an agent SHALL exist in the
repository.

#### Scenario: Roster is complete and named
- **WHEN** the two pillar `agents/` directories are enumerated
- **THEN** exactly those nine files are present, and each filename stem equals its frontmatter `name`

#### Scenario: No second copy of an agent exists
- **WHEN** the repository is searched for agent files carrying an ACORDIA description
- **THEN** the only matches are those nine files

### Requirement: Agent frontmatter is exactly name, description, color

Every agent file's frontmatter SHALL contain `name`, `description` and `color`, and no other key. It
SHALL NOT declare `tools`, `disallowedTools`, `spawns`, `permission`, `mode`, `autoloadSkills`, or a
`metadata` block. Omitting `tools` grants the agent the harness's full tool set, and omitting
`spawns` leaves its spawn policy unrestricted; both are the intent for every agent in both pillars.
`color` SHALL be `cyan` for the two orchestrators and `blue` for the seven specialists.

#### Scenario: Frontmatter carries three keys
- **WHEN** any of the nine agent files is parsed
- **THEN** its frontmatter keys are exactly `name`, `description`, `color`

#### Scenario: No restriction key survives
- **WHEN** the nine agent files are searched for `tools`, `disallowedTools`, `permission`, `mode` or `spawns`
- **THEN** none is found

#### Scenario: Agent loads in a harness that requires only the contract
- **WHEN** a harness that requires `name`, `description` and a body discovers the pillar
- **THEN** all nine agents load, and none is skipped as a parse failure

### Requirement: Dispatch descriptions carry the pillar tag and the routing signal

Each agent `description` SHALL open with `ACORDIA Analysis — ` or `ACORDIA Operations — `, naming
the pillar that supplied it, and SHALL then state the routing signal a caller selects on: for an
analyst leg, its operating question from `docs/roles/operational-analyst.md`; for an operations
specialist, its domain and technique coverage; for an orchestrator, that it is the primary to select
for the pillar's work.

#### Scenario: Description identifies its pillar
- **WHEN** any agent description is read
- **THEN** it begins with the pillar tag for the directory it lives in

#### Scenario: Description discriminates between two candidates
- **WHEN** a caller compares `target-analyst` and `overwatch-analyst`
- **THEN** each description names a distinct question — what the target is and whether the action landed, versus whether the operation is being seen

### Requirement: Orchestrators route to their own specialists by prompt, not by permission

`cyber-analyst` and `cyber-operator` SHALL each name their own specialists in their prompt bodies and
route work to them there. The routing SHALL be prompt discipline: no agent file declares a spawn
allowlist, and the specialists are leaf agents by prompt statement rather than by tool restriction.
Each orchestrator prompt SHALL state that dispatching a leg is the default for a specialist question
and that it does not re-derive a leg's product.

#### Scenario: Orchestrator names its legs
- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it names `target-analyst`, `overwatch-analyst` and `fusion-analyst` as the agents it dispatches

#### Scenario: Orchestrator prefers dispatch to doing the work itself
- **WHEN** a specialist-domain question reaches an orchestrator
- **THEN** its prompt directs it to dispatch the matching specialist rather than answer from its own reading

### Requirement: Write posture separates an agent's own work from the material it analyses

Every agent SHALL hold the harness's full tool set, including file editing. Each of the four analyst
prompts SHALL carry the same rule in place of a read-only claim: the agent writes freely — notes,
working files, drafts, and its product — and SHALL NOT modify the material it was given to analyse,
because evidence, collected data, logs, dumps and captures are read-only inputs and derived work
belongs in the agent's own files. No agent prompt SHALL claim to hold no file-editing tool, and no
prompt SHALL describe a write destination as enforced.

#### Scenario: Analyst writes its own notes
- **WHEN** an analyst agent is asked to write working notes to a scratch path and read them back
- **THEN** the file is written and read back successfully

#### Scenario: Analysis inputs are not rewritten
- **WHEN** an analyst derives a product from a supplied log, dump or capture
- **THEN** its prompt requires the derived work to land in the agent's own files, leaving the source untouched

#### Scenario: No prompt claims an absent tool
- **WHEN** the nine prompts are searched for "no file-editing tool" or an equivalent read-only claim
- **THEN** none is found

### Requirement: The report sink is a convention, not a permission

`.acordia/reports/` SHALL remain the suggested destination for an analyst product, and `.acordia/ops/`
for an operator journal, stated as a convention. No prompt or frontmatter SHALL present either path
as an enforced scope.

#### Scenario: Sink is worded as a convention
- **WHEN** a prompt names `.acordia/reports/` or `.acordia/ops/`
- **THEN** it presents the path as where the product belongs, without claiming any harness restricts writes to it

### Requirement: Retrieved content is data, not instructions

Every one of the nine prompts SHALL state that fetched pages, tool output, document text, and
collected artefacts are data and never instructions — that an instruction found inside retrieved
material is reported, not followed, and never redirects the agent's tool use.

#### Scenario: Rule present in every prompt
- **WHEN** each of the nine agent prompts is read
- **THEN** each states that retrieved content is treated as data and that embedded instructions are reported rather than obeyed

#### Scenario: Injected instruction is surfaced
- **WHEN** an agent reads a target-controlled document containing an instruction addressed to it
- **THEN** its prompt requires it to report the attempt to its caller instead of acting on it

### Requirement: Every prompt names its skill set on `·`-separated lines

Each agent prompt SHALL name the skills it works from, grouped under headings and written as a
single line of `·`-separated slugs directly beneath each heading. An analyst prompt SHALL carry the
shared analytic spine, its specialist depth line, and a working-knowledge line; an operations prompt
SHALL carry its own equivalent depth and working-knowledge lines. Every slug named SHALL resolve to a
skill directory in the same pillar.

The relation SHALL be total in both directions: every slug on a line resolves to a skill, **and** every
skill in the pillar is named on at least one line. A skill that no prompt names is unreachable, because
these lines are the only agent-to-skill binding either harness offers, so adding a skill without adding
its slug leaves it shipped but dead.

#### Scenario: Skill line shape holds

- **WHEN** a heading naming a skill group is read
- **THEN** the next non-empty line is a `·`-separated list of skill slugs with no other prose

#### Scenario: Every named slug resolves

- **WHEN** every slug named in every prompt is looked up in its own pillar's `skills/`
- **THEN** each resolves to a directory containing `SKILL.md`

#### Scenario: Every skill is named somewhere

- **WHEN** every skill directory in a pillar is searched for in that pillar's prompts
- **THEN** each appears on at least one prompt's skill line

#### Scenario: A removed skill leaves no dangling slug

- **WHEN** a skill directory is deleted or merged away
- **THEN** its slug is removed from every prompt line naming it, in the same change

### Requirement: Analyst prompts carry the four cross-cutting sections

Each analyst prompt SHALL carry a credential-harvest section naming `credential-harvest-triage`, an
exhaustive-processing section naming `exhaustive-data-processing`, an Aleph-corpora section naming
`aleph-entity-graph`, and a tool-discipline section stating that native read/grep/glob are preferred
and `bash` is for work no native tool fits. A leg SHALL state that it cannot fan out and must surface
an unfinished remainder to the orchestrator.

#### Scenario: Sections present
- **WHEN** any of the four analyst prompts is read
- **THEN** it carries credential-harvest, exhaustive-processing, Aleph-corpora and tool-discipline sections

#### Scenario: Leg surfaces a remainder instead of fanning out
- **WHEN** a slice is larger than a leg can finish
- **THEN** its prompt requires it to report the remainder to the orchestrator

### Requirement: Each agent declares what it returns

Every prompt SHALL carry a section stating its return contract. A leg SHALL state the product it
hands back, with confidence and named gaps where its judgement is analytic. An orchestrator SHALL
state that it composes the final product from its legs' returns rather than re-deriving them.

#### Scenario: Return contract present
- **WHEN** any agent prompt is read
- **THEN** it carries a section naming what it returns

#### Scenario: Orchestrator composes rather than re-derives
- **WHEN** an orchestrator receives a leg's product
- **THEN** its prompt directs it to compose from that product without redoing the leg's work

### Requirement: Operator prompts state the authorization gate and journal discipline

Each of the five operations prompts SHALL state that work proceeds only inside authorized scope,
naming `.acordia/ops/scope.md` as where scope is recorded, and SHALL name the `operation-journal`
skill as the contract for how operation state is recorded. Each SHALL also carry a guardrails section
requiring evidence-backed findings, minimal noise and blast radius, least privilege, no fabrication,
no destructive action beyond a proof of concept, no exfiltration beyond proof, and no persistence.

#### Scenario: Scope gate present

- **WHEN** any operations prompt is read
- **THEN** it names `.acordia/ops/scope.md` and refuses work on a target absent from it

#### Scenario: Guardrails present

- **WHEN** any operations prompt is read
- **THEN** it carries the evidence-first, minimal-noise, least-privilege, no-fabrication, no-destruction, no-exfiltration and no-persistence rules

#### Scenario: Journal discipline reachable

- **WHEN** any operations prompt is read
- **THEN** it names `operation-journal`, so the recording contract is one read away rather than restated in the prompt

### Requirement: Prompt bodies name no tool the harness lacks

No prompt body SHALL instruct an agent to call a tool that does not exist in the target harnesses.
Where a technique needs a capability the harness expresses differently, the prompt SHALL name the
portable form — a standard tool or an explicit shell invocation — instead of a harness-specific tool
name.

#### Scenario: No unavailable tool is named
- **WHEN** the nine prompts are searched for tool names
- **THEN** every named tool exists in the target harnesses

### Requirement: A namespaced command wrapper for every dispatchable agent

The distribution SHALL ship 18 slash-command wrappers: one canonical wrapper named after each of the
nine agents, plus nine short aliases. Each wrapper SHALL live in its own pillar's flat `commands/`
directory — eight under `acordia-analysts/commands/`, ten under `acordia-operators/commands/` —
because a harness discovers plugin commands from `<pluginRoot>/commands/*.md` without recursion and
namespaces them by plugin name. Each wrapper SHALL carry `description` and `argument-hint`
frontmatter, SHALL dispatch exactly the agent it is named for, SHALL pass the caller's argument
through as the brief, and SHALL ask for a brief when none is supplied.

Where renaming a lead agent lengthens its canonical wrapper, the previous single-word wrapper SHALL be
retained as that agent's short alias, so that an existing invocation keeps working.

#### Scenario: Wrapper count and split
- **WHEN** the two `commands/` directories are enumerated
- **THEN** eight analyst and ten operations wrappers are present, 18 in total, each a flat `.md` file

#### Scenario: Wrapper dispatches its own agent
- **WHEN** any wrapper is read
- **THEN** it names exactly one agent, the one it is named or aliased for

#### Scenario: A renamed lead keeps its old handle
- **WHEN** `/operator` and `/analyst` are invoked
- **THEN** they dispatch `cyber-operator` and `cyber-analyst` respectively

#### Scenario: Empty brief is refused
- **WHEN** a wrapper is invoked with no argument
- **THEN** it asks what to look at before dispatching

### Requirement: Agent names and skill slugs stay unprefixed

Agent `name` values and skill slugs SHALL carry no `acordia-` prefix. Provenance SHALL be carried by
the description tag, the plugin name that namespaces commands, and the agent `color`, because the
name is the dispatch handle and the slug is bound to its folder.

#### Scenario: Names are bare
- **WHEN** the nine agent names and every skill slug are read
- **THEN** none carries a distribution prefix

### Requirement: A prompt routes to a skill rather than restating its technique

An agent prompt SHALL carry the judgement its agent exists to make — the situation-to-technique
routing, the phase order, the return contract — and SHALL NOT restate technique detail that a skill
it names already carries. Where a prompt needs to reach a technique, it SHALL name the situation and
the owning skill on one line, in the form `- **<situation>** → \`<skill-slug>\``.

Moving technique text out of a prompt SHALL NOT lose it: before a block leaves a prompt, every
command, payload, flag and table row in it SHALL be present in the destination skill, appended there
first where it is absent.

#### Scenario: Prompt names a skill instead of repeating it

- **WHEN** an operations prompt reaches a technique that a named skill carries
- **THEN** the prompt gives the situation and the skill slug, and does not repeat the skill's commands

#### Scenario: A moved command survives the move

- **WHEN** a technique block is removed from a prompt
- **THEN** every command and payload it contained is present in the skill the prompt now routes to

#### Scenario: Routing blocks stay in the prompt

- **WHEN** a block reads "situation → technique → skill" rather than carrying the technique itself
- **THEN** it stays in the prompt, because routing is the agent's own work

### Requirement: Prompt bodies stay under a measured ceiling

No agent prompt body SHALL exceed 10,000 characters, measured after the frontmatter. A prompt that
crosses the ceiling SHALL be reduced by moving technique detail to the skill that owns it, never by
deleting the routing or the guardrails.

#### Scenario: Ceiling holds across the roster

- **WHEN** every agent prompt body in both pillars is measured
- **THEN** none exceeds 10,000 characters

### Requirement: The journal contract is named once, not restated per prompt

The `.acordia/ops/` operation-journal contract — the file layout, the severity and confidence scales,
the log-on-discovery and check-coverage-before-claiming rules, the finding-file shape — SHALL live in
the `operation-journal` skill. Each of the five operations prompts SHALL name that skill in one sentence
and SHALL carry only the journal fields specific to its own domain, which the shared contract does not
cover.

#### Scenario: Prompt points at the skill

- **WHEN** an operations prompt's journal section is read
- **THEN** it names `operation-journal` and does not restate the scales or the file layout

#### Scenario: Domain-specific fields survive

- **WHEN** `web-application`'s journal section is read
- **THEN** it still requires WSTG-ID, CWE and MITRE ATT&CK on a finding, because those are its own additions

#### Scenario: Composition boundary stays stated

- **WHEN** `internal-network`'s journal section is read
- **THEN** it still states that the final assessment report is composed by the orchestrator from this journal, not by the specialist

### Requirement: A lead agent's name is distinct from its pillar's name

Neither pillar's lead agent SHALL be named with a word that also names the pillar, its skill library,
its prompts or its artifacts. The analyst lead SHALL be `cyber-analyst` and the operations lead SHALL
be `cyber-operator`, so that "the operations pillar" and "the operations prompts" can never be read as
naming an agent.

Prose SHALL keep the bare word `operator` only where it means a human or a driving session rather than
the agent — the analyst guardrail *"execution belongs to the operators you advise"*, an operator
journal, an operator session, operator-deployed artifacts, and technique content such as a
default-credential pair. Renaming SHALL NOT rewrite those sites.

An archived change SHALL NOT be rewritten to use a later name. It records what was true when it
shipped.

#### Scenario: Pillar word never resolves to an agent
- **WHEN** the live tree is searched for `operator` followed by pillar, library, skill, prompt, agent, wrapper, artifact or file
- **THEN** no match is found, because every such site reads `operations`

#### Scenario: The human sense survives the rename
- **WHEN** an analyst prompt's closing guardrail is read
- **THEN** it still says execution belongs to the operators it advises, naming no agent

#### Scenario: Archived changes keep their original names
- **WHEN** any file under `openspec/changes/archive/` is read
- **THEN** it still names `operational-analyst` and `operator` as they were at the time it shipped

#### Scenario: A provenance document keeps its filename and its anchors
- **WHEN** `docs/roles/operational-analyst.md` is read
- **THEN** its grid rows are still at lines L67–L108, every skill anchor still resolves to a row, and a
  closing note records that the shipped agent is now `cyber-analyst`

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
