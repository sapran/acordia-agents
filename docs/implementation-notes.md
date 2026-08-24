# Implementation notes

Out-of-scope findings recorded during work on other changes. Nothing here has been acted on.

_All three entries recorded before 3.0.0 were resolved by `collapse-to-authored-tree` and removed:
the `todo`-not-in-the-generated-tool-inventory note (agents no longer declare a tool list at all),
the four single-cased SQL-to-RCE deny patterns (the deny map was dropped with opencode; the upstream
gap is recorded in `docs/roles/operator.md`), and the missing rule that retrieved content is data
rather than instructions (now stated in all nine prompts)._

## Parked in 4.1.0

- **The bolt registry is not announced anywhere an agent reads first.** `.acordia/bolts.json` is
  defined only inside `bolts/SKILL.md`. The five operations prompts each point explicitly at
  `.acordia/ops/` so an agent knows the journal exists before it loads `operation-journal`; nothing
  gives it the same signal for the bolt registry. Because the working-knowledge line only makes a
  skill _available_ for selection rather than autoloading it, an agent that never selects `bolts` can
  run tooling locally without learning that a registry of network positions was configured for the
  engagement. The fix is one clause in the prompts' journal sentence, or a row in
  `operation-journal`'s file table marking `.acordia/bolts.json` as the sibling that records execution
  position. Parked because `cyber-operator`'s prompt body has 16 characters of headroom against the
  10,000-character ceiling, so adding prose there is blocked until technique detail moves into a
  skill — which is the same work the ceiling note below calls for.
- **`cyber-operator` has 16 characters left.** 9,984 of 10,000, measured on the body after the closing
  frontmatter delimiter with leading and trailing whitespace stripped, counting characters not bytes
  (the em dashes are multi-byte, so `wc -c` disagrees). State the convention whenever quoting this:
  the same body is 9,987 raw and 9,985 lstripped. Two values for this one measurement already existed
  before 4.2.0 — 9,962 here and 9,963 in the revive-bolts proposal, the same body under two unstated
  conventions — and 4.2.0 adds a third, 9,960, by stating one. 4.2.0's lead heading, heading
  spacing and three fence languages took it from 9,960, spending 24 of the 40 characters that were
  free — 60% of the headroom, for a change that altered no prose. What still fits is a slug of up to
  13 characters plus its 3-character ` · ` separator. Of the forty operations slugs only four are short
  enough and not already named in this prompt: `attack-cors`, `attack-sqli`, `attack-ssti` and
  `attack-xxe`, all 10 or 11 characters. The median operations slug is 17 and would not fit. What is
  blocked outright is prose. `agent-roster` prescribes the remedy: move technique detail into the
  skill that owns it, never delete routing or guardrails. Formatting is charged against this budget
  too, so treat a repo-wide style change as a content change on this one file.
- **`skill-library`'s cloned-count header says thirty, the tree carries thirty-one.** The requirement
  `Thirty operations skills cloned from CyberStrike` enumerates 26 standalone + 4 WSTG bundles = 30,
  but 31 files carry `metadata.cyberstrike`; `attack-sqli` accounts for the difference and has its own
  requirement. Pre-existing, untouched by 4.1.0, and cosmetic — but the header will keep reading wrong
  until the enumeration admits it.
- **A real routable IPv4 remains fetchable from GitHub by SHA.** The July `feat/operator-bolts`
  branch shipped the author's own WireGuard egress address in the bolts registry example. It never
  entered `develop`, both branches carrying it are deleted, and it is purged locally — but GitHub
  keeps unreachable objects, so `git fetch <remote> 33e2b88` still returns it. The repository is
  private, so exposure is limited to accounts with access. **Before making this repository public,
  ask GitHub Support to garbage-collect unreachable objects**, or treat the address as disclosed.

