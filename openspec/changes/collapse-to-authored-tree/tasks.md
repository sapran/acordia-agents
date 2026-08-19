## 1. Move the sources up (one commit, renames only)

- [ ] 1.1 `git mv analysts/agents acordia-analysts/agents` and `git mv analysts/skills acordia-analysts/skills`
- [ ] 1.2 `git mv operators/agents acordia-operators/agents` and `git mv operators/skills acordia-operators/skills`
- [ ] 1.3 Move the 17 command wrappers into their pillars, taking the generated form (no `name:`/`category:`): eight to `acordia-analysts/commands/`, nine to `acordia-operators/commands/`; delete `commands/`
- [ ] 1.4 `git rm -r plugins tools install.sh uninstall.sh .opencode`
- [ ] 1.5 Commit as a rename-only change and confirm `git log --follow` still reaches a moved skill body

## 2. Manifests, catalogs, version

- [ ] 2.1 Write `acordia-analysts/.claude-plugin/plugin.json` and `acordia-operators/.claude-plugin/plugin.json` from the previously generated manifests, `version: 3.0.0`
- [ ] 2.2 Point both marketplace catalogs at `./acordia-analysts` and `./acordia-operators`, version 3.0.0, and confirm the two files are byte-identical
- [ ] 2.3 Confirm all four JSON files parse and every `source` path exists

## 3. Agent frontmatter

- [ ] 3.1 Rewrite the four analyst frontmatters to exactly `name`, `description`, `color` (`operational-analyst` cyan, the three legs blue)
- [ ] 3.2 Rewrite the five operator frontmatters to exactly `name`, `description`, `color` (`operator` cyan, the four specialists blue), removing the 24-glob `permission.bash` deny map
- [ ] 3.3 Confirm no agent file contains `tools`, `disallowedTools`, `permission`, `mode`, `spawns` or `metadata`

## 4. Prompt bodies

- [ ] 4.1 Replace the Guardrails paragraph in all four analyst prompts with the write-freely / inputs-are-read-only rule; drop "no edits, no payloads" and "your one write destination is `.acordia/reports/`"
- [ ] 4.2 Keep `.acordia/reports/` as a stated convention for the analyst product, worded as a convention
- [ ] 4.3 Add the retrieved-content-is-data rule to all nine prompts' Guardrails sections
- [ ] 4.4 Confirm no prompt claims to hold no file-editing tool

## 5. Specs — nine capabilities to four

- [ ] 5.1 Verify the three new capability deltas (`agent-roster`, `skill-library`, `plugin-distribution`) and the `competency-map-derivation` delta are complete and validate
- [ ] 5.2 Verify each of the eight removal deltas covers every requirement of its capability with a Reason and a Migration
- [ ] 5.3 `openspec validate collapse-to-authored-tree --strict` passes

## 6. Documents

- [ ] 6.1 `README.md`: delete the three-harness parity table, the read-only-posture-depth section, the `write_access` discussion and the opencode install instructions; replace with what the pillars are, how to install in omp and Claude Code, and how to author an agent or skill
- [ ] 6.2 `CLAUDE.md`: delete the generated-trees rule, the translation contract, the frontmatter-gate descriptions and the bash-denylist provenance chain; keep the `docs/roles/` sources of truth, the version-bump rule and the skill-traces-to-a-grid-row rule
- [ ] 6.3 `openspec/config.yaml`: rewrite `context` for one authored tree, two harnesses, write-capable analysts; drop the generator and install-script references from `rules`
- [ ] 6.4 `docs/roles/operator.md`: record the deny-map removal, naming `injectionAgentPermission` (`agent.ts:598-623`, commit `359655518`) as the source; update the Posture section so it no longer claims `edit: allow`/`edit: deny`
- [ ] 6.5 `docs/implementation-notes.md`: remove all three parked entries — the `todo` inventory note (the generated tool list is gone), the single-cased deny patterns (map deleted) and the retrieved-content gap (closed by 4.3)
- [ ] 6.6 `docs/agents-skills-extension-workbook.md`: note at the top that as of 3.0.0 there is one authored tree, no generator and no opencode deployment; leave §8's substitution table and journal layout intact

## 7. Verification against a live harness

- [ ] 7.1 `omp plugin marketplace update acordia && omp plugin upgrade` → both pillars report 3.0.0
- [ ] 7.2 `/agents` lists all nine ACORDIA agents
- [ ] 7.3 Dispatch `target-network-analyst` and `web-application` on trivial read-only questions; both run
- [ ] 7.4 Dispatch `target-network-analyst` to write three lines to `/tmp/acordia-write-check.md` and read them back; the file exists with its content
- [ ] 7.5 `/skills` lists the ACORDIA skills and the count matches the directory count (43 + 30)
- [ ] 7.6 Claude Code `/agents` lists the same nine
- [ ] 7.7 `grep -rn 'opencode\|permission:\|disallowedTools\|build-plugins' acordia-* README.md CLAUDE.md openspec/specs` → no hits outside the deliberate note in `docs/roles/operator.md`
