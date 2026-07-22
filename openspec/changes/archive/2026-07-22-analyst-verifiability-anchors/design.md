## Context

The analyst pillar has three source-of-truth artifacts: the grid in `docs/roles/operational-analyst.md`, the derivation contract (`competency-map-derivation`), and the two artifact rosters (`analyst-skill-library`, `analyst-agent-roster`). Each spec today mandates traceability, but the traceability lives in prose — either in the artifact body or in reviewer memory.

Adjacent work in the DFIR domain (see `~/cab/cyber-ops-roles/plugins/cyber-ops-analyst`) has shown three specific shape gaps in read-only analyst artifacts:

- Evidence-reading skills without a *method contract* produce differently shaped findings per run.
- Leg agents without a *return contract* force the orchestrator into per-leg re-parsing.
- Grid bijection kept in prose is verifiable only by manual audit.

This change closes all three, without lifting any read-only guardrail and without adopting DFIR-specific ceremony (chain of custody, on-disk `out/<engagement>/`, DCWF citations). The changes are additive and structural.

## Goals / Non-Goals

**Goals:**
- Give evidence-reading skills a fixed method spine that makes findings verifiable back to a byte range.
- Give leg subagents a compact return contract that the primary can aggregate mechanically.
- Give the grid-to-artifact bijection a frontmatter anchor that can be verified by lint.
- Land all three in one change because they share a single motivation (verifiability) and touch the same artifact frontmatter.

**Non-Goals:**
- Not writing the lint step. Frontmatter anchors are consumable by future automation; that automation is out of scope here.
- Not touching the analytic-spine skills' Method sections — they read no files.
- Not renaming skills, moving files, or changing dispatch topology.
- Not adopting DCWF external anchors — the grid is the anchor.
- Not restructuring the leg `description` frontmatter (must remain the italic operating question).
- Not changing permissions.

## Decisions

### Method contract applies to the "evidence-reading" subset only

**Choice:** The Method-contract requirement scopes to skills that read collected material — the ~15 named in the proposal. Analytic-spine skills (`reasoning-under-uncertainty`, `key-assumptions-check`, etc.) are exempted by scoping the requirement on skill class rather than uniformly.

**Rationale:** A "cite by `<path>:<offset>`" clause is meaningless for a skill whose input is the analyst's own reasoning. Applying the contract uniformly would push analytic-spine skills toward playbook-style structure — the wrong altitude.

**Alternative considered:** Apply uniformly. Rejected — introduces bogus structure into spine skills.

### `## What to return` is prompt structure, not typed schema

**Choice:** Legs declare return shape in prose under a named H2 section, not via a JSON schema, structured-output tool, or typed metadata block.

**Rationale:** opencode has no structured-output layer for subagent returns. A prose contract is what the model actually reads. A schema would either be aspirational or force runtime enforcement this repo does not have.

**Alternative considered:** JSON schema in leg frontmatter. Rejected — no consumer.

### `metadata.acordia` is spec-verified, not runtime-required

**Choice:** The anchor block is required by the spec, but nothing in opencode reads it at runtime. Consumers are future lint steps or human review.

**Rationale:** opencode's frontmatter rule (§6 of the workbook) is: required fields are `name` and `description`; unknown keys are silently ignored. Adding `metadata.acordia` is a spec-level addition, not a runtime addition — it does not change how skills load or dispatch. It also means the frontmatter carries provenance in a machine-checkable shape without opencode having to grow a feature.

**Alternative considered:** Body-text anchor (`Source: docs/roles/operational-analyst.md#L42`). Rejected — survives grep, but not row renames or grid restructure; frontmatter is more diff-stable.

### Anchor line numbers are source-of-truth citations, not source-of-truth themselves

**Choice:** `source: docs/roles/operational-analyst.md#L<n>` is a pointer to where the derivation started. It is not the grid; the grid is. If the grid moves, the anchor updates via openspec change, not via silent fixup.

**Rationale:** Line numbers rot. If they rot faster than they are useful, the pointer is worse than no pointer. Anchoring via a change forces intentional maintenance and creates a natural place for the compile contract to sit.

**Alternative considered:** Anchor by row slug only (no line number). Rejected — slug matches are ambiguous when the grid grows; line number narrows it.

### Bundling all three layers in one change

**Choice:** One change touches three specs (`analyst-skill-library`, `analyst-agent-roster`, `competency-map-derivation`), one branch, one PR.

**Rationale:** All three modify frontmatter of the same set of files. Splitting into three PRs would produce three merge conflicts and three review rounds against the same lines. The motivation is one thing (verifiability).

**Alternative considered:** Three separate changes. Rejected — synthetic split, higher review overhead.

## Risks / Trade-offs

- **[Method contract nudges skills toward runbook shape]** — The four-step contract (inventory → sampling → citation → degradation) reads like operator ceremony if applied too broadly. Mitigation: scope to the ~15 evidence-reading skills; keep the analytic-spine skills untouched.

- **[`## What to return` formalises leg outputs, drifting them from advisor toward workflow node]** — A leg that returns a structured block reads less like a specialist and more like a stage in a pipeline. Mitigation: keep the return contract's tone advisory (hypothesis + confidence, not "status: PASS"); do not enumerate mandatory keys — describe fields in prose.

- **[Frontmatter anchor rots as grid line numbers shift]** — A row insertion above a target line changes every downstream anchor. Mitigation: the anchor is `grid_row` + `source:` with the row slug as the primary key; line number is a locator, not identity. When the grid renumbers, the spec change that renumbered it also updates the anchors.

- **[Scope of "evidence-reading" is soft]** — Reviewer disagreement over whether e.g. `evasion-antianalysis` is evidence-reading or analytic-spine. Mitigation: the proposal enumerates the 15 explicitly; disagreements are resolved in review, not by inferring from the class name.

- **[`metadata.acordia` re-opens the drift path acordia closed against CyberStrike fields]** — CyberStrike shipped `category`, `cwe_ids`, `chains_with`, `severity_boost` — acordia explicitly forbids them. Adding `metadata.acordia` risks pattern drift. Mitigation: the spec locks the schema (grid_row, columns, source) and states the schema is exhaustive; new keys under `metadata.acordia` require a further spec change.
