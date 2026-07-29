## 1. Skill body

- [ ] 1.1 Create `operators/skills/bolts/SKILL.md` with frontmatter (`name: bolts`, triggering `description`, `metadata.acordia.authored` and `metadata.acordia.ancestor`) and body covering: posture split (what runs remotely vs locally), bolt verification (status, egress), command transport (base64 over SSH), detached long-running scans (`setsid nohup`), output polling and artifact retrieval, registry at `.acordia/bolts.json`.
- [ ] 1.2 Verify the directory contains only `SKILL.md` — no helper script, no other file.

## 2. Agent prompts

- [ ] 2.1 Append ` · bolts` to the `## Working knowledge (draw on as needed)` line in `operators/agents/operator.md`.
- [ ] 2.2 Append ` · bolts` to the same line in `operators/agents/web-application.md`.
- [ ] 2.3 Append ` · bolts` to the same line in `operators/agents/mobile-application.md`.
- [ ] 2.4 Append ` · bolts` to the same line in `operators/agents/cloud-security.md`.
- [ ] 2.5 Append ` · bolts` to the same line in `operators/agents/internal-network.md`.
- [ ] 2.6 Verify no agent's `## Your specialist depth (deep)` line mentions `bolts`.

## 3. Provenance record

- [ ] 3.1 Update `docs/roles/operator.md`: library membership 30 → 31, record `bolts` as locally authored with CyberStrike Bolt as ancestor, noting the change name.

## 4. Validation

- [ ] 4.1 Run `openspec validate --all --strict` — must pass.
- [ ] 4.2 Run `./install.sh --dry-run` — the thirty-first skill directory must appear in the plan with no errors.
- [ ] 4.3 Run `tools/translate-omp.py --autoload deep` on each operator agent — `bolts` must NOT appear in any `autoloadSkills` output (it is working knowledge, not deep).
