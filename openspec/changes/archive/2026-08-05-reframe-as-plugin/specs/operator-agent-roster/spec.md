## MODIFIED Requirements

### Requirement: Prompt names its skill set

Because opencode has no per-agent `skills:` field, each operator prompt SHALL name the operator-library skills it draws on, under a `## Your specialist depth (deep)` heading followed by a single `·`-separated line of skill names. The skills named SHALL exist in `operators/skills/`.

The single-line-under-the-heading shape remains load-bearing, but for a different reason than before. No emitter consumes the line any more — the generated omp agents leave `autoloadSkills` unset unconditionally, because a prebuilt plugin is installed by the harness rather than by a user-invoked command and so has no flag to carry. `tools/build-plugins.py` nonetheless parses the line on every build and SHALL fail when the heading is absent or the line names no skills, so the shape this requirement mandates cannot rot unnoticed.

#### Scenario: Deep heading present with a skill line

- **WHEN** any operator agent file is inspected
- **THEN** it contains a `## Your specialist depth (deep)` heading whose immediately following line is a non-empty `·`-separated list of skill names

#### Scenario: Named skills exist

- **WHEN** the skill names in any operator prompt are resolved against `operators/skills/`
- **THEN** every named skill has a directory with a `SKILL.md`

#### Scenario: A broken deep line fails the build

- **WHEN** an operator prompt's `(deep)` heading is removed, or the line beneath it is blanked
- **THEN** `tools/build-plugins.py` exits non-zero naming that source file
- **AND** no plugin tree is regenerated
