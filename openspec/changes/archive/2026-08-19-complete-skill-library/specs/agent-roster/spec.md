## MODIFIED Requirements

### Requirement: Every prompt names its skill set on `·`-separated lines

Each agent prompt SHALL name the skills it works from, grouped under headings and written as a
single line of `·`-separated slugs directly beneath each heading. An analyst prompt SHALL carry the
shared analytic spine, its specialist depth line, and a working-knowledge line; an operator prompt
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
