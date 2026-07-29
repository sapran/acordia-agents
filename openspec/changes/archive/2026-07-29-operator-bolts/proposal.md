## Why

Every operator skill assumes its tooling runs *somewhere*, and none of them says where. In practice the agent runs `nmap`, `ffuf`, `netexec` and friends on whatever host the harness happens to sit on — usually the operator's own laptop, which is the one machine whose address should never appear in a target's logs. CyberStrike solved this with **Bolt**: named remote tool servers, deployed on hosts chosen for their toolkit and network position, driven from the local client. The Operations pillar was ported from that fork without the concept, so the port is missing the piece that decides *where the packets come from*.

The gap is not theoretical: the twenty-six technique skills all emit traffic, and an operator following them today has no stated discipline for keeping that traffic off the local machine, no convention for where remote artifacts live, and no way to record which host holds which network position.

## What Changes

**Skill body layer**

- Add a thirty-first operator skill, `operators/skills/bolts/SKILL.md`, defining remote tool execution as an operating posture: what must run on a bolt, what stays local, how a bolt is selected and verified, how long-running scans survive a dropped connection, and how artifacts come back.
- The skill is **locally authored**, not cloned — the first operator skill with no CyberStrike source. It carries the concept from CyberStrike's Bolt servers but none of its code: SSH replaces the Ed25519/MCP pairing protocol, because the harness already has SSH keys and this repository ships no runtime that could pair.
- Markdown-only, like every other skill here: the body documents command patterns the agent runs through `bash`. No helper script, no registry implementation, nothing executable is vendored.

**Agent prompt layer**

- Name `bolts` in the `## Working knowledge (draw on as needed)` line of all five operator agents. It is a cross-cutting execution posture rather than a domain depth, so it does not enter any agent's `## Your specialist depth (deep)` line and therefore does not grow omp's `autoloadSkills`.

**Docs layer**

- Update the provenance record in `docs/roles/operator.md`: library membership 30 → 31, with `bolts` recorded as locally authored and the CyberStrike Bolt concept named as its ancestor.

**Not in scope**

- No new pillar, agent, or permission change. Operators already hold `edit: allow` and `bash: allow`, which is everything the posture needs.
- No enforcement mechanism. This is a discipline stated in a prompt, not a sandbox: neither opencode nor omp can bind a tool call to a remote host.

## Capabilities

### New Capabilities

(none — this extends two existing capabilities)

### Modified Capabilities

- `operator-skill-library`: library membership becomes thirty-one; the provenance requirement, which today mandates a `metadata.cyberstrike` block on every skill, must admit locally-authored skills and say what they record instead.
- `operator-agent-roster`: a new requirement that every operator prompt names the remote-execution posture in its working-knowledge line, so the discipline reaches all five agents rather than sitting in a library nobody references.

## Impact

- `operators/skills/bolts/SKILL.md` — new file.
- `operators/agents/{operator,web-application,mobile-application,cloud-security,internal-network}.md` — one line each, inside `## Working knowledge`; no frontmatter or permission block touched.
- `docs/roles/operator.md` — provenance record.
- `openspec/specs/{operator-skill-library,operator-agent-roster}/spec.md` — via delta specs at archive time.
- `install.sh` / `uninstall.sh` — unchanged: both walk the skill directories, so a thirty-first directory deploys with no code change. `tools/translate-omp.py --autoload deep` is unaffected because no deep line changes.
- Runtime cost: one more skill name and description in every operator session's prompt.
