## 1. The report-layout reference

- [x] 1.1 Create `acordia-analysts/skills/credential-harvest-triage/references/report-layout.md`
  with eight sections in order — lede, organising principle, document order, stylesheet, block
  anatomies, what fills the fixed blocks, rules that are not cosmetic, self-check; verify the file
  is markdown, carries exactly one ` ```css ` block, four ` ```html ` blocks and one ` ```sh `
  block, and that the section order matches
- [x] 1.2 Reproduce the delivered stylesheet verbatim plus exactly two added rules — `.cred.sys`
  and `.mono` — and name both additions and their reasons immediately below the block; verify every
  class the four anatomies use has a rule in the sheet
- [x] 1.3 Write the four block anatomies as placeholder-only HTML in `ANGLE_CAPS` form, never
  `{BRACED}`, with an example entity identifier of at least 40 characters; verify the file carries
  no real credential value, no real entity id and no real hostname, and that
  `grep -cE '\{[A-Z_]{2,}\}'` over the file returns 0
- [x] 1.4 State the seven rules that are not cosmetic, and close the section by deferring
  disclosure to `SKILL.md`'s `## Guardrails`, rendering and citation to `briefing-reporting`, and
  the coverage denominator to `exhaustive-data-processing`; verify the file asserts no doctrinal
  claim and therefore carries no `doctrine_source` anywhere
- [x] 1.5 Add the self-check script and the sentence stating its expected verdict; verify the
  script prints only class names, integer counts and stripped `h2` text, and emits no `pre`,
  `summary` or attribute value

## 2. The skill body

- [x] 2.1 Append one sentence to triage step 8 of
  `acordia-analysts/skills/credential-harvest-triage/SKILL.md` pointing at
  `references/report-layout.md` and naming the organising principle; verify step 8's existing
  sentences are unchanged and the new sentence is last
- [x] 2.2 Insert a `## Report layout` naming-pointer section between `## Pattern library` and
  `## Signals / outputs`, matching the shape of the pattern-library pointer; verify
  `grep -c 'references/report-layout.md' SKILL.md` returns 2 and that the frontmatter, guardrails
  and every other section are untouched

## 3. Spec, version and notes

- [x] 3.1 Author `openspec/changes/credential-sweep-report-layout/` with `proposal.md`,
  `design.md`, `tasks.md` and `specs/skill-library/spec.md`; verify the delta's two MODIFIED blocks
  each reproduce every scenario the published requirement has, by title
- [x] 3.2 Bump 6.8.0 → 6.9.0 in all three occurrences —
  `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.omp-plugin/marketplace.json`; verify with the version-lockstep check in
  `~/ai/checks/check-acordia.sh`
- [x] 3.3 Record the measured `acordia-map.html` drift in `docs/implementation-notes.md` as parked
  out-of-scope work; verify the entry names the figures and does not propose a fix here

## 4. Gates

- [x] 4.1 Run `openspec validate --all --strict`; verify it passes
- [x] 4.2 Run `~/ai/checks/check-acordia.sh` against the worktree; verify all six checks report ok,
  including the worktree-only artifacts-changed-without-a-bump check
- [x] 4.3 Run the four by-hand invariant checks from `CLAUDE.md` — slug resolution, grid-mark
  transcription, catalog byte-identity plus JSON parse, and skill-set declaration; verify every one
  reports zero problems and that the grid check's row count equals the grid's own
- [x] 4.4 Assemble a minimal document from the reference file's own CSS and HTML blocks and run the
  file's own self-check against it; verify it prints `none`, `0`, `none`, `0`, a short-link count of
  `0`, and a section list ending Coverage, Gaps, Hand-off
- [x] 4.5 Mutation-prove the self-check: delete the `.mono` rule and confirm it names `mono`;
  restore, change one example href to a `{BRACED}` token and confirm it names that token; restore
  and confirm the verdict returns clean
- [x] 4.6 Render the assembled document in a browser and confirm it paints — one `.cred.sys`, every
  `<details>` closed by default, the `pre.key` panel dark, the `table.kv` label column 150px
- [x] 4.7 Confirm the competency grid is untouched: `git diff --stat origin/develop -- docs/roles/`
  is empty
