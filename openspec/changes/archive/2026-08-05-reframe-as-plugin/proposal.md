## Why

This repository reaches its harnesses through a bespoke shell installer. `install.sh` symlinks the opencode-native artifacts into `~/.config/opencode/`, translates the agent frontmatter for omp into a gitignored `.build/` directory and copies that into `~/.omp/agent/`, and writes the slash-command wrappers into `~/.claude/commands/acordia/` so that omp and Claude Code both pick them up. Every one of those destinations is a flat directory shared with the harness's own built-ins, which is why the repository had to grow its own ownership-evidence protocol, preflight refusal, and `--force` override just to avoid destroying a stranger's file.

Two of the three harnesses have a first-class answer to all of that. omp reads a marketplace catalog at `.omp-plugin/marketplace.json` (falling back to `.claude-plugin/marketplace.json`), and Claude Code reads `.claude-plugin/marketplace.json`; both install a plugin directory whose `agents/`, `skills/`, and `commands/` subtrees are discovered automatically, namespaced by plugin name, and uninstalled by the harness. opencode has no plugin system at all — its "plugins" are JS/TS hook modules that cannot ship markdown, and its only Claude interop is `.claude/skills/` — so it keeps the installer.

Current behaviour: one installer, one `--harness` selector, one gitignored build directory, and a `/acordia:` namespace that exists only because the installer writes into Claude Code's command tree. Desired behaviour: the repository root **is** a plugin marketplace, `omp plugin marketplace add` and `/plugin marketplace add` both work against the same checkout, and `install.sh` is opencode-only.

## What Changes

### Two plugins, not one

`acordia-analysts` and `acordia-operators`, independently installable so the read-only analysis pillar can be taken without the write-capable offensive pillar. Slash commands therefore become `/acordia-analysts:fusion` and `/acordia-operators:webapp` — both omp and Claude Code prefix a plugin's commands with the plugin name, so the two harnesses agree and the old `/acordia:` namespace is retired.

### Two generated plugin trees, because one `agents/*.md` cannot serve both harnesses

Both harnesses read `tools` from the fixed `<plugin-root>/agents/` path, but Claude Code expects capitalised Claude tool names while omp expects lowercase omp names and additionally needs `spawns` for the orchestrators' delegation allowlists. Claude Code's `agents` path override *supplements* `./agents` rather than replacing it, so the two harnesses cannot be pointed at different directories inside one plugin. Dropping `tools` entirely would make both harnesses inherit every tool and destroy the analysts' enforced read-only posture.

So `tools/build-plugins.py` (renamed from `tools/translate-omp.py`) materialises `plugins/claude/<plugin>/` and `plugins/omp/<plugin>/` from the one opencode-format source. Skills and commands are byte-identical across the two; only `agents/` differs. The trees are **committed**, because a marketplace install clones the repository, and `tools/build-plugins.py --check` is the drift gate.

### Claude posture is a denylist

Claude Code plugin agents get `disallowedTools`, never `tools`. An allowlist would have to enumerate Claude's whole tool vocabulary and would silently strip tools this repository never audited; a denylist expresses exactly what the opencode `permission` map encodes and nothing more. Plugin agents silently ignore `metadata`, `hooks`, `mcpServers`, and `permissionMode` for security, so the provenance omp carries in `metadata.generated` is emitted as YAML comments, along with the three postures Claude Code cannot express: the spawn allowlist, the `.acordia/reports/**` path scope, and the per-command bash denies.

### Sources do not move

`analysts/`, `operators/`, and `commands/acordia/` stay opencode-native and remain the only editable artifacts. Everything under `plugins/`, `.claude-plugin/`, and `.omp-plugin/` is generated build output.

### The installers become opencode-only

Clean cutover: `--harness`, `--autoload`, `OMP_ROOT`, `BUILD_ROOT`, the translation step, the `nested` command shape, the `CLAUDE_COMMANDS_ROOT` target, and the translated-agent branch of the ownership evidence are deleted rather than deprecated. `.gitignore` loses `.build/`, because nothing writes there any more.

## Capabilities

### New Capabilities

- `plugin-packaging` — the two-plugin split, the two generated trees and two catalogs, the generated-and-committed contract with `--check` as its gate, and the Claude `disallowedTools` mapping.

### Modified Capabilities

- `omp-harness-distribution` — the harness selector and the materialised-not-symlinked requirement are removed; the source-artifact destination becomes the committed plugin tree, and skill autoloading becomes unconditionally unset. The translation contract itself, the `list`-token check, the unmappable-permission reporting, ownership evidence, refuse-to-overwrite, `--force`, idempotence, pillar auto-discovery, and the write-capable-pillar rule all stand as written.
- `acordia-command-namespace` — the namespace shape becomes three shapes, two of them supplied by the harness from the plugin name; the deployment guarantees are scoped to the opencode install path.

## Impact

- **Renamed:** `tools/translate-omp.py` → `tools/build-plugins.py`.
- **New generated files:** `plugins/{claude,omp}/{acordia-analysts,acordia-operators}/**`, `.claude-plugin/marketplace.json`, `.omp-plugin/marketplace.json`.
- **Modified tooling:** `install.sh`, `uninstall.sh`, `tools/command-layout.sh`, `tools/ownership.sh`, `.gitignore`.
- **Modified docs:** `README.md`, `CLAUDE.md`.
- **Unchanged:** every source agent file, every skill, every command wrapper, both pillars' names and slugs, and the competency grid.
- **Capability change for Claude Code users:** the analysts' read-only posture is *enforced* there for the first time — `disallowedTools` really does subtract the tools, where omp can only remove `edit` and `task`.
