## MODIFIED Requirements

### Requirement: One authored tree per pillar serves every harness

The plugin SHALL be a single authored directory at the repository root — `acordia-analysts/` —
containing `.claude-plugin/plugin.json`, `agents/`, `commands/` and `skills/`. The same directory
SHALL serve every target harness: there SHALL be no per-harness tree, no generated or translated copy
of any agent, skill or command, and no build step between the checkout and an install.

An install SHALL be one of exactly two routes into that one directory, and both SHALL read the
authored files rather than a copy of them. The marketplace route resolves the catalog and copies the
plugin directory, and is the documented default for both harnesses. The script route, specified below,
symlinks the pillar's agents and skills into omp's native roots, and exists only because a marketplace
install is inert when the `claude-plugins` discovery provider is disabled. Neither route SHALL generate,
translate or restructure an artifact, so the one-tree guarantee holds under both: what a user receives
is the authored file, reached either by copy of the authored directory or by symlink to it.

#### Scenario: Plugin layout is the authored layout

- **WHEN** a plugin directory is inspected
- **THEN** it contains `.claude-plugin/plugin.json`, `agents/`, `commands/` and `skills/`, and nothing declares itself generated

#### Scenario: No second tree exists

- **WHEN** the repository is searched for a per-harness plugin tree or a generator that would emit one
- **THEN** none is found

#### Scenario: One tree loads in both harnesses

- **WHEN** the same plugin directory is installed in omp and in Claude Code
- **THEN** both discover the pillar's agents, commands and skills from it

#### Scenario: Both install routes read the authored files

- **WHEN** the marketplace route and the script route are compared
- **THEN** each resolves to files inside `acordia-analysts/`, and neither produces a generated or translated artifact

## ADDED Requirements

### Requirement: Two scripts install the pillar into omp's native roots

The repository SHALL carry `tools/install-omp.sh` and `tools/uninstall-omp.sh`, executable bash under
`set -euo pipefail`, as a second route into omp. The installer SHALL symlink each
`acordia-analysts/agents/*.md` into `<agent-dir>/agents/` and each `acordia-analysts/skills/*/` into
`<agent-dir>/skills/`. It SHALL symlink rather than copy, so that a `git pull` in the checkout changes
what omp serves without a reinstall and no second tree comes into being.

This route exists because the marketplace route can be inert while reporting health. Verified
2026-08-21 against the 5.0.0 tree: omp serves a marketplace plugin's `agents/` directory only when the
`claude-plugins` discovery provider is enabled — discovery input 4 of `omp://task-agent-discovery.md`
— and marketplace skills and command wrappers arrive through the same provider. With it disabled,
`omp plugin list` shows the plugin, `~/.omp/plugins/installed_plugins.json` records it,
`~/.omp/plugins/omp-plugins.lock.json` says `"enabled": true`, and
`~/.omp/plugins/node_modules/<name>` symlinks into the cache, with no error and no warning; only
`omp config get disabledProviders` reports the merged effective value that names the cause. Disabling
it is a defensible choice, because `claude-plugins` reads both
`~/.omp/plugins/installed_plugins.json` and `~/.claude/plugins/installed_plugins.json` and therefore
also surfaces every plugin registered in Claude Code's registry, and because `claude-plugins` and
`claude` are distinct ids in the one shared `disabledProviders` namespace, so disabling `claude` does
not disable marketplace plugins.

The native roots the scripts write to — the nearest project `.omp/agents` and the user agent
directory's `agents/`, discovery inputs 1 and 2 — are gated by no discovery provider at all, and a
skill directory reached by symlink in the native skills root resolves correctly. No packaging change
SHALL be attempted as an alternative: verified with `claude-plugins` disabled, a user `extensions:`
entry pointing at a bare directory loads the skills and drops the agents, the same directory carrying
a `package.json` behaves identically, and a registered `omp plugin link` npm plugin reporting
`enabled: true` in the lockfile behaves identically again. Only CLI `omp -e <absolute path>` serves
agents from such a root. This contradicts discovery input 3 of the same document, so it is an omp
defect rather than a packaging error, and a `package.json` SHALL NOT be added to the pillar to chase
it.

Both scripts SHALL take one interface — `[--profile <name>] [--agent-dir <path>] [--dry-run]` plus
`-h/--help` — with `--profile` and `--agent-dir` mutually exclusive. The target directory SHALL be
resolved in the order `--agent-dir`, then `--profile` resolving to `~/.omp/profiles/<name>/agent`,
then `$PI_CODING_AGENT_DIR`, then `~/.omp/agent`.

Neither script SHALL edit a configuration file. No `config.yml`, profile, plugin registry or lockfile
SHALL be written, and the only filesystem changes SHALL be inside the two roots. A script that rewrote
a user's `config.yml` would have to parse YAML it did not author, preserve comments it does not
understand and reverse all of it on uninstall, damaging a file that governs every session rather than
just this pillar.

