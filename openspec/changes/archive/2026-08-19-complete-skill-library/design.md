## Context

See proposal.md — Why. The measurements, taken in this worktree:

`wstg-injection` (9,715 bytes) sections: SQL Injection 12–104 (2,599 chars: Detection Payloads 14–29 ·
DB Fingerprinting 30–39 · Union-Based Extraction 40–62 · Blind SQLi 63–78 · sqlmap Quick Reference
79–104) · XSS 105–176 (1,495, **keep**) · Command Injection 177–219 (558, keep) · SSTI 220–244 (1,535,
→ `attack-ssti`) · SSRF 245–296 (993, → `attack-ssrf`) · XXE 297–330 (629, → `attack-xxe`) ·
LFI/Path Traversal 331–354 (480, keep) · Host Header 355–370 (325, → `attack-host-header`) · HTTP
Parameter Pollution 371–382 (215, keep) · Mass Assignment 383–400 (505, keep).

`wstg-auth-session` (7,294): JWT 87–113 (676, → `attack-jwt`) · IDOR 167–188 (585, →
`attack-idor-automation`) · Privilege Escalation Patterns 189–209 (629, **keep** — WSTG-AUTHZ material
broader than IDOR).

`wstg-logic-client-api` (8,887): Rate Limiting & Function Abuse 50–73 (558, →
`attack-rate-limit-bypass` + `attack-race-condition`) · CORS 197–220 (935, → `attack-cors`) · GraphQL
247–273 (994, → `attack-graphql`) · WebSocket 274–292 (448, → `attack-websocket`) · Mass Assignment in
APIs 293–310 (675, **keep**).

`wstg-recon-config` (5,684): only the takeover portion of `## Subdomain & Cloud Storage` 145–173 (866)
→ `attack-subdomain-takeover`.

Removable: 3,482 + 1,261 + 2,935 + ~400 ≈ **8,078 characters, ≈ 270 lines**. That is the ceiling. A
larger cut means content is being deleted rather than de-duplicated.

Descriptions: **73 of 73 measured before 3.1.0 open with boilerplate** — 54 "Use when", 8 "Apply when",
4 "Use to", 7 other "Use …". `macos-postexploit` and `windows-postexploit` sit at 0.38 Jaccard overlap.

Grid rows to merge, `docs/roles/operational-analyst.md`:

- L74 `| Outcome judgement — end achieved (effect or intel) & what now | ● | ○ | | ○ |`
- L82 `| Effect-on-target verification (did the system actually change?) | ○ | ● | | |`

## Goals / Non-Goals

**Goals:**

- Every vulnerability class the pillar tests has exactly one owning skill.
- The four bundles keep their WSTG identity and lose only what a dedicated skill already carries.
- A description's first clause discriminates.
- Every skill is reachable from a prompt, and every family is visible.

**Non-Goals:**

- Rewriting skill bodies. 3.2.0 moves text and rewrites descriptions; it does not re-author methodology.
- Merging any pair other than `outcome-judgement` ← `effect-on-target-verification`.
  `human-automation-teaming` stays: its autonomy tiers and failure-mode taxonomy are distinct material.
- Adding families as a runtime mechanism. `metadata.acordia.family` is a tag; nothing reads it.

## Decisions

**`attack-sqli` is a move, so it inherits the bundle's provenance.** The text is CyberStrike's, carried
here in `wstg-injection`; a new skill holding that text carries the same `metadata.cyberstrike`
`source` and `commit`. Authoring a fresh SQLi skill instead would replace reviewed upstream payloads
with invented ones — the characteristic failure of this repository.

**The bundles keep the sections nothing else owns.** XSS, command injection, LFI/path traversal, HTTP
parameter pollution, mass assignment, and the WSTG-AUTHZ privilege-escalation patterns have no
dedicated skill; they stay whole. The alternative — creating six more `attack-*` skills — is a bigger
change than the duplication costs, and would be a content decision dressed as de-duplication.

