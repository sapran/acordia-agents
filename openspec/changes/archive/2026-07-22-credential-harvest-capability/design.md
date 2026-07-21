## Context

The analyst pillar has 39 skills organised by competency (a row in `docs/roles/operational-analyst.md`'s appendix grid). Seven of those rows touch credentials in their domain (identity, disk/memory, OS internals, cloud control plane, web/API auth, logs, implant RE). Their current `SKILL.md` bodies name the competency at a high level — "locate credential and secret material at rest and in memory" — but stop before the operational detail an analyst needs to actually extract, classify, and triage the material.

Adjacent to those seven specialist skills, no shared procedural skill exists for the cross-cutting question every analyst hits when a collection archive lands: **what is this material, is it usable, and what do we do with it?** That triage does not belong inside any single grid row — it applies across all of them.

The analyst agents are read-only (`edit: deny`), dispatch is fixed to three named legs, and skill binding is by prompt reference (opencode has no `skills:` field). Any new skill must be discovered by the same install-script glob (`analysts/skills/*/SKILL.md`) and named in the appropriate agent prompt to be usable.

Layer 4 of the archived proposal (repo split) already happened as a side effect of the CyberStrike relocation. Layers 1-3 remain unimplemented.

## Goals / Non-Goals

**Goals:**
- Give each of the seven credential-adjacent skills the operational depth needed for post-collection credential extraction — specific artefact paths, canonical tools, portable patterns.
- Add one cross-cutting procedural skill (`credential-harvest-triage`) with a classification schema, a triage procedure, and a pattern library.
- Wire the triage skill and the enrichments into the four agent prompts so dispatch is explicit.
- Keep the analyst posture: passive analysis, read-only, no target interaction, no active credential validation, no raw-value storage.

**Non-Goals:**
- Not adding a new grid row. The triage skill is procedural/cross-cutting; the competency map stays 39 rows.
- Not writing credential-extraction tooling — the skills reference existing tools (Mimikatz, secretsdump.py, pypykatz, jwt-cli, etc.) but ship no code.
- Not changing agent permissions, dispatch topology, or the install script.
- Not covering active credential replay/validation — that is an operator concern, not an analyst concern.
- Not touching the six other pillars (Collection, Operations, Reflection, Direction, Independent action) — they do not exist yet in this repo.

## Decisions

### `credential-harvest-triage` is a skill, not a capability

**Choice:** Land the new skill inside the existing `analyst-skill-library` capability rather than creating a new `credential-harvest-triage` capability.

**Rationale:** Capabilities in this repo map to whole subsystems (the roster, the library, the derivation contract). One skill does not warrant its own capability spec — that would inflate the taxonomy and force spec-level ceremony for a single file. The archived proposal declared it a new capability; that was a mistake worth correcting on re-implementation.

**Alternative considered:** Separate capability `credential-triage`. Rejected — no other single skill has its own capability.

### Procedural skill, not a competency row

**Choice:** Mark `credential-harvest-triage` explicitly as procedural/cross-cutting in its own body and in the delta spec; do not add a row to the grid in `docs/roles/operational-analyst.md`.

**Rationale:** The grid is a competency map — what an operational analyst knows. Triage of collected credential material is a *procedure that reuses seven competencies*, not an eighth competency. Keeping the grid stable protects the derivation contract; adding a row would force a competency-map-derivation spec change and blur the "one skill per grid row" invariant.

**Alternative considered:** Add row 40 to the grid and derive the skill as usual. Rejected — same reasoning; procedural skills are a documented escape valve in the extension workbook.

### Enrichment is additive, in a named `## Credential extraction` section

**Choice:** Each of the seven enriched skills gains one new `## Credential extraction` section appended after the existing body. The section lists artefact locations, canonical tools, and portable patterns for the skill's domain. Existing sections (Objective, When to use, Method, Signals / outputs) are not rewritten.

**Rationale:** Existing skill bodies were derived from role-doc paragraphs; rewriting them risks breaking the derivation trace. An additive section is easy to review, easy to revert if a skill's grid meaning shifts, and mirrors how the CyberStrike attack-* skills accrete new payload sections.

**Alternative considered:** Rewrite `Method` to weave credential extraction throughout. Rejected — makes the enrichment invisible in diffs and couples enrichment to overall skill posture.

### Agent-prompt amendment is one paragraph per agent, under a `## Credential harvest` heading

**Choice:** Each of the four agent prompts gains one new `## Credential harvest` section (H2), one short paragraph, describing that agent's role in the triage dispatch flow. Existing sections (defining spine, baseline, tool discipline, guardrails) are not touched.

**Rationale:** Prompt real estate is precious. A named section is skimmable and easy to keep in sync across the four agents; inlining into existing paragraphs makes the addition invisible and hard to update.

**Alternative considered:** Extend the `You direct three specialists` section on the primary and the equivalent sections on legs. Rejected — that section is topology-focused, not workflow-focused.

### No pattern library file — patterns live inline in the triage skill

**Choice:** The regex/pattern library ships inside `credential-harvest-triage/SKILL.md` as a fenced code block, not as a separate `patterns.yaml` or reference file.

**Rationale:** Analysts are markdown-only; the runtime is opencode reading the file. A separate machine-readable pattern file would need code to load — this repo has no code path. Inline patterns are readable, greppable, and copy-paste usable in ad-hoc scripts.

**Alternative considered:** Ship a `patterns.md` sibling in the skill dir. Rejected — opencode loads `SKILL.md` specifically; sibling files are loaded only if referenced, adding a discovery hop for no gain.

## Risks / Trade-offs

- **[Skill body grows past skimmability]** → Each `## Credential extraction` section stays under ~30 lines; longer per-tool detail (e.g. full Mimikatz cheat-sheet) is out of scope and belongs in operator tooling docs, not analyst skills.
- **[Pattern library rots as providers rotate key formats]** → The library carries a "verify current format at the provider's docs" note; patterns are anchored on stable prefixes (`AKIA`, `ghp_`, `sk-`, `xoxb-`) that change less often than full length/checksum rules.
- **[Analyst starts feeling like a harvester]** → Every enriched section reaffirms passive-only posture: no active validation, no raw-value storage, output is classification and prioritisation, not the material itself.
- **[Grid-row invariant weakens if more procedural skills follow]** → Document the exception in the triage skill's own body: procedural/cross-cutting skills are permitted when they reuse multiple grid rows and would violate one-competency-per-row if added as a row.
- **[Agent-prompt amendments drift out of sync]** → Same H2 heading across all four agents; a grep for `## Credential harvest` verifies presence; delta spec makes the requirement enforceable.
