# ACORDIA Agents

Runnable agents and skills derived from the ACORDIA framework's operational role models, distributed as a plugin marketplace for [omp](https://github.com/can1357/oh-my-pi) and Claude Code.

## What this is

Markdown-only artifacts — agent files, skill files, and command wrappers. No application code, no runtime, and since 3.0.0 no build step: the pillar is one authored tree that both harnesses read as it stands in the checkout, and a marketplace install clones this repository and points at that tree directly.

One tree serves both because both accept the same agent file: omp's `parseAgentFields()` requires `name`, `description` and a body and treats `tools` as optional, and Claude Code requires the same three keys. Every artifact traces to a source — each skill to a row of the competency map, each doctrinal claim to an entry in the literature register.

## Scope

One pillar, one installable plugin:

- **`acordia-analysts/`** — the Analysis pillar: one orchestrator and four specialist legs, and the 45-skill library realising their shared analytic spine. Decision support and target understanding; no target interaction, no active testing.

The roster is derived one-for-one from the five columns of the competency map:

- **`cyber-analyst`** — the lead. Holds the operating picture, correlates across sources, and runs the end-neutral loop that decides what is worth doing next.
- **`mission-analyst`** — the target as an organisation: what it is for, what it depends on, crown jewels and mission threads, and its procedures, redundancy and reporting culture.
- **`terrain-analyst`** — the technical terrain: networks, protocols and routing, identity and directory, cloud control planes, web and application stacks, host internals, attack surface, and operational technology where the target demands it.
- **`overwatch-analyst`** — the defender: detection capability, evasion reasoning, own-footprint, and live overwatch of whether the operation is seen.
- **`collection-analyst`** — the take: what the collected material is actually worth, working bulk material at volume, and the data-integration and correlation tooling that makes it usable.

**The product goes to a person.** Nothing here executes: an analysis is handed to a human operator who then acts, so a recommended course of action is a hand-off rather than a dispatch, and the loop judges the outcome from evidence that operator reports back. A finished product belongs in `.acordia/reports/`, by convention.

Research is the ACORDIA-aligned pillar to compile next if one follows — it composes with Analysis and makes no target contact.

```text
acordia-agents/
├── acordia-analysts/                 # plugin root — installed as-is
│   ├── .claude-plugin/plugin.json
│   ├── agents/     cyber-analyst · mission-analyst · terrain-analyst
│   │               overwatch-analyst · collection-analyst
│   ├── commands/   10 command wrappers
│   └── skills/     45 skills, one SKILL.md each
├── .claude-plugin/marketplace.json   # Claude Code reads this catalog
├── .omp-plugin/marketplace.json      # omp prefers this one; byte-identical
├── docs/roles/                       # the competency map and the source register
└── openspec/                         # capability specs and change history
```

## Install

```sh
# omp
omp plugin marketplace add sapran/acordia-agents
omp plugin install acordia-analysts@acordia

# Claude Code
claude plugin marketplace add sapran/acordia-agents
claude plugin install acordia-analysts@acordia
```

`acordia` is the marketplace name, from the `name` field of both catalogs. omp resolves `.omp-plugin/marketplace.json` in preference and Claude Code reads `.claude-plugin/marketplace.json`; the two are byte-identical.

In omp, marketplace content is delivered by the `claude-plugins` capability provider, which reads Claude Code's plugin registry alongside omp's own — so one Claude Code install can be inherited rather than registered twice, and so disabling that provider leaves the plugin installed and contributing nothing. `/reload-plugins` refreshes skills and commands after an install; new tools or hooks need a restart.

**opencode was dropped in 3.0.0**, with the shell installer that was its only route in and the generator that existed to express its permission maps; opencode users have no upgrade path and must switch harness.

### Installing without the marketplace

The route above works on a stock omp config, where `claude-plugins` is enabled; use it unless that provider is off. When it is off, the install is inert and every stored signal still reports health: `omp plugin list` shows the plugin, `~/.omp/plugins/installed_plugins.json` records it, `~/.omp/plugins/omp-plugins.lock.json` says `"enabled": true`, and `~/.omp/plugins/node_modules/acordia-analysts` symlinks into the plugin cache — with no error and no warning anywhere. One command names the cause, because it reports the merged effective value rather than what any single config file holds:

