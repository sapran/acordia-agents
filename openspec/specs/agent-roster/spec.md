# agent-roster Specification

## Purpose

Defines the five ACORDIA Analysis agents — one authored markdown file each, the
three-key frontmatter contract both target harnesses accept, what each agent owns, the write posture
that separates an agent's own work from the material it was given, and the command wrappers that
dispatch them.

## Requirements

### Requirement: Agent frontmatter is exactly name, description, color

Every agent file's frontmatter SHALL contain `name`, `description` and `color`, and no other key. It
SHALL NOT declare `tools`, `disallowedTools`, `spawns`, `permission`, `mode`, `autoloadSkills`, or a
`metadata` block. Omitting `tools` grants the agent the harness's full tool set, and omitting
`spawns` leaves its spawn policy unrestricted; both are the intent for every agent in the roster.
`color` SHALL be `cyan` for the single orchestrator, `cyber-analyst`, and `blue` for the four legs.

#### Scenario: Frontmatter carries three keys

- **WHEN** any of the five agent files is parsed
- **THEN** its frontmatter keys are exactly `name`, `description`, `color`

#### Scenario: No restriction key survives

- **WHEN** the five agent files are searched for `tools`, `disallowedTools`, `permission`, `mode` or `spawns`
- **THEN** none is found

#### Scenario: Agent loads in a harness that requires only the contract

- **WHEN** a harness that requires `name`, `description` and a body discovers the pillar
- **THEN** all five agents load, and none is skipped as a parse failure

### Requirement: Dispatch descriptions carry the pillar tag and the routing signal

Each agent `description` SHALL open with `ACORDIA Analysis — `, naming the pillar that supplied it,
and SHALL then state the routing signal a caller selects on: for a leg, its operating question from
`docs/roles/operational-analyst.md`; for the orchestrator, that it is the primary to select for the
pillar's work. `ACORDIA Operations — ` SHALL NOT appear in any shipped artifact, the pillar that
carried it having been removed.

#### Scenario: Description identifies its pillar

- **WHEN** any agent description is read
- **THEN** it begins with the pillar tag for the directory it lives in

#### Scenario: Description discriminates between two candidates

- **WHEN** a caller compares `mission-analyst` and `terrain-analyst`, the two legs cut from one
- **THEN** each description names a distinct question — what the target is for and what it depends on,
  versus which substrates it runs on and where they can be reached

### Requirement: Orchestrators route to their own specialists by prompt, not by permission

`cyber-analyst` SHALL name its four legs in its prompt body and route work to them there. The routing
SHALL be prompt discipline: no agent file declares a spawn allowlist, and the legs are leaf agents by
prompt statement rather than by tool restriction. The orchestrator prompt SHALL state that dispatching
a leg is the default for a specialist question and that it does not re-derive a leg's product.

#### Scenario: Orchestrator names its legs

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it names `mission-analyst`, `terrain-analyst`, `overwatch-analyst` and `collection-analyst`
  as the agents it dispatches

#### Scenario: Orchestrator prefers dispatch to doing the work itself

- **WHEN** a specialist-domain question reaches an orchestrator
- **THEN** its prompt directs it to dispatch the matching specialist rather than answer from its own reading

### Requirement: Write posture separates an agent's own work from the material it analyses

Every agent SHALL hold the harness's full tool set, including file editing. Each of the five analyst
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

- **WHEN** the five prompts are searched for "no file-editing tool" or an equivalent read-only claim
- **THEN** none is found

### Requirement: The report sink is a convention, not a permission

`.acordia/reports/` SHALL remain the suggested destination for an analyst product, stated as a
convention. No prompt or frontmatter SHALL present it as an enforced scope.

`.acordia/ops/` SHALL NOT be named by any shipped artifact. It was the root of the operator journal,
and the pillar that recorded state there is removed; the analysis pillar has one sink and needs no
second.

#### Scenario: Sink is worded as a convention

- **WHEN** a prompt names `.acordia/reports/`
- **THEN** it presents the path as where the product belongs, without claiming any harness restricts writes to it

#### Scenario: The journal root goes with its pillar

