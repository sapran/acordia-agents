## 1. Translator

- [x] 1.1 Create `tools/translate-omp.py` as a `uv` PEP 723 script declaring `pyyaml`, taking one or more source agent paths, an output directory, and the `--autoload deep` opt-in
- [x] 1.2 Implement frontmatter parsing and the `name` / `description` emission, failing non-zero on a source file missing either
- [x] 1.3 Implement the permission-to-`tools` mapping, including `mode: primary` → `task` plus an explicit `spawns` list and `mode: subagent` → no `task`, failing non-zero on an unrecognised `mode`
- [x] 1.4 Record the real write posture in the generated frontmatter: omp cannot deny `write` while `tools.xdev` is on, so state that rather than implying the allowlist enforces it
- [x] 1.5 Implement `metadata` pass-through plus generated-file provenance naming the source path
- [x] 1.6 Implement the Tool-discipline paragraph rewrite by exact-string match, failing non-zero when the paragraph is absent
- [x] 1.7 Implement `--autoload deep`, extracting skill names from the source prompt's `(deep)` heading line

## 2. Install and uninstall

- [x] 2.1 Add `--harness opencode|omp|both` to `install.sh`, defaulting to `opencode`, rejecting other values with a non-zero exit
- [x] 2.2 Add the omp deploy path: translate each pillar's agents into `.build/omp/<pillar>/agents/` and copy them to `~/.omp/agent/agents/`
- [x] 2.3 Deploy pillar skills to `~/.omp/agent/skills/`, honouring `--link` / `--copy`
- [x] 2.4 Force copy mode for translated agents even under `--link`, and print the notice explaining why
- [x] 2.5 Make the omp path respect `--dry-run`, including running no translation that writes to disk
- [x] 2.6 Add the matching `--harness` selector to `uninstall.sh`, removing only the agent names and skill slugs this repository owns
- [x] 2.7 Add `.build/` to `.gitignore`

## 3. Verification

- [x] 3.1 Run `./install.sh --harness omp --dry-run` and confirm no filesystem change
- [x] 3.2 Run `./install.sh --harness omp` and confirm four regular files under `~/.omp/agent/agents/` and every pillar skill under `~/.omp/agent/skills/`
- [x] 3.3 Confirm omp discovers all four analysts by name and that each carries the expected tool allowlist
- [x] 3.4 Confirm the orchestrator's `spawns` resolves to the three legs and that a leg cannot dispatch
- [x] 3.5 Re-run the install and confirm idempotence; then run `./uninstall.sh --harness omp` and confirm only repository-owned entries were removed
- [x] 3.6 Confirm `./install.sh` with no arguments still produces exactly the previous opencode deployment

## 4. Documentation

- [x] 4.1 Add the omp install path and the harness selector to `README.md`
- [x] 4.2 Document the two parity gaps in `README.md`: no path-scoped write permission, and `bash` as a write channel in both harnesses
- [x] 4.3 Add the opencode-to-omp frontmatter mapping table to `docs/agents-skills-extension-workbook.md`
- [x] 4.4 State in `README.md` that translated agents are build output and that editing them is a drift bug