```sh
omp config get disabledProviders    # `claude-plugins` in the list means no marketplace plugin loads
```

Disabling it is a mechanical choice rather than a mistake. The provider is the reader for marketplace plugins, and it reads both `~/.omp/plugins/installed_plugins.json` and `~/.claude/plugins/installed_plugins.json`, so enabling it also surfaces every plugin registered in Claude Code's registry, not only omp's. `claude-plugins` and `claude` are distinct ids in one shared `disabledProviders` namespace: disabling `claude` — Claude Code's context files, commands, skills and MCP — does not disable marketplace plugins, and disabling `claude-plugins` does not disable the rest.

For that case the checkout installs itself into omp's native agent and skill roots, which are gated by no discovery provider at all:

```sh
tools/install-omp.sh                       # ~/.omp/agent, or $PI_CODING_AGENT_DIR when set
tools/install-omp.sh --profile gdx         # ~/.omp/profiles/gdx/agent
tools/install-omp.sh --agent-dir <path>    # an explicit agent directory
tools/install-omp.sh --dry-run             # print what would be linked, change nothing
tools/uninstall-omp.sh                     # same three flags; removes only our own links
```

Target-directory precedence is `--agent-dir`, then `--profile` (resolving to `~/.omp/profiles/<name>/agent`), then `$PI_CODING_AGENT_DIR`, then `~/.omp/agent`; the first two are mutually exclusive. The five agent files and 45 skill directories are linked as **symlinks rather than copies**, so a `git pull` changes what omp serves, and no configuration file is edited. Anything already in either root that is not one of our own symlinks aborts the run with every colliding path printed and nothing created at all, so the installer can never take over a dispatch handle you own; re-running it is idempotent. The uninstaller matches each link on its recorded target, so a real file or a symlink pointing elsewhere is left alone, and a link whose checkout has since been deleted, renamed or moved is still cleaned up.

**The command wrappers are not installed by this route.** A wrapper takes its namespace from the plugin name, applied by the harness, so `/acordia-analysts:terrain` exists only through a plugin root. Agents dispatch by bare name either way, so the roster is fully reachable without them.

**A native install silently shadows a marketplace one.** Native roots resolve before plugin roots and dedup first-wins by exact agent name, so with both routes active you are running your checkout while believing you run the published version, and nothing says so. Run `tools/uninstall-omp.sh` before returning to the marketplace route.

No packaging change would remove the need for these scripts. With `claude-plugins` disabled, a user `extensions:` entry and a properly registered `omp plugin link` package both load the skills and serve none of the agents; only the CLI flag `omp -e <absolute path>` serves agents from such a root, which contradicts omp's own discovery documentation and is an omp bug rather than a packaging error. Adding a `package.json` to the pillar buys nothing, so it ships none.

### Upgrading to 6.0.0

**6.0.0 withdraws nothing.** The roster, the skill library and the marketplace route are unchanged; what is new is the second install route above, for users whose `claude-plugins` provider is off. An existing marketplace install upgrades in place as usual, and a user who never disabled that provider has nothing to do differently.

If you adopt the script route, adopt only one: a native install shadows a marketplace one silently, so uninstall whichever you are leaving.

### Upgrading to 5.0.0

**5.0.0 ships the Analysis pillar alone, and an upgrade does not remove what it withdraws.** The `acordia-operators` plugin was published up to 4.2.0 and has no catalog entry any more, so no upgrade path can resolve it and none uninstalls it: an install made before 5.0.0 stays resident and dispatchable at that version until you remove it yourself.

```sh
omp plugin uninstall acordia-operators@acordia
```

In Claude Code, uninstall it the same way you installed it: that harness takes no action from a catalog change at all.

