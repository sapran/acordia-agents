## 1. The report-layout reference

- [x] 1.1 Create `acordia-analysts/skills/credential-harvest-triage/references/report-layout.md`
  with eight sections in order — lede, organising principle, document order, stylesheet, block
  anatomies, what fills the fixed blocks, rules that are not cosmetic, self-check; verify the file
  is markdown, carries exactly one ` ```css ` block, four ` ```html ` blocks and one ` ```sh `
  block, and that the section order matches
- [x] 1.2 Reproduce the delivered stylesheet verbatim plus three changed rules — `.cred.sys`,
  `.mono` and `ul,ol` — and name each change and its reason immediately below the block; verify
  every class the four anatomies use has a rule in the sheet, that `.mono` is actually used
  somewhere in the layout, and that the Gaps `<ol>` resolves to the authored margins rather than
  user-agent defaults
- [x] 1.3 Write the four `div.cred` anatomies as placeholder-only HTML drawn from a closed
  `ANGLE_CAPS` vocabulary declared in its own section, never `{BRACED}`, with an example entity
  identifier of at least 40 characters, an `Ownership` row on both credential blocks, the holder
  named by role only, and a derived key-type label rather than the artefact's own first line;
  verify the file carries no real credential value, no real entity id and no real hostname, that
  `grep -cE '\{[A-Z_]{2,}\}'` over the file returns 0, and that every token in the vocabulary
  section appears in an anatomy and vice versa
- [x] 1.4 State the eight rules that are not cosmetic, including the ownership gate on the
  disclosure element, and close the section by deferring disclosure to `SKILL.md`'s
  `## Guardrails`, rendering and citation to `briefing-reporting`, the coverage denominator to
  `exhaustive-data-processing` and the shape of a gap to `naming-the-gaps`; verify the file asserts
  no doctrinal claim — no sentence arguing why a product should be shaped a given way rather than
  stating a rule — and therefore carries no `doctrine_source` anywhere
- [x] 1.5 Add the self-check script, the sentence stating its expected verdict, the basis of the
  40-character short-link constant, and the statement that a clean verdict is a lint result rather
  than a proof and does not replace resolving a sample of the evidence references; verify the
  script blanks every `<pre>` body before its class and placeholder scans and that no probe can
  emit a `pre` body, a `summary` body, an attribute value or an evidence identifier

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
- [x] 4.5 Mutation-prove every probe against the substituted skeleton, each mutation moving
  exactly one output line: `.mono` rule deleted; a surviving `{BRACED}` token; the template copied
  with nothing substituted; an href truncated to its display form; an href that is not the anchor's
  first attribute; a single-quoted `style`; a single-quoted undefined class; an orphan `pre.key`
  carrying an extra attribute; a keyless `<details>` preceding an orphan `pre.key`; a `<details
  open>`; an anchor with no `href`. Re-run the pre-review patterns against the same documents and
  confirm they reported clean, and confirm an artefact quoted inside a `<pre>` body reaches none of
  the script's output
- [x] 4.6 Render the assembled document in a browser and confirm it paints — one `.cred.sys`, every
  `<details>` closed by default, the `pre.key` panel dark, the `table.kv` label column 150px
- [x] 4.7 Confirm the competency grid is untouched: `git diff --stat origin/develop -- docs/roles/`
  is empty
