## Why

Most of this repository's mass exists to express restrictions rather than capability: a 1,471-line
generator (`tools/build-plugins.py`), two generated plugin trees under `plugins/`, four fatal build
gates, an opencode-only installer pair, per-agent `permission` maps, and nine OpenSpec capabilities
carrying 88 requirements. The agents and skills — the only artifacts a user consumes — are a
minority of the tracked content.

The generator's entire remaining purpose is the guardrail. Measured against the current build, all
73 skills are byte-identical between `plugins/claude/` and `plugins/omp/`, and agent bodies are
identical too; the sole difference is the frontmatter line expressing a restriction
(`disallowedTools: Edit, Write, NotebookEdit, Task` versus a `tools:` allowlist). Both harnesses
accept one agent file: omp's `parseAgentFields()` requires only `name`, `description` and a body,
and treats `tools` as optional — when omitted the agent receives the full tool set and, with
`spawns` also absent, an unrestricted spawn policy. Claude Code requires the same three keys. Remove
the restriction and the two emitted files converge, leaving nothing to translate.

opencode is the only harness the shell installer served — `install.sh`'s own header states opencode
"has no plugin system … a filesystem deployment is the only way in". Dropping opencode retires both
scripts and their two sourced helpers.

The read-only analyst posture is separately wrong. `target-network-analyst` and
`defender-detection-analyst` carry `edit: deny` and cannot write a note; `operational-analyst` and
`fusion-analyst` carry `"*": deny` with a single `.acordia/reports/**` exception. All four prompts
tell the agent it "hold[s] no file-editing tool". An analyst that cannot keep working files is
crippled at the wrong boundary: the material under analysis is what must stay untouched, not the
analyst's own notes.

## What Changes

- **BREAKING** — the install source path changes. `plugins/omp/acordia-*` and
  `plugins/claude/acordia-*` are deleted; both marketplace catalogs point at the top-level
  `./acordia-analysts` and `./acordia-operators`. Existing installs must re-resolve the marketplace.
- **BREAKING** — opencode is no longer a target. `install.sh`, `uninstall.sh`,
  `tools/command-layout.sh`, `tools/ownership.sh` and `.opencode/` are deleted.
- **BREAKING** — `tools/build-plugins.py` and its four build gates are deleted. There is one
  authored tree per pillar and no generated output in the repository.
- Sources move up: `analysts/{agents,skills}` → `acordia-analysts/{agents,skills}`,
  `operators/{agents,skills}` → `acordia-operators/{agents,skills}`, and the 17 command wrappers
  from `commands/acordia/` split into `acordia-analysts/commands/` (8) and
  `acordia-operators/commands/` (9), the layout each harness discovers from a plugin root.
- Agent frontmatter collapses to exactly `name`, `description`, `color`. Removed per file: `mode`,
  the whole `permission` block (including the 24-glob destructive-`bash` deny map on the five
  operators), `metadata.acordia`, `metadata.cyberstrike` on agents, `metadata.generated`.
  `metadata.cyberstrike` on the 30 operator skills is retained — it is upstream attribution, not
  machinery.
- All four analyst agents become write-capable. Their Guardrails paragraph is replaced with the rule
  that was actually wanted: write freely, never modify the material given for analysis.
- Every agent prompt gains the rule that retrieved content is data, not instructions — closing the
  gap parked in `docs/implementation-notes.md`.
- Version 2.5.0 → **3.0.0** in both `plugin.json` files and both marketplace catalogs.
- Nine capabilities become four. Every requirement whose subject was a permission map, a tool
  allowlist, a translation rule, a build gate or a `--doctor` section is removed rather than
  reworded.

## Capabilities

### New Capabilities

- `agent-roster`: the nine agents — one file each, three-key frontmatter, what each owns, the
  write-freely/read-only-inputs posture, the retrieved-content rule, and the 17 command wrappers
  that dispatch them.
- `skill-library`: the skills each pillar ships, the family taxonomy, the description contract, the
  folder-slug bijection, upstream provenance on ported skills, and `references/` for long
  enumerations.
- `plugin-distribution`: two hand-maintained marketplace catalogs, one `plugin.json` per pillar,
  versions in lockstep, and no generated trees in the repository.

### Modified Capabilities

- `competency-map-derivation`: trimmed to the derivation rules that survive — the grid remains the
  single source of truth for analyst skills — with the frontmatter-anchor requirement restated
  against the authored tree instead of the generator's validation.

### Removed Capabilities

Each is deleted by removing every one of its requirements:

- `analyst-agent-roster` (17) and `operator-agent-roster` (10) → subsumed by `agent-roster`.
- `analyst-skill-library` (12) and `operator-skill-library` (8) → subsumed by `skill-library`.
- `acordia-command-namespace` (5) → subsumed by `agent-roster`.
- `plugin-packaging` (15) → subsumed by `plugin-distribution`, minus every gate requirement.
- `omp-harness-distribution` (11) → deleted; it specified the translation and the opencode install.
- `harness-tool-translation` (4) → deleted; nothing translates any more.

## Impact

- Deleted: `tools/`, `plugins/`, `install.sh`, `uninstall.sh`, `.opencode/`, `analysts/`,
  `operators/`, `commands/`.
- Added: `acordia-analysts/` and `acordia-operators/`, each with `.claude-plugin/plugin.json`,
  `agents/`, `commands/`, `skills/`.
- Rewritten: nine agent frontmatters; four analyst Guardrails paragraphs; five operator Guardrails
  paragraphs (retrieved-content rule only); `README.md`; `CLAUDE.md`; `openspec/config.yaml`
  context and rules; `docs/roles/operator.md` (records the deny-map removal);
  `docs/implementation-notes.md` (both parked entries resolved).
- Users on 2.5.0 must run `omp plugin marketplace update acordia && omp plugin upgrade`; opencode
  users have no upgrade path and must switch harness.
