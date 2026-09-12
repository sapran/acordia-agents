## Why

The orchestrator's entry guard is phrased as the absence of a tool: *if you cannot dispatch subagents, you were dispatched as a subagent yourself and you are not a lead: stop and say so.* It does not fire.

This is measured, not suspected. On the opwe run of 2026-09-02 (`~/ai/tasks/tele2-siem`) `cyber-analyst` was dispatched as a peer leg, enumerated its own tool inventory in a thinking block at 14:13:15, saw no `task` tool — omp strips it when the profile sets `task.maxRecursionDepth: 1` — and never fired the guard: zero occurrences of its language across 391,251 characters of that leg's prose. The finding was parked in `docs/implementation-notes.md` at the time with a named candidate fix. The same profile still carries `maxRecursionDepth: 1` today.

The defect is the phrasing, not the doctrine. A model does not notice an absence it was not asked to look for, so a guard that triggers on a missing tool triggers on nothing. The remedy is a positive determination the orchestrator must perform and report.

The canon supports treating this as analytic work rather than preamble. Monte describes the operational analyst as one who "must not only analyze the information they have, but also determine what they are lacking" (*Network Attacks & Exploitation: A Framework*, document `c159a333`, p. 60) — determining an absence is the job, not a preliminary to it. Styran and Yashchuk establish what the silent failure costs: ACORDIA adds "'Analysis' as an explicit core activity rather than an implicit component of 'People' or 'Tools'" (document `1152d85c`, p. 20), so a lead quietly doing four specialists' work has hollowed out a core pillar while the product still reads as though four seats filled it.

## What Changes

- Replace the orchestrator's absence-phrased entry guard with a positive check: enumerate the tool inventory, look for `task` by name, and open with `dispatch: available` or `dispatch: unavailable` before anything else.
- Keep every downstream consequence unchanged — the refusal, the named entry route, and the prohibition on quietly doing the legs' work.
- Move the instrument-choice technique detail out of the orchestrator prompt into `gain-loss-calculus`, which owns comparison against alternatives, to stay under the prompt-body ceiling. This is the remedy the ceiling requirement itself prescribes.
- Update `docs/roles/operational-analyst.md` in the same change, per the source-of-truth rule.
- Version `6.11.0` → `6.12.0` (three-file lockstep).

## Impact

- `acordia-analysts/agents/cyber-analyst.md`, and both wrappers that carry its body byte-identically.
- `acordia-analysts/skills/gain-loss-calculus/SKILL.md` — gains the instrument comparison; its grid row is unchanged.
- `openspec/specs/agent-roster/spec.md` — one requirement modified.
- No new agent, skill, competency-grid row, command wrapper, permission boundary or install route. The grid table is unchanged; the prose above it moves.
