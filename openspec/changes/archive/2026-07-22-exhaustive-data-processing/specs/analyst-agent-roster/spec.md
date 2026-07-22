## ADDED Requirements

### Requirement: Exhaustive-processing section in every agent prompt

Every analyst agent prompt SHALL carry a named `## Exhaustive data processing` H2 section describing that agent's role in processing bulk collected material in full rather than sampling its opening portion, and SHALL name the `exhaustive-data-processing` skill. The section SHALL be additive — existing sections (defining spine, baseline, dispatch topology, tool discipline, output discipline, credential harvest, what-to-return, guardrails) are not rewritten. No permission change SHALL result from this addition.

The primary orchestrator's section SHALL state that exhaustive coverage is a **precondition** for a recommended course of action (script-first over the whole input before any judgement), and that the orchestrator **owns coverage reconciliation** — it rejects any leg return whose coverage receipt does not reconcile to the slice it was dispatched, and re-dispatches or sub-partitions rather than compiling a sampled result.

Each leg's section SHALL state that the leg never samples its assigned slice, script-exhausts it, emits a coverage receipt (declared scope reconciled to covered scope) alongside its `## What to return` surface, and — because a leg is `task: deny` and cannot fan out — surfaces any un-processable overflow back to the orchestrator for sub-partition rather than sampling it.

#### Scenario: Section present in all four agents

- **WHEN** any of the four analyst agent files is inspected
- **THEN** it contains a `## Exhaustive data processing` H2 section that names `exhaustive-data-processing`

#### Scenario: Primary states precondition and owns reconciliation

- **WHEN** `operational-analyst`'s exhaustive-processing section is read
- **THEN** it states that exhaustive coverage precedes a recommended course of action and that the orchestrator rejects any leg return whose coverage receipt does not reconcile to its dispatched slice, re-dispatching or sub-partitioning instead

#### Scenario: Each leg never samples and surfaces overflow

- **WHEN** any leg agent's exhaustive-processing section is read
- **THEN** it states the leg script-exhausts its slice, emits a coverage receipt, and surfaces un-processable overflow back to the orchestrator rather than sampling — and does not itself fan out

#### Scenario: Permissions unchanged

- **WHEN** the frontmatter of any analyst agent is compared before and after the amendment
- **THEN** `edit`, `bash`, and `task` permission blocks are unchanged, and the orchestrator's three-leg `task` whitelist is intact
