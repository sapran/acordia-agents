## Why

`analysts/skills/exhaustive-data-processing/SKILL.md:3` has an unquoted `description` whose `processed in full: cover 100%` substring makes the frontmatter invalid YAML — `yaml.safe_load` raises `mapping values are not allowed here` at line 3, column 202. It is the only parse failure among the 282 frontmatter-bearing files in the repository, and it ships today: `plugins/claude/acordia-analysts/skills/exhaustive-data-processing/SKILL.md` and the omp copy carry the identical defect.

The defect matters more than one malformed file, because of how it survived. `analyst-skill-library` requires valid frontmatter and offers the scenario "Required fields present and valid"; `operator-skill-library` requires the same and scopes a scenario to "WHEN any operator skill's frontmatter is **parsed**"; `CLAUDE.md` restates the contract as a format rule. Three normative statements, and nothing parses a skill. The generator copies skill trees with `shutil.copytree` and never opens them, while `--check` compares bytes with `filecmp.cmp` — so two byte-identical broken trees pass the gate green. omp's lenient reader tolerates the file, which is why nobody noticed; opencode's stricter contract is the harness that would drop it silently.

Agents already have exactly the enforcement skills lack: `read_agent()` parses frontmatter through `split_frontmatter()` and raises `TranslationError`, failing the build. Skills were routed around it on the rationale that they are valid unchanged across harnesses — a rationale this file disproves.

Current behavior: a skill can carry unparseable frontmatter, ship to both plugin trees, and pass `--check`. Desired behavior: the generator parses every `SKILL.md` it packages and fails the build on a violation, exactly as it already does for agents.

## What Changes

### Skill body — the malformed description is repaired

`analysts/skills/exhaustive-data-processing/SKILL.md:3` gains a quoted `description` value. Wording is unchanged; only the YAML scalar is quoted, so the trigger-quality requirement that governs it is unaffected.

### The generator — skills are parsed before they are packaged

`tools/build-plugins.py` gains a skill-frontmatter gate that runs before the skill tree is copied, checking what the two skill-library specs and `CLAUDE.md` already require:

- frontmatter parses as a YAML mapping,
- `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, is ≤64 chars, and equals the containing folder slug,
- `description` is 1–1024 characters,
- no key outside `name` / `description` / `metadata`,
- no `sha256`, `signature`, or `signed_by`.

A violation raises `TranslationError` and fails the build, the same failure path `read_agent()` uses. The gate covers both pillars, since both skill libraries state the contract.

### The version — a MINOR bump

`VERSION` moves `2.2.0` → `2.3.0`. A skill body reaches users, and an unbumped version means the repaired file never arrives at anyone who already installed the plugin.

### Generated trees — rebuilt

The six version-carrying files and the two copies of the repaired skill are regenerated, and `--check` is run by hand.

**Deliberately not added:** no CI, no hooks, no lint automation, and no new script. The gate is ~20 lines inside the one generator that already exists, and is run the same way every other command here is run — by hand. This follows `harden-plugin-distribution`, which recorded the same exclusion.

**Not in scope**, each a separate finding from the same review, none of them blocking this one:

- enforcing the `VERSION`-bump obligation itself (commit `cc7339a` edited a source skill without a bump; it self-healed only because `97c6b40` later bumped),
- extending the `Method` contract at `analyst-skill-library` beyond its closed 15-skill list to the 24 grid skills that read raw artefacts without a verifiability anchor,
- wiring `aleph-mcp` so `aleph-entity-graph`'s primary path is reachable (already a recorded Non-Goal),
- supplying `web_search` doctrine for the four analysts granted the tool.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plugin-packaging`: a new build gate. The generator SHALL parse and validate every skill frontmatter it packages and fail the build on violation, closing the asymmetry with agents. The frontmatter contract itself is unchanged — it already exists in `analyst-skill-library` (opencode frontmatter contract) and `operator-skill-library` (frontmatter reduction, signing-triple removal); this change makes those existing requirements enforced rather than merely stated, so neither spec's requirements move.

## Impact

- **Modified:** `tools/build-plugins.py` (skill gate, `VERSION`), `analysts/skills/exhaustive-data-processing/SKILL.md` (quoted description).
- **Regenerated:** both `plugins/` trees — the repaired skill in each, plus the six files carrying the version.
- **Unchanged:** every agent prompt, every command wrapper, `install.sh`, and the other 42 analyst skills.
- **Behavioral risk:** the gate may reject skills that are currently shipping. All 282 files were parsed during the review and exactly one fails, so the expected blast radius is the single file this change repairs; the build failing on anything else is new information and should be treated as a finding, not worked around.
- **Verified during the review that motivated this change:** the parse failure and its exact position, its propagation into both plugin trees, that `--check` is a byte comparison and passes green on it, and that agents alone hold the parse-and-fail path.
