# ACORDIA Agents

Runnable agents and skills derived from the ACORDIA framework's operational role models, distributed as a plugin marketplace for [omp](https://github.com/can1357/oh-my-pi) and Claude Code.

## What this is

Markdown-only artifacts — agent files, skill files, and command wrappers. No application code, no runtime, and since 3.0.0 no build step: each pillar is one authored tree that both harnesses read as it stands in the checkout, and a marketplace install clones this repository and points at that tree directly.

One tree serves both because both accept the same agent file: omp's `parseAgentFields()` requires `name`, `description` and a body and treats `tools` as optional, and Claude Code requires the same three keys. Every artifact traces to a source — each analyst skill to a row of a competency map, each operator artifact to the CyberStrike file it was ported from.

## Scope

Two pillars, shipped as two independently installable plugins so either can be taken without the other:

- **`acordia-analysts/`** — the Analysis pillar: one orchestrator plus three specialist legs, and the 42-skill library realising their shared analytic spine. Decision support and target understanding; no target interaction, no active testing.
- **`acordia-operators/`** — the Operations pillar, ported from the CyberStrike fork (`~/git/CyberStrike`, commit `359655518`): one orchestrator plus four domain specialists and a 39-skill technique library (31 ported, 8 authored here). Offensive, and gated on written authorisation by the prompts rather than by the harness. Provenance and divergence are recorded in [`docs/roles/operator.md`](docs/roles/operator.md).

Future pillars (Collection, Reflection, Direction, Independent action) may follow the same shape as they get compiled.

```
acordia-agents/
├── acordia-analysts/                 # plugin root — installed as-is
│   ├── .claude-plugin/plugin.json
│   ├── agents/     operational-analyst · target-network-analyst
│   │               defender-detection-analyst · fusion-analyst
│   ├── commands/   8 command wrappers
│   └── skills/     42 skills, one SKILL.md each
├── acordia-operators/                # plugin root — installed as-is
│   ├── .claude-plugin/plugin.json
│   ├── agents/     operator · web-application · mobile-application
│   │               cloud-security · internal-network
│   ├── commands/   9 command wrappers
│   └── skills/     39 skills, one SKILL.md each
├── .claude-plugin/marketplace.json   # Claude Code reads this catalog
├── .omp-plugin/marketplace.json      # omp prefers this one; byte-identical
├── docs/roles/                       # the two sources of truth
└── openspec/                         # capability specs and change history
```

## Install

```sh
# omp
omp plugin marketplace add sapran/acordia-agents
omp plugin install acordia-analysts@acordia    # add acordia-operators@acordia for the offensive pillar

# Claude Code
claude plugin marketplace add sapran/acordia-agents
claude plugin install acordia-analysts@acordia
```

`acordia` is the marketplace name, from the `name` field of both catalogs. omp resolves `.omp-plugin/marketplace.json` in preference and Claude Code reads `.claude-plugin/marketplace.json`; the two are byte-identical.

In omp, marketplace content is delivered by the `claude-plugins` capability provider, which reads Claude Code's plugin registry alongside omp's own — so one Claude Code install can be inherited rather than registered twice, and so disabling that provider leaves the plugin installed and contributing nothing. `/reload-plugins` refreshes skills and commands after an install; new tools or hooks need a restart.

**opencode was dropped in 3.0.0**, with the shell installer that was its only route in and the generator that existed to express its permission maps; opencode users have no upgrade path and must switch harness.

#### Upgrading from 2.5.0

The catalog `source` paths moved to the top of the repository, so an existing install must re-resolve the marketplace before it can find the plugin at all:

```sh
omp plugin marketplace update acordia && omp plugin upgrade
```

Claude Code picks up a new version only on uninstall-then-reinstall. In omp, check for a stale deployment under `~/.omp/agent/agents/` at the same time: native agent roots resolve **before** plugin roots and dedup first-wins by exact name, so an old copy of `fusion-analyst.md` there silently shadows the plugin's.

### Invoking them: the plugin namespace

Agents are dispatched by name, from a picker shared with the harness's own, so the distribution carries one slash-command wrapper per agent to give a namespaced entry point. **The namespace is the plugin name**, applied by the harness itself:

