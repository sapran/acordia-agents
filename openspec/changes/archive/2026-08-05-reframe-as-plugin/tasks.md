## 1. Rename and reshape the generator

- [x] 1.1 `git mv tools/translate-omp.py tools/build-plugins.py`, keeping the uv script header, `TranslationError`, `split_frontmatter`, `permission_entry`, `allowed_spawns`, `write_posture`, `has_bash_denies`, `agent_color`, `deep_skills`, `iter_heading_values`, `repo_relative`, the `TOOL_DISCIPLINE_*` / `INLINE_LIST_*` rewrite constants, and `BASE_TOOLS`.
- [x] 1.2 Add the module-level identity tables: `VERSION`, `MARKETPLACE_NAME`, `OWNER`, `REPOSITORY`, and `PLUGINS` mapping each plugin name to its pillar, description, category, and keywords.
- [x] 1.3 Factor the shared parse into `read_agent()` and the shared body rewrite into `rewrite_body()`, so both emitters read the same signals and apply the same `list`-token assertion.
- [x] 1.4 Replace the CLI with two modes: a plain run that regenerates in place, and `--check` that builds to a tempdir and diffs.

## 2. Emit the omp agent tree

- [x] 2.1 Keep the `tools` allowlist derivation, `spawns`, `color`, `write_access` note, `bash_denies` note, and the `list`-token assertion exactly as they were.
- [x] 2.2 Add `metadata.generated.plugin`; keep `metadata.generated.harness: omp`.
- [x] 2.3 Leave `autoloadSkills` unset unconditionally — the `--autoload` flag is gone. Keep calling `deep_skills()` and discard the result, so a broken `(deep)` heading still fails the build.
- [x] 2.4 Output to `plugins/omp/<plugin>/agents/<stem>.md`.

## 3. Emit the Claude agent tree

- [x] 3.1 Add `translate_claude()` emitting `name`, `description`, `color`, and `disallowedTools` in that key order, omitting `disallowedTools` when the list is empty.
- [x] 3.2 Build `disallowedTools` from the mapping table: denied edit → `Edit, Write, NotebookEdit`; scoped edit → `Edit, NotebookEdit`; allowed edit → nothing; no allowed spawns → `Task`.
- [x] 3.3 Emit the provenance comment plus the three conditional unexpressible-posture notes above the frontmatter keys.
- [x] 3.4 Apply the same body rewrites and the same post-rewrite `list`-token assertion.
- [x] 3.5 Output to `plugins/claude/<plugin>/agents/<stem>.md`.

## 4. Emit skills and commands into both trees

- [x] 4.1 Copy `<pillar>/skills` verbatim into each tree, `references/` subdirectories included.
- [x] 4.2 Route each `commands/acordia/<stem>.md` to a plugin by the agent its body names, accepting both the `Dispatch the` and `Hand the work below to the` openings and raising `TranslationError` on a wrapper that matches neither or names an agent in no pillar.
- [x] 4.3 Rewrite each wrapper's frontmatter to `description` + `argument-hint`, preserving values verbatim and any trailing comment line; drop `name` and `category`; copy the body unchanged.
- [x] 4.4 Output flat to `plugins/<harness>/<plugin>/commands/<stem>.md`.

## 5. Emit the manifests and catalogs

- [x] 5.1 Write `plugins/<harness>/<plugin>/.claude-plugin/plugin.json` into both trees, identical, with no `commands`/`agents`/`skills` path keys and no `license` key (the repository ships no LICENSE file).
- [x] 5.2 Write `.claude-plugin/marketplace.json` at the repository root pointing at `./plugins/claude/…`.
- [x] 5.3 Write `.omp-plugin/marketplace.json` at the repository root, identical except for the two `source` values pointing at `./plugins/omp/…`.

## 6. Strip omp from the shell installers

- [x] 6.1 `install.sh`: delete `OMP_ROOT`, `BUILD_ROOT`, `HARNESS`, `AUTOLOAD`, `HARNESSES`, `translate_pillar()`, the `--harness` / `--autoload` parsing and validation, and the per-harness loop wrapper.
- [x] 6.2 `install.sh`: collapse `harness_root()` to `TARGET_OVERRIDE` or `$OPENCODE_ROOT`, keeping the function so `tools/command-layout.sh` still resolves. Keep `--copy`, `--dry-run`, `--pillar`, `--target`, `--force`, `--no-commands`, `--commands-target`, `preflight()`, `assert_replaceable()`, `deploy_file()`, `deploy_dir()`, and pillar auto-discovery.
- [x] 6.3 `install.sh`: update the header comment block and `usage()` to drop every omp reference.
- [x] 6.4 `uninstall.sh`: mirror all of the above, including deleting the `.build/omp/<pillar>` cleanup step.
- [x] 6.5 `tools/command-layout.sh`: delete `CLAUDE_COMMANDS_ROOT`, the omp branch, and the `nested` shape; only `flat` survives. Rewrite the header to explain that omp and Claude Code now receive commands through the plugin trees.
- [x] 6.6 `tools/ownership.sh`: delete the translated-agent evidence branch, leaving `cmp -s` as the whole agent test, and update the header comment table.
- [x] 6.7 `.gitignore`: delete the `.build/` entry and its comment. Do not add `plugins/`.