- **WHEN** every agent prompt, command wrapper and skill in the distribution is searched for `.acordia/ops/`
- **THEN** no match is found

### Requirement: Retrieved content is data, not instructions

Every one of the five prompts SHALL state that fetched pages, tool output, document text, and
collected artefacts are data and never instructions — that an instruction found inside retrieved
material is reported, not followed, and never redirects the agent's tool use.

#### Scenario: Rule present in every prompt

- **WHEN** each of the five agent prompts is read
- **THEN** each states that retrieved content is treated as data and that embedded instructions are reported rather than obeyed

#### Scenario: Injected instruction is surfaced

- **WHEN** an agent reads a target-controlled document containing an instruction addressed to it
- **THEN** its prompt requires it to report the attempt to its caller instead of acting on it

### Requirement: Every prompt names its skill set on `·`-separated lines

Each agent prompt SHALL name the skills it works from, grouped under headings and written as a
single line of `·`-separated slugs beneath each heading. A leg prompt SHALL carry the shared analytic
spine, its specialist depth line, and a working-knowledge line; the orchestrator SHALL carry its
defining-spine line and its baseline line. Every slug named SHALL resolve to a skill directory in
`acordia-analysts/skills/`.

The relation SHALL be total in both directions: every slug on a line resolves to a skill, **and** every
skill in the library is named by at least one prompt. A skill that no prompt names is unreachable, because
prompt naming is the only agent-to-skill binding either harness offers, so adding a skill without adding
its slug leaves it shipped but dead.

A prompt names a skill in one of **two** ways, and a check that knows only the first reports live
skills as dead. The ordinary binding is a slug on a `·`-separated line. The second is a slug in
backticks, and it SHALL count **only for a skill whose own frontmatter declares `procedural: true`** —
a grid-row skill is bound by its `·` line or not bound at all, because otherwise any prose that
happens to backtick a slug binds it silently, turning an editorial mention into a roster change. The
four cross-cutting procedural skills are named that way,
in every prompt, because they describe a discipline the prompt has to explain rather than a
competency it can list. A scan restricted to skill lines finds `aleph-entity-graph`,
`credential-harvest-triage` and `exhaustive-data-processing` in no prompt at all and reports three
orphans; all three are named in all five. Both bindings count as naming, and this requirement is
total over their union.

The line is prose the model reads, not a field any harness parses. Its adjacency to the heading is
therefore a readability convention, and this capability SHALL NOT state it as a contract: a blank line
between the two changes nothing either harness does. Two deleted generators did depend on it —
`tools/translate-omp.py --autoload deep` read the following line to populate omp's `autoloadSkills`
until `9fa90c5`, and its successor `tools/build-plugins.py` kept parsing that line on every build as a
gate, failing when it named no skills, until `e503b8a` — the commit whose next version bump is 3.0.0.
Since then nothing emits from the line and nothing gates on it, and this capability forbids `autoloadSkills`
outright.

A check of these lines SHALL locate them by heading text rather than by line position, and SHALL accept
the full set of heading texts in use: the three `CLAUDE.md` names, plus `## Your defining spine (deep)`
and `## Baseline you carry (working)`, which the orchestrator uses instead. A check written from
the three alone reports the orchestrator as broken while it is correct — the deleted
`tools/build-plugins.py` carried both depth variants for exactly this reason. A positional
check reports success when it can no longer find them: every slug line in the roster is separated from
its heading by a blank line, so a check keyed on position would silently inspect none while still
passing.

#### Scenario: Skill line shape holds

- **WHEN** a heading naming a skill group is read
- **THEN** the next non-empty line is a `·`-separated list of skill slugs with no other prose

#### Scenario: Every named slug resolves

- **WHEN** every slug named in every prompt is looked up in the pillar's `skills/`
- **THEN** each resolves to a directory containing `SKILL.md`

#### Scenario: Every skill is named somewhere

- **WHEN** every skill directory in the pillar is searched for in the pillar's prompts
- **THEN** each appears either on a prompt's skill line or in backticks in a prompt's procedural section

#### Scenario: A backticked grid-row slug does not bind