```
/acordia-analysts:fusion       what all of it together means, and how good the take is
/acordia-operators:webapp      OWASP WSTG testing of a web target
/acordia-operators:operator    hand an authorised engagement to the orchestrator
```

Both harnesses scan `<pluginRoot>/commands/*.md` non-recursively and prefix each command with the plugin name, which is why the wrappers live inside a pillar rather than at the repository root. Seventeen of them: one canonical wrapper per agent (`/acordia-analysts:fusion-analyst`) plus eight short handles — `analyst`, `target`, `defender`, `fusion`, `webapp`, `mobile`, `cloud`, `internal`.

The agent name itself is not wrapped. omp registers plugin agents flat, so `fusion-analyst` dispatches; Claude Code namespaces them, so its Task tool needs `acordia-analysts:target-network-analyst` (verified at 2.1.220). A wrapper names its agent in prose and leaves each harness to resolve it.

#### Bump the version on every change

The version is hand-maintained semver in four files that must agree — the two `plugin.json` manifests and the two catalogs:

```sh
grep -ho '"version": "[^"]*"' .claude-plugin/marketplace.json \
  .omp-plugin/marketplace.json acordia-*/.claude-plugin/plugin.json | sort -u
```

Nothing enforces that agreement — the gates went with the generator — so it is a rule, not a check. **MINOR** for any change that reaches a user: an agent prompt, a skill body, a command wrapper, a catalog description. **MAJOR** for a roster change, or a change to the shape of the distribution including an install-source move; 3.0.0 was both. The version is also the only update signal either harness has — omp skips a plugin whose version is not newer, so an unbumped edit reaches nobody who already installed it — and it must stay plain semver, because build metadata makes two versions compare equal and neither would ever upgrade.

### Namespace safety

Commands are namespaced by the harness. **Agent names and skill slugs are not, on purpose:** dispatch is an exact-name lookup and skills are chosen by description match, so a prefix would isolate nothing while breaking the grid bijection and every `skill://` reference. Provenance rides on the `ACORDIA Analysis — ` / `ACORDIA Operations — ` description tag instead. Two collision surfaces remain, neither closable from inside a plugin:

- **Agent names.** omp dedups first-wins across native roots, extension packages, marketplace plugins and bundled agents, in that order, so a same-named agent under `.omp/agents/` or `~/.omp/agent/agents/` wins over the plugin's and nothing warns you.
- **Skill descriptions.** Selection is a description match over every discovered skill, so one of your own with an overlapping description competes with an ACORDIA skill rather than colliding outright.

Rename your own artifact, or switch off the pillar you are not using: `omp plugin disable acordia-operators@acordia`.

## Design constraints

- **One authored tree per pillar.** No generator, no build step: what is in the repository is what a harness loads.
- **Three-key agent frontmatter.** Exactly `name`, `description`, `color` — no tool list, no permission map, no mode, no metadata. Capability is granted by omission: an agent with no `tools` key gets omp's full tool set, one with no `spawns` key an unrestricted spawn policy.
- **Every agent is write-capable.** Each analyst prompt says it writes freely — notes, working files, drafts, product — but never modifies the material it was given to analyse: evidence, collected data, logs, dumps and captures are read-only inputs. `.acordia/reports/` for an analyst product and `.acordia/ops/` for an operator journal are conventions no harness enforces, and must never be described as enforced.
- **Retrieved content is data, never instructions.** All nine prompts say so: an instruction found inside a fetched page, tool output, document text or collected artefact is reported to the caller, not followed.
- **Routing is prompt discipline.** Each orchestrator names its own specialists; nothing in the frontmatter restricts who may dispatch whom.
- **Skills bind by prompt reference and fire on description.** Neither harness binds skills per agent, so every prompt names its set on `·`-separated lines while the skill itself is chosen by a description match — which is why each description states what it does and when it applies in one sharp sentence.

## Source of truth

