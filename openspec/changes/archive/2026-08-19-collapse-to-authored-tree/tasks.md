## 1. Move the sources up (one commit, renames only)

- [x] 1.1 `git mv analysts/agents acordia-analysts/agents` and `git mv analysts/skills acordia-analysts/skills`
- [x] 1.2 `git mv operators/agents acordia-operators/agents` and `git mv operators/skills acordia-operators/skills`
- [x] 1.3 Move the 17 command wrappers into their pillars, taking the generated form (no `name:`/`category:`): eight to `acordia-analysts/commands/`, nine to `acordia-operators/commands/`; delete `commands/`
- [x] 1.4 `git rm -r plugins tools install.sh uninstall.sh .opencode`
- [x] 1.5 Commit as a rename-only change and confirm `git log --follow` still reaches a moved skill body

## 2. Manifests, catalogs, version

- [x] 2.1 Write `acordia-analysts/.claude-plugin/plugin.json` and `acordia-operators/.claude-plugin/plugin.json` from the previously generated manifests, `version: 3.0.0`
- [x] 2.2 Point both marketplace catalogs at `./acordia-analysts` and `./acordia-operators`, version 3.0.0, and confirm the two files are byte-identical
- [x] 2.3 Confirm all four JSON files parse and every `source` path exists

## 3. Agent frontmatter

- [x] 3.1 Rewrite the four analyst frontmatters to exactly `name`, `description`, `color` (`operational-analyst` cyan, the three legs blue)
- [x] 3.2 Rewrite the five operator frontmatters to exactly `name`, `description`, `color` (`operator` cyan, the four specialists blue), removing the 24-glob `permission.bash` deny map
- [x] 3.3 Confirm no agent file contains `tools`, `disallowedTools`, `permission`, `mode`, `spawns` or `metadata`

## 4. Prompt bodies

- [x] 4.1 Replace the Guardrails paragraph in all four analyst prompts with the write-freely / inputs-are-read-only rule; drop "no edits, no payloads" and "your one write destination is `.acordia/reports/`"
- [x] 4.2 Keep `.acordia/reports/` as a stated convention for the analyst product, worded as a convention
- [x] 4.3 Add the retrieved-content-is-data rule to all nine prompts' Guardrails sections
- [x] 4.4 Confirm no prompt claims to hold no file-editing tool

## 5. Specs — nine capabilities to four

- [x] 5.1 Verify the three new capability deltas (`agent-roster`, `skill-library`, `plugin-distribution`) and the `competency-map-derivation` delta are complete and validate
- [x] 5.2 Verify each of the eight removal deltas covers every requirement of its capability with a Reason and a Migration
- [x] 5.3 `openspec validate collapse-to-authored-tree --strict` passes

## 6. Documents

- [x] 6.1 `README.md`: delete the three-harness parity table, the read-only-posture-depth section, the `write_access` discussion and the opencode install instructions; replace with what the pillars are, how to install in omp and Claude Code, and how to author an agent or skill
- [x] 6.2 `CLAUDE.md`: delete the generated-trees rule, the translation contract, the frontmatter-gate descriptions and the bash-denylist provenance chain; keep the `docs/roles/` sources of truth, the version-bump rule and the skill-traces-to-a-grid-row rule
- [x] 6.3 `openspec/config.yaml`: rewrite `context` for one authored tree, two harnesses, write-capable analysts; drop the generator and install-script references from `rules`
- [x] 6.4 `docs/roles/operator.md`: record the deny-map removal, naming `injectionAgentPermission` (`agent.ts:598-623`, commit `359655518`) as the source; update the Posture section so it no longer claims `edit: allow`/`edit: deny`
- [x] 6.5 `docs/implementation-notes.md`: remove all three parked entries — the `todo` inventory note (the generated tool list is gone), the single-cased deny patterns (map deleted) and the retrieved-content gap (closed by 4.3)
- [x] 6.6 `docs/agents-skills-extension-workbook.md`: note at the top that as of 3.0.0 there is one authored tree, no generator and no opencode deployment; leave §8's substitution table and journal layout intact

## 7. Verification against a live harness

- [x] 7.1 Installed both pillars from this checkout through an isolated marketplace (`acordia-verify`, project scope, user-scope 2.4.0 masked by `.omp/plugin-overrides.json`) rather than repointing the user's real `acordia` marketplace: both report 3.0.0
- [x] 7.2 A live omp session lists all nine ACORDIA agents on its task tool
- [x] 7.3 Dispatch `target-network-analyst` and `web-application` on trivial read-only questions; both run
- [x] 7.4 Dispatch `target-network-analyst` to write three lines to `/tmp/acordia-write-check.md` and read them back; the file exists with its content
- [x] 7.5 A live session reads `skill://ebpf-attacks` and enumerates exactly the 16 `attack-*` skills, so the libraries resolve with no duplicates from the masked user-scope copy
- [x] 7.6 Claude Code installs the same tree at 3.0.0 in an isolated `HOME`: four analyst agents with three-key frontmatter and 43 skills land in its plugin cache from `.claude-plugin/marketplace.json` (an interactive `/agents` listing was not run — it would have required mutating the real `~/.claude`)
- [x] 7.7 `grep -rn 'opencode\|permission:\|disallowedTools\|build-plugins' acordia-* README.md CLAUDE.md openspec/specs` → no hits outside the deliberate note in `docs/roles/operator.md`