- **WHEN** a prompt's prose names a grid-row skill in backticks without carrying it on a `·`-separated line
- **THEN** that skill is not counted as named for the agent, because the backtick binding applies only where the skill declares `procedural: true`

#### Scenario: Group names and the orchestrator's spine are checked

- **WHEN** a declaration carries a group name outside `spine`/`deep`/`working`/`procedural`, or the orchestrator carries a `spine` group
- **THEN** the check reports it, rather than passing because the union of the groups is unchanged

#### Scenario: A procedural skill counts as named

- **WHEN** `aleph-entity-graph`, `credential-harvest-triage` and `exhaustive-data-processing` are searched for
- **THEN** each is found in backticks in a procedural section of all five prompts, and none is reported unreachable for being absent from a `·`-separated line

#### Scenario: A removed skill leaves no dangling slug

- **WHEN** a skill directory is deleted or merged away
- **THEN** its slug is removed from every prompt line naming it, in the same change

#### Scenario: Adjacency is not stated as a contract

- **WHEN** this capability and `CLAUDE.md` are searched for a requirement that the skill line sit immediately under its heading with no blank line
- **THEN** neither states one

#### Scenario: Every required heading is followed by a skill line

- **WHEN** each prompt's skill-group headings are located by their heading text
- **THEN** each is followed by a `·`-separated line before the next heading, and a prompt yielding none for a required heading is a failure

### Requirement: Analyst prompts carry the four cross-cutting sections

Each of the five analyst prompts SHALL carry a credential-harvest section naming
`credential-harvest-triage`, an exhaustive-processing section naming `exhaustive-data-processing`, an
Aleph-corpora section naming `aleph-entity-graph`, and a tool-discipline section stating that native
read/grep/glob are preferred and `bash` is for work no native tool fits. A leg SHALL state that it
cannot fan out and must surface an unfinished remainder to the orchestrator.

#### Scenario: Sections present

- **WHEN** any of the five analyst prompts is read
- **THEN** it carries credential-harvest, exhaustive-processing, Aleph-corpora and tool-discipline sections

#### Scenario: Leg surfaces a remainder instead of fanning out

- **WHEN** a slice is larger than a leg can finish
- **THEN** its prompt requires it to report the remainder to the orchestrator

### Requirement: Each agent declares what it returns

Every prompt SHALL carry a section stating its return contract. A leg SHALL state the product it
hands back, with confidence and named gaps where its judgement is analytic. An orchestrator SHALL
state that it composes the final product from its legs' returns rather than re-deriving them.

The orchestrator's product SHALL be addressed to a human operator who then acts on it. With no
executing agent in the distribution, a recommended course of action is a hand-off to a person rather
than a dispatch: the prompt SHALL state what the operator is being asked to decide or do, and the
end-neutral loop SHALL judge whether the end was achieved from evidence the operator reports back,
naming what evidence would settle the question, rather than from action the orchestrator took itself.

#### Scenario: Return contract present

- **WHEN** any agent prompt is read
- **THEN** it carries a section naming what it returns

#### Scenario: Orchestrator composes rather than re-derives

- **WHEN** an orchestrator receives a leg's product
- **THEN** its prompt directs it to compose from that product without redoing the leg's work

#### Scenario: The product names its human consumer

- **WHEN** `cyber-analyst`'s return contract is read
- **THEN** it hands a recommended course of action to the operator it advises, and directs no agent to
  execute any part of it

#### Scenario: The loop closes on reported evidence

- **WHEN** the orchestrator judges whether an action landed
- **THEN** its prompt has it judge from what the operator reports, naming the evidence that would
  settle it, rather than from an action it dispatched

### Requirement: Prompt bodies name no tool the harness lacks

No prompt body SHALL instruct an agent to call a tool that does not exist in the target harnesses.
Where a technique needs a capability the harness expresses differently, the prompt SHALL name the
portable form — a standard tool or an explicit shell invocation — instead of a harness-specific tool
name.

#### Scenario: No unavailable tool is named

- **WHEN** the five prompts are searched for tool names
- **THEN** every named tool exists in the target harnesses

### Requirement: A namespaced command wrapper for every dispatchable agent

