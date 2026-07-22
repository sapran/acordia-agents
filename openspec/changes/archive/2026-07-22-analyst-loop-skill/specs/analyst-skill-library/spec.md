## ADDED Requirements

### Requirement: `analyst-loop` skill exists

The library SHALL contain a skill `analysts/skills/analyst-loop/SKILL.md` naming the end-neutral analytic loop — target-read (through the T&N leg), defender-read (through the Def leg), fusion (through the Fus leg), judgement (calibrated, via spine skills), next-move — as a first-class procedural cross-cutting skill.

The skill body SHALL contain: (a) a **cross-cutting notice** declaring the skill procedural and non-grid; (b) a **loop-shape** section naming the five steps in one sentence each; (c) a **loop-invariants** section stating end-neutrality (every pass reaches a judgement plus a next move), gap-naming on every judgement, calibrated confidence on every judgement, and passive posture; (d) a **where-this-runs** paragraph stating the loop is the orchestrator's workflow, and that a leg session matching this skill surfaces the need for a full pass back to the orchestrator rather than attempting the loop itself.

The skill's `description` SHALL be authored for trigger quality — stating WHEN to run the loop, not WHAT it is — so opencode's description-match selection fires cleanly on operator sessions asking for a fresh analytic round.

The skill SHALL declare its cross-cutting/procedural nature and SHALL NOT be added as a row to the competency grid. The `## Method` contract for evidence-reading skills (from `analyst-verifiability-anchors`) SHALL NOT apply — this skill reads no files.

#### Scenario: Loop skill loads from opencode

- **WHEN** opencode starts
- **THEN** `analyst-loop` is discovered from `~/.config/opencode/skills/` and is invokable

#### Scenario: Body carries the four required sections

- **WHEN** the loop skill is inspected
- **THEN** it contains a cross-cutting notice, a loop-shape section naming five steps, a loop-invariants section, and a where-this-runs paragraph

#### Scenario: Trigger-quality description

- **WHEN** an operator session asks for a fresh end-neutral analytic pass
- **THEN** `analyst-loop`'s `description` is specific enough for opencode to select it

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `analyst-loop`

#### Scenario: Orchestrator references the skill; legs do not

- **WHEN** `analysts/agents/operational-analyst.md` is inspected
- **THEN** it names `analyst-loop` in one sentence within its existing loop-describing paragraph

- **WHEN** any leg agent (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is inspected
- **THEN** it does not name `analyst-loop`