The installer SHALL run a collision preflight before creating anything. A target that already exists
and is not one of our own symlinks — a symlink whose `readlink` target lies inside this checkout's
pillar — SHALL abort the run, SHALL cause every colliding path to be printed, and SHALL leave the
filesystem unchanged, including the entries that would not have collided. A partial install would
answer by accident the question of which agent omp dispatches for a shared name, in a warning printed
in the middle of a success message. Because an entry that is already one of our own symlinks is not a
collision, a re-run over an existing install SHALL be idempotent.

The uninstaller SHALL remove only a symlink whose `readlink` target contains
`/acordia-analysts/agents/` or `/acordia-analysts/skills/` respectively. It SHALL NOT delete a real
file and SHALL NOT delete a symlink pointing elsewhere. It SHALL match on the symlink's recorded
target rather than on a manifest file or on the current checkout's contents, and SHALL therefore also
clean links whose checkout has since been deleted, renamed or moved, because a dangling symlink is
still readable. It SHALL remove the two roots only when it emptied them itself.

Command wrappers SHALL NOT be installed by this route, and the installer SHALL say so in its own
output. A wrapper takes its invocation name from the plugin namespace, which only a plugin root
supplies; a flat name invented for a native root would differ from the same wrapper's name under the
marketplace route.

The scripts SHALL introduce no build step and no gate. This repository ships no build, nothing in a
hook or a workflow SHALL invoke them, and running either SHALL remain a deliberate act by a user.

#### Scenario: Both scripts ship and are executable

- **WHEN** `tools/` is inspected
- **THEN** `install-omp.sh` and `uninstall-omp.sh` are present, executable, and both set `-euo pipefail`

#### Scenario: Install links agents and skills into the resolved roots

- **WHEN** the installer is run against an agent directory with no prior ACORDIA install
- **THEN** every `acordia-analysts/agents/*.md` is a symlink in `<agent-dir>/agents/` and every `acordia-analysts/skills/*/` is a symlink in `<agent-dir>/skills/`
- **AND** the counts reported are the five agents and 45 skills the pillar ships

#### Scenario: A checkout update changes what omp serves

- **WHEN** the checkout is updated after an install and omp is restarted
- **THEN** the updated agent and skill bodies are served, because the entries are symlinks into the checkout rather than copies

#### Scenario: The target directory follows one precedence

- **WHEN** either script resolves its target
- **THEN** it takes `--agent-dir`, else `--profile` as `~/.omp/profiles/<name>/agent`, else `$PI_CODING_AGENT_DIR`, else `~/.omp/agent`
- **AND** passing both `--agent-dir` and `--profile` is rejected

#### Scenario: No configuration file is edited

- **WHEN** an install or uninstall completes
- **THEN** no `config.yml`, profile, plugin registry or lockfile has been written, and every change is inside `<agent-dir>/agents/` or `<agent-dir>/skills/`

#### Scenario: A collision aborts the run and changes nothing

- **WHEN** a target name is already held by a real file or by a symlink that does not point into this pillar
- **THEN** the run aborts, every colliding path is printed, and nothing is created — not the collision, and not the entries that would have succeeded

#### Scenario: Re-running an install is idempotent

- **WHEN** the installer is run again over an install it made
- **THEN** the existing entries are not treated as collisions and the resulting roots are unchanged

#### Scenario: Uninstall removes only our own links

- **WHEN** the uninstaller runs in a root holding ACORDIA links, a real file of the user's own, and a symlink pointing outside any pillar
- **THEN** only the symlinks whose recorded target lies in an `acordia-analysts` checkout are removed, the count of those left behind is reported, and both other entries survive

#### Scenario: A deleted checkout is still cleanable

- **WHEN** the uninstaller runs after the checkout the links point into has been deleted, renamed or moved
- **THEN** the dangling links are still matched on their recorded target and removed

#### Scenario: The roots are removed only if the script emptied them

- **WHEN** the uninstaller finishes
- **THEN** `<agent-dir>/agents/` and `<agent-dir>/skills/` are removed only if it emptied them itself, and a directory still holding an entry the user owns is left in place

#### Scenario: Command wrappers are absent by this route

- **WHEN** the pillar is installed by the script route
- **THEN** no command wrapper is installed, and the script's output states that this route cannot supply the plugin namespace a wrapper's name comes from

#### Scenario: A native install shadows a marketplace install silently

- **WHEN** the script route is used while a marketplace install of the same pillar is live
- **THEN** the native entries win, because native roots dedup first-wins by exact agent name and resolve before plugin roots
- **AND** no warning distinguishes that from having only one install, so the cost is documented rather than guarded

#### Scenario: The scripts introduce no build step or gate

- **WHEN** the repository is searched for an invocation of either script in a build script, hook or workflow
- **THEN** none exists, and running either remains a deliberate act by a user
