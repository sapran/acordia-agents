## 1. Prompt

- [x] 1.1 Replace `## If you cannot dispatch` in `acordia-analysts/agents/cyber-analyst.md` with
      `## First, establish that you can dispatch`, carrying the positive check.
- [x] 1.2 Keep the refusal, the named entry route, the no-quiet-substitution rule and the
      `analyst-loop` pointer intact.
- [x] 1.3 Splice the new body into `commands/cyber-analyst.md` and `commands/analyst.md` byte-identically.

## 2. Ceiling

- [x] 2.1 Move the instrument-choice technique detail from the prompt into
      `acordia-analysts/skills/gain-loss-calculus/SKILL.md`, per the ceiling requirement's own remedy.
- [x] 2.2 Confirm the orchestrator body is under 10,500 characters.

## 3. Source of truth and specs

- [x] 3.1 Add the positive-guard paragraph to `docs/roles/operational-analyst.md`, citing Monte p. 60
      and Styran & Yashchuk p. 20.
- [x] 3.2 Modify the `agent-roster` requirement so it asserts the positive determination.
- [ ] 3.3 Sync the delta into `openspec/specs/agent-roster/spec.md`.
- [ ] 3.4 Remove the resolved parked finding from `docs/implementation-notes.md`.

## 4. Release

- [x] 4.1 Version `6.10.0` → `6.11.0` across the three manifests.
- [ ] 4.2 `openspec validate --all --strict` passes.
- [ ] 4.3 `~/ai/checks/check-acordia.sh` passes all eight checks.
- [ ] 4.4 A/B proof: the old guard does not fire without a `task` tool; the new one does.
