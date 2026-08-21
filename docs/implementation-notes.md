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
- **`cyber-operator` has 16 characters left.** 9,984 of 10,000, measured on the body after the
  frontmatter with `wc -m` (not `wc -c` — the em dashes are multi-byte). 4.2.0's lead heading, heading
  spacing and three fence languages took it from 9,960, spending 24 of the 40 characters that were
  free — 60% of the headroom, for a change that altered no prose. What still fits is a slug of up to
  13 characters plus its 3-character ` · ` separator: `bolts` (5), `attack-jwt` (10) and
  `ad-security` (11) would all land, but the median operator slug is around 15 and would not. What is
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
  command wrappers — with two near variants at `analyst-loop/SKILL.md:32` (_"is the operation still
  clean"_) and `overwatch-analyst.md:46` (_"is the footprint still clean"_). That is six other sites;
  seven counting `cyber-analyst` itself, and a settling change must touch all seven. Parked rather than
  propagated because choosing the wording is an authoring decision, not a formatting one: either the
  new phrasing is right and the other six follow it, or the canonical one is and the prompt reverts.

- **`cyber-analyst` no longer says what the target is _for_.** The same edit replaced _"what the
  target is **for**, what it depends on"_ with _"what the target **is**, what it **does**"_. Three
  further authored sites still carry the superseded phrasing, one of them in the same file:
  `cyber-analyst.md:26` (the `target-analyst` bullet, sixteen lines below the rewritten line, so the
  prompt now describes the target picture two ways within itself), `analyst-loop/SKILL.md:31`, and
  `target-analyst`'s own `description`, which opens _"What is the target for, what does it depend
  on"_. `docs/roles/operational-analyst.md` italicises _for_ twice deliberately — objectives, and the
  processes that carry them — which is the content of `target-mission-analysis`. Four sites, same
  decision, same change.
