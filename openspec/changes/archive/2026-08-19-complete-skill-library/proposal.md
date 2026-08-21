## Why

The skill library has four defects that all reduce to the same thing: a reader cannot tell which skill
owns what.

**One vulnerability class has no skill.** Sixteen `attack-*` skills exist —
`cache-poison, cors, graphql, host-header, idor-automation, jwt, open-redirect, prototype-pollution,
race-condition, rate-limit-bypass, request-smuggling, ssrf, ssti, subdomain-takeover, websocket, xxe` —
and SQL injection, the most common of the set, is not among them. It sits inside `wstg-injection` at
lines 12–104.

**The four WSTG bundles restate skills that already exist.** `wstg-injection` carries SSTI, SSRF, XXE
and Host Header sections whose Method the dedicated skills already own; `wstg-auth-session` restates
JWT and IDOR; `wstg-logic-client-api` restates CORS, GraphQL, WebSocket, rate limiting and race
conditions; `wstg-recon-config` restates subdomain takeover. Measured removable duplication: about
8,078 characters, 270 lines.

**Ordinary Linux post-exploitation has no home.** `ebpf-attacks` covers only the eBPF path — kernel
instrumentation, uprobes, `sys_getdents64` hiding, the blind-spot monitors. SUID and capability abuse,
sudo-rule abuse, cron and systemd-timer persistence, SSH key and agent-socket theft, shadow handling,
container-escape checks from the host and kernel-exploit triage are homeless, and
`internal-network`'s `**Linux privilege escalation:**` block has nowhere to move.

**Not one description discriminates.** All 73 descriptions measured before 3.1.0 open with
boilerplate — 54 "Use when", 8 "Apply when", 4 "Use to", 7 other "Use …". Since both harnesses select a
skill by matching its description, the opening clause is the only discriminator that matters, and none
of them names its skill's distinct job first. `macos-postexploit` and `windows-postexploit` sit at 0.38
Jaccard overlap, the highest pair in the repository.

Three smaller defects come with it: `effect-on-target-verification` and `outcome-judgement` are the
same judgement split across two skills; `aleph-entity-graph`, `credential-harvest-triage` and
`exhaustive-data-processing` appear on no agent's skill line, so no agent reaches them by name; and
nothing groups the library, so a reader cannot see which skills compete.

## What Changes

- Promote SQL injection out of `wstg-injection` into a new `attack-sqli`, on the `attack-ssrf`/
  `attack-xxe` pattern, keeping the bundle's CyberStrike provenance because the text is moved rather
  than authored.
- Write `linux-postexploit` for ordinary-userland Linux post-exploitation, with the boundary stated in
  both bodies: `ebpf-attacks` owns anything needing `CAP_BPF`/`CAP_SYS_ADMIN` and a loaded BPF program;
  `linux-postexploit` owns what ordinary userland access reaches. Move `internal-network`'s
  `**Linux privilege escalation:**` block into it.
- Reduce the four WSTG bundles to category, provenance, routing and the sections no dedicated skill
  owns. A section whose Method a skill already carries becomes a one-line pointer — after confirming
  the destination carries it, and appending any payload or flag the bundle holds and the skill lacks.
- Rewrite all 81 descriptions discriminator-first: open with an imperative naming what only that skill
  does, then the trigger, within 1–1024 characters.
- Add `metadata.acordia.family` to every skill: a plain tag, no gate, in twelve families.
- Merge `effect-on-target-verification` into `outcome-judgement`, editing the competency grid first.
  Only this pair — `human-automation-teaming` stays, its autonomy tiers and failure-mode taxonomy are
  distinct material.
- Name the three orphan analyst skills on `fusion-analyst`'s working-knowledge line.
- **BREAKING** for anyone naming skills directly: `effect-on-target-verification` no longer exists.
- Final counts: operators 39, analysts 42, 81 total. Version 3.1.0 → **3.2.0**.

## Capabilities

### Modified Capabilities

- `skill-library`: the description contract becomes discriminator-first and measurable; the family
  taxonomy is added; `attack-sqli` and `linux-postexploit` are required to exist; the WSTG bundles gain
  a pointer-not-duplicate rule; counts move to 42 analyst and 39 operator skills.
- `competency-map-derivation`: the grid loses its `Effect-on-target verification` row, and the
  `Outcome judgement` row absorbs it with T&N promoted from `○` to `●`.
- `agent-roster`: `fusion-analyst` names the three previously unreachable analyst skills;
  `target-network-analyst`'s deep line drops the merged slug.

## Impact

- New: `acordia-operators/skills/attack-sqli/`, `acordia-operators/skills/linux-postexploit/`.
- Deleted: `acordia-analysts/skills/effect-on-target-verification/`.
- Edited: all 81 `SKILL.md` frontmatters (description, `metadata.acordia.family`); the four WSTG
  bundles; `outcome-judgement`'s body; `docs/roles/operational-analyst.md` rows 74 and 82;
  `internal-network.md`, `fusion-analyst.md`, `target-network-analyst.md`,
  `operational-analyst.md` skill lines; both manifests and both catalogs.
- Anything naming `effect-on-target-verification` must be updated in the same change — prompts, the
  grid, specs, `README.md`, `CLAUDE.md`.