The distribution SHALL ship 10 slash-command wrappers: one canonical wrapper named after each of the
five agents, plus five short aliases. All ten SHALL live in the pillar's flat
`acordia-analysts/commands/` directory, because a harness discovers plugin commands from
`<pluginRoot>/commands/*.md` without recursion and namespaces them by plugin name. Each wrapper SHALL
carry `description` and `argument-hint` frontmatter, SHALL dispatch exactly the agent it is named for,
SHALL pass the caller's argument through as the brief, and SHALL ask for a brief when none is supplied.

The canonical stems SHALL be the five agent names, and the aliases SHALL be `analyst`, `mission`,
`terrain`, `overwatch` and `collection`. An alias stem SHALL NOT equal any agent stem: the canonical
wrapper already holds that stem, so such an alias is a filename collision in one flat directory rather
than a second handle.

Where renaming a lead agent lengthens its canonical wrapper, the previous single-word wrapper SHALL be
retained as that agent's short alias, so that an existing invocation keeps working.

#### Scenario: Wrapper count and split

- **WHEN** the pillar's `commands/` directory is enumerated
- **THEN** ten wrappers are present, five canonical and five aliases, each a flat `.md` file, and no
  second `commands/` directory ships

#### Scenario: Wrapper dispatches its own agent

- **WHEN** any wrapper is read
- **THEN** it names exactly one agent, the one it is named or aliased for

#### Scenario: A renamed lead keeps its old handle

- **WHEN** `/analyst` is invoked
- **THEN** it dispatches `cyber-analyst`

#### Scenario: Empty brief is refused

- **WHEN** a wrapper is invoked with no argument
- **THEN** it asks what to look at before dispatching

#### Scenario: No alias collides with a canonical wrapper

- **WHEN** the ten wrapper stems are compared with the five agent names
- **THEN** all ten stems are distinct and no alias stem equals an agent name

### Requirement: Agent names and skill slugs stay unprefixed

Agent `name` values and skill slugs SHALL carry no `acordia-` prefix. Provenance SHALL be carried by
the description tag, the plugin name that namespaces commands, and the agent `color`, because the
name is the dispatch handle and the slug is bound to its folder.

#### Scenario: Names are bare

- **WHEN** the five agent names and every skill slug are read
- **THEN** none carries a distribution prefix

### Requirement: A prompt routes to a skill rather than restating its technique

An agent prompt SHALL carry the judgement its agent exists to make — the situation-to-technique
routing, the phase order, the return contract — and SHALL NOT restate technique detail that a skill
it names already carries. Where a prompt needs to reach a technique, it SHALL name the situation and
the owning skill on one line, in the form ``- **<situation>** → `<skill-slug>` ``.

Moving technique text out of a prompt SHALL NOT lose it: before a block leaves a prompt, every
command, payload, flag and table row in it SHALL be present in the destination skill, appended there
first where it is absent.

#### Scenario: Prompt names a skill instead of repeating it

- **WHEN** an agent prompt reaches a technique that a named skill carries
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

- **WHEN** every agent prompt body in the roster is measured
- **THEN** none exceeds 10,000 characters

### Requirement: A lead agent's name is distinct from its pillar's name

The pillar's lead agent SHALL NOT be named with a word that also names the pillar, its skill library,
its prompts or its artifacts. The analyst lead SHALL be `cyber-analyst`, so that "the analysis pillar"
and "the analyst prompts" can never be read as naming an agent.

Prose SHALL keep the bare word `operator` only where it means a human or a driving session rather than
the agent — the analyst guardrail *"execution belongs to the operators you advise"*, an operator
session, operator-deployed artifacts, and technique content such as a default-credential pair.
Removing the operations pillar strengthens that reading rather than weakening it: with no executing
agent in the distribution, every `operator` in a shipped prompt is the human the product is handed to.

An archived change SHALL NOT be rewritten to use a later name. It records what was true when it
shipped. A specification MAY quote a superseded name where it does so in order to forbid it, and a
provenance document MAY quote superseded wording in order to record its replacement; neither is a
site the rename sweep rewrites.

#### Scenario: Pillar word never resolves to an agent

- **WHEN** the five agent `name` values are compared with the words that name the pillar, its skill
  library, its prompts and its artifacts
