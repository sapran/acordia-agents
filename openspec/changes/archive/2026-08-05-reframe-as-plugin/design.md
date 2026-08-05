## Context

Three harnesses, two distribution mechanisms, one source tree. The verified facts that constrain the design:

**omp** reads a marketplace catalog at `.omp-plugin/marketplace.json` in preference to `.claude-plugin/marketplace.json`, falling back to the latter only when the former is absent. A repo may ship both, which is the documented way to hand each harness a different tree. Plugin agents are discovered at the fixed path `<plugin-root>/agents/`; the marketplace `agents` field is preserved but not consumed, so there is no override. Frontmatter takes `name`, `description`, `tools` (lowercase omp tool names), `spawns`, `model`, `color`, `autoloadSkills`, `metadata`. Omitting a tool removes it *except* `read`/`write`, which are `XDEV_TRANSPORT_TOOLS`.

**Claude Code** requires `.claude-plugin/plugin.json` at the plugin root and auto-discovers `./commands`, `./agents`, `./skills`; the manifest's path fields *supplement* those defaults rather than replacing them. Plugin agents support only `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation` — `hooks`, `mcpServers`, and `permissionMode` are silently ignored for security, and `metadata` is not a key. `tools` is a CSV of capitalised Claude tool names. Plugin commands and skills are automatically namespaced `<plugin-name>:<name>`.

**opencode** has no plugin system: no marketplace, no registry, no `.claude-plugin` reader. Its "plugins" are JS/TS hook modules. Markdown discovery is a filesystem scan of `agents/`, `skills/<slug>/SKILL.md`, `commands/*.md` (flat) under `~/.config/opencode/` and `.opencode/`. Its Claude interop is narrow and hardcoded: `CLAUDE.md` for rules and `.claude/skills/` for skills — not agents, not commands, not `.claude-plugin`.

## Goals / Non-Goals

**Goals.** Install through each harness's own mechanism where one exists. Preserve the analysts' read-only posture to the deepest extent each harness permits, and state honestly where it cannot be enforced. Keep exactly one editable source per artifact.

**Non-Goals.** Codex is out of scope. No attempt to give opencode a plugin experience it does not have. No change to any agent prompt, skill, or command body.

## Decisions

### Two plugins rather than one

The pillars have opposite postures: analysts are read-only decision support, operators are write-capable offensive tooling with a shell that throws payloads. Shipping them as one plugin would make installing the analytic library imply installing the offensive one. Two plugin ids — `acordia-analysts`, `acordia-operators` — under one marketplace named `acordia`.

The cost is that the command namespace changes shape: `/acordia-analysts:fusion` rather than `/acordia:fusion`. That is accepted, because the prefix is now supplied by the harness from the plugin name and is therefore identical in omp and Claude Code, where previously it existed only because the installer wrote into a specific directory.

*Alternative rejected:* one `acordia` plugin with both pillars. Shorter handles, but no way to decline the offensive pillar, and no way to describe the two postures in one plugin description.

### Two generated trees, not one shared tree

This is forced, not chosen. Both harnesses read `tools` off `<plugin-root>/agents/`, Claude Code expects `Read, Grep, Glob, Bash` and omp expects `read, grep, glob, bash`, omp needs `spawns`, and Claude Code's `agents` path override supplements rather than replaces the default. The three escape routes all fail:

- *Omit `tools` entirely.* Both harnesses then inherit everything, and the analysts' read-only posture — normative in `analyst-agent-roster` — evaporates in both.
- *Point Claude Code elsewhere via the manifest.* It supplements `./agents`, so omp's tree would load in Claude Code too, with an unparsable `tools` list.
- *Emit a union of both vocabularies.* Each harness would see the other's names as unknown tools; omp's allowlist semantics make that a silent capability grant.

So: generate both, gate them with `--check`, and keep skills and commands byte-identical between them so only `agents/` can ever differ.

### Generated output is committed

