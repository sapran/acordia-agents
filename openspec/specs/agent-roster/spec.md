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

### Requirement: Orchestrator fan-out follows real dependencies

`cyber-analyst` SHALL dispatch every independent, bounded specialist question without waiting for an unrelated specialist return. It MAY dispatch more than one instance of the same leg when it partitions a corpus or other input into disjoint, bounded slices. A specialist assignment SHALL name its question and input slice; the orchestrator SHALL retain responsibility for joining returns and SHALL NOT use fan-out to delegate that fusion.

A return SHALL block a later assignment only when the later assignment needs the return's information. In a directed credential sweep, Collection and Terrain orientation SHALL precede credential prioritisation, but their paired launch SHALL NOT imply a two-agent dispatch ceiling. Mission valuation SHALL wait only when it needs the oriented asset register, and Overwatch SHALL be dispatched when its operating question is independently material.

#### Scenario: Independent specialist questions fan out together

- **WHEN** an operation contains multiple independent, bounded specialist questions
- **THEN** the orchestrator's prompt directs it to dispatch them together rather than serialising them by roster order or a fixed pair

#### Scenario: One specialist receives disjoint slices

- **WHEN** a bounded corpus question requires more than one slice owned by the same specialist
- **THEN** the orchestrator's prompt permits multiple assignments to that specialist, each carrying a disjoint bounded slice

#### Scenario: A real dependency keeps its barrier

- **WHEN** a later specialist question requires an earlier return to define its input
- **THEN** the orchestrator's prompt directs it to read that return before dispatching the dependent question

#### Scenario: Lead retains fusion

- **WHEN** parallel specialist returns arrive
- **THEN** the orchestrator's prompt directs it to reconcile and fuse them itself rather than assigning the joined operating picture to a leg

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

It is one of the two sinks under the `.acordia/` workspace root, the other being `.acordia/work/`
for task directories. The two are siblings with distinct contents — finished product on one side,
the working behind it on the other — and a product SHALL be addressable from its working by the
shared stem rather than by a path recorded anywhere. That pairing is a property of the stem, so
where a brief names the working directory instead, the stem no longer carries it and the product's
location SHALL be recorded explicitly.

`.acordia/ops/` SHALL NOT be named by any shipped artifact. It was the root of the operator journal,
and the pillar that recorded state there is removed; the analysis pillar records no operation state
and needs no journal root, which is a separate question from how many sinks its workspace holds.

#### Scenario: Sink is worded as a convention

- **WHEN** a prompt names `.acordia/reports/`
- **THEN** it presents the path as where the product belongs, without claiming any harness restricts writes to it

#### Scenario: The journal root goes with its pillar

- **WHEN** every agent prompt, command wrapper and skill in the distribution is searched for `.acordia/ops/`
- **THEN** no match is found

#### Scenario: The product is reachable from its working

- **WHEN** a finished product exists in `.acordia/reports/` and the scheme, rather than a brief,
  named its task directory
- **THEN** its filename stem equals the name of the `.acordia/work/` directory the working was done
  in, so one is found from the other without a recorded path

#### Scenario: A briefed directory records the pairing instead

- **WHEN** a brief names the working directory, so its name is not the scheme's stem
- **THEN** the convention requires the product's location to be recorded explicitly, rather than
  leaving a reader to derive it from a stem that no longer carries it

### Requirement: `.acordia/` is the workspace root for an analyst's own files

Where a dispatch names no working directory, `.acordia/` SHALL be the root under which an analyst's
**own** generated files belong — notes, the
task `README.md`, working drafts, the credential file and the finished product alike — and not the
destination of the product alone. Every agent prompt SHALL give each kind of file it tells the agent
to write a destination under that root, naming the sink where the prompt states the instruction: a
prompt that directs notes, working files and drafts to a task directory SHALL name `.acordia/work/`
there, and a prompt that states where a finished product belongs SHALL name `.acordia/reports/`.
Naming both sinks names the root; a prompt is not required to repeat one sink in the section that
states the other. The root exists so that what the analyst writes stays out of the material it was
given to analyse, which is the same separation the write-posture requirement states from the other
side. Where a brief does name a directory, that directory SHALL be used exactly as given, per the
orchestrator requirement below, and this root SHALL NOT be taken to override it.