- **THEN** no agent name is one of those words: `analysis` and `analyst` name the pillar and its
  material, while `cyber-analyst` names the agent

#### Scenario: The human sense survives the rename

- **WHEN** an analyst prompt's closing guardrail is read
- **THEN** it still says execution belongs to the operators it advises, naming no agent

#### Scenario: Archived changes keep their original names

- **WHEN** the archive is compared against its state before the rename
- **THEN** no occurrence of `operational-analyst` or `operator` in any pre-existing archived file has been rewritten, and the diff adds files without deleting lines

#### Scenario: A provenance document keeps its filename and its anchors

- **WHEN** `docs/roles/operational-analyst.md` is read
- **THEN** it is still that file, a closing note still records that the shipped agent is
  `cyber-analyst`, and every skill's grid reference resolves to a row by that row's own identifier
  rather than by a line number

### Requirement: A leg agent is named for the question it answers

Each analyst leg SHALL be named for the work its prompt leads with, not for the competency-grid
column it was derived from. The legs SHALL be `mission-analyst`, `terrain-analyst`,
`overwatch-analyst` and `collection-analyst`. A leg's prompt body SHALL introduce it under its own
name, so that a dispatched leg never identifies itself to the orchestrator under a name absent from
the roster.

The competency grid in `docs/roles/operational-analyst.md` SHALL keep the column set
`competency-map-derivation` fixes — *Core*, **Mission**, **Terrain**, **Def** and **Coll**. Where a
column label and a leg name now read as the same word, the column was relabelled to the leg's
question; the leg was not named after the column. **Def** ships as `overwatch-analyst`, which is where
the direction of naming stays visible. A column labels a leg of the role that document describes; it
does not name the agent file that implements the leg. The mapping between the two SHALL be recorded in
that document, and its placement is free, because a skill binds to a stable row identifier rather than
to a line number and no anchor shifts when the grid is edited.

A short alias SHALL be formed from its own agent's name — a word of that name, or a legible
contraction of it. An alias SHALL NOT outlive the name it was formed from: when an agent is renamed
and its alias no longer derives from the new name, the alias SHALL be renamed with it rather than
retained as a handle for vocabulary the roster has dropped. Where this rule and the lead-agent
retention rule above both bear on one alias, this rule governs: a handle is kept only if it still
derives from the renamed agent.

#### Scenario: No leg is named after a grid column

- **WHEN** the analyst `agents/` directory is enumerated
- **THEN** no filename contains `network` or `detection`, and each name states the leg's own question

#### Scenario: A leg introduces itself under its own name

- **WHEN** each leg prompt's opening line is read
- **THEN** it names the agent's own name, not a competency-grid column

#### Scenario: Old leg names are gone from the live tree

- **WHEN** the live tree outside `openspec/specs/` and `openspec/changes/` is searched for `target-network-analyst` or `defender-detection-analyst`
- **THEN** no match is found, the specifications being free to quote a superseded name in order to forbid it

#### Scenario: A shared word is the column following the leg

- **WHEN** the **Def** column is traced to the agent that implements it
- **THEN** it ships as `overwatch-analyst`, so a column label matching a leg name is the column taking
  the leg's question rather than the leg taking the column's label

#### Scenario: Every alias derives from its own agent

- **WHEN** the five short aliases are compared with the agents they dispatch
- **THEN** each alias is a word of its agent's name or a legible contraction of it, and none names a
  term absent from that agent's name

### Requirement: Every prompt opens with a heading naming its agent

Each agent prompt body SHALL open with a level-one heading formed from the prompt's lead sentence, so
that the first thing read is which agent this is. Where the opening paragraph carried more than one
sentence, the remainder SHALL follow the heading as prose rather than being deleted or folded into it.

The heading SHALL carry no trailing punctuation. It SHALL NOT replace the `description` frontmatter key,
which remains the dispatch signal. This is a readability convention for whoever opens the file; no
harness reads it.

The first scenario below keeps the title it was published under, though the roster it counts is now
five. OpenSpec matches a `MODIFIED` block's scenarios to the published spec by title and treats a
retitle as a dropped scenario, failing validation and refusing the archive, so the count that binds
is the one in the scenario body. Renumbering the title is a defect, not a tidy-up.

