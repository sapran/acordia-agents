## 1. Edit the orchestrator prompt body

- [x] 1.1 In `analysts/agents/operational-analyst.md`, strengthen the "You direct three specialists" dispatch prose so that dispatching the legs whose operating question the task touches is stated as a **precondition** of delivering a recommended course of action — grounded in "three technical reads feeding one analytic judgement" (`docs/roles/operational-analyst.md` L52). (spec: *Dispatch stated as a precondition, not an option*)
- [x] 1.2 Reframe the self-service clause ("if a piece of work fits none of them, do it yourself…") so self-service via native `read`/`grep`/`glob`/`list`/`bash` is bounded to work matching **no** leg's operating question plus trivial single-artefact lookups, and no longer reads as a co-equal alternative to dispatch for specialist questions. (spec: *Self-service is bounded to no-leg work*)
- [x] 1.3 Confirm the edit is additive to existing prose — no new H2 introduced; the `## Credential harvest`, `## Output discipline`, `## Tool discipline`, and `## Guardrails` sections are left intact.

## 2. Verify contracts preserved

- [x] 2.1 Diff the frontmatter of `operational-analyst.md`: the `edit`, `bash`, and `task` blocks, `mode: primary`, and the three-leg `task` whitelist are byte-unchanged (`git diff` on the frontmatter + `opencode debug agent operational-analyst`). (spec: *Dispatch topology and permissions unchanged*)
- [x] 2.2 Confirm the three leg files (`target-network-analyst.md`, `defender-detection-analyst.md`, `fusion-analyst.md`) are untouched and each `description` remains its italic operating question. (spec: *Leg descriptions unchanged*)
- [x] 2.3 Confirm `docs/roles/operational-analyst.md` and the competency grid are unchanged — the mandate traces to existing prose, so the source map and bijection are not modified.

## 3. Validate

- [x] 3.1 Run `openspec validate --all --strict` and resolve any errors.
- [x] 3.2 Read-through check: the body unambiguously routes specialist questions to the legs before a course of action, and bounds self-service — the four delta-spec scenarios are satisfied.
