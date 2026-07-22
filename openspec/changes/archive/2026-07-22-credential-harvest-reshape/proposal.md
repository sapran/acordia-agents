## Why

`credential-harvest-triage` shipped in the previous change (`2026-07-22-credential-harvest-capability`, PR #2) with two design compromises worth revisiting now that the skill is settled and being used:

1. **The pattern library is inlined in `SKILL.md`.** ~50 lines of provider prefixes, hash formats, connection-string shapes, and private-key markers live inside the skill body. The original design decision (recorded in that change's `design.md`) was "inline patterns are readable, greppable, and copy-paste usable in ad-hoc scripts" — which held while patterns were the only content. The skill body has since grown, and the pattern block now competes with the classification schema and triage procedure for reader attention. Adding a new provider (e.g. rotating an API-key prefix) is a full-skill edit; splitting into a co-located reference file makes it a targeted edit that other skills can reuse.

2. **Triage is single-threaded across categories.** The current procedure inventories, then scans, then classifies, then correlates, then prioritises — one category at a time. On a large collection (multiple archives, mixed dump types), the sequential shape blocks the operator on the slowest category. cyber-ops-analyst demonstrated bucket-partitioned parallel fan-out over five fixed buckets, dispatched to the same skill each time; adapted to acordia's three-leg topology, the same shape gives an obvious parallelism win.

Neither change touches guardrails, permissions, agents, or the grid. Both are internal reshapes of a single procedural skill.

## What Changes

### Layer 1: Co-located `references/credential-patterns.md`

Move the pattern library out of `analysts/skills/credential-harvest-triage/SKILL.md` into `analysts/skills/credential-harvest-triage/references/credential-patterns.md`. `install.sh`'s `deploy_dir` symlinks the whole skill folder — the sibling file lands next to `SKILL.md` at deploy time without any install-script change.

Structure the reference by class:

- **API keys** — provider prefixes (`AKIA`, `ghp_`, `sk-`, `xoxb-`, `AIza`, `pk_live_`, …) with a "verify current format at provider docs" note.
- **Auth material** — Kerberos ticket file magic bytes, JWT header patterns, OAuth token shapes.
- **Password hashes** — bcrypt, argon2, LM/NTLM, MD5crypt, SHA-crypt markers.
- **Connection strings** — provider-shaped DSN patterns for common databases and message brokers.
- **Private keys** — PEM/OpenSSH/PuTTY markers.

The `SKILL.md` body keeps a one-sentence naming pointer (see `references/credential-patterns.md` for the pattern library) plus the classification schema, triage procedure, and cross-cutting notice. All seven credential-adjacent skills' `## Credential extraction` sections (from the earlier change) that referenced the inline library are updated to point at the sibling file.

### Layer 2: Bucket-partitioned parallel triage procedure

Amend the `## Triage procedure` in `credential-harvest-triage/SKILL.md` to add a **bucket partition step** between inventory and per-category scan:

- Bucket A — identity/directory/cloud-controlplane material → routed to `target-network-analyst`'s domain
- Bucket B — host-forensic (memory, SAM, DPAPI, keychain, shadow) material → routed to whichever leg holds the host under analysis
- Bucket C — web/API auth material → routed to `target-network-analyst`
- Bucket D — log-artefact material → routed to `defender-detection-analyst`
- Bucket E — implant/payload RE material → cross-cutting, resolved via `implant-payload-re` skill and reported to `fusion-analyst`

Each bucket's slice is passed to its handling leg with only that slice — the primary orchestrator dispatches three legs in parallel over three disjoint slices. Fusion re-merges classifications via `multi-source-fusion` for cross-leg correlation (fusion's existing responsibility per the grid, not a new one).

The procedure remains prose in the triage skill; no orchestrator prompt change is required beyond a note in `## Credential harvest` naming the bucket-partition step. The four-agent prompt structure and the existing `task` whitelist (three legs) are unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `analyst-skill-library` — one modified requirement (`credential-harvest-triage` skill exists → gains the bucket-partition step and references the sibling pattern file), one new requirement (co-located reference files for procedural skills).

## Impact

- **Modified files:** `analysts/skills/credential-harvest-triage/SKILL.md` (pattern block removed; classification schema + triage procedure + reference pointer remain; bucket-partition step added). Seven `analysts/skills/*/SKILL.md` bodies whose `## Credential extraction` sections previously named the inline pattern block (references retargeted).
- **New files:** `analysts/skills/credential-harvest-triage/references/credential-patterns.md`.
- **Install script:** no change. `deploy_dir` already picks up sibling files in the skill folder.
- **Agents:** minor — one sentence added to `operational-analyst.md`'s `## Credential harvest` naming the bucket-partition step. No permission changes, no dispatch topology changes.
- **Analyst posture:** preserved. Passive, read-only, no active credential validation, no raw-value storage.
- **Grid:** untouched. Both layers modify the existing procedural skill.
