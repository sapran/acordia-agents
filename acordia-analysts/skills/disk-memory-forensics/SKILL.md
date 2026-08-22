---
name: disk-memory-forensics
description: Read a host's disk and memory as a responder would, driving Volatility walks and parsing filesystem timelines, registry and event logs, when checking what your actions left behind.
metadata:
  acordia:
    family: evidence-forensics
    grid_row: disk-memory-forensics
    grid_deep_in: [Def]
    grid_working_in: [Terrain]
    row: disk-memory-forensics
    source: docs/roles/operational-analyst.md
---

# Disk & Memory Forensics

## Objective

Apply forensic technique to disk and memory to see a host the way a responder would — either as a self-detection check on the evidence your own activity left behind, or to understand a target's state, history, and defensive posture.

## When to use

- Self-detection: verifying what artifacts your on-host actions actually left, and whether cleanup succeeded, before you rely on stealth.
- Target understanding: reconstructing a compromised or accessed host's history, defenses, and stored secrets.

## Method

- Inventory the collected evidence with `ls` / `find` / `glob` — enumerate memory dumps, disk images, hive files, event-log exports, browser profile folders — before opening any single artefact.
- Memory: enumerate processes, injected regions, hooks, network connections, and in-memory artifacts to confirm what a live-response capture would reveal about you. Drive the walk with Volatility 3 plugin output (e.g. `windows.pslist`, `windows.malfind`, `linux.pslist`) rather than reading raw dumps wholesale; scope any `strings` sweeps to known offsets or plugin-flagged regions.
- Disk: examine filesystem timelines, prefetch/amcache/shimcache, event logs, registry, browser and shell history, and deletion/recovery traces. Read structured artefacts through their parsers (registry hives via `impacket-secretsdump` or `regripper`, event logs via `evtx_dump`) and bound raw image reads to the byte-range the parser flagged; do not slurp full images into a viewer.
- Build a timeline and diff it against your own action log to find residual indicators you did not expect to remain.
- For target work, mine the same sources for credentials, defensive tooling, prior-incident traces, and pivot opportunities.
- Cite every finding by `<image-or-dump>:<byte-offset>` or `<parsed-artefact>@L<line>` (event-log record number, registry key path treated as line-shaped) so a peer can re-open the exact locus.
- Judge what a responder arriving now would reconstruct, and prioritize cleanup or avoidance of the highest-fidelity remnants.
- If pypykatz, Volatility, impacket, `regripper`, or a similar named parser is unavailable, either substitute a documented offline equivalent (Mimikatz `sekurlsa` on trusted material, `hivex`, `python-registry`) or flag the gap and stop — never eyeball a hex dump in lieu of a parser.

## Signals / outputs

- A forensic timeline of the host with your operation's residual artifacts flagged.
- A self-detection verdict: what cleanup missed and what a responder would find.
- For targets, extracted secrets, defensive-posture intel, and pivot leads.

## Credential extraction

Post-collection extraction from disk images and memory captures. All work is passive: parse artefacts already collected, never validate live.

**Memory captures**

- LSASS process dump — parse with `pypykatz lsa minidump <dump>` or Mimikatz `sekurlsa::minidump / sekurlsa::logonpasswords`. Yields NTLM hashes, Kerberos tickets, cleartext (WDigest, tspkg, DPAPI master keys) if present.
- Full-system memory (raw/AFF4/VMEM) — Volatility 3: `windows.hashdump`, `windows.lsadump`, `windows.cachedump`, `windows.mimikatz`. Linux: `linux.pslist` + `strings`-hunt for `/etc/shadow`-shaped lines.
- String-scan patterns for un-parsed dumps: `\$NT\$`, `krbtgt`, `-----BEGIN`, `AKIA[0-9A-Z]{16}`, `eyJ` (JWT), `Bearer `, `password=`.

**Disk images**

- Registry hives — `impacket-secretsdump -sam SAM -security SECURITY -system SYSTEM LOCAL`. Yields local SAM hashes, LSA secrets (cached machine account, service credentials), DPAPI master key pointers.
- Cached logon (MSCache/MSCache2) — `impacket-secretsdump` from `SYSTEM` + `SECURITY`; brute-forceable offline, do not attempt.
- Filesystem sweep — carve for `%APPDATA%\Microsoft\Credentials\`, `%LOCALAPPDATA%\Microsoft\Credentials\`, `NTUSER.DAT`, browser profile dirs (`Login Data` SQLite), SSH `known_hosts`/`config`, `.aws/credentials`, `.docker/config.json`.
- Prefetch / amcache / shimcache — evidence of credential-tool execution (mimikatz.exe, procdump.exe, `comsvcs.dll`), not credentials themselves; feed to `overwatch-analyst`.

**Cross-cutting**

- Every extraction is classified and reported via [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); this skill never emits raw values.
