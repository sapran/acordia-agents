## 1. Wrappers

- [ ] 1.1 Rewrite `acordia-analysts/commands/cyber-analyst.md`: keep the frontmatter, replace the
  delegating body with a framing line, the orchestrator's prompt body verbatim from
  `agents/cyber-analyst.md`, and the `$ARGUMENTS` brief.
- [ ] 1.2 Apply the same to `acordia-analysts/commands/analyst.md`, keeping its own frontmatter and
  its alias comment.
- [ ] 1.3 Confirm no wrapper any longer says "dispatch it as a subagent" or "switch the session to".

## 2. Agent prompt

- [ ] 2.1 Add the refusal instruction to `acordia-analysts/agents/cyber-analyst.md`: an orchestrator
  that cannot dispatch stops, says it was entered by the wrong route, and names the command wrapper.
- [ ] 2.2 Verify no `·`-separated skill line changed, so `skill-sets.json` needs no edit.

## 3. Drift gate

- [ ] 3.1 Add a fifth invariant to `~/ai/checks/check-acordia.sh`: the orchestrator body appears
  byte-identically in both wrappers and the agent file; failure names the diverging file.
- [ ] 3.2 Negative-test it — induce drift in one wrapper, confirm the gate fails naming that file,
  restore, confirm it passes.

## 4. Version

- [ ] 4.1 Bump `6.4.0` → `6.5.0` in all three manifests:
  `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.omp-plugin/marketplace.json`.

## 5. Verify

- [ ] 5.1 `~/ai/checks/check-acordia.sh .worktrees/lead-in-main` passes.
- [ ] 5.2 `openspec validate --all --strict` passes.
- [ ] 5.3 Install the worktree and invoke `/acordia-analysts:cyber-analyst` in a live session; confirm
  the session holds the orchestrator doctrine **and** can dispatch a leg. Evidence: the leg's own
  session-init prompt on disk carries `You are the **collection analyst**`.
- [ ] 5.4 Dispatch `cyber-analyst` as a subagent and confirm it refuses and names the wrapper.

## 6. Land

- [ ] 6.1 `openspec archive 2026-09-02-lead-runs-in-main-session --yes`, re-validate.
- [ ] 6.2 Review with `reviewer` and `security-reviewer`; fix or dismiss each finding.
- [ ] 6.3 Merge to `develop`, then fast-forward `main` so installs reach it.
- [ ] 6.4 Remove the worktree and delete the branch.