#### Scenario: All nine prompts open with a heading

- **WHEN** the body of each of the five agent prompts is read
- **THEN** its first non-empty line is a level-one heading naming that agent

#### Scenario: No heading ends in punctuation

- **WHEN** each prompt's opening heading is read
- **THEN** it ends in no full stop, comma, colon or semicolon

#### Scenario: The rest of the opening paragraph survives

- **WHEN** a prompt whose lead paragraph carried more than one sentence is read
- **THEN** the sentences after the first appear as prose beneath the heading

#### Scenario: The heading does not displace the description

- **WHEN** a prompt's opening heading is compared with its `description` frontmatter
- **THEN** the frontmatter still carries the pillar tag and the routing signal

### Requirement: Five agents, one pillar, one authored file each

The distribution SHALL ship exactly five agent files, all under `acordia-analysts/agents/`, each the
single editable source for every harness. They SHALL be `cyber-analyst.md`, `mission-analyst.md`,
`terrain-analyst.md`, `overwatch-analyst.md` and `collection-analyst.md`. Filename stem SHALL equal
frontmatter `name`. No generated or translated copy of an agent SHALL exist in the repository.

`acordia-operators/` SHALL NOT exist. Its five agent files are deleted with the pillar rather than
moved into this one: "Operations" is not an ACORDIA pillar, and a roster organised by target surface
is not derived from a competency the way this one is.

#### Scenario: Roster is complete and named

- **WHEN** the pillar's `agents/` directory is enumerated
- **THEN** exactly those five files are present, and each filename stem equals its frontmatter `name`

#### Scenario: No second copy of an agent exists

- **WHEN** the repository is searched for agent files carrying an ACORDIA description
- **THEN** the only matches are those five files

#### Scenario: The removed pillar leaves no agent behind

- **WHEN** the repository is searched for `acordia-operators/` and for agent files named
  `cyber-operator`, `web-application`, `mobile-application`, `cloud-security` or `internal-network`
- **THEN** neither the directory nor any of those files is present

### Requirement: The roster derives from the grid's five columns

The five agents SHALL be derived one-for-one from the five columns of the competency grid in
`docs/roles/operational-analyst.md` — *Core*, **Mission**, **Terrain**, **Def** and **Coll** — as
`cyber-analyst`, `mission-analyst`, `terrain-analyst`, `overwatch-analyst` and `collection-analyst`
respectively. A column no agent implements, or an agent no column derives, SHALL be a defect in one
of the two, resolved in the same change rather than left as a roster the grid does not account for.

`target-analyst` and `fusion-analyst` SHALL cease to exist. `target-analyst` SHALL split by the seam
its own prompt carried: the organisational half — what the target is for, what it depends on,
crown-jewels and mission-thread work, and the target's bureaucratic characteristics, redundancy and
reporting culture — becomes `mission-analyst`, and the technical half — networks, protocols, routing,
identity and directory, cloud control planes, web and application stacks, host internals,
vulnerability and attack-surface mapping, and operational technology where the target demands it —
becomes `terrain-analyst`.

`fusion-analyst` SHALL decompose three ways rather than be renamed: the operating picture and
multi-source correlation go to `cyber-analyst`, which already claimed to hold the target picture;
non-technical context integration goes to `mission-analyst`, whose subject it is; and the value and
quality of the collected take, data-integration and correlation tooling, and working bulk material at
volume go to `collection-analyst`. No agent SHALL inherit the whole of it, because the grid records
that leg as shallow-but-wide and it failed the grid's own separation criterion — a specialist is made
by the technical substrate it commands deeply enough to take apart from the inside.

The retirement SHALL be total in the shipped distribution: no agent file, command wrapper, dispatch
list, skill line or `description` names either retired agent. A specification MAY quote a retired name
in order to forbid it, and an archived change keeps the names it shipped with.

#### Scenario: Every column has an agent and every agent a column

- **WHEN** the grid's five columns are compared with `acordia-analysts/agents/`
- **THEN** the mapping is one-to-one in both directions, with no column unimplemented and no agent
  underived

