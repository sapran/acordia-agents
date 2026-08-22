## ADDED Requirements

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

## MODIFIED Requirements

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