The root SHALL hold exactly two sinks:

- `.acordia/work/` — one directory per task, holding that task's `README.md`, notes, drafts and
  credential file.
- `.acordia/reports/` — the finished product.

A prompt SHALL NOT direct an analyst to create a working file, a notes file or a task directory in
the current directory, or in any location outside `.acordia/`, when its brief names no directory.
Writing beside the corpus is the outcome the root exists to prevent, so the brief-names-none case
SHALL resolve into `.acordia/work/` rather than into whatever directory the agent happens to be in.

Like the sink it contains, the root is a **convention and not a permission**. No prompt, frontmatter
or spec SHALL present it as an enforced scope, because no harness in the distribution restricts a
write to it and a claim otherwise would describe an enforcement that does not exist.

#### Scenario: The root covers working files, not only the product

- **WHEN** an agent prompt tells the agent to write a notes file, a working file or a draft
- **THEN** it gives that file a destination under `.acordia/` — the task directory under
  `.acordia/work/` — rather than leaving the parent unstated

#### Scenario: The product sink is still named

- **WHEN** an agent prompt states where a finished product belongs
- **THEN** it names `.acordia/reports/`, so the prompt names both sinks and therefore the root

#### Scenario: An unbriefed dispatch does not write beside the corpus

- **WHEN** a prompt or skill describes what to do when the brief names no working directory
- **THEN** it directs the agent to create the directory under `.acordia/work/`, and no prompt or
  skill instructs the agent to create it in the current directory or under a bare slug

#### Scenario: The root is worded as a convention

- **WHEN** a prompt or skill names `.acordia/` or either of its two sinks
- **THEN** it presents the path as where the material belongs, without claiming any harness
  restricts writes to it

### Requirement: A task directory and its product are addressed by corpus, then date

A task directory and the report produced from it SHALL share one stem of the form
`<corpus>-<YYYY-MM-DD>-<task-slug>`: the directory is `.acordia/work/<stem>/` and the product is
`.acordia/reports/<stem>.<ext>`. A date alone SHALL NOT be the sole discriminator in either name.
Where one task produces more than one product, each product's name SHALL carry the stem plus what
that product is, so the two do not contend for one filename.

The **corpus token** SHALL be derived from the material under analysis rather than from the wording
of the request, so that two differently-worded dispatches against one corpus address the same
directory. It SHALL be derived as:

- an Aleph collection's `foreign_id`, where the instance supplies one;
- otherwise a slug of that collection's label;
- for a file corpus, a slug of the name of the directory or archive analysed.

Where a stem is already taken — the same corpus, the same date and the same task slug — the new
directory SHALL take a numeric suffix (`-2`, `-3`) and its product SHALL take the same suffixed
stem. The convention SHALL be stated so that no run overwrites another run's directory or product,
and so that no analyst overwrites another's notes or credential file inside a task directory they
share — nothing enforces either, which is why both are stated.

The reason is stated rather than only the rule: a write to a colliding name **succeeds**. Nothing in
either harness detects it, so a sweep of a second corpus silently replaces the first day's product
and the loss surfaces only when a reader opens the report and finds the wrong corpus inside it.

#### Scenario: The stem carries the corpus ahead of the date

- **WHEN** a prompt or skill states how a task directory or a report file is named
- **THEN** it gives the form `<corpus>-<YYYY-MM-DD>-<task-slug>` and states that the report takes the
  same stem under `.acordia/reports/`

#### Scenario: The corpus token comes from the material

- **WHEN** the derivation of the corpus token is stated
- **THEN** it names the Aleph `foreign_id`, the collection label as its fallback, and the analysed
  directory or archive name for a file corpus — and does not derive the token from the request text

#### Scenario: Two corpora on one day do not collide

- **WHEN** two tasks run on the same date against two different corpora
- **THEN** their stems differ by the corpus token, and neither directory nor report overwrites the
  other

#### Scenario: A repeated run is suffixed rather than overwritten

- **WHEN** a task directory's stem is already taken
- **THEN** the convention states a numeric suffix for both the directory and its product, and states
  that a colliding write would otherwise succeed undetected

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

