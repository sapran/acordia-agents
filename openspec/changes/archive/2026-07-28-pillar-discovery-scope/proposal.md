## Why

`install.sh` treats any top-level directory carrying an `agents/` or `skills/` subdirectory as a deployable pillar. That sweeps in `.opencode/` and `.claude/`, which hold this repository's own OpenSpec workflow skills — `openspec-apply-change`, `openspec-archive-change`, `openspec-explore`, `openspec-propose`, `openspec-sync-specs`. Those five are development tooling for maintaining *this* repository, not ACORDIA distribution artifacts, yet a plain `./install.sh` publishes them into the user's global config, where they surface in every unrelated project. Adding the omp harness target doubled the blast radius: they now land under `~/.omp/agent/skills/` as well.

## What Changes

- **Pillar auto-discovery skips dot-directories.** A pillar must be a *visible* top-level directory carrying `agents/` or `skills/`. This matches how `README.md` has always described the layout.
- **Explicit `--pillar` still works for any directory**, including a dot-directory, so nothing becomes unreachable — only the default sweep narrows.
- **BREAKING for anyone relying on the leak.** A user who installed the five `openspec-*` skills globally via `./install.sh` stops receiving them on the next install. They were never intended as distribution artifacts; the migration is to remove them, which `./uninstall.sh --pillar .opencode` does.
- `docs/implementation-notes.md` drops the finding, now that it is fixed.

Current behaviour: `./install.sh` deploys 4 agents, 42 analyst skills, and 5 OpenSpec dev-tooling skills.
Desired behaviour: `./install.sh` deploys 4 agents and 42 analyst skills.

## Capabilities

### Modified Capabilities
- `omp-harness-distribution`: the pillar-selection rule that governs what both harnesses deploy is currently implicit in the requirements that say "`<pillar>/agents/`" and "`<pillar>/skills/`" without defining what qualifies as a pillar. This change makes it explicit and narrows it.

## Impact

- `install.sh`, `uninstall.sh` — one predicate each in the auto-discovery loop.
- `docs/implementation-notes.md` — remove the resolved finding.
- Deployment surface: five skill entries stop being published to `~/.config/opencode/skills/` and `~/.omp/agent/skills/`.
- No change to `analysts/`, to the translator, or to the `--harness` selector.