**Pointer conversion is destination-checked, not assumed.** Before a section becomes a pointer, the
destination skill is read and any payload or flag the bundle holds and the skill lacks is appended.
Otherwise the "de-duplication" silently deletes content.

**Descriptions open with an imperative naming the distinct job.** Both harnesses match on description,
and every current description opens with a clause common to all of them, so the discriminating words
arrive after the model has already stopped reading closely. The worked example is the four-way analyst
collision on bulk-material handling: "Prove complete coverage of a bulk corpus" versus "Inventory and
rank credential material inside a dump" versus "Judge whether collected take is genuine, complete and
worth having" versus "Join heterogeneous datasets into one queryable corpus" versus "Script a parser,
extractor or transform".

**Twelve families, each skill in exactly one, verified by count.** `analytic-spine` 13 ·
`target-modelling` 10 · `defender-reading` 7 · `evidence-forensics` 4 · `take-handling` 8 ·
`web-attack` 17 · `web-methodology` 5 · `host-postexploit` 4 · `cloud-postexploit` 5 ·
`directory-attack` 2 · `mobile` 5 · `operations-discipline` 1 = **81**. Two assignments differ from the
first sketch and are decided here: `analytic-tooling-scripting` is `analytic-spine`, because it sits on
the grid's spine line in all four analyst prompts, and `analyst-loop` joins it there as the procedure
that runs the spine; `maintaining-operating-picture` is `take-handling`, matching its grid section.

**The merge edits the grid first, and folds rather than deletes.** L74 becomes
`| Outcome judgement — end achieved (effect or intel), did the system actually change, & what now | ● | ● | | ○ |`
— T&N promotes `○` → `●` because that column held the deep mark on the absorbed row — and L82 is
deleted. Then the unique Method content moves into `outcome-judgement`'s effect branch: the
observable-channel inventory, the first-party versus independent-confirmation split, the
`<log>:<offset>` citation form, the honeypot tells. `outcome-judgement` ends with
`grid_deep_in: [Core, 'T&N']`, `grid_working_in: [Fus]`, `source: docs/roles/operational-analyst.md#L74`.

**The three orphans go to `fusion-analyst`.** `aleph-entity-graph`, `credential-harvest-triage` and
`exhaustive-data-processing` appear in body sections of the analyst prompts but on no skill line. The
fusion analyst ingests bulk take and works an entity graph, so its working-knowledge line is where they
belong; the other legs already reach them through their own body sections.

## Risks / Trade-offs

- **A pointer conversion deletes a payload** → destination is read and topped up first; verification
  greps every removed payload span against the destination skill.
- **A rewritten description drifts from what the skill does** → the rewrite touches the first clause and
  the trigger only, never the body, and each is checked against its own body's Objective.
- **The merge loses the effect-verification method** → the fold is verified element by element against
  the deleted body, and the change fails if the slug survives anywhere or an element does not.
- **Family tags rot** → accepted; they are documentation with no gate, and the count check in
  verification is the only guard.
- **81 frontmatter edits is a large mechanical diff** → done by script for the `family` key, by hand for
  the descriptions, and reviewed as two separate commits so the mechanical half is auditable at a glance.

## Migration Plan

1. Grid first: edit L74, delete L82 in `docs/roles/operational-analyst.md`.
2. `attack-sqli` and `linux-postexploit`; move `internal-network`'s Linux block into the latter.
3. Fold `effect-on-target-verification` into `outcome-judgement`; delete the directory; strip the slug
   from every line naming it.
4. Bundle pointer conversions, destination-checked.
5. `metadata.acordia.family` on all 81 skills (scripted), then the 81 description rewrites.
6. `fusion-analyst`'s working-knowledge line gains the three orphans.
7. 3.2.0 in both manifests and both catalogs; counts in both descriptions.
8. Verify: counts, family coverage, no boilerplate opening, no dangling slug, slug resolution, prompt
   sizes, and a live dispatch that reads `attack-sqli` and `linux-postexploit`.
