## 1. The skill that carries the scheme

- [x] 1.1 Rewrite the "Give the task its own directory" bullet in
      `acordia-analysts/skills/briefing-reporting/SKILL.md` to carry the full scheme: the
      `.acordia/work/` parent for the brief-names-none case with its reason (the current directory is
      where the corpus lives), the `<corpus>-<YYYY-MM-DD>-<task-slug>` stem, and the same stem for the
      product under `.acordia/reports/`.
- [x] 1.2 State the corpus-token derivation in the same skill — Aleph `foreign_id`, falling back to a
      slug of the collection label, and for a file corpus a slug of the analysed directory or archive
      name — with why it derives from the material rather than the request.
- [x] 1.3 State the collision rule: a taken stem takes `-2`, `-3` for both directory and product, and
      a colliding write succeeds with nothing reporting it.
- [x] 1.4 Update the `## Signals / outputs` bullet that names `.acordia/reports/` so the product is
      described as taking the task directory's stem.
- [x] 1.5 Confirm the bullet keeps the existing `README.md` requirement (request verbatim, its date,
      one line on what is being settled) unchanged, and adds no claim of enforcement.

## 2. The four leg prompts

- [x] 2.1 `acordia-analysts/agents/mission-analyst.md:105` — replace the bare "one you create and
      identify by name" with creation under `.acordia/work/`, deferring the stem to
      `briefing-reporting`.
- [x] 2.2 `acordia-analysts/agents/terrain-analyst.md:107` — same edit.
- [x] 2.3 `acordia-analysts/agents/collection-analyst.md:113` — same edit.
- [x] 2.4 `acordia-analysts/agents/overwatch-analyst.md:80` — same edit.
- [x] 2.5 Update the `## Guardrails` paragraph in all four so `.acordia/` is named as the root for the
      agent's own generated files, with `.acordia/reports/` still the product's place, and both still
      worded as convention rather than permission.

## 3. The orchestrator — character-neutral, three carriers

- [x] 3.1 Record the baseline: `len(body.strip())` for `acordia-analysts/agents/cyber-analyst.md` is
      **10,499 of 10,500** (1 character of slack). Note the exact character count of every insertion and every cut in this
      task list as it is made, so the arithmetic is auditable in review.
- [x] 3.2 Edit `## A directory per task, a bound per reply` so the brief-names-none case creates the
      directory under `.acordia/work/`, leaving `briefing-reporting` carrying the stem.
- [x] 3.3 Pay for the addition with a cut of equal or greater length **in the same section**,
      chosen for redundancy rather than for length. Do not touch the `## Guardrails` section or any
      sentence stating a restriction, a bound, or a hand-back obligation.
- [x] 3.4 Update the orchestrator's `## Guardrails` paragraph for the `.acordia/` root **only if** the
      arithmetic allows it after 3.3; if it does not, leave the guardrail exactly as it is and record
      the omission in `docs/implementation-notes.md` rather than cutting something else to fit.
- [x] 3.5 Propagate the identical body to `acordia-analysts/commands/analyst.md` and
      `acordia-analysts/commands/cyber-analyst.md`.
- [x] 3.6 Read the before/after diff of the orchestrator section by eye and confirm no guardrail,
      bound or obligation was lost. Gate check 7 compares bytes across carriers and cannot detect a
      deletion that happened in all three — this is the 6.10.0 failure shape and the gate does not
      catch it.

## 4. The credential-handling skills

- [x] 4.1 `acordia-analysts/skills/credential-harvest-triage/SKILL.md:168` — confirm the credential
      file stays "beside the notes" in the task directory and that the skill does **not** restate the
      stem rule; adjust only the wording that implies the directory has no defined parent.
- [x] 4.2 `acordia-analysts/skills/credential-harvest-triage/references/report-layout.md:206` and
      `:235` — the working-file and credential-file placement language now resolves to the addressed
      task directory.
- [x] 4.3 `references/report-layout.md:21` and `:196` — the product `<title>` and footer already carry
      target and date; confirm they identify the corpus, and adjust only if a title could name two
      corpora identically.

## 5. Specs, docs and version

- [x] 5.1 `openspec validate acordia-workfile-addressing --strict` passes.
- [x] 5.2 `/opsx:sync` — sync the two delta specs into `openspec/specs/agent-roster/spec.md` and
      `openspec/specs/skill-library/spec.md`.
- [x] 5.3 `README.md:25` and `:168` — describe `.acordia/` as the workspace root with its two sinks,
      keeping "a convention no harness enforces, and must never be described as enforced".
- [x] 5.4 `CLAUDE.md:19` and `:238` — same, so the authoring contract matches what ships.
- [x] 5.5 Bump 6.14.0 → 6.15.0 in all three JSON files:
      `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
      `.omp-plugin/marketplace.json`.

## 6. Verification

- [x] 6.1 `bash ~/ai/checks/check-acordia.sh .` — 8/8, with check 8 reporting the orchestrator body
      still within 10,500 and check 1 reporting 6.15.0 three times.
- [x] 6.2 Run the skill-set declaration check from `CLAUDE.md` (`skill-sets.json` vs the prompts) —
      `problems: 0`. No skill is added or removed, so the declaration should be untouched; a
      non-zero result means a prompt edit disturbed a `·`-separated line.
- [x] 6.3 Run the grid-transcription check from `CLAUDE.md` — `problems: 0` with the full row count.
      No grid row changes in this change; this confirms no prompt edit dropped a skill slug.
- [x] 6.4 `diff .claude-plugin/marketplace.json .omp-plugin/marketplace.json` — silent.
- [x] 6.5 Grep every shipped artifact for a working-file instruction that names no parent, to confirm
      none survived: the phrase "identify by name", a bare "dated slug", and any task-directory
      sentence in `acordia-analysts/` that does not resolve under `.acordia/`.
- [x] 6.6 Grep `acordia-analysts/` for `.acordia/ops/` — no match, confirming the withdrawn journal
      root did not return through `work/`.
- [x] 6.7 Confirm no prompt or skill describes the scheme as enforced: grep the new wording for
      "must be written to", "restricted to", "only writes" and similar, and read the guardrail
      paragraphs.

## 7. Land it

- [x] 7.1 Commit on the worktree branch, one commit per logical group.
- [x] 7.2 `/opsx:archive` the change.
- [ ] 7.3 Open a PR to `develop`.
- [ ] 7.4 Review the diff with `pr-review-toolkit:code-reviewer`, addressing or dismissing each
      finding before merge.
