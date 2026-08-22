## Why

`docs/handoff-skill-catalogue-prompt-budget.md` asks, as its first acceptance criterion, that each
analyst declare its skill set in a machine-readable form. The reason is that a host loads all 45
skills or none: the role→skill mapping is already authored, correctly, in each prompt — a
`·`-separated line under each skill heading, plus procedural skills named in their own sections — but
it is running text in the middle of a markdown body, so nothing can act on it. Role-scoping is what
keeps a catalogue inside a host's character budget, and role-scoping is impossible while the mapping
is prose.

Producing the declaration also settles two things that were previously guessed at, and corrects the
record on both.

**The three procedural skills are not orphans.** `6.1.0` parked a finding that `aleph-entity-graph`,
`credential-harvest-triage` and `exhaustive-data-processing` were named in no agent prompt. That was
an artefact of the scan, which read only `·`-separated lines. All three are named — in backticks, in
dedicated sections — in **all five** prompts. No skill in the library is unreachable.

**The largest analyst was over the target, not under it.** Because those three were missed, every
analyst's set was undercounted by three, and `6.1.0` reported `overwatch-analyst` at 11,114
characters against a 12,000 target. Its real cost was **12,211** — over. The error was in the
counting, not in the descriptions; the 18,000-character host budget was never at risk, but the
criterion `6.1.0` claimed to meet was not met.

## What Changes

- Add `acordia-analysts/skill-sets.json`: a hand-maintained declaration of each analyst's skill set,
  grouped as the prompt groups it — `spine`, `deep`, `working`, `procedural` — with the agent prompts
  remaining the authority the declaration is checked against.
- Make the two prompt conventions the declaration is transcribed from **normative** in `agent-roster`,
  so the declaration is verifiable rather than merely plausible: the `·`-separated skill line under a
  heading, and the procedural skill named in backticks in its own section.
- Trim 24 descriptions to bring `overwatch-analyst`'s **true** 33-skill catalogue from 12,211 to
  11,943, under the 12,000 target that `6.1.0` reported as met on an undercount.
- Document the declaration check in `CLAUDE.md` beside the two invariants that already lost their
  build gate, and correct the two records that carry the wrong finding.
- No agent prompt prose, no competency grid, no skill body, and no `metadata.acordia` anchor changes.

## Capabilities

### New Capabilities

None. The declaration describes the roster that `agent-roster` already governs rather than
introducing a capability of its own.

### Modified Capabilities

- `agent-roster`: each agent SHALL declare its skill set in `skill-sets.json`, and the two prompt
  conventions that declaration is transcribed from become normative rather than a readability habit.
- `plugin-distribution`: the distribution gains a fourth JSON file, which carries no version and so
  leaves the three-occurrence version lockstep untouched.

## Impact

- **New file**: `acordia-analysts/skill-sets.json`.
- **45 files** — `acordia-analysts/skills/*/SKILL.md`, 24 of them with a trimmed `description`.
- **Specs**: `agent-roster`, `plugin-distribution`.
- **Docs**: `CLAUDE.md`, `docs/implementation-notes.md` (a parked finding that is wrong),
  `docs/handoff-skill-catalogue-prompt-budget.md` (figures computed on the undercount).
- **Version**: MINOR, `6.1.0` → `6.2.0`. A user receives a new artifact, so it reaches them; the
  roster is unchanged and the install source path has not moved, so it is not MAJOR. That reading is
  worth challenging at review — "the shape of the distribution itself" could be argued to cover a new
  declared file — but nothing a consumer depends on breaks, which is what the MAJOR examples
  (a roster change, an install-path move) have in common.
- **No literature selection**, and this time not because the library is unreachable. Nothing here
  asserts a doctrinal claim: the declaration transcribes what the prompts already say, and the
  description trims restate unchanged bodies. The one doctrinal question in this area stays open —
  see *Still deferred*.

## Still deferred

**The competency grid and the prompts disagree about the analytic spine.** The grid marks the
12 spine rows in the `Core` column alone; all four legs carry the spine in prose. This change does
not resolve that, because whether every analyst carries the analytic spine is a claim about how
analytic work is divided, and `CLAUDE.md` requires such a claim be selected from the literature
first. The lib.ai library was unreachable throughout this work — first `database disk image is
malformed`, then `Could not find session`.

What the change does instead is stop the drift being invisible. The declaration records the spine as
the prompts state it, and the check proves the 12-skill spine is **identical across all four legs** —
so the divergence from the grid is now a difference between two machine-readable records, catchable
in one command, rather than a discrepancy nobody was comparing. Resolving it remains a grid edit in
its own change.
