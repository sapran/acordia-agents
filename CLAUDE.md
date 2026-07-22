# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Markdown-only distribution of [opencode](https://opencode.ai) agents and skills derived from the ACORDIA operational-role framework. **No application code, no build, no runtime, no tests.** Only frontmatter-carrying markdown files plus a shell installer that symlinks (or copies) them into `~/.config/opencode/`.

Only one pillar is currently wired: **`analysts/`** (the ACORDIA Analysis pillar) — one primary orchestrator (`operational-analyst`) plus three subagent legs (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) and a 39-skill library. Future pillars (Collection, Operations, Reflection, Direction, Independent action) may follow the same shape once compiled.

## Commands

Everything the repo does is deployment or spec-workflow. There is no lint, no test suite, no build.

```sh
./install.sh                         # symlink agents + skills into ~/.config/opencode/
./install.sh --copy                  # frozen snapshot instead of live symlinks
./install.sh --dry-run               # print actions, do nothing
./install.sh --pillar analysts       # restrict to a single pillar
./install.sh --target DIR            # override target root
./uninstall.sh                       # remove links/copies this repo owns

opencode debug agent operational-analyst          # verify resolved mode, permissions, prompt
opencode debug skill reasoning-under-uncertainty  # verify a skill loads

openspec validate --all --strict     # gate any change touching openspec/
```

Both `install.sh` and `uninstall.sh` are idempotent — safe to re-run.

## Source of truth — do not skip this

The load-bearing chain is:

```
docs/roles/operational-analyst.md   (competency grid + prose paragraphs)
        │
        │  compile contract
        ▼
openspec/specs/{competency-map-derivation, analyst-agent-roster, analyst-skill-library}
        │
        │  derives
        ▼
analysts/agents/*.md   +   analysts/skills/*/SKILL.md
```

**Editing artifacts under `analysts/` without touching the grid is a source-of-truth drift bug.** When the grid changes, regenerate from it; when an artifact needs to change, change the grid (or add a normative openspec requirement) first.

The bijection is normative: one skill row → one `SKILL.md`; each grid column (Core / T&N / Def / Fus) defines exactly one agent's prompt skill set; `●` = deep/defining, `○` = working/baseline, both place the skill in the agent's prompt. Italic section-header rows are **not** skills and produce no file. Two skills are explicitly cross-cutting and are not agents: `implant-payload-re` and `ot-embedded`. One skill (`credential-harvest-triage`) is procedural and does not correspond to a grid row — it declares its non-grid status in its own body.

## Format contracts

Follow opencode's frontmatter, not CyberStrike's superset. `docs/agents-skills-extension-workbook.md` §6 has the verified opencode conventions; the CyberStrike-specific sections above it are for context only.

### Agents (`analysts/agents/<name>.md`)

- Required frontmatter: `description` (dispatch signal — the leg's italic operating question, verbatim in meaning) and `mode` (`primary` for the orchestrator, `subagent` for the three legs).
- **Read-only posture is mandatory.** Every analyst carries `edit: deny` (in opencode `edit` governs edit/write/patch collectively; there is no separate `write` key, and a top-level `"*": deny` does *not* deny-default because per-tool built-ins override it — express read-only as `edit: deny`).
- **Legs additionally carry `task: deny`** — they are leaf specialists and never dispatch subagents.
- **The orchestrator's `task` block whitelists only the three legs** (`"*": deny` then `target-network-analyst`, `defender-detection-analyst`, `fusion-analyst` allowed). Never route to a general-purpose or explore agent from the primary.
- **Bash discipline is encoded in permissions:** `cat`/`head`/`tail`/`less`/`more`/`ls` → `deny`; `grep`/`egrep`/`rg`/`find`/`fd` → `ask`; `"*": allow` for genuine scripting (python, jq, custom tooling). Prefer opencode native `read`/`grep`/`glob`/`list` over shelling out.
- Body = agent prompt. It must name the skill set the agent draws on (opencode has **no per-agent `skills:` field**; composition is by prompt reference plus triggering-quality skill descriptions).
- Every prompt must carry a `## Credential harvest` H2 section describing that agent's role in the triage flow (added by change `2026-07-22-credential-harvest-capability`, PR #2). Adding/removing sections must not touch the `edit`/`bash`/`task` permission blocks.

### Skills (`analysts/skills/<slug>/SKILL.md`)

- Required frontmatter: `name` (kebab-case, `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars, **must equal the folder slug**, no prefix) and `description` (1–1024 chars, triggering-quality — a single sharp sentence stating **when** the skill applies, because opencode selects skills by description match).
- Optional: `metadata` only. Do **not** use CyberStrike-only fields (`category`, `cwe_ids`, `chains_with`, `severity_boost`), and do **not** include `sha256`/`signature` — a stale hash silently drops the skill as `tampered`.
- Seven credential-adjacent skills carry an additive `## Credential extraction` section: `disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`. Enrichment is additive — do not rewrite existing `Objective` / `When to use` / `Method` / `Signals / outputs` sections. Passive posture: analysis of already-collected material only, no active credential validation, no raw values in examples.

## OpenSpec workflow

Spec-driven changes are how this repo evolves. Config lives at `openspec/config.yaml`; active proposals in `openspec/changes/<slug>/`; archived changes in `openspec/changes/archive/<date>-<slug>/`; published specs in `openspec/specs/<capability>/spec.md`.

Slash commands (available under both `.claude/commands/opsx/` and `.opencode/commands/opsx/`):

- `/opsx:explore` — think through an idea before proposing.
- `/opsx:propose` — create a change with proposal / design / tasks / delta specs.
- `/opsx:apply` — implement tasks from a change.
- `/opsx:archive` — finalise a completed change and archive it.
- `/opsx:sync` — sync delta specs into main specs without archiving.

Preferred sequence for a feature/change/bugfix: **explore → propose → apply → archive → finalise & push branch → open PR to `main` → review → session-finalise**. Assume parallel agent work: apply changes in worktrees on branches.

Every normative claim in a spec must trace to either an artifact in this repo (agent file, skill file, install script) or a row/paragraph in `docs/roles/operational-analyst.md` / `docs/agents-skills-extension-workbook.md`. State the *actual* behaviour in specs even when it is a trap; capture the ideal in `design.md`.

## Extending the repo

Read `docs/agents-skills-extension-workbook.md` **before** authoring new pillars, new agents, or new skills — it is the frontmatter and permission contract, with the opencode-vs-CyberStrike differences that bite documented in §6. Key portable rules: plural `agents/` and `skills/` directory names under opencode config; kebab-case slugs with no prefix; the agent filename becomes the agent name; unknown skill fields are silently ignored; there is no agent→skill binding — skills fire by `description` and the agent prompt names its set.

## Guardrails baked into every analyst

- Read, model, judge — do not modify files or throw payloads. Execution belongs to the operators the analyst advises.
- The orchestrator delegates only to its three named legs; work that fits none of them stays in the orchestrator using native `read`/`grep`/`glob`/`list`.
- Skill and agent bodies never carry raw credential values — classifications, sources, and priorities only.