- **`cyber-analyst` describes the overwatch leg differently from how that leg describes itself.**
  4.2.0 rephrased the bullet in `cyber-analyst`'s prompt to _"is there a threat of detection, and is
  our operation still undetected"_. The canonical question stands verbatim in four authored places —
  `docs/roles/operational-analyst.md:39`, `overwatch-analyst`'s own `description`, and both of its
  command wrappers — with two near variants at `analyst-loop/SKILL.md:33` (_"is the operation still
  clean"_) and `overwatch-analyst.md:47` (_"is the footprint still clean"_). That is six other sites;
  seven counting `cyber-analyst` itself, and a settling change must touch all seven. Parked rather than
  propagated because choosing the wording is an authoring decision, not a formatting one: either the
  new phrasing is right and the other six follow it, or the canonical one is and the prompt reverts.

- **`cyber-analyst` no longer says what the target is _for_.** The same edit replaced _"what the
  target is **for**, what it depends on"_ with _"what the target **is**, what it **does**"_. Three
  further authored sites still carry the superseded phrasing, one of them in the same file:
  `cyber-analyst.md:27` (the `target-analyst` bullet, sixteen lines below the rewritten line 11, so the
  prompt now describes the target picture two ways within itself), `analyst-loop/SKILL.md:32`, and
  `target-analyst`'s own `description`, which opens _"What is the target for, what does it depend
  on"_. Both of its command wrappers carry the same description verbatim —
  `acordia-analysts/commands/target.md:2` and `acordia-analysts/commands/target-analyst.md:2` — and
  `README.md:145` quotes it as the worked frontmatter example, so a rewording has to reach those too.
  Two more carry it: `docs/roles/operational-analyst.md:33` quotes the canonical target question
  verbatim, and `target-analyst.md:47` opens its return contract with _"what it is for, what it depends
  on"_ — the structural twin of the `overwatch-analyst.md:47` site the note above cites. That document
  also italicises _for_ twice deliberately, at lines 11 and 23 — objectives, and the processes that
  carry them — which is the content of `target-mission-analysis`. Eight authored sites plus the README
  echo, same decision, same change.

- **A shell pipeline inside a table cell cannot be correct for both consumers.** GFM requires a `|`
  inside a table cell to be escaped as `\|`, even within a code span. Escaped, the cell renders right
  and the raw markdown is wrong: under `grep -E` a `\|` matches a literal pipe, so
  `grep -rIED 'password\|token\|secret\|api[_-]?key'` does not match `password=hunter2` — it exits 1
  with no output, which an operator reads as _no credentials found_. Unescaped, the raw command is
  right and the renderer splits the row, dropping the description column entirely. A skill is fed to
  the agent as raw markdown, so the raw form is the one that executes, and 4.2.0 chose the escaped
  form because the alternative was three rows whose command and description both disappeared.
  Affected: `linux-postexploit:34` and `:59` (both ERE alternations, the higher-risk pair),
  `k8s-postexploit:61` (a descriptive pipeline, not runnable as written), and
  `gcp-postexploit:67`, which already carried the escaped form before this change. The fix is to move
  these four commands out of their table cells into fenced blocks, where a pipe needs no escaping and
  both forms agree. Not done here: three of the four files are provenance-tracked ports and
  restructuring their tables is a content change, not a formatting one.

## `doctrinal-provenance` spec violates the repository's own lint policy

Found while linting the 6.0.0 install-scripts change, which does not touch this file.
`openspec/specs/doctrinal-provenance/spec.md:3` fires MD022 (blanks-around-headings): its `## Purpose`
heading is followed immediately by prose with no blank line. The `plugin-distribution` requirement _A
committed lint policy governs the authored markdown_ asserts that applying the policy to every
unexcluded file reports zero violations, and `openspec/specs/` is not excluded — so the published spec
currently contradicts itself by one line. Fix is a single blank line after line 3. Parked because the
file is outside this change's scope and the assertion it breaks is about the tree, not about anything
this change altered.

## Parked in 6.0.0

- **The lint policy is not clean, and the obvious command says it is.** `npx markdownlint-cli2 .`
  resolves `.` to `*.{md,markdown}` because `.markdownlint-cli2.jsonc` declares no `globs`, so it
  lints two top-level files and reports `0 issues` — a green that proves nothing. The scope the
  `plugin-distribution` requirement actually asserts is every unexcluded file, which is
  `npx markdownlint-cli2 "**/*.md"`: 74 files, and it reports three violations, not the one the note
  above records. `docs/methodology-alignment-proposal.md:96` (MD032, a list without surrounding
  blanks) and `docs/roles/archive/operator.md:1` (MD041, first line not a top-level heading) join
  `openspec/specs/doctrinal-provenance/spec.md:3`. Anyone fixing only the blank line believes the
  requirement is satisfied and it is not. Parked because three unrelated files sit outside the scope
  of the change that found this.
- **`CLAUDE.md` still tells the reader the repository has no lint.** `CLAUDE.md:42` opens the
  Commands section with _"There is no build, no lint and no test suite"_, while
  `.markdownlint-cli2.jsonc` has been committed since 4.2.0 and the requirement above asserts it is
  clean — so the one check a contributor can run locally is the one the section says does not exist.
  The fix is to correct that sentence and name the `"**/*.md"` form beside the external gate, not the
  bare `.` form. Parked because rewriting what that section claims is a change to the section, not
  one of the four additions the change that found this was scoped to.
- **The ceiling's measurement convention is stated everywhere except the spec that mandates it.**
  `openspec/specs/agent-roster/spec.md:338` says only _"10,000 characters, measured after the
  frontmatter"_, and its scenario at line 345 repeats the same unstated wording. That ambiguity is
  exactly what gave one prompt body three different recorded figures. `CLAUDE.md` now states the
  convention — body after the closing frontmatter delimiter, whitespace-stripped, characters not
  bytes — but a spec is the authority a normative claim is supposed to trace to, so anyone measuring
  from the spec reproduces the ambiguity and only readers arriving via `CLAUDE.md` get the answer.
  The fix belongs in the spec and is therefore an OpenSpec change, which is why it is parked rather
  than folded into a docs commit.

## Parked in 6.1.0

Both surfaced while measuring the skill-description compression
(`openspec/changes/archive/*-compress-skill-descriptions/`). Neither is fixed there, because both
turn on a claim about how analytic work is divided, and `CLAUDE.md` requires such a claim be selected
from the literature before it is written — the lib.ai library returned `database disk image is
malformed` on every call throughout that work, so the selection could not be made.

- **The competency grid and the agent prompts disagree about the analytic spine.** All four legs
  carry a 12-skill `Shared analytic spine (every analyst carries this)` line, but the grid in
  `docs/roles/operational-analyst.md:96-106` marks those rows in the `Core` column alone — `○` marks
  appear in the leg columns only sporadically. Derived from the grid, `mission-analyst` owns 10
  skills; its prompt names 19. The prose is almost certainly right and the grid is the record that
  never caught up, but `CLAUDE.md` makes the grid normative, so the fix is a grid edit that adds the
  spine marks across the four leg columns, not a prompt edit. This matters more than a bookkeeping
  drift: acceptance criterion 1 of `docs/handoff-skill-catalogue-prompt-budget.md` asks for a
  machine-readable per-analyst skill list, which necessarily records one of the two as the set.
  **Still open after 6.2.0**, which declared the sets as the prompts state them rather than as the
  grid does. That was judged to surface the drift rather than harden it: `skill-sets.json` and the
  grid are now two machine-readable records whose disagreement a single command can show, where
  before nothing compared them at all. The check also proves the 12-skill spine is identical across
  all four legs, so what remains is one question — whether the grid should carry `○` marks for the
  spine in the four leg columns — and that is still a claim about how analytic work is divided, so it
  still needs the literature the outage withheld.
- **~~Three skills are named in no agent prompt.~~ Withdrawn in 6.2.0 — the finding was wrong.**
  `aleph-entity-graph`, `credential-harvest-triage` and `exhaustive-data-processing` are named in
  **all five** prompts, in backticks, in their own procedural sections. The scan that produced the
  finding read only `·`-separated skill lines, which is not the only binding a prompt uses. No skill
  in the library is unreachable. The real consequence was a three-skill undercount in every
  analyst's set, which is corrected in `openspec/changes/archive/*-declare-analyst-skill-sets/` along
  with the catalogue figures that were computed from it.

- **`target-mission-analysis` prose contradicts its own row.** `docs/roles/operational-analyst.md`
  says of the crown-jewels / mission-thread paragraph "Every operational analyst carries this at a
  working level; the deep method lives with the Target & Network specialist" — but the row is
  marked `Core ○ · Mission ●` only, and just
  `cyber-analyst` and `mission-analyst` name the slug — so three legs do not carry it at any level.
  The sentence also names the **Target & Network** leg, which v1.2 split into Mission and Terrain.
  Found while fixing the spine rows in 6.3.0 and parked: it is a different row, the marks and the
  prompts already agree with each other, and nothing is broken downstream. Resolving it means
  deciding which is true — mark `○` in Terrain/Def/Coll and add the slug to those three prompts, or
  correct the sentence — and that is a doctrinal call needing a literature selection, not a
  transcription fix.

## Parked in 6.3.0

Both found while rebuilding `acordia-map.html`, and both sit outside that rebuild's scope.

- **The map's search icon emits a console error and draws no circle.** `acordia-map.html` carries
  `<circle cx=11 cy=11 r=7/>` in the sidebar search SVG. The attribute value is unquoted, so the
  parser reads the self-closing slash as part of it and the browser rejects `r` with
  `Expected length, "7/"`. Verified in a real page load: one console error, and the magnifier's
  circle is missing. The fix is `r="7"`. Parked because the defect is in the page's hand-written
  shell, which a data rebuild does not touch.
- **Nothing in the repository can rebuild the map.** The DATA blob inside `acordia-map.html` is
  generated output with no generator: each regeneration has re-derived the renderer and the metric
  formulas by reading the previous blob. This one was rebuilt by a script kept outside the repo,
  because committing a build tool would change the shape of the distribution — a MAJOR bump plus an
  OpenSpec change under `plugin-distribution`, which is a decision of its own rather than part of a
  docs refresh.
