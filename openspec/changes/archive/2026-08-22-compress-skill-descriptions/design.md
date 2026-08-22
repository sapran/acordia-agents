## Context

The cost model is arithmetic, not estimation. A catalogue entry costs
`97 + len(name) + len(description) + len(location)`, where `location` is the absolute `SKILL.md` path
on the host. Every term but `description` is fixed by the distribution: the 45 slugs sum to 1,004
characters, and `location` is the host's install prefix plus the slug plus `/SKILL.md`.

That model was verified rather than assumed. Solving it against the figure measured on the live
gateway — 24,639 characters for the 45 skills in full format — yields a host install prefix of
exactly 40.00 characters. An integer falling out of a five-term reconstruction is the model
reproducing the measurement, so the projections below are arithmetic on a verified formula.

Measured on this tree at `origin/develop`: 45 skills, 16,061 description characters, **mean 357, max
438, minimum 298**. The minimum matters more than the mean — there is no tail to trim and no subset
already compliant. Every one of the 45 is above the target, so every one is rewritten.

Projected catalogue cost per analyst, at a uniform description length, using the verified formula:

| Analyst | skills | now | @180 | @200 | @220 |
|---|--:|--:|--:|--:|--:|
| mission-analyst | 19 | 10,364 | 7,072 | 7,452 | 7,832 |
| collection-analyst | 22 | 11,980 | 8,156 | 8,596 | 9,036 |
| cyber-analyst | 26 | 13,907 | 9,582 | 10,102 | 10,622 |
| terrain-analyst | 28 | 15,242 | 10,364 | 10,924 | 11,484 |
| overwatch-analyst | 30 | 16,331 | 11,084 | 11,684 | 12,284 |
| whole library | 45 | 24,639 | 16,678 | 17,578 | 18,478 |

Skill counts are the union of the `·`-separated lines in each prompt, which is the only agent→skill
binding this distribution has.

## Goals / Non-Goals

**Goals:**

- Every description at or under a hard per-description ceiling, so that a host loading any single
  analyst's skill set renders its catalogue with descriptions intact.
- Descriptions that still do the job the `skill-library` spec assigns them: state the work only this
  skill does, and the situation that calls for it, discriminating from siblings.
- A ceiling that is checkable by reading one field, not by computing an aggregate.

**Non-Goals:**

- Fitting the **whole** 45-skill library into an 18,000-character budget alongside a host's own
  skills. At 180 characters the library still costs 16,678, leaving 1,322 for the host — less than
  the ~3,953 the reference host's own 17 skills need even in compact form. The whole-library case
  stays over budget by design; role-scoping is the fix, and this change is what makes role-scoping
  sufficient once it exists.
- Changing any `SKILL.md` body, any `metadata.acordia` anchor, or any agent prompt.
- The machine-readable per-analyst declaration. Deferred, with reasons, in the proposal.

## Decisions

**A hard ceiling of 200 characters, with a library mean target of 180.**

The handoff proposed "mean ≤180, none exceeding ~250". A mean is the wrong instrument: it bounds the
library without bounding any role, so a distribution meeting the mean can still put the long
descriptions into one analyst's set and push that role over. The table above shows the binding case
is `overwatch-analyst` at 30 skills — the largest set, and the one with the least slack.

A hard 200 bounds the worst case directly: even if *every* description in the library sat exactly at
the ceiling, overwatch would cost 11,684 and still clear 12,000. At 220 it costs 12,284 and does not.
So 200 is the largest round ceiling that survives the worst case, and it is checkable per file.

The mean target of 180 is kept as a second, softer obligation, because it is what buys headroom: at
180 the worst role costs 11,084, roughly 900 characters of margin.

*Alternative considered — a per-analyst budget instead of a per-description ceiling.* Rejected: a
skill sits in up to five analysts' sets, so a per-role budget makes one skill's length a shared
resource negotiated across roles, and every roster change re-opens the negotiation. A per-description
ceiling is local and stable.

**What gets cut, stated in the spec rather than left to judgement.**

Halving 357 characters to 180 is not trimming; it is a rewrite, and a rewrite invites the wrong
economy — dropping the trigger clause, which is short, instead of the enumeration, which is long. The
existing descriptions overrun mostly on worked examples and lists of artefact types, all of which the
body already carries and the selecting model does not need to choose a file. The spec delta therefore
names the priority explicitly: enumeration goes, the work-plus-trigger pair stays.

**No literature selection for this change.**

`CLAUDE.md` requires a literature selection before prose is written for an agent prompt, a skill body,
a competency grid or a doctrine section. A `description` is none of those: it is frontmatter, and a
compressed description restates the claim its unchanged body already makes. Nothing here asserts
anything the canon has not already been consulted for.

This is recorded rather than assumed because the lib.ai library was unavailable throughout this work
(`database disk image is malformed` on every call), and the reader should be able to tell that the
step was reasoned about and found inapplicable rather than skipped under an outage. The two findings
that **do** need the canon are deferred to their own change for exactly that reason.

## Risks / Trade-offs

- **A compressed description discriminates worse than its predecessor.** This is the real risk, and
  it is not caught by a character count. Mitigation: the per-family sibling comparison in the spec's
  existing scenarios is re-run after the rewrite, and the worked `multi-source-fusion` /
  `maintaining-operating-picture` collision is checked by hand, since it is the pair the spec already
  names as the hard case.
- **The ceiling is calibrated against one host's budget.** 18,000 is OpenClaw 2026.7.1's
  `DEFAULT_MAX_SKILLS_PROMPT_CHARS`. A host with a smaller budget would still degrade. The ceiling
  does not claim universality; it claims the largest analyst set clears 12,000, which is the
  criterion the handoff set and leaves 6,000 for a host on the reference budget.
- **Nothing in the repository enforces the ceiling.** There is no build and no test suite, so this
  joins the other invariants that rely on the external gate `~/ai/checks/check-acordia.sh` and on a
  reviewer. The measurement is one line of Python over the 45 files, given in `tasks.md`.
- **The version bump reaches installed users only through omp.** Claude Code has no working upgrade
  path for marketplace plugins, so a Claude Code user keeps the old descriptions until they uninstall
  and reinstall. That is pre-existing and unchanged by this work, but it means the degradation
  persists in the field longer than the release does.