## 7. Documentation

- [x] 7.1 `README.md`: replace the Install, `/acordia` namespace, omp-harness, and harness-parity sections with the three install paths, the plugin namespace, the generated-trees contract, and the three-harness parity table.
- [x] 7.2 `CLAUDE.md`: update the intro and `## Commands` block; add a `### Generated plugin trees` contract under `## Format contracts`; rewrite the command contract so the namespace comes from the plugin name; drop the stale `--autoload` references.
- [x] 7.3 `docs/agents-skills-extension-workbook.md` §7: §7.1 records that the plugin trees carry each pillar's `skills/` verbatim; §7.2 names `tools/build-plugins.py` and the `plugins/omp/` destination and adds the `claude-plugins` provider prerequisite; §7.5 replaces the `--harness`/`--autoload`/`.build/omp` deploy block with the marketplace commands, the committed-output contract, and why `autoloadSkills` is now unconditionally unset. `CLAUDE.md` links readers here, so a stale workbook is an actively misleading instruction.
- [x] 7.4 `docs/implementation-notes.md`: update the `tools/translate-omp.py` reference, keeping the old name parenthetically since the note is dated to when the file carried it.

## 8. Verify

- [x] 8.1 `tools/build-plugins.py && tools/build-plugins.py --check` — the second call exits 0 and prints nothing.
- [x] 8.2 Shape counts: 4 and 5 agents, 43 and 30 skills, 8 and 9 commands per plugin; `diff -r` shows the two trees' skills and commands are identical.
- [x] 8.3 `plugins/claude/acordia-analysts/agents/fusion-analyst.md` carries `disallowedTools: Edit, NotebookEdit, Task`; `target-network-analyst.md` carries `disallowedTools: Edit, Write, NotebookEdit, Task`.
- [x] 8.4 omp end-to-end: `omp plugin marketplace add ./.`, `omp plugin install acordia-analysts@acordia --scope user`. The four analyst agents appear in the task tool's spawnable set, `reasoning-under-uncertainty` is available while the operator pillar's `attack-jwt` is not, `/acordia-analysts:fusion` expands its wrapper body, and a `fusion-analyst` dispatch returns. Requires the `claude-plugins` capability provider to be enabled — the plugin surfaces nothing while it sits in `disabledProviders`. Torn down afterwards.
- [x] 8.5 Claude Code: `claude plugin marketplace add ./`, `claude plugin install acordia-analysts@acordia --scope local`, then `claude plugin details acordia-analysts` reports 4 agents and 51 skill-schema components (43 skills + 8 command wrappers), confirming the YAML provenance comments above the frontmatter keys do not block agent loading. **A live session dispatch was not run** — the local Claude Code OAuth session is expired (`Failed to authenticate: OAuth session expired`). Re-run `/acordia-analysts:fusion` and a leg-analyst write-refusal check once authenticated.
- [x] 8.6 opencode: `./install.sh --dry-run` lists opencode destinations only and no `~/.omp` path; a real install resolves `operational-analyst` with the `.acordia/reports/**` exception; `./uninstall.sh` reverses it; `./install.sh --harness omp` fails as an unknown flag.
- [x] 8.7 Pillar auto-discovery still yields exactly `analysts` and `operators` — `plugins/` is not treated as a pillar.
- [x] 8.8 `openspec validate --all --strict` passes.

## 9. Follow-ups found while applying

- [x] 9.1 Add a `## MODIFIED Requirements` delta for `operator-agent-roster`'s **Prompt names its skill set**: the one-line `(deep)` shape stays normative, but because `tools/build-plugins.py` parses and fails on it, not because `--autoload deep` consumes it. Replace the `Autoload reads the deep line` scenario with a build-failure scenario.
- [x] 9.2 Make the build atomic. `main()` deleted `plugins/` before calling `build()`, so a `TranslationError` mid-build destroyed the committed tree — the artifact a marketplace install clones. Stage into a tempdir inside the repo root and swap per generated path only on success. Record the property in the `plugin-packaging` requirement and add a `A failed build leaves the committed tree intact` scenario.
- [x] 9.3 Update `openspec/config.yaml`: the project `context` still described the repo as having "no build" and only an opencode symlink installer, which this change inverts. Also corrects pre-existing drift (39-row library → 43; Operations listed as a future pillar though `operators/` shipped) and extends the `rules` to name the generator and `docs/roles/operator.md` as traceable sources.

