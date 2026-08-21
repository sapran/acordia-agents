## 1. Remove the operations pillar

- [ ] 1.1 `git rm -r acordia-operators/` — five agents, forty skills, ten wrappers, one manifest
- [ ] 1.2 `git mv docs/roles/operator.md docs/roles/archive/operator.md` and add a header line stating
      it is retired provenance for a pillar no longer shipped, retained because it is the only record
      of the CyberStrike port at commit `359655518` and its deliberate divergences
- [ ] 1.3 Drop the `acordia-operators` entry from `.claude-plugin/marketplace.json` and
      `.omp-plugin/marketplace.json`; confirm the two files remain byte-identical with `diff`
- [ ] 1.4 Strip the operations sections from `CLAUDE.md`: the pillar bullet, the `metadata.cyberstrike`
      contract, the `.acordia/ops/` conventions, the operations half of the source-of-truth table, and
      the "To add an operations skill" instruction
- [ ] 1.5 Strip operations references from `README.md`

## 2. Split and retire the analyst legs

Prompt *bodies* are not authored here — see §4. This section moves files and fixes structure only.

- [ ] 2.1 `git mv acordia-analysts/agents/target-analyst.md acordia-analysts/agents/terrain-analyst.md`
- [ ] 2.2 Create `acordia-analysts/agents/mission-analyst.md`
- [ ] 2.3 Create `acordia-analysts/agents/collection-analyst.md`
- [ ] 2.4 `git rm acordia-analysts/agents/fusion-analyst.md`
- [ ] 2.5 Set frontmatter on all five: `name` equal to the filename stem, `description` opening
      `ACORDIA Analysis — `, `color` cyan for `cyber-analyst` and blue for the four legs. Exactly
      three keys, nothing else
- [ ] 2.6 Rename the canonical wrappers to match, add wrappers for the two new agents, remove the
      `fusion-analyst` wrapper and its alias, and repoint the aliases: `analyst`, `mission`, `terrain`,
      `overwatch`, `collection`. Assert 10 wrappers, five canonical and five aliases
- [ ] 2.7 Confirm no alias stem equals an agent stem, and that every wrapper names a live agent

## 3. Re-anchor the grid

- [ ] 3.1 Mint a stable kebab-case row id for every skill row in the appendix grid of
      `docs/roles/operational-analyst.md` and record it in the row itself
- [ ] 3.2 Rewrite the grid's four leg columns as five: Core, Mission, Terrain, Def, Coll. Redistribute
      the Fusion column per the design — operating picture and multi-source correlation to Core,
      non-technical context integration to Mission, take quality and data tooling to Coll
- [ ] 3.3 Update all 38 skills carrying `source: docs/roles/operational-analyst.md#L<n>` to
      `row: <id>` plus a `source:` with no line number; keep `grid_row`, `grid_deep_in` and
      `grid_working_in` correct against the new columns
- [ ] 3.4 Verify every `row:` resolves to exactly one grid row and every grid row is claimed by
      exactly one skill

## 4. Author the prose — passages selected 2026-08-21

**Write from `docs/methodology-alignment-proposal.md` §8 and nothing else.** Thirty of the
thirty-four passages were selected in a four-tranche walkthrough; §8 assigns each to a seat. A passage
absent from §8 was considered and rejected, so reaching for it is not a shortcut, it is a reversal.
Authoring from recall instead of from §8 is the failure this repository's characteristic bug comes
from, and the literature-first rule exists to prevent it.

- [ ] 4.1 Write the `mission-analyst` prompt body — organisational target model, crown-jewels and
      mission-thread work, and the target's procedures, redundancy and reporting culture
- [ ] 4.2 Write the `collection-analyst` prompt body — take quality and value, bulk material at
      volume, data integration and correlation tooling
- [ ] 4.3 Rewrite the `terrain-analyst` prompt body for the narrowed technical scope
- [ ] 4.4 Rewrite the `cyber-analyst` prompt: it holds the operating picture and multi-source
      correlation, routes to four legs, and produces a product for a **human operator** — its
      end-neutral loop judges from reported evidence, not from its own dispatched action
- [ ] 4.5 State the Analysis/Control boundary in the `overwatch-analyst` prompt: it analyses
      detection and own-emissions, it does not perform the Control action that follows
- [ ] 4.6 Add the third end to the grid and the lead — effect, collection, **and access held for
      later use** — replacing the current dual end
- [ ] 4.7 Add the operating-logic axis: espionage / subversion / sabotage, with the coding rule
- [ ] 4.8 Update the `·`-separated skill lines in all five prompts; confirm every slug resolves
- [ ] 4.9 Confirm every prompt body stays under the 10,000-character ceiling

## 4b. Edit the published specs directly — a delta cannot reach these

`openspec instructions specs` states that a `## Purpose` in a delta for an *existing* capability is
ignored; the published Purpose is edited in place. All four still describe two pillars, so the deltas
alone would leave the synced specs self-contradicting.

- [ ] 4b.1 Rewrite the `## Purpose` of `openspec/specs/agent-roster/spec.md`
- [ ] 4b.2 Rewrite the `## Purpose` of `openspec/specs/skill-library/spec.md` — it currently reads
      "the skill libraries the two pillars ship … the operations library's upstream provenance"
- [ ] 4b.3 Rewrite the `## Purpose` of `openspec/specs/competency-map-derivation/spec.md`
- [ ] 4b.4 Rewrite the `## Purpose` of `openspec/specs/plugin-distribution/spec.md`
- [ ] 4b.5 Update `openspec/config.yaml` — its project context still names two pillars, three legs and
      a 40-skill technique library


## 5. Doctrinal provenance

- [ ] 5.1 Create `docs/roles/sources.md` — the register: author, title, library document id, one per
      work the doctrine draws on
- [ ] 5.2 Add the attribution field to `metadata.acordia` on skills whose bodies rest on a specific
      work rather than on general practice
- [ ] 5.3 Record the searched-and-empty findings rather than leaving them implicit

## 6. Version and gates

- [ ] 6.1 Bump 4.2.0 → **5.0.0** in all three remaining occurrences: one `plugin.json`, one entry in
      each of the two catalogs
- [ ] 6.2 Update `~/ai/checks/check-acordia.sh` — it asserts one semver at exactly six occurrences
      across four JSON files, which is now three across three. It fails on a correct repo until fixed
- [ ] 6.3 Run `~/ai/checks/check-acordia.sh .worktrees/analysis-only`
- [ ] 6.4 Run `openspec validate --all --strict`
- [ ] 6.5 Install from the checkout and confirm `/agents` lists all five, then dispatch one leg and the
      lead and confirm each runs

## 7. Land it

- [ ] 7.1 `openspec archive analysis-only --yes`, re-validate, commit the archive in the same PR
- [ ] 7.2 Review with `reviewer` and `security-reviewer`; fix or dismiss each finding
- [ ] 7.3 Merge to `develop` with a merge commit, then remove the worktree and delete the branch
- [ ] 7.4 State plainly in the PR body that an installed `acordia-operators` stays resident at 4.2.0
      and is not removed by this change
