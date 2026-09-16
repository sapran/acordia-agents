## Why

`.acordia/` exists so that what an analyst generates stays out of the material it was given to
analyse. Today only the *finished product* has a home there. Notes, the task `README.md`, working
drafts and the credential file are told to go to "the working directory the brief names — or, if it
names none, one you create and identify by name" (`mission-analyst:105`, `terrain-analyst:107`,
`collection-analyst:113`, `overwatch-analyst:80`) and to "a short dated slug"
(`briefing-reporting/SKILL.md:32`). No parent is named in either place, so an unbriefed dispatch
creates its task directory in the current directory — beside the corpus it is analysing, which is
the one outcome the `.acordia/` convention exists to prevent.

The same sentence carries a second defect. "A short dated slug" is the *only* naming rule the
distribution states, and a date does not identify a corpus. Two sweeps run on two different Aleph
collections on the same day resolve to the same directory name and the same report filename, and the
second silently overwrites the first. Neither failure raises anything: the write succeeds, and the
loss is discovered only when someone opens the report and finds the wrong corpus in it.

## What Changes

- **`.acordia/` becomes the workspace root for everything an analyst generates**, not just the
  product. A second sink, `.acordia/work/`, holds task directories; `.acordia/reports/` keeps its
  existing meaning unchanged. Both stay conventions, not permissions.
- **Every task directory and every report filename carries a corpus token** ahead of the date:
  `<corpus>-<YYYY-MM-DD>-<task-slug>`. The report is the same stem under `.acordia/reports/`, so a
  product and the working behind it are addressable from each other by name alone.
- **The corpus token is derived from the material, not from the request**: an Aleph collection's
  `foreign_id`, falling back to a slug of its label; for a file corpus, the slugified name of the
  directory or archive analysed. Two differently-worded dispatches against one corpus therefore land
  together instead of splitting.
- **A same-day collision resolves by numeric suffix** (`-2`, `-3`), so no run can ever overwrite
  another's directory or report.
- The four leg prompts, the orchestrator's `## A directory per task, a bound per reply` section,
  `briefing-reporting`, `credential-harvest-triage` and its `references/report-layout.md` are brought
  onto the scheme. The credential file keeps its existing "beside the notes" placement and inherits
  the addressing from the directory that now has one.
- No new capability, no roster change, no change to the shape of the distribution: **MINOR** bump,
  6.14.0 → 6.15.0.

**Literature finding, recorded rather than filled in.** The library was searched for what the canon
says about analytic workfile organisation and about keeping derived work out of the material under
analysis (queries: *analyst working files, workfile organisation, keeping analytic notes separate
from source material*; *contaminating evidence, preserving integrity of collected material during
analysis, chain of custody*). **Nothing in the register prescribes a file-naming or directory
scheme**, and no registered work in `docs/roles/sources.md` addresses one. Two unregistered works
touch the surrounding principle — Plohmann et al., *Patterns of a Cooperative Malware Analysis
Workflow*, p. 5–6 (documentation produced alongside the analysis, held in a case repository separate
from the analyst's workstation) and NIST SP 800-61, p. 46 (a snapshot taken before handlers
"inadvertently altered the state of the machine during the investigation") — but both support the
read-only-input posture the prompts already carry, not a naming scheme. **The addressing scheme in
this change is engineering convention and carries no `doctrine_source`**, per the register rule that
a skill codifying common practice omits the field rather than carrying an empty one. No register
entry is added.

## Capabilities

### New Capabilities

None. This change modifies how an existing convention is addressed; it introduces no capability.

### Modified Capabilities

- `agent-roster`: the report-sink requirement widens from one sink to a workspace root with two
  sinks, and states that an agent's own generated files never land outside it. The
  task-directory requirement gains the corpus token, the `.acordia/work/` parent for the
  brief-names-none case, and the same-day suffix rule; its "no directory path in a prompt"
  clause is clarified to bind absolute and deployment-specific paths, not the relative
  convention root the prompts already name.
- `skill-library`: `briefing-reporting` — the skill that carries the task directory's shape — gains
  the addressing scheme it must state, including how the corpus token is derived and what happens
  when two runs collide.

## Impact

- **Prompts (5)**: `cyber-analyst`, `mission-analyst`, `terrain-analyst`, `collection-analyst`,
  `overwatch-analyst`. The orchestrator body is byte-duplicated into `commands/analyst.md` and
  `commands/cyber-analyst.md`, so its edit lands in **three** files and gate check 7 verifies it.
- **Constraint — zero headroom.** The `cyber-analyst` body measures exactly 10,500 of 10,500
  characters (gate check 8). Its edit MUST be character-neutral or negative, offsetting any addition
  with an equal cut, and the cut MUST NOT remove a guardrail — 6.10.0 lost two guardrails to an edit
  of this shape and still passed 8/8, because the gate compares the body across carriers rather than
  auditing what it contains.
- **Skills (2)**: `briefing-reporting/SKILL.md`, `credential-harvest-triage/SKILL.md` and
  `credential-harvest-triage/references/report-layout.md`.
- **Specs (2)**: delta specs for `agent-roster` and `skill-library`.
- **Docs**: `README.md` and `CLAUDE.md` both describe `.acordia/reports/` as the single sink and must
  describe the workspace root instead.
- **Version**: three occurrences in three JSON files, 6.14.0 → 6.15.0.
- **No harness enforces any of this.** The scheme is prose an agent follows; nothing validates a path
  at install or dispatch time, and no prompt may present it as enforced.
