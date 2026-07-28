## Why

The 47-skill analyst library already loads in the omp harness — omp ships an `opencode` skill provider that reads `~/.config/opencode/skills`, so `install.sh` gets skills into omp for free today. The four analyst **agents** do not load. omp discovers task agents only from `<project>/.omp/agents`, `~/.omp/agent/agents`, and Claude plugin roots, and it deliberately skips cross-harness agent directories because their frontmatter is a different schema. The result is a half-installed pillar: an omp operator gets the analytic spine but not the analysts that wield it.

## What Changes

- **Install script.** `install.sh` gains a `--harness opencode|omp|both` selector (default `opencode`, preserving today's behaviour). The `omp` harness deploys translated agent files into `~/.omp/agent/agents/` and skill directories into `~/.omp/agent/skills/`. `uninstall.sh` learns the same selector and removes what the omp harness owns.
- **New translator.** A `tools/translate-omp.py` script converts one opencode agent file into one omp task-agent file: it derives the required `name` field, maps the opencode `permission` map onto omp's `tools` allowlist, maps `mode: primary` onto `tools: [..., task]` plus an explicit `spawns` list of the three legs, maps `mode: subagent` onto an allowlist without `task`, preserves `metadata`, and rewrites the one prompt paragraph that names a `list` tool omp does not have.
- **Generated, never hand-maintained.** Translated agent files are build output under a gitignored `.build/omp/`, produced from `analysts/agents/*.md` at install time. Editing a translated file is a drift bug in the same sense that editing `analysts/` without touching the competency map is.
- **No change to the source artifacts.** `analysts/agents/*.md` and `analysts/skills/*/SKILL.md` stay opencode-native and remain the single source of truth for both harnesses.
- **Docs.** `docs/agents-skills-extension-workbook.md` gains the frontmatter mapping table; `README.md` gains the omp install path and the two harness-parity gaps (no path-scoped write permission; `bash` is still a write channel in both harnesses).

Current behaviour: `./install.sh` deploys to `~/.config/opencode/` only; agents are invisible to omp.
Desired behaviour: `./install.sh --harness omp` deploys a working analyst roster into omp, translated from the same source files.

## Capabilities

### New Capabilities
- `omp-harness-distribution`: how the opencode-native source artifacts are translated and deployed into the omp harness — the frontmatter mapping contract, the deployment locations, the generated-output rule, and the parity gaps that translation cannot close.

### Modified Capabilities

None. The opencode artifacts and their existing requirements are unchanged; this change adds a second deployment target that reads them.

## Impact

- `install.sh`, `uninstall.sh` — new `--harness` selector, new deploy paths.
- `tools/translate-omp.py` — new; a `uv` PEP 723 script, `pyyaml` as its only declared dependency, resolved into uv's isolated environment.
- `.gitignore` — ignore `.build/`.
- `README.md`, `docs/agents-skills-extension-workbook.md` — omp install and mapping documentation.
- Deployment surface outside the repo: `~/.omp/agent/agents/`, `~/.omp/agent/skills/`.
- No change to `analysts/`, to `openspec/specs/analyst-agent-roster/`, or to `openspec/specs/analyst-skill-library/`.
