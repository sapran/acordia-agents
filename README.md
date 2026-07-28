# ACORDIA Agents

Runnable [opencode](https://opencode.ai) agents and skills derived from the ACORDIA framework's operational role models, deployable to opencode or to the [omp](https://github.com/can1357/oh-my-pi) harness.

## What this is

Markdown-only artifacts — agent files and skill files — authored to opencode's schema. No application code. Each artifact traces back to a specific row or paragraph in a source competency map maintained separately (see [Source of truth](#source-of-truth)).

Two harnesses can load them. opencode reads them as they are. omp reads the skills as they are but needs the agent frontmatter translated, which `install.sh` does for you.

## Scope

Currently one pillar wired up:

- **`analysts/`** — the ACORDIA Analysis pillar, realised as four decision-support agents plus their skill library. Read-only by design (`edit: deny`); no target interaction, no active testing.

Future pillars (Collection, Operations, Reflection, Direction, Independent action) may follow the same shape as they get compiled.

## Layout

```
acordia-agents/
├── analysts/
│   ├── agents/                   # 4 opencode agent files
│   │   ├── operational-analyst.md            (mode: primary)
│   │   ├── target-network-analyst.md         (mode: subagent)
│   │   ├── defender-detection-analyst.md     (mode: subagent)
│   │   └── fusion-analyst.md                 (mode: subagent)
│   └── skills/                   # 42 opencode skills
│       ├── reasoning-under-uncertainty/SKILL.md
│       ├── identity-directory-trust/SKILL.md
│       └── ... (40 more)
├── tools/
│   └── translate-omp.py          # opencode agent frontmatter → omp task agent
└── install.sh                    # deploy to opencode and/or omp
```

## Install

```sh
./install.sh                    # symlink into ~/.config/opencode/ (default)
./install.sh --harness omp      # translate + deploy into ~/.omp/agent/
./install.sh --harness both     # both harnesses in one run
./install.sh --copy             # copy instead of symlink (frozen snapshot)
./install.sh --dry-run          # print what would happen, do nothing
./install.sh --pillar analysts  # explicit pillar select (default: all)
```

Uninstall takes the same `--harness` selector:

```sh
./uninstall.sh                  # remove what this repo owns from opencode
./uninstall.sh --harness both   # …from both harnesses
```

Both scripts are idempotent — safe to re-run.

### The omp harness

Skills need no translation: omp ships an `opencode` skill provider, so an opencode install already makes the library visible to omp. `--harness omp` additionally places the skills under `~/.omp/agent/skills/` so omp works without an opencode config at all.

Agents do need translation. omp discovers task agents only from `.omp/agents` and `~/.omp/agent/agents`, and its frontmatter contract differs: a required `name`, a `tools` allowlist in place of the `permission` map, no `mode`, and `spawns` for delegation. `tools/translate-omp.py` performs the mapping; the full table is in the [extension workbook](docs/agents-skills-extension-workbook.md#7-omp-oh-my-pi--the-second-harness).

Translated agents are **build output**, generated into the gitignored `.build/omp/` and copied (never symlinked) into place. Editing a file under `~/.omp/agent/agents/` is a drift bug — edit `analysts/agents/` and reinstall.

One optional flag changes the omp posture:

```sh
./install.sh --harness omp --autoload deep  # preload each agent's deep skills
```

### Harness parity gaps

The read-only posture is **weaker in omp than in opencode**, in two ways. Both were verified empirically against omp 17.1.8, not assumed:

- **`write` cannot be denied.** The translated allowlist omits `write`, and omp exposes it anyway: `read` and `write` are omp's `XDEV_TRANSPORT_TOOLS`, the channel every `xd://` device is driven through, so they are present whenever the `tools.xdev` setting is on — which is the default. A leg agent was asked to create a scratch file with `write`; it succeeded. `edit` and `task` *are* removed by omission, so the allowlist is not merely advisory — `write` is the one hole. The generated frontmatter records this in `metadata.generated.write_access` rather than implying a guarantee it cannot keep. Consequently opencode's scoped `.acordia/reports/**` sink has no omp counterpart: in omp those agents can write anywhere.
- **`bash` is still a write channel.** Both harnesses grant `bash`, so "read-only" means "has no file-editing tool", not "cannot write". Unchanged from the opencode install; `bash` stays because the analytic-tooling and exhaustive-data-processing skills depend on it.

In omp, treat the read-only posture as prompt-level for writes and enforced only for `edit` and dispatch. If you need it enforced, disable `tools.xdev` in omp's settings — then the allowlist bites and `write` disappears.

## Design constraints

- **opencode-native only.** Skill frontmatter uses opencode's `name` + `description` schema. No `chains_with`, `category`, `severity_boost`, `sha256`, or other vendor extensions.
- **Prompt-level composition.** opencode has no per-agent `skills:` field — each agent's prompt names the skill set it draws on.
- **Triggering-quality descriptions.** Skills fire by description match; each description states *when* the skill applies in one sharp sentence.
- **Read-only analysts.** All four agent files carry `edit: deny`. The three leg subagents additionally carry `task: deny` (leaf specialists — do not dispatch).

## Source of truth

The competency map that drives the analyst artifacts lives at [`docs/roles/operational-analyst.md`](docs/roles/operational-analyst.md). The compile contract that binds the map to the artifacts (grid row → skill, grid column → agent's named skill set, ●/○ → deep/working membership) is specified in [`openspec/specs/competency-map-derivation/`](openspec/specs/competency-map-derivation/spec.md), with the roster and library shape in [`openspec/specs/analyst-agent-roster/`](openspec/specs/analyst-agent-roster/spec.md) and [`openspec/specs/analyst-skill-library/`](openspec/specs/analyst-skill-library/spec.md).

The exploratory history that produced the current shape is preserved under [`openspec/changes/archive/`](openspec/changes/archive/) — the original `derive-analyst-agents-skills` change and the follow-on `credential-harvest-capability` proposal.

Editing the artifacts under `analysts/` without touching the map is a source-of-truth drift bug. When the map changes, regenerate from it.

## How to extend

The mechanism for adding new agents or skills — frontmatter contracts, permission model, prompt-level composition — is documented in [`docs/agents-skills-extension-workbook.md`](docs/agents-skills-extension-workbook.md). Read it before authoring new pillars or new skills.

## Verifying an install

```sh
opencode debug agent operational-analyst    # resolves permissions, mode, prompt
opencode debug skill reasoning-under-uncertainty
```

Expect `edit: deny` on all four analyst agents; `task: deny` on the three legs.