#### Scenario: Neither retired leg survives in the live tree

- **WHEN** the live tree outside `openspec/` is searched for `target-analyst` or `fusion-analyst`
- **THEN** no match is found — no agent file, no wrapper, no orchestrator dispatch list, no skill line
  and no description

#### Scenario: The split is a division, not a rename

- **WHEN** the `mission-analyst` and `terrain-analyst` prompts are read side by side
- **THEN** the organisational half of the retired leg is in the first and the technical half in the
  second, and neither claims the other's depth

#### Scenario: The dissolved leg's work is placed, not dropped

- **WHEN** each of that leg's five unique deep competencies is traced into the new roster
- **THEN** multi-source correlation and the operating picture are the lead's, non-technical context
  integration is `mission-analyst`'s, and take value and data-integration tooling are
  `collection-analyst`'s

### Requirement: Each analyst's skill set is declared in a machine-readable file

The pillar SHALL carry `acordia-analysts/skill-sets.json`, declaring for every agent in the roster
the set of skills that agent works from, grouped as its prompt groups them: `spine`, `deep`,
`working`, and `procedural`. The orchestrator carries no `spine` group, because its `deep` group is
that spine.

The file SHALL be hand-maintained and SHALL NOT be generated at build or install time — there is no
build step, and a generated artifact would violate the one-authored-tree guarantee. The **agent
prompts remain the authority**: the declaration is a transcription of what each prompt names, and
where the two disagree the prompt is right and the declaration is the defect.

The declaration exists so a host can render a catalogue for **one** analyst rather than for the whole
library. A host injects name, description and location per skill against a finite character budget,
and a library that overruns that budget loses every description at once rather than dropping the
overrunning entry; role-scoping is the remedy, and role-scoping requires a mapping something other
than a human can read. That the correct mapping was already authored in prose is exactly why this is
a transcription and not a decision.

The file SHALL carry no version field. The version lives in three places and the count is checked;
a fourth occurrence would break that check while adding nothing, since the file ships and versions
with the pillar.

The declared set for each agent SHALL equal the set its prompt names, counting both bindings the
prompt uses: a slug on a `·`-separated skill line, and a slug named in backticks where that skill
declares `procedural: true`.

Naming covers **directing**, not only doing. The orchestrator declares the procedural skills it
routes to a leg, because it has to hold the discipline to judge what the leg returns — `cyber-analyst`
names `aleph-entity-graph` while sending corpus work to `collection-analyst`, and both declare it.

Group names SHALL be exactly `spine`, `deep`, `working` and `procedural`, and the orchestrator SHALL
carry no `spine` group. Both are invisible to a check that compares the union of the groups: a
misspelled group still unions to the right set of slugs while a host reading `deep` gets nothing. A declared slug SHALL resolve to a directory under `acordia-analysts/skills/`, and every
skill in the library SHALL be declared for at least one agent.

The `spine` group SHALL be identical across all four legs. It is the one group whose meaning is that
every analyst carries the same thing, so a leg whose spine differs is either a transcription error or
an undeclared change to what the spine is.

#### Scenario: Every agent is declared

- **WHEN** `skill-sets.json` and `acordia-analysts/agents/` are compared
- **THEN** the declared agent names are exactly the agent file stems, with no agent missing and none declared that has no file

#### Scenario: Declaration matches the prompt in both directions

- **WHEN** an agent's declared set is compared against the slugs its prompt names on skill lines and in procedural sections
- **THEN** the two sets are equal, and neither a slug declared but unnamed nor a slug named but undeclared is present

#### Scenario: Every declared slug resolves

- **WHEN** every slug in `skill-sets.json` is looked up under `acordia-analysts/skills/`
- **THEN** each resolves to a directory containing `SKILL.md`

#### Scenario: Every skill is declared for some agent

- **WHEN** every skill directory is searched for across all declared sets
- **THEN** each appears in at least one agent's declaration

#### Scenario: The shared spine is one set

- **WHEN** the `spine` groups of the four leg agents are compared
- **THEN** they are identical, and the orchestrator carries no `spine` group

#### Scenario: The declaration carries no version