**Two legs were divided, and every handle they carried goes with them.** `target-analyst` split along the seam its own prompt carried: `mission-analyst` took the organisation, `terrain-analyst` the technical terrain. `fusion-analyst` decomposed three ways rather than being renamed — the operating picture and multi-source correlation to `cyber-analyst`, non-technical context to `mission-analyst`, take value and data tooling to the new `collection-analyst`. Anything dispatching `target-analyst` or `fusion-analyst`, or the `/target` and `/fusion` handles, must be updated; there are no compatibility aliases under a retired name.

#### Rename history

Agent names have moved twice. 4.0.0 named every agent for the question it answers rather than for the pillar it leads or the grid column it came from; 5.0.0 divided the two legs above. A short alias is formed from its own agent's name, so it is renamed when that name changes — `/defender` became `/overwatch` in 4.0.0, and `/target` and `/fusion` are gone in 5.0.0. `/analyst` is unchanged: still a word of its agent's name, so an existing invocation through it keeps working.

| In | Was | Became |
|---|---|---|
| 4.0.0 | `operational-analyst` | `cyber-analyst` |
| 4.0.0 | `defender-detection-analyst` | `overwatch-analyst` |
| 4.0.0 | `target-network-analyst` | `target-analyst` |
| 5.0.0 | `target-analyst` | `mission-analyst` + `terrain-analyst` |
| 5.0.0 | `fusion-analyst` | retired; its work divided three ways |

#### Upgrading from 2.5.0

The catalog `source` paths moved to the top of the repository, so an existing install must re-resolve the marketplace before it can find the plugin at all:

```sh
omp plugin marketplace update acordia && omp plugin upgrade
```

Claude Code picks up a new version only on uninstall-then-reinstall. In omp, check for a stale deployment under `~/.omp/agent/agents/` at the same time: native agent roots resolve **before** plugin roots and dedup first-wins by exact name, so an old copy of `cyber-analyst.md` there silently shadows the plugin's.

### Invoking them: the plugin namespace

Agents are dispatched by name, from a picker shared with the harness's own, so the distribution carries one slash-command wrapper per agent to give a namespaced entry point. **The namespace is the plugin name**, applied by the harness itself:

```text
/acordia-analysts:analyst      hand the operating picture and the next decision to the lead
/acordia-analysts:terrain      networks, identity, cloud control planes, host internals
/acordia-analysts:overwatch    what the defender can see, and what being seen would cost
```

Both harnesses scan `<pluginRoot>/commands/*.md` non-recursively and prefix each command with the plugin name, which is why the wrappers live inside the pillar rather than at the repository root. Ten of them: one canonical wrapper per agent (`/acordia-analysts:terrain-analyst`) plus five short handles — `analyst`, `mission`, `terrain`, `overwatch`, `collection`.

The agent name itself is not wrapped. omp registers plugin agents flat, so `terrain-analyst` dispatches; Claude Code namespaces them, so its Task tool needs `acordia-analysts:terrain-analyst` (verified at 2.1.220). A wrapper names its agent in prose and leaves each harness to resolve it.

#### Bump the version on every change

The version is hand-maintained semver in three places across three files that must agree — the manifest and one entry in each catalog:

```sh
grep -ho '"version": "[^"]*"' .claude-plugin/marketplace.json \
  .omp-plugin/marketplace.json acordia-analysts/.claude-plugin/plugin.json | sort -u
```

One line out means the three agree. Nothing inside the repository enforces that — the gates went with the generator — so it is a rule plus one external drift check. **MINOR** for any change that reaches a user: an agent prompt, a skill body, a command wrapper, a catalog description. **MAJOR** for a roster change, or a change to the shape of the distribution including an install-source move; 5.0.0 removed a pillar, 6.0.0 added a second install route, and 3.0.0 was both. The version is also the only update signal either harness has — omp skips a plugin whose version is not newer, so an unbumped edit reaches nobody who already installed it — and it must stay plain semver, because build metadata makes two versions compare equal and neither would ever upgrade.

### Namespace safety

