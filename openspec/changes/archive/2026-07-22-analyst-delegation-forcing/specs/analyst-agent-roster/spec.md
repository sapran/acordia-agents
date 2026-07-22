## ADDED Requirements

### Requirement: Primary prompt compels leg dispatch before a course of action

The role model defines the orchestrator's recommended course of action as **"three technical reads feeding one analytic judgement"** (`docs/roles/operational-analyst.md` L52; "How the pieces fit" L48–52). To encode that faithfully, the `operational-analyst` prompt **body** SHALL compel dispatch of every leg subagent whose operating question the task touches **before** the orchestrator delivers a recommended course of action — not merely state that it *can* dispatch (which the existing "Orchestrator dispatches a leg" scenario already establishes at the permission level).

The prompt body SHALL bound **self-service** — the orchestrator using its own `read` / `grep` / `glob` / `list` / `bash` in place of a leg — to work that matches **no** leg's operating question, plus trivial single-artefact lookups. It SHALL NOT present self-service as a co-equal alternative to dispatch for questions that fall to a specialist.

This mandate SHALL be realised in the **prompt body only**. It SHALL NOT alter the `task` whitelist, the `edit` / `bash` permission blocks, `mode`, or any leg `description`; it SHALL add no grid row and no new skill. It complements — does not replace — the existing "Primary orchestrator, subagent legs" requirement.

#### Scenario: Dispatch stated as a precondition, not an option

- **WHEN** the `operational-analyst.md` prompt body is inspected
- **THEN** it states that the legs whose operating question the task touches are dispatched **before** a recommended course of action is delivered, rather than presenting dispatch as one option among several

#### Scenario: Self-service is bounded to no-leg work

- **WHEN** the prompt body's self-service clause is read
- **THEN** it limits the orchestrator's own `read`/`grep`/`glob`/`list`/`bash` reads to work matching no leg's operating question (and trivial single-artefact lookups), rather than offering self-service as a co-equal path for specialist questions

#### Scenario: Dispatch topology and permissions unchanged

- **WHEN** `operational-analyst`'s `task`, `edit`, and `bash` permission blocks and `mode` are compared before and after the amendment
- **THEN** they are unchanged — the three-leg `task` whitelist (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) is intact and `mode` remains `primary`

#### Scenario: Leg descriptions unchanged

- **WHEN** each leg subagent's `description` is compared before and after the amendment
- **THEN** it remains the italic operating question of that leg (the routing signal surfaced to the model is untouched)