A marketplace install clones the repository and reads the tree as it stands; there is no build step on the installing machine. The trees must therefore exist in git. That makes drift the risk, so a plain build deletes `plugins/`, `.claude-plugin/`, and `.omp-plugin/` wholesale before regenerating — a renamed skill cannot leave an orphan — and `--check` builds into a tempdir and diffs, naming every missing, extra, and differing path.

### `disallowedTools`, and the `scoped` → keep-`Write` decision

Claude Code plugin agents get a denylist derived from the same three source signals the omp translator already reads:

| source signal | contributes |
| --- | --- |
| `permission.edit` denied | `Edit, Write, NotebookEdit` |
| `permission.edit` path-scoped | `Edit, NotebookEdit` — `Write` retained |
| `permission.edit: allow` | nothing |
| `permission.task: deny` (no allowed spawns) | `Task` |

An allowlist would have to name Claude's whole vocabulary and would silently strip tools this repository never audited (`Skill`, `NotebookEdit`, `WebFetch`). The denylist expresses exactly what the source encodes.

The `scoped` row deliberately differs from the omp translator, which drops the tool. opencode confines `operational-analyst` and `fusion-analyst` writes to `.acordia/reports/**`. Claude Code cannot express a path scope in plugin-agent frontmatter; denying `Write` outright would leave those two unable to produce the reports their prompts require, which is a competency the grid assigns them. So `Write` is granted and the confinement becomes prompt-level, recorded in a comment. Under omp the same choice costs nothing either way, because `write` is an `xd://` transport tool and returns regardless — which is why the two emitters legitimately diverge here.

### Provenance as YAML comments

`metadata` is not a supported plugin-agent key in Claude Code, so the `metadata.generated` block omp carries has nowhere to live. Comment lines above the frontmatter keys carry the source path plus, conditionally, the three postures the harness cannot express: no spawn allowlist, no path scope, no per-command bash rules. If a future Claude Code release rejects comments in that position, the fallback is an HTML comment at the top of the prompt body — the frontmatter keys themselves are all documented-supported.

### Command routing by the agent the wrapper names

A wrapper belongs to whichever plugin owns the agent it dispatches. That agent is extracted from the body's opening sentence, which is one of two shapes — `Dispatch the \`x\` agent` for the fourteen leaf wrappers and `Hand the work below to the \`x\` agent` for the three orchestrator wrappers, which must name a session-switch fallback because a primary agent cannot always be dispatched. A wrapper matching neither shape, or naming an agent in no pillar, fails the build rather than being guessed at.

Wrappers land flat at `<plugin-root>/commands/<stem>.md`. Flat is mandatory: omp's plugin command provider scans that directory non-recursively, so a subdirectory would be invisible to omp. `name` and `category` are dropped from the frontmatter — the handle is now `<plugin>:<stem>`, so a frontmatter `name` would fight the prefix, and `category` is a key in neither plugin schema.

## Risks / Trade-offs

- **Committed build output can drift.** Mitigated by `--check` and by the wholesale delete-then-regenerate. Not mitigated for someone who edits `plugins/` and never runs the check; `CLAUDE.md` names that as a drift bug of the same class as editing `analysts/` without touching the grid.
- **Skills are duplicated four times on disk** (two plugins × two harnesses). Accepted: both trees are generated and gate-checked, so the copies cannot diverge, and the alternative — a shared directory referenced by manifest path — is not expressible, since Claude Code's path fields supplement rather than replace.
- **`disallowedTools` names must match Claude Code's vocabulary.** An unknown entry is ignored silently rather than erroring. Verified by asking an installed leg analyst to write a scratch file and confirming refusal.
- **opencode users lose nothing but gain nothing.** The installer is simpler; the deployment is identical.

## Open Questions

None blocking. Two contingencies are recorded rather than resolved: if omp ever rejects a plugin directory carrying `.claude-plugin/plugin.json`, that file is deleted from the omp tree only; if omp surfaces the Claude tree despite `.omp-plugin/` being present, the Claude catalog moves to a second repository path, since the omp tree is the one that must win for omp.
