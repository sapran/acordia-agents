# Tasks

## 1. Establish what actually serves an agent

Measured 2026-08-21 against the 5.0.0 tree, in isolated `--profile` sandboxes so no live install was
disturbed. Every claim in the proposal and the delta comes from this section.

- [x] 1.1 Confirm the marketplace route works on a stock config, so the change is understood as
      additive: `omp plugin marketplace add sapran/acordia-agents` then
      `omp plugin install acordia-analysts@acordia` in a profile whose effective `disabledProviders`
      was `[]`. `collection-analyst` dispatched and its subagent `session_init` prompt carried the six
      skill slugs unique to that agent.
- [x] 1.2 Confirm the gate: with `claude-plugins` disabled the same install is inert while
      `omp plugin list`, `installed_plugins.json`, `omp-plugins.lock.json` and the `node_modules`
      symlink all report health, with no error and no warning. Only
      `omp config get disabledProviders` names the cause.
- [x] 1.3 Confirm `claude-plugins` is a distinct id from `claude` in the one shared
      `disabledProviders` namespace, and that it reads both `~/.omp/plugins/installed_plugins.json`
      and `~/.claude/plugins/installed_plugins.json` — 19 Claude Code plugins surfaced on this machine.
- [x] 1.4 Test every documented alternative surface with `claude-plugins` disabled: user `extensions:`
      with a bare directory, the same with a `package.json`, and a registered `omp plugin link` npm
      plugin. All three load the skills and drop the agents. Only CLI `omp -e <path>` serves agents.
      This contradicts discovery input 3 of `omp://task-agent-discovery.md` — an omp bug, so no
      packaging change fixes it.
- [x] 1.5 Confirm the native roots are gated by no provider, and that a symlinked skill directory
      resolves: a `skill://` read logged its resolved path as
      `profiles/insttest/agent/skills/take-domain-interpretation`, through the symlink.
- [x] 1.6 Confirm native roots dedup first-wins by exact agent name and resolve before plugin roots,
      so a native install shadows a marketplace install of the same five names silently.

## 2. The scripts

- [x] 2.1 Write `tools/install-omp.sh` — bash, `set -euo pipefail`, executable. Symlinks the five
      `acordia-analysts/agents/*.md` into `<agent-dir>/agents/` and the 45
      `acordia-analysts/skills/*/` into `<agent-dir>/skills/`. Symlinks, not copies, so a `git pull`
      changes what omp serves.
- [x] 2.2 Give both scripts one interface: `[--profile <name>] [--agent-dir <path>] [--dry-run]` plus
      `-h/--help`, `--profile` and `--agent-dir` mutually exclusive. Precedence `--agent-dir`,
      `--profile` → `~/.omp/profiles/<name>/agent`, `$PI_CODING_AGENT_DIR`, `~/.omp/agent`.
- [x] 2.3 Edit no configuration file — no `config.yml`, no profile, no plugin registry, no lockfile.
      The only writes are inside the two roots.
- [x] 2.4 Add the collision preflight: any existing target that is not already one of our own symlinks
      aborts the run, prints every colliding path, and changes nothing. A re-run over our own links is
      idempotent.
- [x] 2.5 Write `tools/uninstall-omp.sh` — removes only symlinks whose `readlink` target contains
      `/acordia-analysts/agents/` or `/acordia-analysts/skills/`. Match on the recorded target, not on
      a manifest and not on the current checkout, so links from a deleted, renamed or moved checkout
      are still cleaned.
- [x] 2.6 Remove the two roots only when the script emptied them itself.
- [x] 2.7 Do not install the command wrappers by this route, and say so in the script's own output:
      a wrapper's invocation name comes from the plugin namespace, which a native root cannot supply.
- [x] 2.8 Have both scripts tell the user to restart omp — a running session holds the roster it
      started with, so a successful install otherwise looks like a no-op.

## 3. Verify the scripts

- [x] 3.1 Install into an isolated profile: five agents and 45 skills linked.
- [x] 3.2 Dispatch `collection-analyst` from that profile and confirm it returns its exact token, with
      the five agent-unique slugs present in its subagent prompt.
- [x] 3.3 Confirm `skill://take-domain-interpretation` resolves through the symlink.
- [x] 3.4 Plant a real `cyber-analyst.md` and re-run the installer: it aborted and left all 45 skills
      unlinked, changing nothing.
- [x] 3.5 Uninstall with 50 ACORDIA links plus a planted real `mine.md` and a planted foreign symlink
      `decoy` present: reported `Removed 50 ACORDIA links` and `Left 2 entries that are not ours`, and
      both planted entries survived.

## 4. Documentation

- [x] 4.1 Document the second route in `README.md`: when to use it — a marketplace install that
      reports health and serves nothing — the two commands, the interface, and the two costs, that it
      installs no command wrappers and that it shadows a live marketplace install silently.
- [x] 4.2 Record the discovery finding in `CLAUDE.md`, including that `claude-plugins` also reads
      Claude Code's registry and that `extensions:` and linked npm plugins drop agents.
- [x] 4.3 Correct `openspec/config.yaml`'s project context — it stated "There is no generator, no
      build step and no shell installer"; the last clause is now false and the first two still hold.

## 5. Specs and version

- [x] 5.1 `plugin-distribution`: modify *One authored tree per pillar serves every harness*. Its body
      ends "A harness install SHALL therefore consist of resolving the catalog and copying the plugin
      directory", which is no longer true as an exclusive claim. Carry all three published scenario
      titles forward verbatim — `Plugin layout is the authored layout`, `No second tree exists`,
      `One tree loads in both harnesses` — because a `## MODIFIED` block replaces the whole
      requirement and OpenSpec matches scenarios by title.
- [x] 5.2 `plugin-distribution`: add the script-route requirement, every clause scenario-bound,
      including the shadowing cost and the standing no-gate constraint.
- [x] 5.3 Bump 5.0.0 → **6.0.0** in all three occurrences: one `plugin.json`, one entry in each of the
      two catalogs. MAJOR because the shape of the distribution changes — it gains a second install
      route.
- [x] 5.4 Run `openspec validate --all --strict`.

## 6. Land it

- [ ] 6.1 `openspec archive native-install-scripts --yes`, re-validate, commit the archive in the same
      PR.
- [ ] 6.2 Review with `reviewer` and `security-reviewer` — the scripts create symlinks in a user's
      home directory and delete entries from it, which is the surface that most warrants it. Fix or
      dismiss each finding.
- [ ] 6.3 Merge to `develop` with a merge commit, then remove the worktree and delete the branch.
