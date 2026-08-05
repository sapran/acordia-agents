# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Markdown-only distribution of agents and skills derived from the ACORDIA operational-role framework. **No application code, no runtime, no tests.** Frontmatter-carrying markdown files, one Python generator, and a shell installer.

It reaches three harnesses two ways. omp and Claude Code install it as a **plugin**, from the marketplace catalogs at `.omp-plugin/marketplace.json` and `.claude-plugin/marketplace.json`; the plugin trees under `plugins/` are generated from the opencode sources by `tools/build-plugins.py` and committed, because a marketplace install clones the repository. opencode has no plugin system — its "plugins" are JS/TS hook modules that cannot ship markdown — so `install.sh` symlinks (or copies) the sources into `~/.config/opencode/`.

Two pillars are wired, shipped as two independently installable plugins: **`analysts/`** → `acordia-analysts` (the ACORDIA Analysis pillar) — one primary orchestrator (`operational-analyst`) plus three subagent legs (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) and a 43-skill library, read-only (`edit: deny`) — and **`operators/`** → `acordia-operators` (the ACORDIA Operations pillar) — one primary orchestrator (`operator`) plus four subagent specialists (`web-application`, `mobile-application`, `cloud-security`, `internal-network`) and a 30-skill library, write-capable (`edit: allow`), ported from the CyberStrike fork (`~/git/CyberStrike`, commit `359655518`). Future pillars (Collection, Reflection, Direction, Independent action) may follow the same shape once compiled.

## Commands

Everything the repo does is build, deployment, or spec-workflow. There is no lint and no test suite; the build is one deterministic generator and `--check` is its gate.

```sh
tools/build-plugins.py               # regenerate plugins/, .claude-plugin/, .omp-plugin/
tools/build-plugins.py --check       # diff the committed trees against the generator; exit 1 on drift

omp plugin marketplace add ./.       # omp install from this checkout — note `./.`, a bare `.` is rejected
omp plugin install acordia-analysts@acordia --scope user
claude plugin marketplace add ./     # Claude Code install from this checkout
claude plugin install acordia-analysts@acordia --scope local

./tools/migrate-omp.sh               # clear the retired ~/.omp/agent deployment that shadows the plugin
./tools/migrate-omp.sh --apply

./install.sh                         # opencode only: symlink agents + skills into ~/.config/opencode/
./install.sh --copy                  # frozen snapshot instead of live symlinks
./install.sh --dry-run               # print actions, do nothing
./install.sh --pillar analysts       # restrict to a single pillar
./install.sh --target DIR            # override target root
./install.sh --force                 # replace artifacts this repo does not own
./uninstall.sh                       # remove links/copies this repo owns

opencode debug agent operational-analyst          # verify resolved mode, permissions, prompt
opencode debug skill reasoning-under-uncertainty  # verify a skill loads

openspec validate --all --strict     # gate any change touching openspec/
shellcheck -x install.sh uninstall.sh tools/*.sh
```

Both `install.sh` and `uninstall.sh` are idempotent — safe to re-run. `tools/build-plugins.py` is deterministic: a second run leaves the tree byte-identical.

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

`operators/` does not have a counterpart chain. It has no competency grid to derive from — it is a provenance-tracked port from the CyberStrike fork. Its source of truth is `docs/roles/operator.md`, which records the CyberStrike-agent-to-operator-agent table and the skill-clone provenance instead of a grid; see the `### Agents (operators/agents/<name>.md)` format contract below.

## Format contracts

Follow opencode's frontmatter, not CyberStrike's superset. `docs/agents-skills-extension-workbook.md` §6 has the verified opencode conventions; the CyberStrike-specific sections above it are for context only.

### Agents (`analysts/agents/<name>.md`)

