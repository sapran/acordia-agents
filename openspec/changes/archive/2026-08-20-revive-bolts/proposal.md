# Revive the bolts skill against the current tree

## Why

Every operations skill assumes its tooling runs *somewhere*, and none of them says where. In practice
the agent runs `nmap`, `ffuf`, `netexec` and the rest on whatever host the harness sits on — usually
the operator's own laptop, which is the one machine whose address should never appear in a target's
logs. All 31 cloned technique skills emit traffic, and not one states a discipline for keeping that
traffic off the local machine, a convention for where remote artifacts live, or a way to record which
host holds which network position.

CyberStrike solved this with **Bolt**: named remote tool servers, chosen for their toolkit and network
position, driven from a local client. The Operations pillar was ported from that fork without the
concept, so the port is missing the piece that decides *where the packets come from*.

The skill was written for this in July on `feat/operator-bolts` and never merged — the branch targeted
the flat `operators/` layout and the `operator-skill-library` / `operator-agent-roster` spec names, all
of which were demolished by the 3.0.0 relayout. The prose survived that change intact; only its
frontmatter, its placement and its spec deltas did not. This change lands the skill against the tree as
it stands.

## What Changes

**Skill layer**

- Add `acordia-operators/skills/bolts/SKILL.md`, the fortieth operations skill and the ninth authored
  here rather than cloned. Body carried over unchanged from the July branch: what must run on a bolt
  and what stays local, the registry at `.acordia/bolts.json`, verifying a bolt before first use,
  surviving a dropped connection, and how artifacts come back.
- Frontmatter rewritten for the current contract. The original opened its description with
  `Use when …`, which `skill-library` now prohibits as selection boilerplate, and carried
  `metadata.acordia.authored` / `.ancestor` keys that predate the family taxonomy. It now leads with
  the imperative and declares `family: operations-discipline`, the second member of that family.
- It carries no `metadata.cyberstrike`: the concept descends from CyberStrike's Bolt servers but none
  of its code does, and claiming upstream attribution for local text would corrupt the port record.

**Prompt layer**

- Name `bolts` in the working-knowledge line of all five operations agents. It is a cross-cutting
  execution posture rather than a domain depth, so it enters no agent's specialist-depth line and does
  not grow omp's `autoloadSkills`.

**Counts and provenance**

- Operations library 39 → 40 and total 81 → 82, in both catalogs, `acordia-operators`'s manifest,
  `README.md`, `CLAUDE.md`, `openspec/config.yaml` and the family scenario.
- `docs/roles/operator.md` records `bolts` as the ninth authored skill and names its ancestor.
- The authored-skills sentence in `skill-library` said "Seven exist as of 3.1.0" and was already stale
  by one before this change: `linux-postexploit` was authored afterwards and has carried its own
  requirement since. It now reads nine, enumerated.
- 4.0.0 → 4.1.0. MINOR, because this adds an artefact a user receives without changing the roster,
  the pillars, or the shape of the distribution.

## Impact

- No agent, pillar, wrapper or permission is added or changed; five prompts gain one slug each.
- `cyber-operator`'s prompt body goes to 9,963 characters against the 10,000 ceiling
  `agent-roster` states — **37 characters of headroom**. The next edit to that prompt has to move
  technique detail into a skill first, which is what the spec prescribes for a prompt near the limit.
- Runtime cost: one more skill name and description in every operations session's system prompt,
  since both harnesses list all of them. 487 characters, ~122 tokens.
- Nothing enforces the posture. It is a discipline stated in a prompt, not a sandbox: neither harness
  can bind a tool call to a remote host.
