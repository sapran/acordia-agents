# ACORDIA Agents

Runnable [opencode](https://opencode.ai) agents and skills derived from the ACORDIA framework's operational role models.

## What this is

Markdown-only artifacts — agent files and skill files — that opencode loads from `~/.config/opencode/`. No code, no build. Each artifact traces back to a specific row or paragraph in a source competency map maintained separately (see [Source of truth](#source-of-truth)).

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
│   └── skills/                   # 39 opencode skills, one per grid row
│       ├── reasoning-under-uncertainty/SKILL.md
│       ├── identity-directory-trust/SKILL.md
│       └── ... (37 more)
└── install.sh                    # deploy to ~/.config/opencode/
```

## Install

```sh
./install.sh              # symlink agents + skills into ~/.config/opencode/
./install.sh --copy       # copy instead of symlink (frozen snapshot)
./install.sh --dry-run    # print what would happen, do nothing
./install.sh --pillar analysts  # explicit pillar select (default: all)
```

Uninstall:

```sh
./uninstall.sh            # remove links/copies this repo owns
```

Both scripts are idempotent — safe to re-run.

## Design constraints

- **opencode-native only.** Skill frontmatter uses opencode's `name` + `description` schema. No `chains_with`, `category`, `severity_boost`, `sha256`, or other vendor extensions.
- **Prompt-level composition.** opencode has no per-agent `skills:` field — each agent's prompt names the skill set it draws on.
- **Triggering-quality descriptions.** Skills fire by description match; each description states *when* the skill applies in one sharp sentence.
- **Read-only analysts.** All four agent files carry `edit: deny`. The three leg subagents additionally carry `task: deny` (leaf specialists — do not dispatch).

## Source of truth

The competency map that drives the analyst artifacts lives in the [CyberStrike](https://github.com/BerezhaSecurity/CyberStrike) repo at `docs/roles/operational-analyst.md`. The compile contract (grid row → skill, grid column → agent's named skill set) is specified in CyberStrike's OpenSpec under `openspec/specs/analyst-agent-roster/` and `openspec/specs/analyst-skill-library/`.

Editing the artifacts here without touching the map there is a source-of-truth drift bug. Regenerate from the map when the map changes.

## Verifying an install

```sh
opencode debug agent operational-analyst    # resolves permissions, mode, prompt
opencode debug skill reasoning-under-uncertainty
```

Expect `edit: deny` on all four analyst agents; `task: deny` on the three legs.