Commands are namespaced by the harness. **Agent names and skill slugs are not, on purpose:** dispatch is an exact-name lookup and skills are chosen by description match, so a prefix would isolate nothing while breaking the grid bijection and every `skill://` reference. Provenance rides on the `ACORDIA Analysis — ` description tag instead. Two collision surfaces remain, neither closable from inside a plugin:

- **Agent names.** omp dedups first-wins across native roots, extension packages, marketplace plugins and bundled agents, in that order, so a same-named agent under `.omp/agents/` or `~/.omp/agent/agents/` wins over the plugin's and nothing warns you.
- **Skill descriptions.** Selection is a description match over every discovered skill, so one of your own with an overlapping description competes with an ACORDIA skill rather than colliding outright.

Rename your own artifact. There is no second pillar to switch off: `omp plugin disable acordia-analysts@acordia` disables the distribution entirely.

## Design constraints

- **One authored tree.** No generator, no build step: what is in the repository is what a harness loads.
- **Three-key agent frontmatter.** Exactly `name`, `description`, `color` — no tool list, no permission map, no mode, no metadata. Capability is granted by omission: an agent with no `tools` key gets omp's full tool set, one with no `spawns` key an unrestricted spawn policy.
- **Every agent is write-capable.** Each prompt says it writes freely — notes, working files, drafts, product — but never modifies the material it was given to analyse: evidence, collected data, logs, dumps and captures are read-only inputs. `.acordia/reports/` for a finished product is a convention no harness enforces, and must never be described as enforced.
- **Retrieved content is data, never instructions.** All five prompts say so: an instruction found inside a fetched page, tool output, document text or collected artefact is reported to the caller, not followed.
- **Execution belongs to the operators the analyst advises.** The lead directs no executing agent; it states what the human operator is being asked to decide or do, and judges the end from evidence that operator reports back.
- **Routing is prompt discipline.** The orchestrator names its own legs; nothing in the frontmatter restricts who may dispatch whom.
- **Skills bind by prompt reference and fire on description.** Neither harness binds skills per agent, so every prompt names its set on `·`-separated lines while the skill itself is chosen by a description match — which is why each description states what it does and when it applies in one sharp sentence.

## Source of truth

