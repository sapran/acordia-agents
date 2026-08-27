# Handoff to the ACORDIA developer — add a hand-back contract to the five analyst prompts

Written 2026-08-27 from a working OpenClaw deployment of ACORDIA 6.3.0 (`~/.openclaw-gdx` on host
`mini`, five roles live). Everything below was measured on that deployment, named where it matters.
This document does **not** ask for any change to skills, skill sets, roles, or the delegation
architecture — those were checked against the running system and are correct.

## Why you are being asked

ACORDIA's architecture already matches how it is being run. `agents/cyber-analyst.md` says
"Dispatch these subagents, each on its own question, and fuse their reads yourself", and that is
exactly the shape now running: the lead spawns each specialist as its own child session, they run in
parallel, and each returns one read. Nothing needs rewriting for that.

One thing is missing, and it is missing for every harness, not just this one.

**No analyst prompt says anything about how much to hand back.** Grepped 2026-08-27 across all five
prompts: zero occurrences of a size, a limit, a summary contract, or a notes file. The prompts say
what to analyse and say "hand back reads with their evidence", but never how large a read may be.

Every harness truncates a delegated agent's return value. On OpenClaw the child's **last assistant
message only** is promoted to the parent, cut at **6,000 characters**, and tool output is never
promoted at all. Claude Code's Task tool has the same shape: text back, nothing else. So an analyst
that writes a thorough 20,000-character read has most of it silently discarded, and neither the
analyst nor the lead is told. That is a defect in the prompt contract, not in any harness.

## Change 1 — a hand-back contract in all five analyst prompts

Add to each of the four specialists, and to the lead as the thing it must require when dispatching:

- Write the full working — evidence, identifiers, queries run, dead ends, what was deliberately not
  done — to a notes file in the task's working directory.
- Return a **bounded summary that names that file**: the judgement, the confidence, the gaps, and
  where the evidence lives.
- Treat the bound as real. If the read does not fit, the question was too large; say so and name
  what was left, rather than truncating silently.

**Do not hard-code 6,000.** That is OpenClaw's number. Phrase the bound as a deployment-supplied
limit that the dispatching brief states, so a Claude Code or other deployment can set its own.

## Change 2 — the task directory convention

Add to the lead prompt: each task gets its own directory, named with a short dated slug, containing
a `README.md` holding the human's original request verbatim, the date, and one line on what is being
settled. Analysts write their notes files into that same directory. The lead reads them before
fusing.

This is what makes an operation navigable afterwards, by a human or by the lead itself after a
context compaction. Phrase the directory as supplied by the dispatching brief — **do not name a
path**. In this deployment the lead and the analysts see the same directory under different paths
because the analysts are sandboxed, and any absolute path baked into a prompt would be wrong on one
side of that boundary.

## Explicit non-goals

Do not put any of the following in ACORDIA. All are OpenClaw-specific and were handled in the
deployment's own config and prompt layer:

- tool names (`sessions_spawn`, `sessions_send`, `sessions_yield`), or Claude Code's `task` tool
- the 6,000-character figure, watchdog timeouts, `cwd` behaviour, sandbox or bind-mount detail
- concrete filesystem paths of any kind
- anything about models, providers or context windows

## Acceptance

- All five prompts state a hand-back contract; none names a harness, a tool, a path or a number.
- The lead prompt states the task-directory convention and that it supplies the directory and the
  bound in every dispatch.
- `skill-sets.json` still agrees with the prompts — see below. If a skill line is touched while
  editing, that file must be updated in the same change.

## While you are in there: `skill-sets.json` is hand-maintained

`skill-sets.json` says so itself ("Hand-maintained ... transcribed from the skill lines and
procedural sections"), and ACORDIA ships no generator for it. The prompts are the authority; the
JSON is a hand copy. Verified 2026-08-27 on 6.3.0: all five analysts agree **exactly**, in both
directions, against the 45 skills on disk — 29 / 22 / 31 / 33 / 25 for cyber, mission, terrain,
overwatch, collection. So it is correct today, and any future difference is new.

Consumers depend on it. This deployment generates its per-role config arrays from it, and the
failure mode is silent: OpenClaw injects a skills catalogue with an 18,000-character budget and, on
overflow, drops every description and serves bare skill names rather than erroring. That was the
live state under ACORDIA 5.0.0, where 45 skills cost 24,639 characters.

A check now guards the prompts-to-JSON hop downstream
(`~/ops/openclaw-mini/gdx/tools/gen-acordia-skills.py`, `verify_against_prompts`, shown to fail by
injecting a slug and to pass on restore). ACORDIA would benefit from the equivalent in its own CI,
so the drift is caught in the repo that owns both files rather than in one deployment.
