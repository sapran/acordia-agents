# analyst-agent-roster Specification

## ADDED Requirements

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
