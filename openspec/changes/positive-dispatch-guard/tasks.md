## 1. Prompt

- [x] 1.1 Replace `## If you cannot dispatch` in `acordia-analysts/agents/cyber-analyst.md` with
      `## First, establish that you can dispatch`, carrying the positive check.
- [x] 1.2 Keep the refusal, the named entry route, the no-quiet-substitution rule and the
      `analyst-loop` pointer intact.
- [x] 1.3 Splice the new body into `commands/cyber-analyst.md` and `commands/analyst.md` byte-identically.

## 2. Ceiling

- [x] 2.1 Move the instrument-choice technique detail from the prompt into
      `acordia-analysts/skills/gain-loss-calculus/SKILL.md`, per the ceiling requirement's own remedy,
      carrying the substitute / complement / support definitions across rather than only the names.
- [x] 2.2 Add `doctrine_source: [Campaigning]` to that skill — the triad is a registered doctrinal
      claim (`docs/roles/sources.md:32`), and moving it into a skill body activates the provenance
      contract that did not apply while it sat in a prompt.
- [x] 2.3 Move the working-directory convention into `briefing-reporting`, which owns product shape.
- [x] 2.4 Confirm the orchestrator body is under 10,500 characters.

## 2a. Review findings closed

- [x] 2a.1 Lift the fusion sentence and the `analyst-loop` pointer out of the `If unavailable` branch
      into an unconditional paragraph — as written, the lead's core loop doctrine applied only on the
      branch where it had been told to stop. This was the reviewed change reintroducing its own defect.
- [x] 2a.2 Name the dispatch tool in both harness spellings (`task`/`Task`); a false `unavailable` in a
      genuine top-level session is a worse failure than the silence being fixed.
- [x] 2a.3 Name the verdict in `## What you return` so it reaches the caller rather than living only in
      the agent's own transcript.

## 3. Source of truth and specs

- [x] 3.1 Add the positive-guard paragraph to `docs/roles/operational-analyst.md`, citing Monte p. 60
      and Styran & Yashchuk p. 20.
- [x] 3.2 Modify the `agent-roster` requirement so it asserts the positive determination.
- [x] 3.3 Sync the delta into `openspec/specs/agent-roster/spec.md`.
- [x] 3.4 Remove the resolved parked finding from `docs/implementation-notes.md`.

## 4. Release

- [x] 4.1 Version `6.11.0` → `6.12.0` across the three manifests.
- [x] 4.2 `openspec validate --all --strict` passes.
- [x] 4.3 `~/ai/checks/check-acordia.sh` passes all eight checks.
- [x] 4.4 A/B run — **result partly negative, recorded in the PR.** Two arms (cold read; and prompt as
      system prompt via `claude -p --system-prompt-file` with `--disallowed-tools Task`). The old guard
      **fired in both**, so the "never fires" claim is not reproduced in Claude Code and this is not the
      red-then-green proof the parked finding asked for. What it does establish: the new guard emits a
      deterministic verdict on both branches; the old one emits context-dependent prose.
- [ ] 4.5 **Deferred:** reproduce under omp with `task.maxRecursionDepth: 1`, dispatched as a peer leg
      on a real workload — the conditions of the original measurement. Needs 6.11.0 published and a
      session not competing with live work.
