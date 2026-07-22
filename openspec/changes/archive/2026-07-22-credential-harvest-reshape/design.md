## Context

The `credential-harvest-triage` skill shipped in change `2026-07-22-credential-harvest-capability` with an inline pattern library and a sequential triage procedure. Both choices were correct at the time (patterns were novel and the priority was to land the capability), but usage since has shown two friction points:

- New provider prefixes (rotations, additions) require a full-skill edit under a spec that constrains the skill's overall shape.
- The sequential procedure serialises category-level work that could partition cleanly along leg boundaries.

The reshape addresses both. Layer 1 moves the pattern block to a sibling reference file — a shape opencode already supports mechanically (sibling files are read on demand, and `install.sh`'s `deploy_dir` symlinks the whole folder). Layer 2 adds a partition step to the triage procedure that maps the classification bins to the existing three-leg topology.

## Goals / Non-Goals

**Goals:**
- Isolate the pattern library so it can be edited and reused without touching the skill's shape.
- Parallelise the triage flow across legs when the input carries mixed material.
- Leave the grid, agents' permissions, dispatch topology, and analyst posture unchanged.

**Non-Goals:**
- Not promoting the pattern file to a pillar-level `analysts/references/` — that becomes justified when a second skill needs the same file, and can be a future change.
- Not adding a fourth leg or a new subagent. The bucket partition dispatches to the three existing legs (with implant/payload material handled as cross-cutting).
- Not changing the classification schema. Bins P0–P3 and the type/subtype/status/scope/source/reuse-potential/priority shape are unchanged.
- Not changing the `## Credential extraction` section content in the seven credential-adjacent skills — only their reference targets (from inline block to sibling file) update.

## Decisions

### Reference file lives inside the skill folder, not at pillar level

**Choice:** `analysts/skills/credential-harvest-triage/references/credential-patterns.md`, not `analysts/references/credential-patterns.md`.

**Rationale:** `install.sh` already symlinks whole skill folders. A skill-local `references/` subdirectory ships automatically. A pillar-level `analysts/references/` would require an install-script addition and creates a second reachable file whose provenance is diffuse. Promote to pillar-level only when a second skill genuinely needs the same patterns.

**Alternative considered:** Pillar-level `analysts/references/` from the start. Rejected — premature generalisation; install-script cost with no second consumer.

### Sibling file, not YAML or JSON

**Choice:** Markdown with fenced regex/pattern blocks by class, matching the style of the existing skill body.

**Rationale:** No code path loads a YAML or JSON pattern library in this repo. Markdown is what analysts and opencode already read.

**Alternative considered:** YAML with structured entries. Rejected — no consumer; discoverability harmed.

### Bucket partition is a step inside `credential-harvest-triage`, not a new skill

**Choice:** Extend the existing triage procedure to include a bucket-partition step between inventory and per-category scan. Do not add a new `credential-harvest-dispatcher` or similar.

**Rationale:** The procedure describes a workflow the triage skill already owns. Adding a second skill for the partition step would fragment the triage narrative and require its own routing prose. The partition is a step, not a competency.

**Alternative considered:** Split into `credential-harvest-triage` (per-category work) and `credential-harvest-dispatch` (bucket partition). Rejected — synthetic split, extra file, more discovery surface.

### Bucket-to-leg mapping is fixed in the skill body

**Choice:** Enumerate the five buckets and their target legs in the triage skill's procedure section.

**Rationale:** The mapping needs to be visible where the operator actually reads it — inside the triage procedure. Encoding the mapping only in the primary orchestrator's prompt would fragment the workflow.

**Alternative considered:** Dynamic mapping ("classify then choose leg by classification"). Rejected — offers no additional flexibility since the mapping is fixed by the domain, and hides the decision from the skill body.

### Implant/payload RE material is cross-cutting, not a leg's bucket

**Choice:** Bucket E (implant/payload RE) resolves via `implant-payload-re` skill (a cross-cutting deep skill per `analyst-skill-library`) and its findings are reported to `fusion-analyst`, not routed as a leg-owned bucket.

**Rationale:** `implant-payload-re` is explicitly cross-cutting per `competency-map-derivation` and `analyst-skill-library`. Assigning it to a specific leg would violate that classification.

**Alternative considered:** Route to `defender-detection-analyst`. Rejected — implant RE is not a defender-only competency; it feeds fusion's synthesis.

## Risks / Trade-offs

- **[Sibling reference file may be skipped at runtime]** — Model can decline to load the reference file when working from `SKILL.md`. Mitigation: `SKILL.md` retains a one-sentence naming pointer stating the reference file exists and what class of pattern lives there. If a run skips the reference, the classification schema and procedure are still complete enough to produce triaged output — degraded, not broken.

- **[Bucket partition duplicates fusion's cross-strand correlation]** — Fusion's job is cross-source synthesis; a triage-time partition could pre-empt it. Mitigation: the procedure explicitly states that per-leg classifications feed back into `multi-source-fusion` for correlation. The partition parallelises the scan; the fusion step still resolves cross-leg linkages.

- **[Adding a new provider prefix now touches two files if the SKILL.md pointer sentence needs an update]** — In practice the pointer sentence is stable ("see `references/credential-patterns.md`"). Only the reference file needs an edit for a new provider.

- **[Bucket mapping ossifies before the workflow is validated in practice]** — The five-bucket mapping is a design guess. Mitigation: state the mapping as "current mapping" in the procedure, with a note that reclassifications land through openspec change, not through in-file edits.
