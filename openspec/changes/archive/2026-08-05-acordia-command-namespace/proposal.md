## Why

Both harness roots are flat namespaces shared with the harness's own built-in agents and with whatever the user keeps there. This repository deliberately ships unprefixed names — `analyst-agent-roster` publishes "Provenance is carried by the description, not the name" — and carries provenance in the `ACORDIA <pillar> — ` description tag, now joined by the generated `color`. That covers recognition once an agent is already in front of you.

What it does not cover is invocation. There is no ACORDIA-shaped entry point: a user who wants the fusion analyst types the bare agent name into a picker shared with `task`, `scout`, `reviewer`, and every plugin the machine has installed. The OpenSpec workflow in this repo already solved the same problem for itself — `/opsx:propose` — and did it without renaming anything, because **slash commands are the one artifact type that namespaces by directory**.

Current behaviour: nine agents, no commands, no namespaced entry point. Desired behaviour: `/acordia:<agent>` in the Claude-format command tree (which omp also reads), `/acordia-<agent>` in opencode, and no change to a single agent name or skill slug.

## What Changes

### A command wrapper per dispatchable agent

Add `commands/acordia/<stem>.md`, one file for each of the nine agents across both pillars, where `<stem>` is the agent's filename stem — so the command name has exactly one source of truth and a renamed agent cannot leave a stale command behind. Each wrapper carries a portable `description` (the agent's operating question) plus `argument-hint`, and a body that dispatches that agent with `$ARGUMENTS` as the brief.

`commands/` is a visible top-level directory carrying neither `agents/` nor `skills/`, so the existing pillar auto-discovery rule already skips it — commands are deployed by their own step, not swept in as a tenth pillar.

### Two namespace shapes, because the harnesses differ

- **Claude-format tree** (`~/.claude/commands/acordia/<stem>.md`) → `/acordia:<stem>`. omp's `claude` command provider scans `~/.claude/commands/**/*.md` recursively and registers a subdirectory alias (`foo/bar.md` → both `bar` and `foo:bar`), so one deployment lights up Claude Code and omp with the colon form.
- **opencode** (`~/.config/opencode/commands/acordia-<stem>.md`) → `/acordia-<stem>`. opencode command discovery is flat, which is why this repository's own OpenSpec commands are already `.opencode/commands/opsx-apply.md` while the Claude copies are `.claude/commands/opsx/apply.md`. The hyphen form matches that established precedent rather than inventing a second convention.

omp's own `commands/` directory is non-recursive and therefore cannot carry a namespace, so the omp deployment targets the Claude tree deliberately, and the installer says so.

### Installer and uninstaller carry commands

`install.sh` and `uninstall.sh` gain a command step, on by default, with `--no-commands` to skip it and `--commands-target DIR` to place the tree explicitly. Ownership evidence, preflight refusal, `--dry-run`, and idempotence extend to commands unchanged: `tools/ownership.sh` gains a `command` kind so the two scripts still cannot drift.

### Names stay bare

The command namespace is the **only** prefixed surface. No agent filename, agent name, or skill slug changes — the existing roster requirement is preserved verbatim, and this change adds a scenario asserting it stays true.

## Capabilities

### New Capabilities

- `acordia-command-namespace` — the wrapper set, the per-harness namespace shapes, deployment, and the guarantee that slugs stay unprefixed.

### Modified Capabilities

None. Pillar auto-discovery, the frontmatter translation contract, and the roster's naming requirement are all satisfied as they stand; this change adds a capability beside them.

## Impact

- **New files:** `commands/acordia/*.md` (9).
- **Modified tooling:** `install.sh`, `uninstall.sh`, `tools/ownership.sh`.
- **Modified docs:** `CLAUDE.md` (command contract; also corrects a stale claim that the OpenSpec commands live at `.opencode/commands/opsx/` — that tree is flat `opsx-*.md`), `README.md`.
- **Unchanged:** every agent file, every skill, both pillars' names and slugs, the competency grid, and the translator.
- **No new capability class.** A command wrapper dispatches an agent the user could already dispatch by name; it grants nothing the harness did not already allow.