- Required frontmatter: `description` (dispatch signal — the leg's italic operating question, verbatim in meaning, preceded by the pillar provenance tag `ACORDIA Analysis — `) and `mode` (`primary` for the orchestrator, `subagent` for the three legs).
- **Read-only posture is the default.** Every analyst denies edit (in opencode `edit` governs edit/write/patch collectively; there is no separate `write` key, and a top-level `"*": deny` does *not* deny-default because per-tool built-ins override it — express read-only as `edit: deny`). **Scoped-write exception:** the two agents holding the "Briefing & written reporting" grid competency — `operational-analyst` (● Core) and `fusion-analyst` (○ Fus) — carry a path-scoped `edit` (`"*": deny` then `".acordia/reports/**": allow`, last-match-wins) so they can persist reports to `.acordia/reports/`; `target-network-analyst` and `defender-detection-analyst` keep the blanket `edit: deny` (added by change `analyst-report-write-scope`). `edit: deny` is a posture signal, not a hard sandbox — `bash: "*": allow` already permits scripted writes.
- **Legs additionally carry `task: deny`** — they are leaf specialists and never dispatch subagents.
- **The orchestrator's `task` block whitelists only the three legs** (`"*": deny` then `target-network-analyst`, `defender-detection-analyst`, `fusion-analyst` allowed). Never route to a general-purpose or explore agent from the primary.
- **Bash is fully allowed (`bash: allow`) on every analyst:** the read-only CLI tools used for file and data analysis (`cat`/`head`/`tail`/`less`/`more`/`ls`, `grep`/`egrep`/`rg`/`find`/`fd`) are ungated, as is scripting (python, jq, custom tooling). The read-only *posture* lives in `edit`/`task`, not `bash` (`bash: "*": allow` already permitted scripted writes). Preferring opencode-native `read`/`grep`/`glob` over shelling out is advisory guidance in the agent prompts, not a permission gate.
- Body = agent prompt. It must name the skill set the agent draws on (opencode has **no per-agent `skills:` field**; composition is by prompt reference plus triggering-quality skill descriptions).
- Every prompt must carry a `## Credential harvest` H2 section containing a one-line reference to `credential-harvest-triage` (added by change `2026-07-22-credential-harvest-capability`, PR #2; relaxed by `loosen-analyst-interagent`); the skill carries the full procedure — schema, bucket partition, routing — and a prompt must not restate it. A prompt may name its credential-adjacent skills and one domain-specific lens. Adding/removing sections must not touch the `edit`/`bash`/`task` permission blocks.
- The `## Exhaustive data processing`, `## What to return`, and `## Output discipline` sections are **advisory prose** — they state principles and defaults, not schemas or mandatory return formats. Each must exist and name its skill where one owns the method (`exhaustive-data-processing`); none prescribes a template the agent fills in.

### Skills (`analysts/skills/<slug>/SKILL.md`)

- Required frontmatter: `name` (kebab-case, `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars, **must equal the folder slug**, no prefix) and `description` (1–1024 chars, triggering-quality — a single sharp sentence stating **when** the skill applies, because opencode selects skills by description match).
- Optional: `metadata` only. Do **not** use CyberStrike-only fields (`category`, `cwe_ids`, `chains_with`, `severity_boost`), and do **not** include `sha256`/`signature` — a stale hash silently drops the skill as `tampered`.
- Seven credential-adjacent skills carry an additive `## Credential extraction` section: `disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`. Enrichment is additive — do not rewrite existing `Objective` / `When to use` / `Method` / `Signals / outputs` sections. Passive posture: analysis of already-collected material only, no active credential validation, no raw values in examples.

### Agents (`operators/agents/<name>.md`)

- Required frontmatter: `description` (opening with the pillar provenance tag `ACORDIA Operations — `, then the domain sentence), `mode` (`primary` for `operator`, `subagent` for `web-application`/`mobile-application`/`cloud-security`/`internal-network`).
- **Write-capable by default — the deliberate opposite of the analyst posture.** Every operator agent sets `edit: allow`, unscoped. There is no path-scoped write: omp cannot express a path scope for a tool, so a scoped rule would hold in opencode and silently evaporate in omp.
- `bash: allow` carries per-pattern `deny` rules for destructive/RCE primitives (SQL DDL, `INTO OUTFILE`/`DUMPFILE`, `xp_cmdshell` and siblings, `sqlmap --os-*`/`--file-write`/`--reg-*`), ported from CyberStrike's injection-tester ruleset (`injectionAgentPermission` in `agent.ts`). Under omp these per-command denies are **prompt-level only** — omp has no per-pattern `bash` enforcement the way opencode's `permission` map provides.
- **`operator`'s `task` block whitelists exactly its four specialists** (`"*": deny` then `web-application`, `mobile-application`, `cloud-security`, `internal-network` allowed). Each specialist carries `task: deny` as a leaf agent.
- Every prompt records state under `## Operation journal` — the `.acordia/ops/` files (`scope.md`, `intel.md`, `coverage.md`, `findings/<slug>.md`, `reports/<name>.md`), named in prose, never as a permission scope. The fixed substitution table this journal replaces is in `docs/agents-skills-extension-workbook.md` §8.
- Every prompt names its skill set under `## Your specialist depth (deep)`, whose heading line must be followed **immediately** — no blank line — by one `·`-separated line of skill names. `tools/build-plugins.py` parses exactly that line on every build and fails when it is empty or missing; breaking the shape breaks the build, not just the prose. A `## Working knowledge (draw on as needed)` section follows the same one-line shape for the broader skill set.
- **Source of truth is provenance, not a competency grid** — see `docs/roles/operator.md` and the note above.

### Skills (`operators/skills/<slug>/SKILL.md`)

- Required frontmatter: `name` (kebab-case, must equal the folder slug) and `description` (triggering-quality). Optional: `metadata` only — no other CyberStrike-only field, no `sha256`/`signature`/`signed_by`.
- Cloned skills record `metadata.cyberstrike.source` (`.cyberstrike/skill/<path>/SKILL.md`) and `metadata.cyberstrike.commit` (`359655518`), so a re-port against a newer CyberStrike checkout is a diff.
- Library membership is fixed at exactly 30 — 16 `attack-*`, 10 infrastructure, 4 WSTG bundles — listed in full in `docs/roles/operator.md`. Do not add a 31st skill without updating that provenance record.

### Commands (`commands/acordia/<stem>.md`)

- **Canonical wrapper per agent**, filename stem equal to the agent's — one handle guaranteed to exist, named for what it dispatches. Adding an agent means adding a canonical wrapper.
- **Short aliases are allowed beside it** (`fusion` → `fusion-analyst`), generated from the canonical wrapper so the brief cannot diverge, declaring their counterpart in a frontmatter comment. An alias name must not equal any agent stem. The drift guard is a check, not a prohibition: **every wrapper must name a live agent**, which covers canonical wrappers too.
- Body dispatches that agent with `$ARGUMENTS` as the brief, opening either "Dispatch the `<agent>` agent" or "Hand the work below to the `<agent>` agent" — `tools/build-plugins.py` reads that sentence to decide which plugin the wrapper belongs to, and fails on a wrapper it cannot resolve. `$ARGUMENTS` is the only placeholder every harness honours. A wrapper is an entry point — it never restates the prompt or redefines scope.
- **The namespace is the plugin name, not directory placement.** In omp and Claude Code the wrapper ships at `plugins/<harness>/<plugin>/commands/<stem>.md`, flat, and the harness prefixes it: `/acordia-analysts:<stem>`. Flat is mandatory — omp's plugin command provider scans `<plugin-root>/commands/*.md` non-recursively. The source tree keeps its `acordia/` directory purely as the opencode-facing layout, where `install.sh` deploys `<root>/commands/acordia-<stem>.md` → `/acordia-<stem>` because opencode command discovery is flat and carries no namespace.
- The opencode layout lives once in `tools/command-layout.sh`, sourced by both scripts, like `tools/ownership.sh`. `commands/` carries no `agents/` or `skills/`, so pillar auto-discovery already excludes it — and neither does `plugins/` at its top level.
- **Slugs stay bare.** The command namespace is the only prefixed surface: agent dispatch is flat exact-name and skills are picked by description match, so a slug prefix would isolate nothing while breaking the grid bijection and the generator's `(deep)` skill lines.

### Generated plugin trees (`plugins/**`, `.claude-plugin/`, `.omp-plugin/`)

- **Generated build output, committed.** `tools/build-plugins.py` produces every file under those three paths from `analysts/`, `operators/`, and `commands/acordia/`. They are committed because a marketplace install clones the repository, and a plain build deletes them wholesale before regenerating so a renamed artifact cannot leave an orphan.
- **`tools/build-plugins.py --check` is the gate, and CI runs it.** `.github/workflows/check.yml` runs it plus `openspec validate --all --strict` and `shellcheck -x` on every PR and push, and **fails** rather than auto-committing a rebuild. It builds to a tempdir and diffs, naming every missing, extra, and differing path. **Editing a file under `plugins/` is a drift bug of the same class as editing `analysts/` without touching the competency grid** — the next build reverts it silently.
- **The version is content-derived and not semver.** `1.0-<hash>`: `VERSION_EPOCH` by hand (bump on a roster or pillar change), plus 7 hex of sha256 over `VERSION_INPUTS` — the two pillars, `commands/acordia/`, and the generator itself. Never a git revision: the version lands in six committed files, so a git SHA would make the rebuild commit invalidate its own embedded SHA and `--check` would fail on every push forever. Non-semver is load-bearing — verified on omp 17.1.8, bare `omp plugin upgrade` reinstalls on unequal non-semver in either direction, while `1.0.0+aaa` → `1.0.0+bbb` compares equal and never upgrades. Claude Code accepts the string; its upgrade behaviour for one is unverified.
- **Agent-name resolution differs by harness.** Claude Code namespaces plugin agents, so its Task tool needs `acordia-analysts:<agent>` and the bare name fails; omp and opencode are flat. Wrappers absorb the difference by naming the agent in prose.
- **Two trees, because one `agents/*.md` cannot serve both harnesses.** Both read `tools` from the fixed `<plugin-root>/agents/` path, but Claude Code expects capitalised Claude tool names and omp expects lowercase omp names plus `spawns`; Claude Code's `agents` path override supplements rather than replaces `./agents`, so the two cannot be pointed elsewhere. Skills and commands are byte-identical across the trees; only `agents/` differs.
- **Two catalogs, for the same reason.** omp reads `.omp-plugin/marketplace.json` in preference to `.claude-plugin/marketplace.json` and only falls back when the former is absent, so shipping both hands each harness its own tree from one checkout. They differ in exactly the two `source` paths.
- **Claude posture is a denylist.** Plugin agents get `disallowedTools`, never `tools`: an allowlist would enumerate Claude's whole vocabulary and silently strip tools this repo never audited. `edit: deny` → `Edit, Write, NotebookEdit`; a path-scoped `edit` → `Edit, NotebookEdit` (keeps `Write`, because the two reporting analysts must still produce reports and Claude Code cannot express the path scope); `edit: allow` → nothing; `task: deny` → `Task`. Plugin agents silently ignore `metadata`, so provenance and the three unexpressible-posture notes (no spawn allowlist, no path scope, no per-command bash rules) are emitted as YAML comments above the keys.

## OpenSpec workflow

Spec-driven changes are how this repo evolves. Config lives at `openspec/config.yaml`; active proposals in `openspec/changes/<slug>/`; archived changes in `openspec/changes/archive/<date>-<slug>/`; published specs in `openspec/specs/<capability>/spec.md`.

Slash commands (`.claude/commands/opsx/*.md` → `/opsx:*`; the opencode copies are flat `.opencode/commands/opsx-*.md`, because opencode does not namespace commands by directory):

- `/opsx:explore` — think through an idea before proposing.
- `/opsx:propose` — create a change with proposal / design / tasks / delta specs.
- `/opsx:apply` — implement tasks from a change.
- `/opsx:archive` — finalise a completed change and archive it.
- `/opsx:sync` — sync delta specs into main specs without archiving.

Preferred sequence for a feature/change/bugfix: **explore → propose → apply → archive → finalise & push branch → open PR to `develop` → review → session-finalise**. Assume parallel agent work: apply changes in worktrees on branches.

Every normative claim in a spec must trace to either an artifact in this repo (agent file, skill file, install script) or a row/paragraph in `docs/roles/operational-analyst.md` / `docs/agents-skills-extension-workbook.md`. State the *actual* behaviour in specs even when it is a trap; capture the ideal in `design.md`.

## Extending the repo

Read `docs/agents-skills-extension-workbook.md` **before** authoring new pillars, new agents, or new skills — it is the frontmatter and permission contract, with the opencode-vs-CyberStrike differences that bite documented in §6. Key portable rules: plural `agents/` and `skills/` directory names under opencode config; kebab-case slugs with no prefix; the agent filename becomes the agent name; unknown skill fields are silently ignored; there is no agent→skill binding — skills fire by `description` and the agent prompt names its set.

Names stay unprefixed on purpose. Provenance is carried by the agent `description` (the `ACORDIA <pillar> — ` tag above), the generated `color`, and the plugin-name command namespace — never by the agent name or the skill slug: the name is the dispatch handle wired into the orchestrators' `task` whitelists, and the slug is bound to the folder by the skill-library bijection and to the `·`-separated `(deep)` lines `tools/build-plugins.py` parses. Skills are selected by `description` match, so a slug prefix would isolate nothing anyway. The collision risk a prefix would have addressed is handled per harness: the plugin harnesses namespace commands themselves and keep each plugin's artifacts attributable, and for opencode `install.sh` refuses to overwrite an artifact this repository did not deploy (ownership evidence lives in `tools/ownership.sh`, shared with `uninstall.sh`), with `--force` as the explicit override.

## Guardrails baked into every analyst

- Read, model, judge — do not modify files or throw payloads. Execution belongs to the operators the analyst advises.
- The orchestrator delegates only to its three named legs; work that fits none of them stays in the orchestrator using native `read`/`grep`/`glob`.
- Skill and agent bodies never carry raw credential values — classifications, sources, and priorities only.
