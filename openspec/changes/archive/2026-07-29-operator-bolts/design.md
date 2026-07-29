## Context

The Operations pillar was ported from the CyberStrike fork at commit `359655518`, which carries Bolt — remote tool servers paired over MCP with Ed25519 keypairs, managed from CyberStrike's own TUI (`bolt add`, `Ctrl+D` to delete, live status in the sidebar). None of that came across, because all of it is application code and this repository ships markdown only. What did come across is twenty-six technique skills that emit traffic and say nothing about its origin.

Constraints that shape the design:

- **Markdown only.** `openspec/specs/operator-skill-library/spec.md` already forbids vendoring executables ("Attack scripts are not vendored — the repository remains markdown-only"). A `bolt` helper script in the skill directory would break that, and `install.sh` symlinks skill directories without knowing how to put a script on `PATH`.
- **No pairing protocol is available.** Bolt's Ed25519 handshake needs a server process on the remote host and a client that speaks it. Neither exists here.
- **No per-tool host binding exists in either harness.** opencode's permission map and omp's settings both gate *whether* a tool runs, never *where*. So the posture can only be a discipline stated in a prompt.
- **The operator journal convention already exists.** Operator prompts record state under `.acordia/ops/` (`scope.md`, `intel.md`, `coverage.md`, `findings/`, `reports/`), named in prose rather than as a permission scope.

## Goals / Non-Goals

**Goals:**

- State, once and in one place, which classes of tooling must execute on a remote host and which stay local.
- Give the operator a way to know a bolt's network position and public egress address *before* the first packet, since that address is what the target records.
- Make long scans survive the SSH connection that started them, and make their artifacts recoverable without re-scanning.
- Keep provenance honest: record that the concept is CyberStrike's Bolt while the mechanism here is not.

**Non-Goals:**

- Enforcement. Nothing prevents an agent from running `nmap` locally; the change buys discipline and a stated default, not a sandbox.
- Reimplementing Bolt's pairing, streaming, or multi-server fan-out.
- Routing the harness's own traffic — model API calls, documentation fetches, web search — through a bolt. Only tooling aimed at a target moves.
- Provisioning. Installing a toolkit on a fresh host is the operator's job, not the skill's.

## Decisions

**SSH, not a Bolt server.** A bolt is a name in a registry resolving to an SSH destination. *Alternative considered:* port Bolt's HTTP/MCP protocol — rejected, it needs a daemon this repository cannot ship and a keypair store it cannot manage. SSH is already authenticated in the operator's environment, already gives streamed stdout, and already carries files via `scp`. The cost is losing Bolt's live status sidebar; `bolt status` as a documented command covers the same ground on demand.

**Command patterns in prose, not a helper script.** The skill body documents the exact invocations — a run directory per execution, `setsid nohup` for detached scans, `tail` to poll, `scp` to retrieve. *Alternative considered:* ship a `bolt.sh` wrapper — rejected on the markdown-only contract above. The trade-off is verbosity at the call site, mitigated by making each pattern a single copy-paste line. Operators who want the ergonomics can keep a private wrapper outside this repository; the skill deliberately does not depend on one existing.

**Commands cross the SSH hop base64-encoded.** A scan command routinely contains quotes, pipes and `$`, and passing it through `ssh host "…"` mangles it — the failure is silent and produces files named after the flags. Encoding the command locally and decoding it on the bolt makes quoting survive verbatim. This is the one non-obvious mechanic in the body, so it is stated as a rule rather than left to the reader.

**Registry at `.acordia/bolts.json`, engagement-scoped.** *Alternatives considered:* a user-level file (`~/.claude/bolts.json` or similar) — rejected, it is harness-specific and leaks between engagements; hardcoding hosts in the skill — rejected, hosts are per-engagement facts, and a skill body carrying a real address is a provenance leak. `.acordia/` already holds the operation journal, so the registry sits with the rest of the operation's state and is naturally scoped to it.

**Working knowledge on all five agents, deep on none.** The posture applies whenever any operator emits traffic, which makes it cross-cutting rather than a specialist depth. Putting it in a `## Your specialist depth (deep)` line would add it to `autoloadSkills` for that agent and pay the body's prompt cost in every session, including sessions with no remote host at all. *Alternative considered:* deep on `internal-network`, whose work is most position-dependent — rejected as arbitrary: a cloud assessment from the wrong egress IP is exactly as wrong.

**Slug `bolts`, not `remote-tool-execution`.** The name is the provenance. Skills are selected by description match rather than slug, so the descriptive weight belongs in the `description` field, which states the when-clause; the slug can stay short and carry the lineage.

**Locally-authored provenance is a positive statement, not an absent field.** The existing spec requires `metadata.cyberstrike` on every skill. Rather than weakening that to "where applicable", the delta splits it: cloned skills record the source path and commit; a locally-authored skill records `metadata.acordia.authored` with the change that introduced it. An empty `metadata` block would be indistinguishable from an oversight.

## Risks / Trade-offs

- **Stated discipline, not enforcement** → The skill body opens by saying so plainly, so the agent does not mistake it for a guarantee. The counterpart is that violating it is visible: `bolt status` shows the egress address, and a finding whose evidence came from the wrong source address is self-evident on review.
- **A thirty-first skill costs prompt budget in every operator session** → Bounded and known: both harnesses list every skill's name and description in the system prompt, so the cost is one description, not one body. The library cap in `docs/roles/operator.md` exists to keep exactly this decision deliberate, which is why the change updates that record rather than quietly adding a directory.
- **The registry can go stale** — a bolt's address or toolkit changes and the recorded position becomes a lie → The skill makes `bolt status`-style verification a precondition of use rather than a setup step, so the registry is checked against reality at the start of each engagement, not trusted from the last one.
- **Artifacts left only on the bolt are lost when it is rebuilt** → The body treats a bolt as disposable and requires pulling artifacts into the engagement directory as each run completes.
- **Without a wrapper, a mistyped remote command is easy** → The run-directory convention makes every execution self-documenting: `cmd.sh` records exactly what ran next to the `output.txt` it produced, so a bad invocation is diagnosable after the fact.

## Migration Plan

Additive; nothing to migrate. `install.sh` and `uninstall.sh` walk skill directories, so the new skill deploys and removes with no code change. Rollback is deleting `operators/skills/bolts/`, reverting five one-line prompt edits and the provenance record — no state, no dependency, nothing else references it.

## Open Questions

None blocking. If further pillars gain their own remote-execution needs, the registry format is the piece to promote out of this skill into a shared convention; that is a decision for whichever change introduces the second consumer.
