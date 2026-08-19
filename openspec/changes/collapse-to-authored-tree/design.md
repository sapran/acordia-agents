## Context

See proposal.md — Why. Constraints that shape the approach, all measured against the current build:

- omp's `parseAgentFields()` requires `name` and `description` only; `tools` is optional and, when
  omitted, the agent receives the full tool set. `spawns` absent means "allow any"
  (`omp://task-agent-discovery.md`: `"*"` also `true`, `null`, or absent). So an unrestricted agent is
  expressed by writing nothing, not by writing an allowlist.
- omp discovers Claude-format plugin roots (`listClaudePluginRoots`), scanning `<pluginRoot>/agents/`
  and `<pluginRoot>/commands/*.md` — the latter non-recursively, namespaced by plugin name. That is
  how ACORDIA loads in omp today, and it is why command wrappers must live inside a pillar rather than
  at the repository root.
- omp reads `.omp-plugin/marketplace.json` in preference to `.claude-plugin/marketplace.json`;
  Claude Code reads the latter. The installed omp cache confirms it resolved the `.omp-plugin/` copy
  (`~/.omp/plugins/cache/marketplaces/acordia/marketplace.json` carries
  `source: ./plugins/omp/acordia-analysts`).
- The two generated trees differ in nothing but the restriction line: all 73 skills byte-identical,
  agent bodies identical, `disallowedTools: …` versus `tools: […]`.
- `install.sh`/`uninstall.sh` serve opencode only, and both source `tools/ownership.sh` and
  `tools/command-layout.sh`, which have no other caller.

## Goals / Non-Goals

**Goals:**

- One authored tree per pillar that both harnesses load without a build step.
- Every agent holds the full tool set; capability is granted by omission.
- Analysts write their own notes and products; the material under analysis stays untouched.
- Nine capabilities reduced to four that describe agents and skills rather than restrictions.
- History follows the moved files.

**Non-Goals:**

- Prompt slimming, new skills, description rewrites, and the WSTG de-duplication. Those are changes 2
  and 3; this change moves files and frontmatter only.
- Any replacement for the deleted gates. Verification becomes "it loads and runs", plus two shell
  one-liners recorded in this change.
- Reintroducing a restriction under another name. If an agent turns out to need something, the fix is
  a capability, never a denylist.

## Decisions

**One tree, not two, and no generator.** The translator's only remaining output difference was the
restriction line; removing the restriction converges the two files, so the 1,471-line generator has
nothing left to do. Alternative considered: keep the generator and emit one tree from itself — rejected
because a generator whose output equals its input is pure ceremony, and it carried four fatal gates
whose failure modes are worse than the drift they prevent.

**Sources move up into the plugin directories rather than staying under `analysts/`/`operators/` with a
manifest added.** The plugin root must contain `agents/`, `commands/`, `skills/` and
`.claude-plugin/plugin.json`; naming the directory after the plugin (`acordia-analysts`) makes the
catalog `source` a bare `./acordia-analysts` and removes the last indirection. Alternative: keep the
short directory names and point the catalog at `./analysts` — rejected because the plugin name and the
directory name would differ, which is the kind of mismatch that produces a silently skipped plugin.

**Move first, edit second, in two commits.** `git mv` records a rename only when content is
substantially unchanged; frontmatter rewriting in the same commit would show as delete+add and lose
blame for 73 skill bodies. So: commit 1 is pure moves and deletions, commit 2 rewrites frontmatter.

**Commands split by the pillar of the agent they dispatch, adopting the generated form.** The generated
wrappers already dropped the opencode-only `name:` and `category:` keys and are what works in omp
today; the root `commands/acordia/` sources carry those two extra keys and a namespace
(`ACORDIA: fusion`) that no longer applies, since both harnesses namespace by plugin name. Take the
generated 8/9 split as the authored form.

**Both marketplace files stay, hand-maintained and byte-identical.** omp reads one, Claude Code the
other; after the move both carry the same two sources, so they are 30-line twins whose drift is visible
in a diff. Alternative: keep only `.claude-plugin/` and rely on omp's fallback — rejected because omp
prefers `.omp-plugin/` and a repository that ships only the fallback invites a future reader to
"restore" the preferred path with a stale copy.

**`metadata.cyberstrike` stays on the 30 operator skills; `metadata.acordia` leaves the nine agents.**
The first is upstream attribution for ported text — deleting it would make a re-port an archaeology
exercise. The second existed so a generator could read provenance pillar-blind; with the generator
gone, the reader is a person and `docs/roles/*.md` is where they look.

**The deny map is deleted, and its deletion is recorded in `docs/roles/operator.md`.** It was enforced
only by opencode; under omp and Claude Code it was already inert, and each generated file said so. But
the operator pillar is a provenance-tracked port, so a documented element disappearing without the
record changing is exactly the drift `CLAUDE.md` warns about. The record names
`injectionAgentPermission` (CyberStrike `agent.ts:598-623`, commit `359655518`) as the source should it
ever be wanted back.

**Requirements whose mechanism is deleted are removed, not reworded.** 82 of 88 requirements are
removed across eight capabilities; each removal carries a Reason and a Migration naming where the
surviving behaviour is specified. A requirement with no mechanism behind it is worse than no
requirement, because it reads as a live guarantee.

**The two parked entries in `docs/implementation-notes.md` are resolved here.** The single-cased deny
patterns are moot with the map gone. The "retrieved content is data, not instructions" gap is closed by
adding the rule to all nine prompts — the analysts because they read target-controlled material by
design, the operators because they read attacker-influenced responses all day.

## Risks / Trade-offs

- **A frontmatter mistake makes an agent vanish silently** → `discoverAgents()` skips an unparseable
  file with a warning. Verification step 2 is `/agents` listing all nine, and steps 3–4 dispatch one
  agent per pillar; a missing agent is caught there rather than by a build gate.
- **Existing 2.5.0 installs break** → the catalog `source` paths change, so an upgrade must re-resolve
  the marketplace. Recorded as BREAKING in the proposal, and the MAJOR bump is the signal.
- **No gate means drift can reappear** → accepted deliberately. The two remaining invariants that had
  gates (every named skill slug resolves; both catalogs agree) are cheap to check by hand, and the two
  one-liners are recorded in the change's verification section.
- **Omitting `tools` grants more than the old allowlist, including `task` to every agent** → the spawn
  policy defaults to unrestricted, so a specialist could in principle dispatch another agent. Accepted:
  leaf behaviour is prompt discipline now, and the alternative is a `spawns` key, which is the
  restriction frontmatter this change exists to remove.
- **opencode users lose their install path** → they have no upgrade; they must switch harness. Stated in
  the proposal as BREAKING.

## Migration Plan

1. Commit 1 — `git mv` the four source directories and the 17 wrappers into the two pillar
   directories; `git rm` `plugins/`, `tools/`, `install.sh`, `uninstall.sh`, `.opencode/`.
2. Commit 2 — write the two `plugin.json` files at 3.0.0, rewrite the nine frontmatters, replace the
   four analyst Guardrails paragraphs, add the retrieved-content rule to all nine prompts, update both
   catalogs.
3. Commit 3 — specs, `README.md`, `CLAUDE.md`, `openspec/config.yaml`, `docs/roles/operator.md`,
   `docs/implementation-notes.md`.
4. Verify against a live harness: `omp plugin marketplace update acordia && omp plugin upgrade`, then
   `/agents`, then a dispatch per pillar, then the analyst write proof.

Rollback is `git revert` of the three commits plus `omp plugin marketplace update acordia`; nothing
outside the repository holds state.