The credential-harvest section SHALL, in **all five** prompts including the orchestrator, name
`credential-harvest-triage` as the source of the handling rules, state that ownership is settled before
any other handling decision, and express the permission as a **closed grant** — what may be recorded —
rather than as a list of prohibitions, so that an ownership the prompt does not enumerate falls outside
the grant instead of through it.

Each of the **four legs** SHALL additionally state that a credential-reading command terminates in a
file write rather than in standard output; that values, and any command carrying one, are held in a
credential file named in the working notes rather than written inside them; and that a value never
enters what the leg hands back. A leg runs the extractions and writes the notes its caller later reads,
so these are leg-side rules.

The **orchestrator's** section SHALL state that it opens a leg's credential file only as a judgement
needs it rather than as part of the routine read it makes of that leg's notes, and that a product
carrying values is written rather than returned in a reply. It is the agent that correlates across legs
and writes the product, so it SHALL NOT be cut off from the values those two jobs require; the
distinction the prompt draws is between a deliberate read and an automatic one, not between permitted
and forbidden.

#### Scenario: Sections present

- **WHEN** any of the five analyst prompts is read
- **THEN** it carries credential-harvest, exhaustive-processing, Aleph-corpora and tool-discipline sections

#### Scenario: Leg surfaces a remainder instead of fanning out

- **WHEN** a slice is larger than a leg can finish
- **THEN** its prompt requires it to report the remainder to the orchestrator

#### Scenario: Every prompt states the credential routing rule

- **WHEN** each of the five prompts' credential-harvest section is read, the orchestrator's included
- **THEN** it names `credential-harvest-triage` as the source of the handling rules, requires ownership
  to be settled first, and states the permission as a closed grant of what may be recorded rather than
  as a list of prohibitions

#### Scenario: A leg states the extraction and credential-file rules

- **WHEN** each of the four leg prompts' credential-harvest section is read
- **THEN** it requires a credential-reading command to terminate in a file write rather than standard
  output, requires values and any command carrying one to be held in a credential file named in the
  working notes rather than written inside them, and forbids a value entering the hand-back

#### Scenario: A hand-back keeps values out of the notes

- **WHEN** the hand-back contract's written-working clause is read
- **THEN** a credential value, and a command carrying one in its arguments, is excepted from the notes
  file and written to the credential file the notes name

#### Scenario: The orchestrator states the rule rather than delegating it

- **WHEN** `cyber-analyst`'s credential-harvest section is searched for the routing rule
- **THEN** the rule is stated in the section itself and not left to the legs' prompts, and it permits
  the credential file a leg's notes name to be opened as a judgement needs it rather than as part of
  the routine notes read, with a product carrying values written rather than returned

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
carry `description` and `argument-hint` frontmatter, SHALL pass the caller's argument through as the
brief, and SHALL ask for a brief when none is supplied.

A wrapper SHALL resolve to exactly one agent, the one it is named or aliased for. **How it does so
depends on whether that agent dispatches.** A leg wrapper SHALL dispatch its agent as a subagent. A
lead wrapper SHALL instead carry its agent's prompt body into the invoking session, because a
dispatched agent cannot itself dispatch and the lead's work is directing four legs.

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
- **THEN** it resolves to exactly one agent, the one it is named or aliased for

#### Scenario: A leg wrapper dispatches, a lead wrapper carries

- **WHEN** a leg wrapper and a lead wrapper are compared
- **THEN** the leg wrapper dispatches its agent as a subagent, and the lead wrapper carries the agent's
  prompt body into the invoking session

#### Scenario: A renamed lead keeps its old handle

- **WHEN** `/analyst` is invoked
- **THEN** it enters `cyber-analyst`, carrying its prompt body into the invoking session

#### Scenario: Empty brief is refused

- **WHEN** a wrapper is invoked with no argument
- **THEN** it asks what to look at before proceeding

#### Scenario: No alias collides with a canonical wrapper

- **WHEN** the ten wrapper stems are compared with the five agent names
- **THEN** no alias stem equals any agent stem

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

No agent prompt body SHALL exceed 10,500 characters, measured after the frontmatter. A prompt that
crosses the ceiling SHALL be reduced by moving technique detail to the skill that owns it, never by
deleting the routing or the guardrails.

