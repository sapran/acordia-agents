## 1. Amend the spec before touching any prompt

- [x] 1.1 Sync the `analyst-agent-roster` delta into `openspec/specs/analyst-agent-roster/spec.md`: five MODIFIED requirements, one of them renamed from "Primary prompt compels leg dispatch before a course of action" to "Primary prompt defaults to leg dispatch". No requirement added or removed.
- [x] 1.2 Sync the `omp-harness-distribution` delta into `openspec/specs/omp-harness-distribution/spec.md`: `color` derivation added to the frontmatter translation contract; the prompt-text correction requirement restated to match enforced behaviour.
- [x] 1.3 Run `openspec validate --all --strict` and confirm it passes before opening any agent file.

## 2. Relax the CLAUDE.md format contracts

- [x] 2.1 Restate the `## Credential harvest` bullet as a one-line reference to `credential-harvest-triage`, with the skill named as the carrier of the full procedure.
- [x] 2.2 Add a bullet recording that `## Exhaustive data processing`, `## What to return`, and `## Output discipline` are advisory prose — principles and defaults, not schemas or mandatory return formats.

## 3. Rewrite the four agent prompt bodies

- [x] 3.1 `operational-analyst.md` — tighten the identity paragraphs; replace the mandatory-dispatch paragraph with dispatch-as-default plus self-service-as-alternative; cut `## Tool discipline` to one line; cut `## Exhaustive data processing` to the principle plus the skill name; cut `## Credential harvest` to a one-line skill reference; restate `## Output discipline` as the fusion principle; add the omp write-surface note to `## Guardrails`. (spec: *Primary prompt defaults to leg dispatch*, *Primary declares output discipline*)
- [x] 3.2 `target-network-analyst.md` — one-line tool discipline; credential harvest cut to the triage reference plus its credential-adjacent skills; exhaustive processing cut to the principle plus overflow; `## What to return` cut to hypothesis / confidence / gaps; omp write-surface note in guardrails. (spec: *Leg subagents declare what they return*)
- [x] 3.3 `defender-detection-analyst.md` — same trims, keeping the operation-owned vs. target-owned lens in `## Credential harvest` and the go-quiet / move / pull-out call in `## What to return`.
- [x] 3.4 `fusion-analyst.md` — same trims, keeping the correlation-plus-`assessing-take-value` roll-up in `## Credential harvest`.
- [x] 3.5 Confirm every rewrite left the frontmatter, the identity paragraphs, and the four skill-set headings with their `·`-separated lines byte-unchanged — no blank line introduced between a `(deep)` heading and its skill line.

## 4. Patch the omp translator

- [x] 4.1 In `tools/translate-omp.py`, derive `color` from `metadata.acordia` (`leg` or `role` reading `orchestrator` → `cyan`, anything else → `blue`) and emit it in the generated frontmatter. (spec: *Orchestrator and legs are visually distinguishable*)
- [x] 4.2 Correct the comment on `TOOL_DISCIPLINE_SRC`/`TOOL_DISCIPLINE_OMP`: after the prompt trim these are a legacy-wording fallback, not a paragraph byte-identical across all four analyst files. (spec: *Unrecognised Tool-discipline wording is not an error*)

## 5. Verify

- [x] 5.1 `python3 tools/translate-omp.py analysts/agents/*.md --autoload deep --outdir <tmp>` produces four files without error, and no `list` assertion fires.
- [x] 5.2 The four translated `autoloadSkills` arrays are identical to the pre-change output.
- [x] 5.3 Each translated file carries `color: cyan` (orchestrator) or `color: blue` (legs).
- [x] 5.4 Every required H2 still exists in every agent: `## Credential harvest` ×4, `## Exhaustive data processing` ×4, `## What to return` ×3, `## Output discipline` ×1.
- [x] 5.5 All four agents contain the "Under OMP" write-surface line in `## Guardrails`.
- [x] 5.6 Prompt bodies shrink by ~40–50% in total word count; `git diff` shows no frontmatter or permission-block change.
- [x] 5.7 `openspec validate --all --strict` passes after every edit.