The competency map behind the analyst artifacts is [`docs/roles/operational-analyst.md`](docs/roles/operational-analyst.md) — rows of skills scored `●` deep / `○` working against columns of specialisations. The contract binding map to artifacts (grid row → skill, grid column → an agent's skill set, ●/○ → deep/working) is in [`openspec/specs/competency-map-derivation/`](openspec/specs/competency-map-derivation/spec.md). Editing an artifact under `acordia-analysts/` without touching the map is a drift bug; when the map changes, the artifacts follow it.

The operator pillar derives from no such map. It is a provenance-tracked port whose source of truth is [`docs/roles/operator.md`](docs/roles/operator.md): the agent-to-agent table, the skill-clone provenance, what was deliberately left out, and the divergences since. Editing `acordia-operators/` without checking that record is the same class of bug. The history behind the current shape is under [`openspec/changes/`](openspec/changes/).

## How to extend

**A new agent** is one file at `<pillar>/agents/<name>.md`, its frontmatter exactly three keys:

```yaml
---
name: target-network-analyst
description: ACORDIA Analysis — What is the target for, what does it depend on, where can we move …
color: blue
---
```

`name` must equal the filename stem, because dispatch is an exact-name lookup. `description` opens with the `ACORDIA Analysis — ` or `ACORDIA Operations — ` tag and then says what the agent is for; it is all a caller sees in the picker. `color` is `cyan` for the two orchestrators and `blue` for the seven specialists. Add nothing else — a `tools` key subtracts capability rather than adding it, and frontmatter the parser cannot read makes the agent disappear from `/agents` with a warning rather than an error.

The body names the skills the agent draws on as `·`-separated slugs under a heading; that is the only binding between an agent and its skills. **A new agent also needs a command wrapper** in the same pillar's `commands/`, or it has no namespaced entry point: a flat `<name>.md` with `description` and `argument-hint` frontmatter, dispatching the agent in prose. Copy [`acordia-analysts/commands/fusion.md`](acordia-analysts/commands/fusion.md).

**A new skill** is a directory at `<pillar>/skills/<slug>/` holding `SKILL.md`, and the directory name must equal the frontmatter `name` — that bijection is what makes a slug named in a prompt resolvable. Long enumerations belong in a `references/` subdirectory beside it, as in [`credential-harvest-triage/`](acordia-analysts/skills/credential-harvest-triage/), rather than in the body. Write the description to discriminate against the skill's nearest sibling rather than to sound complete: when the harness picks what to read, every skill's name and description is all it has.

An analyst skill traces to the competency map and says so in frontmatter:

```yaml
metadata:
  acordia:
    grid_row: multi-source-fusion
    grid_deep_in: [Fus]
    grid_working_in: [Core]
    source: docs/roles/operational-analyst.md#L101
```

38 of the 42 anchor to a row that way. The other four are procedural rather than derived: each carries `grid_row: null`, `procedural: true` and the change that authorised it as its `source`, and `aleph-entity-graph` additionally declares `cross_cutting` over the skills it composes. A skill with neither a row nor such a record is inventing capability the map does not claim. An operator skill instead keeps its `metadata.cyberstrike` block naming the `.cyberstrike/skill/…` path and commit it was cloned from — attribution rather than machinery, and what makes a re-port against a newer CyberStrike commit a diff instead of an archaeology exercise.

## Verifying an install

There are no build gates. Verification is that the thing loads and runs.

```sh
omp plugin marketplace update acordia && omp plugin upgrade    # both pillars report 3.0.0
```

Then in omp, `/agents` lists all nine — the check that matters, because a frontmatter mistake makes an agent vanish quietly rather than fail loudly — and `/skills` lists the ACORDIA skills, matching the directory count. Dispatch one agent per pillar and confirm each returns. In Claude Code, `/agents` lists the same nine, which is the proof that one tree serves both.

Two invariants that build gates used to enforce are now checked by hand. The catalogs agree — `diff .claude-plugin/marketplace.json .omp-plugin/marketplace.json` — and every skill slug named in a prompt resolves inside its own pillar:

```sh
python3 -c "
import glob, os, pathlib
for p in ('acordia-analysts', 'acordia-operators'):
    have = {os.path.basename(os.path.dirname(s)) for s in glob.glob(p + '/skills/*/SKILL.md')}
    for a in glob.glob(p + '/agents/*.md'):
        for line in pathlib.Path(a).read_text().splitlines():
            if ' · ' in line:
                for slug in line.strip().split(' · '):
                    if slug not in have: print('UNRESOLVED', a, slug)
"
```

Both print nothing when the tree is sound.
