## MODIFIED Requirements

### Requirement: Every prompt names its skill set on `·`-separated lines

Each agent prompt SHALL name the skills it works from, grouped under headings and written as a
single line of `·`-separated slugs beneath each heading. An analyst prompt SHALL carry the
shared analytic spine, its specialist depth line, and a working-knowledge line; an operations prompt
SHALL carry its own equivalent depth and working-knowledge lines. Every slug named SHALL resolve to a
skill directory in the same pillar.

The relation SHALL be total in both directions: every slug on a line resolves to a skill, **and** every
skill in the pillar is named on at least one line. A skill that no prompt names is unreachable, because
these lines are the only agent-to-skill binding either harness offers, so adding a skill without adding
its slug leaves it shipped but dead.

The line is prose the model reads, not a field any harness parses. Its adjacency to the heading is
therefore a readability convention, and this capability SHALL NOT state it as a contract: a blank line
between the two changes nothing either harness does. Two deleted generators did depend on it —
`tools/translate-omp.py --autoload deep` read the following line to populate omp's `autoloadSkills`
until `9fa90c5`, released at 2.4.0, and its successor `tools/build-plugins.py` kept parsing that line
on every build as a gate, failing when it named no skills, until `e503b8a`, released at 3.0.0. Since
3.0.0 nothing emits from the line and nothing gates on it, and this capability forbids `autoloadSkills`
outright.

A check of these lines SHALL locate them by heading text rather than by line position. A positional
check reports success when it can no longer find them: all 196 slug occurrences sat directly under
their heading before this change and all 196 are separated by a blank line after it, so a check keyed
on position would silently inspect none while still passing.

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

#### Scenario: Adjacency is not stated as a contract

- **WHEN** this capability and `CLAUDE.md` are searched for a requirement that the skill line sit immediately under its heading with no blank line
- **THEN** neither states one

#### Scenario: Every required heading is followed by a skill line

- **WHEN** each prompt's skill-group headings are located by their heading text
- **THEN** each is followed by a `·`-separated line before the next heading, and a prompt yielding none for a required heading is a failure

## ADDED Requirements

### Requirement: Every prompt opens with a heading naming its agent

Each agent prompt body SHALL open with a level-one heading formed from the prompt's lead sentence, so
that the first thing read is which agent this is. Where the opening paragraph carried more than one
sentence, the remainder SHALL follow the heading as prose rather than being deleted or folded into it.

The heading SHALL carry no trailing punctuation. It SHALL NOT replace the `description` frontmatter key,
which remains the dispatch signal. This is a readability convention for whoever opens the file; no
harness reads it.

#### Scenario: All nine prompts open with a heading

- **WHEN** the body of each of the nine agent prompts is read
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