The ceiling SHALL be enforced by the repository's drift gate rather than by inspection. An unenforced
ceiling is how the orchestrator was allowed to sit at 9,921 of 10,000 characters with no signal, so
that a 353-character entry guard crossed it silently while every other invariant reported clean.

#### Scenario: Ceiling holds across the roster

- **WHEN** every agent prompt body in the roster is measured
- **THEN** none exceeds 10,500 characters

#### Scenario: A crossed ceiling fails the gate

- **WHEN** an agent prompt body exceeds the ceiling
- **THEN** the drift gate fails, naming the agent and its measured size

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

A lead wrapper's verbatim copy of the orchestrator body is not a second source and SHALL NOT be
edited directly: the agent file remains the only editable one, the copy is carried so that a session
entered through the wrapper holds the doctrine, and `tools/check-acordia.sh` fails when the two
diverge. A contributor changing the orchestrator edits `agents/cyber-analyst.md` and regenerates the
wrappers from it.

`acordia-operators/` SHALL NOT exist. Its five agent files are deleted with the pillar rather than
moved into this one: "Operations" is not an ACORDIA pillar, and a roster organised by target surface
is not derived from a competency the way this one is.

#### Scenario: Roster is complete and named

- **WHEN** the pillar's `agents/` directory is enumerated
- **THEN** exactly those five files are present, and each filename stem equals its frontmatter `name`

#### Scenario: No second copy of an agent exists

- **WHEN** the repository is searched for agent files carrying an ACORDIA description
- **THEN** the only matches are those five files

#### Scenario: A wrapper's carried copy is not a second editable source

- **WHEN** a lead wrapper's copy of the orchestrator body is compared with `agents/cyber-analyst.md`
- **THEN** they are byte-identical, and only the agent file is edited directly

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

Each of the five agent prompts SHALL state how its work returns across a dispatch boundary, in four
parts:

1. **The working is written down.** The full working — evidence with its identifiers, the queries and
   commands run, what was rejected and why, and what was deliberately not done — SHALL be written to
   a notes file in the task's working directory before the agent returns. A credential value, and a
   command carrying one in its arguments, SHALL be excepted from that file and written to the
   credential file beside it, which the notes name; otherwise the hand-back contract would put into
   the notes exactly what the credential rule keeps out of them, and the notes are the file a caller
   reads to fuse.
2. **What returns is bounded and self-describing.** The reply SHALL be a summary carrying the
   judgement, its confidence, the gaps that bound it, and **the name of the notes file** where the
   evidence lives.
3. **The bound is treated as real.** The prompt SHALL state that a read exceeding the bound is cut in
   transit without warning to either side, and that a read which does not fit means the question was
   too large — to be reported as such, naming what was left out, rather than handed back truncated.
4. **The contract holds when nothing supplies its inputs.** Every leg has a command wrapper that
   dispatches it straight from a person, so a leg may run with no orchestrator above it and a brief
   that names neither directory nor bound. Each prompt SHALL therefore address its reply to whoever
   dispatched it rather than to the lead by name; SHALL create a working directory and identify it by
   name when the brief names none; and SHALL keep the summary short, letting the notes carry the
   rest, when no bound is stated.

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

#### Scenario: A leg dispatched directly, with neither input supplied

- **WHEN** a person dispatches a leg through its command wrapper, which passes the brief alone and
  names no directory and no bound
- **THEN** its prompt still requires a notes file — in a directory the leg creates and identifies by
  name — and a short summary pointing at it, rather than a reply addressed to an absent lead

### Requirement: The orchestrator supplies the task directory and the bound

`cyber-analyst` SHALL state the task-directory convention: each task gets its own directory under
`.acordia/work/`, named and shaped as `briefing-reporting` states — the stem
`<corpus>-<YYYY-MM-DD>-<task-slug>`, and a `README.md` carrying the originating request
**verbatim**, the date, and one line on what is being settled. The prompt SHALL name the parent
itself, because that is the part whose absence sends an unbriefed task into the current directory,
and SHALL defer the stem and the `README.md` shape to the skill rather than restating them, per the
requirement that a prompt routes to a skill instead of restating its technique. The analysts' notes
files belong in that same directory, and the orchestrator SHALL read them before it fuses.

