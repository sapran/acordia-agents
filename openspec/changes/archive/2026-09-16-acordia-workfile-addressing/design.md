## Context

The distribution states three things about where files go, in three places, and they do not compose
into a workspace:

1. Five prompts name `.acordia/reports/` for the finished product.
2. Four leg prompts say notes go to "the working directory the brief names — or, if it names none,
   one you create and identify by name". No parent.
3. `briefing-reporting/SKILL.md:32` says the task directory is created "under a short dated slug".
   No parent, and a date as the only discriminator.

Items 2 and 3 resolve, in the unbriefed case, to the current directory — which is the corpus. The
`.acordia/` convention therefore holds for the one artifact that was already going to be handed over
and fails for everything produced on the way to it.

Three constraints shape the implementation rather than the design:

- **The orchestrator body is at exactly 10,500 of 10,500 characters** (gate check 8, `len(body.strip())`).
  Any addition must be paid for by an equal cut in the same file.
- **That body is byte-duplicated** into `commands/analyst.md` and `commands/cyber-analyst.md`; gate
  check 7 compares all three. An edit is a three-file edit.
- **Gate check 7 compares the body across carriers, not against a checklist of what the body must
  contain.** 6.10.0 lost two guardrails to a character-neutral rewrite and still passed 8/8, so the
  cut that pays for the addition must be verified by reading, not by the gate.

## Goals / Non-Goals

**Goals:**

- Everything an analyst generates is addressable under `.acordia/`, in the unbriefed case as much as
  the briefed one.
- A task directory and its product name the corpus, so two corpora on one day cannot collide.
- One authority for the scheme (`briefing-reporting`), referenced by the prompts rather than
  restated in each — the prompt-routes-to-a-skill rule the roster spec already carries.
- The orchestrator edit lands character-neutral or negative with no guardrail lost.

**Non-Goals:**

- **No enforcement.** Nothing validates a path at install or dispatch time and nothing will. The
  scheme is prose an agent follows, and no prompt may describe it as a restriction.
- **No path frontmatter.** A path-scoped `edit:` allowlist is not added; the roster spec forbids
  permission frontmatter outright and omp has no per-path scoping to honour it.
- **No migration of existing work.** Directories already written under the old convention are left
  where they are; nothing in the distribution reads them.
- **No new capability, no roster change.** Five agents, 45 skills, 10 wrappers, unchanged.
- **No `.acordia/ops/`.** The journal root stays withdrawn; `work/` is not a re-entry for it, holds
  no operation state, and is per-task rather than per-operation.

## Decisions

### D1. Two sinks under one root, rather than a corpus-first tree

`.acordia/work/` sits beside `.acordia/reports/`. The alternative considered was a corpus-first tree
(`.acordia/<corpus>/<date-slug>/` with a per-corpus `reports/`), which groups more strongly.

Rejected because it redefines `.acordia/reports/` — a path the roster spec, the README and all five
prompts already describe as *the* sink for a product. The corpus token in the stem buys the grouping
(a sorted listing clusters by corpus) at the cost of one new path rather than the cost of
invalidating an existing contract. A flat `runs/` directory with the product inside it was also
rejected: it collapses the product/working distinction the hand-off posture depends on.

### D2. Corpus, then date, then task slug

`<corpus>-<YYYY-MM-DD>-<task-slug>` sorts by corpus first and chronologically within it. Date-first
would sort chronologically across all corpora, which is the ordering that produced the reported
defect — related work scattered, unrelated work adjacent and colliding.

### D3. The corpus token derives from the material, not the request

`foreign_id` → label slug → analysed directory/archive name. A machine identifier is stable across
rewording and across a collection being renamed in its label; the label slug is the fallback because
many instances supply no `foreign_id`.

The rejected alternative was a caller-supplied token with a corpus fallback. It gives more control
and loses the property that makes the scheme work: two dispatches worded differently against one
corpus must land in one place, and a caller-supplied token splits them exactly when the caller is
least likely to notice. A brief that names a directory outright still wins — that path is unchanged
and is used as given.

### D4. The scheme lives in `briefing-reporting`, not in five prompts

The roster spec's "a prompt routes to a skill rather than restating its technique" already governs
this, and the orchestrator's prompt already says "`briefing-reporting` carries its shape". So the
skill gains the full scheme — parent, stem, derivation, collision rule — and the prompts gain only
the parent, which they need because the parent is the thing whose absence produced the defect.

This is also what makes the character-neutral orchestrator edit achievable: the orchestrator needs
`.acordia/work/` and nothing else.

### D5. The collision rule states the silent failure, not just the suffix

`-2`, `-3` is unremarkable. The part worth writing down is that a colliding write **succeeds**: the
filesystem reports nothing, neither harness checks, and the loss surfaces when a reader opens a
report and finds the wrong corpus in it. This follows the repo's standing pattern of stating the
reason with the rule, because a rule whose failure mode is invisible is the one an agent skips.

A timestamped stem (`YYYY-MM-DDTHHMM`) was rejected: always unique, but it makes every directory
name harder to read and type in exchange for a collision that the corpus token and the task slug
already make rare.

### D6. The "no directory path in a prompt" clause is clarified, not weakened

`agent-roster` currently says "No directory path SHALL be written into any prompt." Read literally
that already conflicts with the five prompts naming `.acordia/reports/`, and adding `.acordia/work/`
sharpens the conflict. The clause is restated to bind **absolute and deployment-specific** paths —
which is what it was protecting against, a lead and a sandboxed leg reaching one directory under two
names — while explicitly permitting the relative convention roots. A relative root cannot be wrong
on one side of a sandbox boundary, because it is resolved on each side rather than carried across.

## Risks / Trade-offs

- **`.acordia/work/` could be read as the journal root returning.** It is not: it holds per-task
  directories, no operation state, and no `scope.md`/`intel.md`/`coverage.md` layout. The delta spec
  keeps the `.acordia/ops/` prohibition intact and separates the two questions explicitly, and gate
  check on `.acordia/ops/` is unaffected.
- **The orchestrator edit is the risk in this change.** Zero headroom plus a gate that compares
  bytes across carriers rather than auditing content is precisely the 6.10.0 failure shape. Mitigated
  by diffing the orchestrator section before and after by eye, not only by running the gate, and by
  recording the character arithmetic in the task list.
- **An agent may not know its corpus token.** Where an Aleph collection has no `foreign_id` and no
  usable label, or a file corpus is a loose set of paths with no common parent, the derivation has no
  input. The skill handles this the way the rest of the library handles a missing input — state what
  was used and why — rather than by inventing a token; a degraded token still beats a bare date.
- **Nothing verifies compliance.** As with every other convention here, a prompt that drifts off the
  scheme loads and runs. The four-invariant checks in `CLAUDE.md` gain no new member, because the
  scheme is prose rather than a resolvable reference. This is a known and accepted gap, not an
  oversight.
