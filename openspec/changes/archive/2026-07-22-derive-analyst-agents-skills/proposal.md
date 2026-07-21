## Why

`docs/roles/operational-analyst.md` is a competency map — a general analyst role, three specialisations, and an appendix grid of ~39 skills mapped across a shared "spine" and three legs. `docs/agents-skills-extension-workbook.md` is the mechanism for extending the tool with markdown agents and skills. Nothing connects them: the map describes analysts no tool can run, and the agent roster has attack-executor agents but no analysis/decision-support role. The appendix grid is already an agent↔skill wiring table; this change compiles it into runnable opencode artifacts.

## What Changes

- Add an **analyst skill library**: one `SKILL.md` per appendix-grid row (~39 skills) under `~/.config/opencode/skills/<name>/`. Plain kebab-case slugs, no prefix. Frontmatter is opencode's schema (`name` + `description` required).
- Add a **four-agent analyst roster** under `~/.config/opencode/agents/`: `operational-analyst` (`mode: primary`, the orchestrator/senior) plus three `mode: subagent` legs — `target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`.
- Establish a **competency-map derivation contract**: the appendix grid stays the single source of truth; grid rows compile to skills, and the ●/○ marks in each grid column define the skill set that agent's prompt draws on. Editing the grid regenerates the wiring — the two are never hand-maintained in parallel.
- The shared analytic "spine" (the `Core ●` rows) is named in the prompt of all four agents. opencode has no per-agent `skills:` binding — skills fire by description — so composition is: triggering-quality skill descriptions + each agent prompt naming its skill set.
- Analyst agents get read/analysis permissions only (deny-default, then read + web + shell for analysis) — no write/edit. They read, model, and judge; they do not throw payloads.

This change is **additive** — no existing agent, skill, or spec is modified or removed. All new files live in the user's opencode config tree.

## Capabilities

### New Capabilities

- `analyst-skill-library`: The skill set. One `SKILL.md` per grid row under `~/.config/opencode/skills/`, opencode frontmatter (`name` + `description` required, unknown fields ignored), and triggering-quality descriptions. The two cross-cutting deep skills — reverse-engineering and operational-technology — are ordinary skills; their attach-to-a-leg relationship is stated in prose.
- `analyst-agent-roster`: The four analyst agents under `~/.config/opencode/agents/`. Modes (one primary orchestrator, three subagents), dispatch `description` lines (the role doc's italic leg questions), portable prompt bodies (the leg paragraphs), deny-default read-only permission blocks, and each agent's skill set named in its prompt (resolved from its grid column).
- `competency-map-derivation`: The compile contract binding the grid to the artifacts. Row→skill, column→the agent's prompt skill set, ●/○→deep/working, section header→grouping (documentation only). Names the grid as source of truth and the regeneration rule that keeps agents and skills in sync with it.

### Modified Capabilities

<!-- None. No existing specs; this change is purely additive. -->

## Impact

- **New files (the user's opencode config, not committed to this repo):** ~39 `~/.config/opencode/skills/<slug>/SKILL.md`; 4 `~/.config/opencode/agents/<name>.md`.
- **Referenced source of truth:** `docs/roles/operational-analyst.md` (appendix grid) — read, not modified.
- **Loader exercised:** opencode's agent discovery (`~/.config/opencode/agents/`) and skill discovery (`~/.config/opencode/skills/`).
- **Doc updated:** `docs/agents-skills-extension-workbook.md` gains a verified opencode locations section + conventions.
- **No application code, no rebuild.** Markdown/config only.