The competency map behind the artifacts is [`docs/roles/operational-analyst.md`](docs/roles/operational-analyst.md) — rows of skills scored `●` deep / `○` working against five columns of specialisation, one per agent. The contract binding map to artifacts (grid row → skill, grid column → an agent's skill set, ●/○ → deep/working) is in [`openspec/specs/competency-map-derivation/`](openspec/specs/competency-map-derivation/spec.md). Editing an artifact under `acordia-analysts/` without touching the map is a drift bug; when the map changes, the artifacts follow it. A row's identity is a stable kebab-case id carried in the row itself rather than a line number: nothing reads the anchor at install time, so a line reference that shifts does not fail, it just points at the wrong competency.

The literature behind the doctrine is registered in [`docs/roles/sources.md`](docs/roles/sources.md): every work introduced once, with author, title and lib.ai document id under a short key, and cited elsewhere by key and section. A doctrinal claim — how the work is divided, why a judgement is framed this way, what an operation is for — traces there; technique detail traces to its grid row instead. [`openspec/specs/doctrinal-provenance/`](openspec/specs/doctrinal-provenance/spec.md) is the contract, and a literature search that finds nothing is recorded as a gap rather than filled in from memory.

[`docs/roles/archive/operator.md`](docs/roles/archive/operator.md) is a retired record, kept for one purpose: it documents what the withdrawn operations pillar ported from the CyberStrike fork (commit `359655518`) and where it deliberately diverged. Nothing in the shipped tree derives from it.

Five capabilities are published under [`openspec/specs/`](openspec/specs/): `agent-roster`, `skill-library`, `competency-map-derivation`, `doctrinal-provenance` and `plugin-distribution`. The history behind the current shape is under [`openspec/changes/`](openspec/changes/).

## How to extend

**A new agent** is one file at `acordia-analysts/agents/<name>.md`, its frontmatter exactly three keys:

```yaml
---
name: terrain-analyst
description: ACORDIA Analysis — What does the target's technical terrain look like, what can reach what …
color: blue
---
```

`name` must equal the filename stem, because dispatch is an exact-name lookup. `description` opens with the `ACORDIA Analysis — ` tag and then says what the agent is for; it is all a caller sees in the picker. `color` is `cyan` for the orchestrator and `blue` for the legs. Add nothing else — a `tools` key subtracts capability rather than adding it, and frontmatter the parser cannot read makes the agent disappear from `/agents` with a warning rather than an error. An agent derives from a column of the map, so a sixth agent means a sixth column, marked across the rows it owns, in the same change.

The body names the skills the agent draws on as `·`-separated slugs under a heading; that is the only binding between an agent and its skills. **A new agent also needs a command wrapper** in `commands/`, or it has no namespaced entry point: a flat `<name>.md` with `description` and `argument-hint` frontmatter, dispatching the agent in prose. Copy [`acordia-analysts/commands/overwatch-analyst.md`](acordia-analysts/commands/overwatch-analyst.md).

**A new skill** is a directory at `acordia-analysts/skills/<slug>/` holding `SKILL.md`, and the directory name must equal the frontmatter `name` — that bijection is what makes a slug named in a prompt resolvable. Long enumerations belong in a `references/` subdirectory beside it, as in [`credential-harvest-triage/`](acordia-analysts/skills/credential-harvest-triage/), rather than in the body. Write the description to discriminate against the skill's nearest sibling rather than to sound complete: when the harness picks what to read, every skill's name and description is all it has.

A skill traces to the competency map and says so in frontmatter:

```yaml
metadata:
  acordia:
    family: target-modelling
    grid_row: protocol-routing-architecture
    grid_deep_in: [Terrain]
    grid_working_in: [Def]
    row: protocol-routing-architecture
    source: docs/roles/operational-analyst.md
```

41 of the 45 anchor to a row that way, `row` naming the row's minted identity and `source` the map with no line fragment. The other four are procedural rather than derived: each carries `grid_row: null`, `procedural: true` and the change that authorised it as its `source`, and `aleph-entity-graph` additionally declares `cross_cutting` over the skills it composes. A skill with neither a row nor such a record is inventing capability the map does not claim. Where a skill's body rests on a specific work it adds `doctrine_source` — register keys from `docs/roles/sources.md` — alongside the grid anchor rather than in place of it.

## Verifying an install

There are no build gates. Verification is that the thing loads and runs.

In omp, check the discovery providers before anything else. The install-state commands answer what is registered, never what is loaded, and all of them report health for a plugin that is serving nothing:

```sh
omp config get disabledProviders                               # must not list `claude-plugins`
omp plugin marketplace update acordia && omp plugin upgrade    # reports 6.0.0
```

Then in omp, `/agents` lists all five — the check that matters, because a frontmatter mistake makes an agent vanish quietly rather than fail loudly — and `/skills` lists the ACORDIA skills, matching the directory count. Dispatch the lead and one leg and confirm each returns. In Claude Code, `/agents` lists the same five, which is the proof that one tree serves both.

After a native install the restart is not optional: a running session holds the roster it started with, so restart omp, then `/agents` must list five and a `skill://<slug>` read must resolve — `skill://take-domain-interpretation`, say, which proves a linked skill directory is served through its symlink rather than merely sitting in the root.

Two invariants that build gates used to enforce are now checked by hand. The catalogs agree — `diff .claude-plugin/marketplace.json .omp-plugin/marketplace.json` — and every skill slug named in a prompt resolves:

```sh
python3 -c "
import glob, os, pathlib
have = {os.path.basename(os.path.dirname(s)) for s in glob.glob('acordia-analysts/skills/*/SKILL.md')}
for a in glob.glob('acordia-analysts/agents/*.md'):
    for line in pathlib.Path(a).read_text().splitlines():
        if ' · ' in line:
            for slug in line.strip().split(' · '):
                if slug not in have: print('UNRESOLVED', a, slug)
"
```

Both print nothing when the tree is sound.
