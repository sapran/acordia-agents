## Why

The operational-analyst orchestrator carries the end-neutral analytic loop in prose in its own prompt body: read target through T&N, read defender through Def, synthesise through Fus, form a calibrated judgement, name the next move, repeat as new material arrives. The loop is the pillar's core workflow shape — everything else (individual competencies, credential harvest, dispatch discipline) hangs off it.

Two consequences of the loop living only in the orchestrator prompt:

1. **It cannot be triggered independently.** opencode selects skills by `description` match. Sessions where the orchestrator is not the entry point (e.g. a session that starts with a leg because the operator dispatched directly, or a future non-primary agent that reuses the same loop) have no way to invoke the loop's shape as a skill.

2. **Future pillars have to re-derive it.** Collection, Operations, Reflection, Direction, Independent action are named as future pillars in the config. Each will need its own end-neutral loop. Naming the analyst loop as a skill gives future pillars a template artifact to point at, not just a paragraph in another agent's prompt.

The loop already exists in prose; this change lifts it out as a first-class skill named `analyst-loop`.

## What Changes

### New skill: `analyst-loop`

Add `analysts/skills/analyst-loop/SKILL.md` — a procedural cross-cutting skill that names the target → defender → fusion → judgement → next-move loop.

The skill body carries:

- **Loop shape** — the five named steps (target-read, defender-read, fusion, judgement, next-move), each one sentence describing the analytic move.
- **Trigger** — a triggering-quality `description` stating "when to execute the analyst loop" (e.g. new material has arrived; a fresh operating question needs an end-neutral pass; the operator is between decision points and wants a full round of analysis).
- **Loop invariants** — end-neutrality (each pass must reach a judgement with a next move, not stop at "insufficient information"), gap-naming (`naming-the-gaps` at every judgement), calibrated confidence (`calibrated-confidence` at every judgement), and passive posture (loop reads and reasons only, never acts).
- **Not-a-competency notice** — the skill is procedural/cross-cutting, does not correspond to a competency-grid row, and inherits the "procedural skill exception" clause from `analyst-skill-library`.

Fires when any agent (primary or leg) is asked to run a fresh analytic round over collected material, or when the operator explicitly asks for an end-neutral pass.

### Agent-prompt reference

`operational-analyst.md` gains a one-sentence pointer in its existing loop-describing paragraph naming `analyst-loop` as the skill that formalises the loop. No new section; no permission change; the existing prose is unchanged.

The three leg agents SHALL NOT reference `analyst-loop` in their prompts — legs are leaf specialists that answer a leg-scoped question when dispatched; running the full loop is the orchestrator's job (or, in future pillars, the orchestrator-analogue's).

## Capabilities

### New Capabilities

None. The new skill lands inside `analyst-skill-library` as a cross-cutting procedural addition, mirroring how `credential-harvest-triage` was added.

### Modified Capabilities

- `analyst-skill-library` — one new requirement (`analyst-loop` skill exists), one modified requirement (procedural skill count moves from 1 to 2).

## Impact

- **Modified files:** `analysts/agents/operational-analyst.md` (one sentence added to existing loop paragraph, no new section).
- **New files:** `analysts/skills/analyst-loop/SKILL.md`.
- **Referenced source of truth:** `docs/roles/operational-analyst.md` (the spine paragraph describing the loop) — read for anchor, not modified.
- **No install script change.** `install.sh` globs `skills/*` and picks up the new skill automatically.
- **No permission change.** No agent's `edit`, `bash`, or `task` block is modified.
- **No leg-agent change.** Legs remain leaf specialists.
- **Analyst posture preserved.** The loop is descriptive — it names an analytic shape the orchestrator already runs. It does not authorise new action.
- **Future-pillar preparation.** Each future pillar's orchestrator can point at `analyst-loop` as the template for its own end-neutral loop, or (more likely) each pillar defines its own `<pillar>-loop` skill and cites this one as prior art.
