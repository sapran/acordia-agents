# ACORDIA Agents

Runnable [opencode](https://opencode.ai) agents and skills derived from the ACORDIA framework's operational role models, distributed as a plugin marketplace for [omp](https://github.com/can1357/oh-my-pi) and Claude Code, and as a filesystem install for opencode.

## What this is

Markdown-only artifacts — agent files and skill files — authored to opencode's schema. No application code. Each artifact traces back to a specific row or paragraph in a source competency map maintained separately (see [Source of truth](#source-of-truth)).

Three harnesses can load them. omp and Claude Code install them as **plugins**, from the marketplace catalogs this repository ships at its root; the plugin trees under `plugins/` are generated from the opencode sources by `tools/build-plugins.py` and committed, because a marketplace install clones the repository. opencode has no plugin system of any kind — its "plugins" are JS/TS hook modules that cannot ship markdown — so it keeps `install.sh`, which symlinks the sources into `~/.config/opencode/`.

## Scope

Two pillars wired up, shipped as two independently installable plugins so the read-only pillar can be taken without the write-capable one:

- **`analysts/`** → plugin `acordia-analysts`. The ACORDIA Analysis pillar, realised as four decision-support agents plus their skill library. Read-only by design (`edit: deny`); no target interaction, no active testing.
- **`operators/`** → plugin `acordia-operators`. The ACORDIA Operations pillar, ported from the CyberStrike fork (`~/git/CyberStrike`, commit `359655518`): five offensive agents (one primary orchestrator plus four domain specialists) and a 30-skill technique library. **Not read-only** — `edit: allow`, unscoped, because an operator writes scripts, evidence, and its own operation journal. Provenance and what was deliberately left out of the port are recorded in [`docs/roles/operator.md`](docs/roles/operator.md).

Future pillars (Collection, Reflection, Direction, Independent action) may follow the same shape as they get compiled.

```
acordia-agents/
├── analysts/                     # SOURCE — opencode-native, the only editable form
│   ├── agents/                   # 4 opencode agent files
│   │   ├── operational-analyst.md            (mode: primary)
│   │   ├── target-network-analyst.md         (mode: subagent)
│   │   ├── defender-detection-analyst.md     (mode: subagent)
│   │   └── fusion-analyst.md                 (mode: subagent)
│   └── skills/                   # 43 opencode skills
│       ├── reasoning-under-uncertainty/SKILL.md
│       ├── identity-directory-trust/SKILL.md
│       └── ... (41 more)
├── operators/                    # SOURCE
│   ├── agents/                   # 5 opencode agent files, write-capable
│   │   ├── operator.md                        (mode: primary)
│   │   ├── web-application.md                 (mode: subagent)
│   │   ├── mobile-application.md              (mode: subagent)
│   │   ├── cloud-security.md                  (mode: subagent)
│   │   └── internal-network.md                (mode: subagent)
│   └── skills/                   # 30 opencode skills
│       ├── attack-jwt/SKILL.md
│       ├── ad-security/SKILL.md
│       ├── wstg-injection/SKILL.md
│       └── ... (27 more)
├── commands/acordia/             # SOURCE — 17 slash-command wrappers
├── plugins/                      # GENERATED — committed build output, never edited
│   ├── claude/{acordia-analysts,acordia-operators}/
│   └── omp/{acordia-analysts,acordia-operators}/
├── .claude-plugin/marketplace.json   # GENERATED — Claude Code reads this catalog
├── .omp-plugin/marketplace.json      # GENERATED — omp prefers this one
├── tools/
│   └── build-plugins.py          # opencode sources → both plugin trees + catalogs
└── install.sh                    # opencode only
```

## Install

Three paths, one per harness.

```sh
# omp
omp plugin marketplace add sapran/acordia-agents
omp plugin install acordia-analysts@acordia      # add acordia-operators@acordia to opt into the offensive pillar

# Claude Code
/plugin marketplace add sapran/acordia-agents
/plugin install acordia-analysts@acordia

# opencode — it has no plugin system
./install.sh
```

In omp, `/reload-plugins` refreshes skills and commands after an install; new tools or hooks would need a restart. **omp only surfaces marketplace plugins while the `claude-plugins` capability provider is enabled** — if `claude-plugins` appears in `disabledProviders` in `~/.omp/agent/config.yml`, the plugin installs cleanly and contributes nothing. Remove that line.

#### Upgrading from the old omp install

Before this became a marketplace, `./install.sh --harness omp` copied translated agents into `~/.omp/agent/agents/`. Those files are not merely stale — omp resolves `~/.omp/agent/agents` **before** plugin roots and dedups first-wins, so an old copy **silently shadows the plugin's agent of the same name** and you run last month's prompts with no indication. Remove the old deployment, then install the plugin: `rm -rf ~/.omp/agent/agents ~/.omp/agent/skills` if those directories hold nothing but this repository's artifacts.

The opencode installer keeps its own flags:

```sh
./install.sh --copy             # copy instead of symlink (frozen snapshot)
./install.sh --dry-run          # print what would happen, do nothing
./install.sh --pillar analysts  # explicit pillar select (default: all)
./install.sh --pillar operators # operators only (write-capable — read the posture above first)
./install.sh --no-commands      # skip the /acordia- command wrappers
./uninstall.sh                  # remove what this repo owns from opencode
```

Both scripts are idempotent — safe to re-run.

### Invoking them: the plugin namespace

Agents are dispatched by name, in a picker shared with the harness's own. So the distribution also carries one slash-command wrapper per agent, giving a namespaced entry point. **The namespace is the plugin name**, applied by the harness itself:

```
/acordia-analysts:fusion       what all of it together means, and how good the take is
/acordia-operators:webapp      OWASP WSTG testing of a web target
/acordia-operators:operator    hand an authorized engagement to the orchestrator
```

Both omp and Claude Code prefix a plugin's commands with the plugin name, so the two harnesses agree without any per-harness placement rule. opencode namespaces nothing — its command discovery is flat — so there the same wrappers deploy as `/acordia-fusion`, with the prefix in the filename. That is the split this repository already uses for its own `/opsx:*` commands.

Short handles — `analyst`, `target`, `defender`, `fusion`, `webapp`, `mobile`, `cloud`, `internal` — sit beside a canonical wrapper named for each agent (`/acordia-analysts:fusion-analyst`), so both spellings work. The canonical set is the source of truth; the aliases are generated from it, and a check asserts every wrapper names an agent that actually exists.

**Agent names and skill slugs stay unprefixed on purpose.** Agent dispatch is an exact-name lookup and skills are selected by description match, so a slug prefix would isolate nothing — while breaking the grid bijection and every `skill://` reference. Provenance rides on the `ACORDIA <pillar> — ` description tag, the generated `color`, and this command namespace instead.

**How the agent name itself resolves differs by harness.** Verified against Claude Code 2.1.220: plugin agents are namespaced there too, so the Task tool takes `acordia-analysts:target-network-analyst` and the **bare name fails** with "agent type is not available". omp registers plugin agents flat, by bare name — `fusion-analyst` dispatches. opencode reads the source files directly, also flat. The command wrappers paper over the difference: a wrapper names the agent in prose and the harness resolves it in its own idiom.

### Generated plugin trees

Everything under `plugins/`, `.claude-plugin/`, and `.omp-plugin/` is build output produced by `tools/build-plugins.py` from the sources under `analysts/`, `operators/`, and `commands/acordia/`. It is committed because a marketplace install clones the repository, and it is regenerated wholesale on every build so a renamed skill cannot leave an orphan behind.

```sh
tools/build-plugins.py            # regenerate the trees in place
tools/build-plugins.py --check    # build to a tempdir, diff, exit 1 on drift
```

`--check` is the gate. **Editing a file under `plugins/` is a drift bug** of the same class as editing `analysts/` without touching the competency grid — the next build silently reverts it.

#### Bump `VERSION` on every change

`VERSION` in `tools/build-plugins.py` is the **only** update signal either plugin harness has. omp compares it against the installed version and skips when they match, so an unbumped version means your edit never reaches anyone who already installed the plugin — silently, with no error and no warning.

- **MINOR** — any change that reaches a user: an agent prompt, a skill body, a command wrapper, the generator's output.
- **MAJOR** — a serious change: the roster (an agent or pillar added or removed), or the shape of the distribution.

Bump it, then rebuild, so the new version lands in the six generated files that carry it.

Real semver, and monotonic on purpose. Verified against omp 17.1.8: bare `omp plugin upgrade` is the path that compares versions, a newer semver upgrades, and an older one is skipped. Two things to avoid — never hang a hash or build metadata off it, because `1.0.0+aaa` and `1.0.0+bbb` compare **equal** and would never upgrade; and note that `omp plugin upgrade <name>@<marketplace>` with an explicit target reinstalls unconditionally and compares nothing, so it is useless for testing this.

**Claude Code has no working upgrade path for marketplace plugins** (verified, 2.1.220): `claude plugin update` fails with "Plugin not found" from either a directory or a GitHub source, and re-running `install` reports "already installed" without refreshing. Only uninstall-then-reinstall picks up a new version, so the version string is informational there. Bump it anyway — omp is the harness that acts on it.

Two trees exist because one `agents/*.md` cannot serve both harnesses: they read `tools` from the same fixed `<plugin-root>/agents/` path, but Claude Code expects capitalised Claude tool names while omp expects lowercase omp names and additionally needs `spawns`. Skills and commands are byte-identical across the trees; only `agents/` differs. Two catalogs exist for the same reason: omp reads `.omp-plugin/marketplace.json` in preference to `.claude-plugin/marketplace.json`, so shipping both hands each harness its own tree from one checkout.

### Namespace safety

The opencode config directory is a flat namespace shared with opencode's own built-ins and with whatever you keep yourself. So `install.sh` refuses to overwrite anything this repository did not deploy: it checks every destination before writing a single file, and aborts naming the conflict, leaving the harness untouched. `--force` replaces the foreign artifact deliberately:

```sh
./install.sh --force            # replace artifacts this repo does not own
```

Ownership is evidence-based, not name-based — a symlink resolving into this checkout, or a byte-identical copy — and the same rule governs `uninstall.sh`, which leaves name-matching strangers in place. It is defined once in [`tools/ownership.sh`](tools/ownership.sh). Note that ownership is per checkout: installing from a second clone or worktree over an existing deployment counts as foreign and needs `--force`. The plugin harnesses have their own install machinery and need none of this.

### Harness parity gaps

The read-only analyst posture is enforced to a different depth in each harness. All three were checked against the harness's actual permission model, not assumed:

| harness | mechanism | strength |
| --- | --- | --- |
| Claude Code | `disallowedTools: Edit, Write, NotebookEdit, Task` on the plugin agent | **enforced** — the tools are subtracted from the inherited set |
| omp | `tools` allowlist omitting `edit` and `task` | **partial** — `edit` and `task` really are removed; `write` survives |
| opencode | `permission.edit: deny`, `permission.task: deny` | **enforced, with a path scope** |

- **omp cannot deny `write`.** The translated allowlist omits it and omp exposes it anyway: `read` and `write` are omp's `XDEV_TRANSPORT_TOOLS`, the channel every `xd://` device is driven through, so they are present whenever the `tools.xdev` setting is on — which is the default. Verified empirically against omp 17.1.8: a leg agent asked to create a scratch file with `write` succeeded. The generated frontmatter records this in `metadata.generated.write_access` rather than implying a guarantee it cannot keep. Disable `tools.xdev` in omp's settings and the allowlist bites.
- **Neither plugin harness can express a path scope.** opencode confines `operational-analyst` and `fusion-analyst` writes to `.acordia/reports/**`. Claude Code has no path-scoped plugin-agent permission, so those two keep `Write` (denying it outright would leave them unable to produce the reports their prompts require) and the confinement is prompt-level; omp cannot scope the tool either. Both generated files say so, in a comment and in `metadata.generated` respectively.
- **`bash` is still a write channel.** All three harnesses grant `bash`, so "read-only" means "has no file-editing tool", not "cannot write". `bash` stays because the analytic-tooling and exhaustive-data-processing skills depend on it.
- **Neither plugin harness enforces per-command bash denies.** The operators' destructive-primitive denylist (SQL DDL, `INTO OUTFILE`, `xp_cmdshell`, `sqlmap --os-*`) is an opencode `permission.bash` map. Under omp and Claude Code it is prompt-level guidance, and each generated agent records that.

## Design constraints

- **opencode-native only.** Skill frontmatter uses opencode's `name` + `description` schema. No `chains_with`, `category`, `severity_boost`, `sha256`, or other vendor extensions. It is valid unchanged in all three harnesses, which is why skills are copied into the plugin trees verbatim.
- **Prompt-level composition.** opencode has no per-agent `skills:` field — each agent's prompt names the skill set it draws on.
- **Triggering-quality descriptions.** Skills fire by description match; each description states *when* the skill applies in one sharp sentence.
- **Read-only analysts.** All four agent files carry `edit: deny`. The three leg subagents additionally carry `task: deny` (leaf specialists — do not dispatch).
- **Write-capable operators.** `operators/` inverts this: every agent carries `edit: allow`, unscoped, because an operator writes scripts, evidence, and its own `.acordia/ops/` journal. Operators are **not read-only** — the harness parity gaps above apply only to the read-only analyst posture and have no bearing on operators, who are already granted write access in every harness.

## Source of truth

The competency map that drives the analyst artifacts lives at [`docs/roles/operational-analyst.md`](docs/roles/operational-analyst.md). The compile contract that binds the map to the artifacts (grid row → skill, grid column → agent's named skill set, ●/○ → deep/working membership) is specified in [`openspec/specs/competency-map-derivation/`](openspec/specs/competency-map-derivation/spec.md), with the roster and library shape in [`openspec/specs/analyst-agent-roster/`](openspec/specs/analyst-agent-roster/spec.md) and [`openspec/specs/analyst-skill-library/`](openspec/specs/analyst-skill-library/spec.md).

The exploratory history that produced the current shape is preserved under [`openspec/changes/archive/`](openspec/changes/archive/) — the original `derive-analyst-agents-skills` change and the follow-on `credential-harvest-capability` proposal.

Editing the artifacts under `analysts/` without touching the map is a source-of-truth drift bug. When the map changes, regenerate from it.

The operator pillar has no competency map and derives nothing from one — it is a provenance-tracked port of an existing offensive agent/skill roster. Its source of truth is [`docs/roles/operator.md`](docs/roles/operator.md): the CyberStrike-agent-to-operator-agent table, the skill-clone provenance, and what was deliberately left out of the port. Editing `operators/` without checking that provenance record is the same class of drift bug as editing `analysts/` without checking the competency map.

## How to extend

The mechanism for adding new agents or skills — frontmatter contracts, permission model, prompt-level composition — is documented in [`docs/agents-skills-extension-workbook.md`](docs/agents-skills-extension-workbook.md). Read it before authoring new pillars or new skills.

## Verifying an install

```sh
tools/build-plugins.py --check              # the plugin trees match their sources

opencode debug agent operational-analyst    # resolves permissions, mode, prompt
```

Expect `edit: deny` on all four analyst agents (with the `.acordia/reports/**` exception on `operational-analyst` and `fusion-analyst`); `task: deny` on the three legs. In omp and Claude Code, confirm the plugin's commands appear as `/acordia-analysts:*`. Agents resolve by bare name in omp, and as `acordia-analysts:<agent>` in Claude Code.
