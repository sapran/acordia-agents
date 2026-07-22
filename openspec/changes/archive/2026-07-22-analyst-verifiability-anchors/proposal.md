## Why

Analysts today return prose. An operator receiving a leg's finding sees a hypothesis and some rationale, but has no engine-guaranteed way to (a) locate the byte-slice of evidence that supports it, (b) know the leg's confidence and named gaps in a compact shape they can aggregate across legs, or (c) verify that a given `SKILL.md` actually descends from a specific row in the competency grid.

Three gaps compound:

1. **Evidence-reading skills carry no method contract.** A skill like `disk-memory-forensics` says *what* to look for and *why*, but not *how* to inventory the input, how to bound sampling, how to cite a finding by `<path>:<offset>`, or what to do when an optional tool is unavailable. Different runs of the same skill produce differently shaped findings.

2. **Leg agents have no `## What to return` contract.** The orchestrator has to assemble a coherent picture from three legs whose outputs are structurally uncomparable. Compactness, aggregation and cross-leg correlation all suffer.

3. **The grid → artifact bijection is prose-only.** `analyst-skill-library` and `analyst-agent-roster` both mandate one-to-one traceability to `docs/roles/operational-analyst.md`, but nothing in the frontmatter carries the anchor. A row rename in the grid silently drifts from the artifact until a human notices.

None of these gaps requires new tools, new agents, or new permissions. They are shape gaps in artifacts that already exist.

## What Changes

### Layer 1: `## Method` contract for evidence-reading skills

Amend `analyst-skill-library` to add a normative contract that every "reads collected material" skill's `## Method` section states, in order: (1) an inventory step naming the tool used to enumerate the input, (2) a bounded sampling discipline (never wholesale reads), (3) a citation format that anchors each observation to `<path>:<offset>` or `<path>@L<line>`, and (4) a degradation policy per optional external tool named in the body.

Applies to the "evidence-reading" subset only — ~15 skills that read collected artefacts: `disk-memory-forensics`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, `implant-payload-re`, `identity-directory-trust`, `packet-traffic-analysis`, `endpoint-telemetry-edr`, `c2-beacon-exfil-analysis`, `protocol-routing-architecture`, `own-footprint-analysis`, `evasion-antianalysis`, `pattern-of-life-baselining`, `vuln-attacksurface-mapping`. Analytic-spine skills (`reasoning-under-uncertainty`, `key-assumptions-check`, `calibrated-confidence`, `hypothesis-testing`, etc.) are exempted — they read no files and have no tools to degrade.

### Layer 2: `## What to return` in each leg agent prompt

Amend `analyst-agent-roster` to require every subagent leg (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) to carry a named `## What to return` H2 section stating the compact surface it emits back to the orchestrator: hypothesis + calibrated confidence + explicitly named gaps + recommended next collection or method + credential findings routed via `credential-harvest-triage` bins (P0–P3) with source paths. The primary orchestrator carries a paired `## Output discipline` H2 stating how it aggregates the three legs' returns.

`description` frontmatter is unchanged — it remains the italic operating question verbatim per the existing spec.

### Layer 3: `metadata.acordia` frontmatter anchors

Amend `competency-map-derivation` to require every `SKILL.md` and every agent file to carry a `metadata.acordia` block anchoring the artifact to its origin in `docs/roles/operational-analyst.md`:

- Skills: `metadata.acordia: { grid_row: "<row-slug>", grid_deep_in: ["<column>", ...], grid_working_in: ["<column>", ...], source: "docs/roles/operational-analyst.md#L<line>" }`
- Agents: `metadata.acordia: { leg: "<leg-name>", column: "<column>", source_paragraph: "docs/roles/operational-analyst.md#L<start>-<end>" }`
- Procedural cross-cutting skills (`credential-harvest-triage`, and any future procedural skills): `metadata.acordia: { grid_row: null, procedural: true, source: "<change-slug>" }`

opencode's frontmatter contract allows arbitrary `metadata.*` fields (the workbook §6 rule: unknown skill fields are silently ignored). The addition is spec-driven, not runtime-required — it exists so a lint step or human review can verify the bijection at any time.

## Capabilities

### New Capabilities

None. All three layers extend existing capabilities.

### Modified Capabilities

- `analyst-skill-library` — one new `Requirement: Method contract for evidence-reading skills`.
- `analyst-agent-roster` — one new `Requirement: Leg subagents declare what they return`, one new `Requirement: Primary declares output discipline`.
- `competency-map-derivation` — one new `Requirement: Frontmatter carries grid anchor`.

## Impact

- **Modified files:** ~15 `analysts/skills/*/SKILL.md` bodies (Method section restructure), all 40 `analysts/skills/*/SKILL.md` (frontmatter anchor), all 4 `analysts/agents/*.md` (frontmatter anchor + `## What to return` H2 on legs + `## Output discipline` H2 on primary).
- **New files:** none.
- **Referenced source of truth:** `docs/roles/operational-analyst.md` grid rows and leg paragraphs — read for `source:` line anchors, not modified.
- **No install script change.** Frontmatter changes are transparent to `install.sh`.
- **No permission change.** `edit: deny`, bash discipline, `task` whitelist are untouched.
- **No new tooling.** The anchor is spec-verified; runtime lint is out of scope for this change but is now unblocked.
- **Analyst posture preserved.** Passive analysis, read-only, no target interaction.