- **WHEN** `skill-sets.json` is parsed
- **THEN** it declares no version field, and the repository still holds exactly three version occurrences across three files

### Requirement: Every prompt states a hand-back contract

Each of the five agent prompts SHALL state how its work returns across a dispatch boundary, in three
parts:

1. **The working is written down.** The full working — evidence with its identifiers, the queries and
   commands run, what was rejected and why, and what was deliberately not done — SHALL be written to
   a notes file in the task's working directory before the agent returns.
2. **What returns is bounded and self-describing.** The reply SHALL be a summary carrying the
   judgement, its confidence, the gaps that bound it, and **the name of the notes file** where the
   evidence lives.
3. **The bound is treated as real.** The prompt SHALL state that a read exceeding the bound is cut in
   transit without warning to either side, and that a read which does not fit means the question was
   too large — to be reported as such, naming what was left out, rather than handed back truncated.

The reason is that a delegated agent's reply is bounded in every harness this pillar targets, and the
bound is enforced by silent truncation: no error is raised, the child is not told its text was cut,
and the parent cannot see that it received a fragment. Files the child wrote are not carried back but
remain readable, so the durable half of the work SHALL travel by the filesystem and only the
judgement by the reply.

The bound SHALL be stated by the dispatching brief and SHALL NOT be written into any prompt as a
number. A count correct for one harness is wrong on every other, and a wrong number in a shipped
prompt is worse than none because it reads as authoritative.

#### Scenario: Contract present in every prompt

- **WHEN** each of the five agent prompts is read
- **THEN** each states that the full working goes to a notes file, that the reply is a bounded
  summary naming that file, and that the bound is treated as real

#### Scenario: No prompt hard-codes a limit

- **WHEN** the five prompts are searched for a character count, a token count or any other numeric
  reply limit
- **THEN** none is found, and each prompt attributes the bound to the dispatching brief

#### Scenario: A read that does not fit is reported, not truncated

- **WHEN** an analyst's read exceeds the bound its brief stated
- **THEN** its prompt requires it to say the question was too large and name what was left out,
  rather than return a summary that stops mid-sentence

#### Scenario: The summary can be followed to the evidence

- **WHEN** a lead receives a leg's reply
- **THEN** the reply names the notes file, and the lead can read the full working from it without
  re-dispatching

### Requirement: The orchestrator supplies the task directory and the bound

`cyber-analyst` SHALL state the task-directory convention: each task gets its own directory, named
with a short dated slug, holding a `README.md` that carries the originating request **verbatim**, the
date, and one line on what is being settled. The analysts' notes files belong in that same directory,
and the orchestrator SHALL read them before it fuses.

The directory SHALL be stated by the dispatching brief and SHALL NOT be written into any prompt as a
path. A lead and a sandboxed leg can reach one directory under two different names, so any absolute
path in a prompt is wrong on one side of that boundary.

`cyber-analyst` SHALL supply **both** the directory and the reply bound in every dispatch, alongside
the objective, operating logic, stage, tempo and risk tolerance it already carries. An unstated bound
is the orchestrator's defect and not the leg's, because a leg told nothing cannot size a reply it was
never given the size of.

The convention exists so an operation is navigable afterwards — by the human operator the pillar
hands its product to, or by the orchestrator itself once its own context has been compacted. The
request is kept verbatim because a paraphrase is already an analytic judgement, made at the moment
least is known.

#### Scenario: Convention stated in the lead prompt

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it states the per-task directory, the dated slug, the `README.md` holding the request
  verbatim with its date and what is being settled, and that the legs' notes go in the same directory

#### Scenario: Both are supplied on dispatch

- **WHEN** `cyber-analyst` dispatches any leg
- **THEN** its prompt requires the brief to state the working directory and the bound on the reply

#### Scenario: No path is baked into a prompt

- **WHEN** the five prompts are searched for an absolute task-directory path
- **THEN** none is found, and the directory is attributed to the dispatching brief

#### Scenario: The lead reads the notes before fusing

- **WHEN** the legs have returned and the orchestrator fuses their reads
- **THEN** its prompt requires it to read the notes files in the task directory, not to fuse from the
  bounded summaries alone
