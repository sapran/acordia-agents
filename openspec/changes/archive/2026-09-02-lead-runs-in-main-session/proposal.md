## Why

Both wrappers that enter the analysis pillar tell the harness to **dispatch** the orchestrator:

> Dispatch it as a subagent if this harness allows dispatching a primary agent; otherwise switch the
> session to `cyber-analyst` and carry the brief across.

In omp neither branch produces a working lead, and the sentence has no third case.

**The first branch produces an orchestrator that cannot orchestrate.** A dispatched agent cannot spawn
further agents. Measured 2026-09-02 by dispatching both `cyber-analyst` and `collection-analyst` and
reading their own session-init prompts from disk: in a profile at `task.maxRecursionDepth: 2` each has
`task` listed but its description reads *"Agent spawning is currently disabled"* with no agent types
offered; in a profile at `1` the tool is absent from the inventory entirely. So a dispatched
`cyber-analyst` receives its full doctrine and loses the one capability that doctrine is about. It
does not fail — it proceeds, alone, looking like a lead.

**The second branch describes a capability that does not exist.** There is no mechanism in omp by
which a session becomes an agent. An agent prompt enters a session only through a spawn.

The consequence was measured on a real four-hour run against a 4.5M-entity corpus, 2026-09-01. Asked
in prose to "use cyber-analyst", the main session's first recorded thought was *"I'm to act as the
cyber-analyst lead"* — it role-played the part with no ACORDIA prompt loaded at all. It made **zero**
skill reads across 92 tool calls. It first encountered pillar doctrine 7 minutes in, by reading a
**leg's** prompt off disk as an ordinary file, five minutes after it had already invented its own
deliverable location. Four of its first ten dispatches omitted the agent type and silently produced
generic workers; an earlier run on 2026-08-31 omitted **all four** and delivered a complete product
built entirely by non-ACORDIA agents, with nothing flagging it.

The distribution has no delivery path for the one prompt that must reach a session capable of
dispatching. Every other prompt in the pillar does: the four legs are dispatched, and dispatch is
exactly what loads them.

## What Changes

- **The canonical wrapper carries the doctrine instead of delegating it.**
  `acordia-analysts/commands/cyber-analyst.md` stops instructing the harness to dispatch the
  orchestrator and instead contains the orchestrator's prompt body verbatim, followed by the brief.
  Invoking the command makes the invoking session the lead — which is the only session that can
  dispatch the legs.
- **The short alias carries the same body.** `acordia-analysts/commands/analyst.md` is inlined
  identically rather than pointing at a command a model cannot invoke on the user's behalf.
- **The agent file stays, and refuses loudly when crippled.** `cyber-analyst` remains dispatchable —
  removing it would be a roster change — but its prompt gains one instruction: if it finds itself
  without the ability to dispatch, it stops and reports that it was entered by the wrong route rather
  than proceeding as a lead without legs.
- **The duplication is made impossible to drift.** The orchestrator's body now exists in three files.
  `~/ai/checks/check-acordia.sh` gains a seventh invariant asserting the two wrappers contain the agent
  body byte-identically, in the same manner as the existing byte-identity check on the two marketplace
  catalogs.
- **No doctrine is authored.** The inlined text is the existing prompt, unchanged. The only new prose
  is the wrapper's framing line and the agent's refusal instruction, both mechanism rather than
  analytic content, so no grid row moves and no competency mapping changes.

## Capabilities

### Modified Capabilities

- `agent-roster`: the orchestrator SHALL be entered by a route that leaves it able to dispatch, and
  SHALL refuse to act as a lead when it cannot.

## Impact

- **2 command wrappers** — `acordia-analysts/commands/{cyber-analyst,analyst}.md`.
- **1 agent prompt** — `acordia-analysts/agents/cyber-analyst.md`, one added instruction. No
  `·`-separated skill line is touched, so `skill-sets.json` stays correct and is verified, not edited.
- **0 source-document changes** — no grid row, column or mark moves, so both grid transcriptions stay
  valid and no `SKILL.md` moves.
- **1 external check** — `~/ai/checks/check-acordia.sh`, outside this repository, carried in the
  handoff rather than here.
- **Specs**: `agent-roster`.
- **Version**: MINOR, `6.4.0` → `6.5.0`. A wrapper and a prompt both reach every user, so it must
  bump; the roster is unchanged and the distribution shape has not moved, so it is not MAJOR.

## Out of scope, recorded not fixed

- **Prose invocation is not caught.** A user who writes "use cyber-analyst" without the command still
  gets a role-playing main session. Nothing the distribution ships can intercept free prose. Parked in
  `docs/implementation-notes.md`.
- **`task.maxConcurrency`** in the consuming profile serialised six legs into three batches and cost
  76% of the run's wall clock. A deployment setting, not a distribution defect.
- **omp's MCP client silently drops unknown tool parameters**, which nearly shipped a report built on
  four wrong collections. Verified not to be a server defect; filed against omp.