Where the orchestrator's own brief names a directory, it SHALL use that directory exactly as given
and SHALL NOT substitute a path of its own: a lead and a sandboxed leg can reach one directory under
two different names, so a constructed path is wrong on one side of that boundary. Where the brief
names none, the orchestrator SHALL create one under `.acordia/work/` with that stem and state where
it is, so the convention has a defined outcome in both cases rather than only when a deployment
supplies the input.

No **absolute or deployment-specific** directory path SHALL be written into any prompt: such a path
is exactly what a brief exists to supply, and baking one in is wrong on one side of a sandbox
boundary. The relative convention roots `.acordia/work/` and `.acordia/reports/` are not paths of
that kind and SHALL be named in the prompts, because a convention nobody states resolves to the
current directory by default.

`cyber-analyst` SHALL supply **both** the directory and the reply bound in every dispatch, alongside
the objective, operating logic, stage, tempo and risk tolerance it already carries. An unstated bound
is the orchestrator's defect and not the leg's, because a leg told nothing cannot size a reply it was
never given the size of.

The convention exists so an operation is navigable afterwards — by the human operator the pillar
hands its product to, or by the orchestrator itself once its own context has been compacted. The
request is kept verbatim because a paraphrase is already an analytic judgement, made at the moment
least is known. The corpus token is part of the name for the same reason: a directory identified only
by its date is navigable on the day it was made and ambiguous on every day after.

#### Scenario: Convention stated in the lead prompt

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it states the per-task directory under `.acordia/work/`, names `briefing-reporting` as
  carrying that directory's shape, and states that the legs' notes go in the
  same directory

#### Scenario: Both are supplied on dispatch

- **WHEN** `cyber-analyst` dispatches any leg
- **THEN** its prompt requires the brief to state the working directory and the bound on the reply

#### Scenario: No path is baked into a prompt

- **WHEN** the five prompts are searched for an absolute or deployment-specific task-directory path
- **THEN** none is found, and the specific directory is attributed to the dispatching brief while the
  relative convention root is stated

#### Scenario: The lead reads the notes before fusing

- **WHEN** the legs have returned and the orchestrator fuses their reads
- **THEN** its prompt requires it to read the notes files in the task directory, not to fuse from the
  bounded summaries alone

### Requirement: The orchestrator is entered by a route that leaves it able to dispatch

`cyber-analyst` exists to direct four legs, so any route that delivers its doctrine while removing its
ability to dispatch delivers a lead that cannot lead. The pillar's lead wrappers SHALL therefore carry
the orchestrator's prompt body into the invoking session rather than instruct a harness to dispatch the
orchestrator as a subagent. A wrapper SHALL NOT describe switching a session to an agent, because no
harness the pillar targets provides that operation.

The orchestrator's prompt body SHALL appear byte-identically in `agents/cyber-analyst.md` and in every
wrapper that carries it. The repository SHALL carry its own drift gate at `tools/check-acordia.sh`,
and that gate SHALL fail when they diverge, in the same manner as the byte-identity check on the two
marketplace catalogs. The gate travels with the files it guards: three hand-maintained copies of a
prose body, where a partial edit still parses and still reads plausibly, are only defensible when a
fresh clone inherits the check along with the duplication.

#### Scenario: A lead wrapper carries the doctrine rather than delegating it

- **WHEN** a lead wrapper is read
- **THEN** it contains the orchestrator's prompt body, and instructs no harness to dispatch the
  orchestrator as a subagent

#### Scenario: No wrapper claims a session can become an agent

- **WHEN** any command wrapper in the pillar is read
- **THEN** it describes no operation that switches the current session to a named agent

#### Scenario: Wrapper and agent bodies are checked for drift

- **WHEN** a lead wrapper's copy of the orchestrator body differs from `agents/cyber-analyst.md`
- **THEN** the drift gate fails, naming the wrapper and the divergence

### Requirement: The orchestrator establishes its dispatch capability positively

The orchestrator SHALL determine whether it can dispatch, and report that determination, before any
other work. Its prompt SHALL direct it to enumerate its own tools, look for the dispatch tool by name,
and open with an explicit verdict — available or unavailable — read from what it holds rather than from
what it expects to hold. An orchestrator that finds itself unable to dispatch has been entered by the
wrong route: it SHALL then stop and report that, naming the correct route, rather than proceeding to do
the legs' work itself.

