## 1. Literature first

- [x] 1.1 Search the library for what the canon says about the size and form of a report handed up,
      and about working notes kept apart from the finished product.
- [x] 1.2 Bring back the passages quoted, with author, work, page and document id, and select from
      them before writing any prose.
- [x] 1.3 Confirm every selected work is already registered in `docs/roles/sources.md`, so the change
      introduces no new register entry.

## 2. Move the source document first

- [x] 2.1 Add the hand-back paragraph to `docs/roles/operational-analyst.md` under *How the pieces
      fit*, beside the Monte p. 63 sentence on inter-unit communication that it extends.
- [x] 2.2 Add no grid row, no column and no mark, so the bijection and both transcriptions are
      untouched.

## 3. The four legs

- [x] 3.1 Add the hand-back section to `mission-analyst`, `terrain-analyst`, `overwatch-analyst` and
      `collection-analyst`, beside each prompt's existing *What to return* section.
- [x] 3.2 State all three parts in each: full working to a notes file in the directory the brief
      names; a bounded summary that names that file; the bound treated as real.
- [x] 3.3 State the overflow rule — a read that does not fit means the question was too large, said
      plainly with what was left out, never truncated in silence.

## 4. The lead

- [x] 4.1 Add the task-directory convention to `cyber-analyst`: a directory per task with a short
      dated slug, a `README.md` holding the request verbatim with the date and one line on what is
      being settled, and the legs' notes written into the same directory.
- [x] 4.2 State that the lead supplies both the directory and the bound in every dispatch, and that
      an unstated bound is the lead's defect.
- [x] 4.3 State that the lead reads the notes files before it fuses.
- [x] 4.4 Bind the lead by the same contract for its own product.

## 5. Prove the acceptance criteria

- [x] 5.1 All five prompts state a hand-back contract — check each by reading it.
- [x] 5.2 No prompt names a harness, a tool, a path or a number: grep the five prompts for digits and
      for the tool and harness vocabulary the handoff excludes, and account for every hit.
- [x] 5.3 The lead prompt states the task-directory convention and that it supplies the directory and
      the bound in every dispatch.
- [x] 5.4 `skill-sets.json` still agrees with the prompts, in both directions, at 29 / 22 / 31 / 33 /
      25 skills.

## 6. The four invariants that lost their gate

- [x] 6.1 Every skill slug named in a prompt resolves.
- [x] 6.2 Every grid mark reaches the skill and the prompt — `problems: 0`, with the row count equal
      to the grid's own.
- [x] 6.3 The two marketplace catalogs are byte-identical and all four JSON files parse.
- [x] 6.4 The declared skill sets match the prompts — `problems: 0`.

## 7. Release mechanics

- [x] 7.1 Bump `6.3.0` → `6.4.0` in lockstep across the three version occurrences.
- [x] 7.2 Record the parked CI finding in `docs/implementation-notes.md`.
- [x] 7.3 `openspec validate --all --strict`.
- [x] 7.4 `~/ai/checks/check-acordia.sh` in the worktree, before the PR.
