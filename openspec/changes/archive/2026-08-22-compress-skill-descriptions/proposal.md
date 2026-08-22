## Why

A host that loads the whole `acordia-analysts` bundle silently loses every skill description. Hosts
inject a skills *catalogue* — name, description and location per skill — into the system prompt, and
that catalogue has a character budget. OpenClaw 2026.7.1 sets it at 18,000
(`DEFAULT_MAX_SKILLS_PROMPT_CHARS`). When the rendered catalogue exceeds it, the host does not fail:
it drops **all** descriptions and renders names and paths only, behind one warning line an operator
sees only by reading the compiled prompt.

ACORDIA's 45 skills cost 24,639 characters in full format — 37% over that budget **before a host adds
a single skill of its own**. That is the state on the live `openclaw-gdx-gateway` deployment today:
the analyst is selecting among 62 skills by bare name. `hypothesis-testing` and `deception-detection`
survive losing their description; `assessing-take-value`, `take-domain-interpretation` and
`change-cycle-forecasting` do not — they are precisely the skills whose name does not tell a model
when to reach for them. The library still loads, still passes every health check, and quietly stops
steering selection.

The defect is not context cost. On that deployment the whole skills block is roughly 3,100 tokens of
a 131,072-token window, which is affordable. The defect is the **silent loss of the selection
surface** — the one thing `openspec/specs/skill-library` says a description exists to be.

The cause is packaging, and therefore this repository's: at a mean of 357 characters, ACORDIA's
descriptions are roughly twice the length the selection job requires. No host configuration fixes it.

## What Changes

- Rewrite all 45 `description` fields under `acordia-analysts/skills/` to a hard ceiling of **200
  characters**, targeting a mean of **≤180**. Current mean is 357, current minimum is 298 — every one
  of the 45 is over, so every one is rewritten.
- Add the ceiling to the `skill-library` spec as a checkable requirement, alongside the existing
  1–1024 bound that the ceiling tightens.
- Preserve, in every rewrite, the three properties the spec already requires of a description: it
  states applicability, it discriminates the skill from its siblings, and it does not open with
  selection boilerplate (`Use when`, `Apply when`, …).
- No `SKILL.md` body changes, no frontmatter keys added or removed, no roster change.

**Not in this change**, and deliberately: the machine-readable per-analyst skill declaration
(acceptance criterion 1 of the handoff). It cannot be authored honestly yet — see *Deferred* below.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `skill-library`: the requirement *The description is the selection surface* gains a length ceiling.
  The description's bound moves from "1–1024 characters" to "1–200 characters", stated as a budget
  obligation — a description is one entry in a host catalogue with a finite character budget, and a
  description that overruns the budget costs every *other* skill its description too.

## Impact

- **45 files** — `acordia-analysts/skills/*/SKILL.md`, frontmatter `description` only.
- **`openspec/specs/skill-library/spec.md`** — one requirement tightened.
- **Version**: MINOR bump, in lockstep across the three occurrences
  (`acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.omp-plugin/marketplace.json`). A description reaches a user, so it is a user-facing change; the
  roster and the distribution shape are untouched, so it is not MAJOR.
- **No agent prompt, competency grid or doctrine section is edited**, which is why this change does
  not carry a literature selection. A description is frontmatter, not a skill body; compressing one
  restates what its unchanged body already says and asserts nothing new. Every doctrinal claim in
  this library continues to live in the bodies and the grid, untouched here.

## Deferred — and why

Two findings surfaced while measuring this change. Both are recorded in
`docs/implementation-notes.md` and neither is fixed here.

1. **The grid and the prompts disagree about the analytic spine.** All four legs carry a 12-skill
   `Shared analytic spine (every analyst carries this)` line, but `docs/roles/operational-analyst.md`
   marks those rows in the `Core` column only. Making the mapping machine-readable would harden that
   drift into a declared field. Resolving it means deciding whether the grid or the prompts are
   right — a claim about how analytic work is divided, which `CLAUDE.md` requires be selected from
   the literature before it is written. The lib.ai library returned `database disk image is
   malformed` on every call during this work, so that selection could not be made.

2. **Three skills are named in no agent prompt.** `aleph-entity-graph`,
   `credential-harvest-triage` and `exhaustive-data-processing` appear in no `·`-separated line in
   any of the five prompts, and prompt naming is the only agent→skill binding this distribution has.
   A declared per-analyst skill set forces a decision about them; that decision is also a
   division-of-work claim, and is blocked by the same outage.

Compressing the descriptions is independent of both, and on its own removes the silent degradation
for every role-scoped host. The declaration is a follow-up change.