The guard SHALL NOT be phrased as a condition on the absence of a tool. A guard so phrased does not
fire: a dispatched orchestrator enumerated its tools, held no dispatch tool, and produced 391,251
characters without once reaching for the guard, because a model does not notice an absence it was not
asked to look for. The failure this prevents is silent in both directions — a dispatched orchestrator
receives its full doctrine, keeps every other tool, and produces a confident product assembled from no
specialist reads.

#### Scenario: Orchestrator states its verdict before working

- **WHEN** `cyber-analyst` begins any session
- **THEN** its prompt directs it to enumerate its tools and open with an explicit dispatch verdict,
  before analysis, dispatch or any other work

#### Scenario: Orchestrator entered as a subagent

- **WHEN** `cyber-analyst` is dispatched as a subagent and cannot spawn further agents
- **THEN** its prompt directs it to stop and report the wrong entry route rather than continue as a lead

#### Scenario: Refusal names the working route

- **WHEN** the orchestrator reports that it cannot dispatch
- **THEN** it names the command wrapper as the route that leaves it able to

#### Scenario: The verdict is read, not assumed

- **WHEN** the orchestrator reports that it can dispatch
- **THEN** its prompt requires that verdict to come from the tools it observed holding, not from the
  capability its role implies

### Requirement: A carried brief is framed as material, not instruction

A wrapper that carries doctrine into the invoking session interpolates the caller's brief into the same
document as that doctrine, at its end, where recency weights it most heavily. The wrapper SHALL
therefore label the brief as material to act on rather than instructions to obey, and SHALL state
before the brief appears that a directive found inside it — to change the doctrine, the entry route, or
tool use — is reported to the caller rather than followed. This extends the retained guardrail on
retrieved content, which names fetched pages and tool output but not the brief.

#### Scenario: Brief is labelled as material

- **WHEN** a lead wrapper is read
- **THEN** the brief is introduced as material rather than instruction, and the sentence saying so
  appears before the interpolation point

### Requirement: Directed credential collection requires orientation first

Before `cyber-analyst` issues a directed credential-sweep brief for an Aleph-backed collection, it SHALL obtain and read a current orientation return covering carried operational knowledge and technical terrain. It SHALL then obtain or derive the mission/value read for the discovered assets, fuse those reads itself, and include the resulting asset-and-credential hypothesis register in the credential brief. Credential extraction SHALL NOT be the first substantive search when this orientation is available and relevant.

Across shipped runtime doctrine the packet SHALL be enumerated once, in `credential-harvest-triage`. The orchestrator prompt SHALL name that skill rather than restate the packet's contents. This spec remains the packet's normative contract.

#### Scenario: Lead dispatches orientation before credential work

- **WHEN** a directed credential sweep is requested against an Aleph-backed collection
- **THEN** `cyber-analyst` dispatches Collection and Terrain orientation work before issuing credential-sweep instructions, and reads their notes before credential prioritisation

#### Scenario: Orientation packet reaches the credential brief

- **WHEN** the lead has read the orientation returns
- **THEN** the credential brief carries scoped collections, corpus state, asset/system classes, non-secret fingerprints, evidence and provenance, observed/inferred status, freshness, confidence, mission relevance, expected credential forms, planned specialist owners, named mission/value gaps, exposure, and omissions

#### Scenario: Runtime doctrine enumerates the packet once

- **WHEN** the orchestrator prompt and `credential-harvest-triage` are read together
- **THEN** the packet is enumerated in the skill, and the orchestrator names the skill rather than restating its contents

#### Scenario: Incomplete orientation blocks prioritisation

- **WHEN** the Aleph orientation return is missing or lacks the fields required for credential scoping
- **THEN** the lead reports the missing fields and requests bounded orientation work rather than presenting generic credential priorities as a completed plan

### Requirement: Orientation returns are role-specific

For an orientation-first credential sweep, `collection-analyst` SHALL return carried-memory and Aleph-corpus state; `terrain-analyst` SHALL return a non-secret technical asset register; and `mission-analyst` SHALL return asset-to-mission and crown-jewel valuation. The orchestrator SHALL fuse these returns; no leg SHALL claim the fused operating picture.

