## Why

`docs/handoff-handback-contract.md` reports one defect, measured on a working deployment of 6.3.0
running all five roles: **no analyst prompt says anything about how much to hand back.** Grepped
across all five prompts, there is no size, no limit, no summary contract and no notes file. The
prompts say what to analyse and say to hand back reads with their evidence, but never how large a
read may be.

The consequence is silent. Every harness truncates what a delegated agent returns — the deployment
that reported this promotes the child's last message only, cut at a fixed character count, and never
promotes tool output at all. An analyst that writes a thorough long read therefore has most of it
discarded, and **neither the analyst nor the lead is told**. The lead fuses from a read that stopped
mid-sentence and cannot see that it stopped.

That is a defect in the prompt contract rather than in any harness, which is why it is fixed here and
in prose that names no harness. The doctrine already covers the outgoing half: `cyber-analyst` calls
the handoff the weakest point in the structure, from Monte p. 63 — different tempos, risk tolerances,
tools and leadership between units produce miscommunication and mistakes. The return leg of that same
handoff was left unspecified.

Two works decide the shape of the fix. Lindsay, *Information Technology and Military Power*, p. 172:
what is "not explicitly recorded in reporting" is what a later reader most needs, while an
administrative load "reproduced at each echelon as slides and text were aggregated and sent forward"
is itself friction — so the working must be written down, and the thing sent up must be small. Both
at once, which is what a notes file plus a bounded summary is. Pherson & Heuer, p. 547: a written
record "more accurately reflects what the analyst was thinking at the time rather than relying on
that person's memory" — the notes file is contemporaneous, not reconstructed. And p. 117: where
face-to-face contact is absent, a team compensates with explicit "communication protocols and
practices" rather than assumed ones, which is why the contract is stated in the prompt rather than
left to each analyst's habit.

## What Changes

- Add a hand-back contract to all five analyst prompts: the full working goes to a notes file in the
  task directory; what crosses the dispatch boundary is a bounded summary that **names that file**;
  the bound is treated as real, and a read that does not fit means the question was too large and is
  reported as such rather than truncated silently.
- Add the task-directory convention to the lead prompt: each task gets its own directory with a
  short dated slug and a `README.md` carrying the request verbatim, the date, and one line on what is
  being settled. Analysts write their notes there; the lead reads them before fusing.
- Make the lead responsible for **supplying both** in every dispatch — the directory and the bound.
  An unstated bound is the lead's defect, not the leg's.
- Move the source document first: a paragraph in `docs/roles/operational-analyst.md` under *How the
  pieces fit*, beside the Monte p. 63 sentence it extends, so the prompts derive from the grid
  document rather than the reverse.
- **No number, no path, no harness and no tool name** appears anywhere in the shipped prose. The
  bound and the directory are stated by the dispatching brief, so each deployment supplies its own.

## Capabilities

### New Capabilities

None. The contract governs how the five agents `agent-roster` already defines return their work.

### Modified Capabilities

- `agent-roster`: every prompt SHALL state a hand-back contract, and the orchestrator SHALL supply
  the task directory and the reply bound in every dispatch.

## Impact

- **5 files** — every `acordia-analysts/agents/*.md`.
- **1 source document** — `docs/roles/operational-analyst.md`, prose only. No grid row, no column and
  no mark changes, so both grid transcriptions stay valid and no `SKILL.md` moves.
- **No `·`-separated skill line is touched**, so `acordia-analysts/skill-sets.json` stays correct and
  is verified rather than edited.
- **Specs**: `agent-roster`.
- **Docs**: `docs/handoff-handback-contract.md` (the handoff itself, copied in beside its predecessor
  so the record is readable without the author's machine) and `docs/implementation-notes.md`.
- **Version**: MINOR, `6.3.0` → `6.4.0`. Prompt prose reaches every user, so it must bump; the roster
  is unchanged and the distribution's shape has not moved, so it is not MAJOR.

## Out of scope, recorded not fixed

The handoff observes that ACORDIA would benefit from carrying the prompts-to-`skill-sets.json` drift
check in its own CI rather than only in a consumer's tooling. That is a repository-infrastructure
change with its own trade-offs — this repository ships no CI at all today — and it is not one of the
three acceptance criteria. Parked in `docs/implementation-notes.md`.