#### Scenario: Collection returns prior knowledge and corpus shape

- **WHEN** Collection performs the pre-credential orientation
- **THEN** its notes identify prior assets, aliases, searches, rejected hypotheses, stale or contradictory facts, collection provenance, freshness, coverage limits, and the explicit no-memory state when no prior notes exist

#### Scenario: Terrain returns asset hypotheses before extraction

- **WHEN** Terrain performs the pre-credential orientation
- **THEN** its notes identify observed or inferred system classes and non-secret fingerprints, attach Aleph provenance and entity ids, state freshness and confidence, list likely credential forms, and distinguish asset clues from credential findings

#### Scenario: Mission returns value before ranking

- **WHEN** Mission receives the technical asset register
- **THEN** its return maps assets to mission threads, organisational processes or crown jewels and states the value, uncertainty and information that would change the ranking

### Requirement: Mission Analyst owns target sustainment analysis

`mission-analyst` SHALL own the organisational sustainment read: whether the target can continue its mission through suppliers and contractors, stock and spares, transport and distribution, maintenance and repair, trained personnel, and external services. The prompt SHALL name `target-sustainment-analysis` as deep skill and state that it hands back an evidenced sustainment judgement, not a recommended action.

The read SHALL remain bounded by the Mission Analyst’s organisational remit. It SHALL not claim Terrain’s technical dependency analysis, create a sixth analyst, or encompass digital supply-chain analysis.

#### Scenario: The Mission prompt names the sustainment competency
- **WHEN** the Mission Analyst deep-skill line and `skill-sets.json` declaration are compared
- **THEN** each contains `target-sustainment-analysis`, and no other analyst’s deep or working declaration gains it

#### Scenario: The hand-back remains analytical
- **WHEN** the Mission Analyst returns a sustainment read
- **THEN** it states the sustainment judgement, confidence, evidence gaps, and notes location without ranking interventions or directing action

### Requirement: The orchestrator works while its legs run and joins before it ends

`cyber-analyst` SHALL treat waiting on a dispatched leg as the residual case rather than its default posture. Before re-entering a wait, its prompt SHALL direct it to perform the analysis available to it without a pending return — verifying returns already in hand, establishing the size and shape of the corpus, naming the gaps its legs are not covering, and revising the operating picture — and SHALL name `maintaining-operating-picture` as the skill that owns that work. Waiting SHALL be what the orchestrator does when no such work remains.

`cyber-analyst` SHALL NOT end a session while a leg it dispatched is still running. Its prompt SHALL direct it either to collect that leg's return, or to cancel the leg explicitly and record in its product what the cancellation gave up. A leg's work ending without either SHALL be treated as a loss rather than a completion.

Every specialist assignment `cyber-analyst` issues SHALL name the agent it is for. The prompt SHALL state this as a positive property of an assignment rather than as a prohibition on omission, because an assignment that names no agent is served by a general-purpose worker without an analyst's doctrine and reports no error.

This requirement governs the interval after dispatch and the boundary at session end. It does not restate `Orchestrator fan-out follows real dependencies`, which governs which questions are dispatched and when.

#### Scenario: Waiting is named as the residual case

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it directs the orchestrator to do the analysis available without a pending return before re-entering a wait, and names `maintaining-operating-picture` as the skill owning that work

#### Scenario: A leg still running blocks session end

- **WHEN** the orchestrator is about to end a session and a dispatched leg has not returned
- **THEN** its prompt directs it to collect the return or to cancel the leg explicitly

#### Scenario: A cancelled leg's loss is recorded

- **WHEN** the orchestrator cancels a leg before that leg returns
- **THEN** its prompt directs it to record in its product what the cancellation gave up

#### Scenario: Every assignment names its agent

- **WHEN** the orchestrator issues a specialist assignment
- **THEN** its prompt states that an assignment names the agent it is for, as a property the orchestrator checks before sending rather than as a prohibition on omitting a field

#### Scenario: The doctrine reaches every surface carrying the orchestrator body

- **WHEN** the orchestrator body is read from the agent file or from either lead command wrapper
- **THEN** all three carry this doctrine byte-identically
