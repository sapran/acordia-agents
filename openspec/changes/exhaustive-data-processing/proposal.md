## Why

The analyst reads only the opening portion of a large collected artefact and concludes from that head sample; data past the first read window is never processed. In a credential-harvest dump this manufactures false negatives — the key on line 5,000 of a 20,000-line export is never seen, and the picture reports "clean" on material never read.

No artefact mandates *exhaustive* processing, and the existing "Method contract for evidence-reading skills" requirement frames reads as a **"bounded sampling discipline"** (scenario: *"Sampling is bounded, never wholesale"*) — the right axis (no wholesale context load) but silent on coverage, so sampling the head and stopping is spec-conformant. Seven skills inherit the "Sample bounded reads" framing. This change makes exhaustive coverage a triggerable discipline and closes that licensing gap. Observed live during a credential-harvest dump.

## What Changes

### New skill: `exhaustive-data-processing`

Add `analysts/skills/exhaustive-data-processing/SKILL.md` — a procedural cross-cutting skill (same class as `analyst-loop` and `credential-harvest-triage`) that fires whenever bulk collected material must be analysed. It carries:

- **The sampling trap** — names *why* head-and-stop happens (a `read` returns a bounded window; grep hits get eyeballed partial; fanning out subagents merely *distributes* the sampling if each leaf still reads a head), so the skill triggers on the right situation.
- **Script-first exhaustion** — the engine: do not read bulk material into context. Run a tool over 100% of the bytes/records (`rg`/`grep -c`/`awk`/`jq`/a parser) → aggregates plus located hits (`path:line`); the model consumes *results*, not raw. Read into context only the located regions, bounded by the hits, never the head. Fan-out (orchestrator only) over bounded slices is reserved for judgement a script cannot make.
- **Strict coverage ledger** — declare the input scope up front (files × bytes, or record/line counts) as a denominator; every step accounts for its scope (scanned / parsed / deferred-with-reason); a numerator that does not reconcile to the denominator is a sampled result. The final output states total coverage or names the deferred remainder explicitly.
- **Fan-out contract** — only the orchestrator fans out (legs are `task: deny`); slices are disjoint and bounded to full-processability; a leg whose slice still overflows **surfaces the remainder back** to the orchestrator for sub-partition rather than sampling it.

### Agent-prompt forcing-functions

All four analyst agents gain a `## Exhaustive data processing` H2 (mirroring how `## Credential harvest` was added to all four):

- `operational-analyst` — exhaustion is a **precondition**, not an option; script-first before any judgement; the orchestrator **owns coverage reconciliation** — it rejects any leg return whose coverage receipt does not reconcile to the slice it was dispatched, and re-dispatches or sub-partitions rather than compiling a sampled result.
- The three legs (`target-network-analyst`, `defender-detection-analyst`, `fusion-analyst`) — never sample the assigned slice; script-exhaust it; emit a coverage receipt alongside the `## What to return` surface; if the slice exceeds full processing, surface the overflow back (a leg cannot fan out).

### Credential-harvest cross-reference

`credential-harvest-triage`'s first-pass scan and deep-pass are made explicitly exhaustive by pointing at `exhaustive-data-processing`: the pattern scan covers 100% of each bucket's text-decodable bytes and every hit is classified; each bucket returns a coverage receipt. Additive — the classification schema, bucket partition, and procedure are unchanged.

### Strengthen the Method contract (root-cause fix)

**MODIFY** the `analyst-skill-library` requirement "Method contract for evidence-reading skills": element (b) becomes a **bounded-context, exhaustive-coverage discipline** — reads into context stay scoped (no wholesale load), **and** the input SHALL be covered in full by a prior tool pass that drives which scoped regions are read; a conclusion SHALL NOT rest on the opening portion while the remainder goes unprocessed. The "Sampling is bounded, never wholesale" scenario is split into a context-bound scenario and a new exhaustive-coverage scenario.

### Harmonise the seven "sample" skills

Reword the read-discipline bullet in the seven evidence-reading skills that frame reading as "sample" so it reads "bounded-context reads driven by an exhaustive tool pass; process every located hit, not just the first": `protocol-routing-architecture`, `own-footprint-analysis`, `evasion-antianalysis`, `pattern-of-life-baselining`, `vuln-attacksurface-mapping`, `log-artefact-interpretation`, `endpoint-telemetry-edr`. Substance unchanged (they already grep-first); the trap word is removed and coverage made explicit. The remaining evidence-reading skills use "bounded" without the "sample" verb and are left untouched.

## Capabilities

### New Capabilities

None. The new skill lands inside `analyst-skill-library` as a cross-cutting procedural addition, mirroring `credential-harvest-triage` and `analyst-loop`.

### Modified Capabilities

- `analyst-skill-library` — one **ADDED** requirement (`exhaustive-data-processing` skill exists) and one **MODIFIED** requirement (Method contract element (b) gains exhaustive-coverage; scenarios split).
- `analyst-agent-roster` — one **ADDED** requirement (an exhaustive-processing section in every agent prompt; the primary owns coverage reconciliation; legs emit receipts and surface overflow).

## Impact

- **New files:** `analysts/skills/exhaustive-data-processing/SKILL.md`.
- **Modified agent files (4):** each gains a `## Exhaustive data processing` H2. No `edit`/`bash`/`task` permission block is touched.
- **Modified skill files (8):** `credential-harvest-triage` (cross-ref) plus the seven reworded evidence-reading skills.
- **Referenced source of truth:** the strengthened Method-contract requirement is the normative anchor for the skill-body rewording, so the edits under `analysts/` trace to an openspec requirement, not to the competency grid — **no grid change, no source-of-truth drift.** The competency grid in `docs/roles/operational-analyst.md` is read for anchor, not modified; `competency-map-derivation` is untouched.
- **No install script change.** `install.sh` globs `skills/*` and picks up the new skill automatically.
- **No permission change.** No agent's `edit`, `bash`, or `task` block is modified; `edit: deny` posture and the three-leg `task` whitelist are intact.
- **Analyst posture preserved.** The discipline reads, models, and judges more completely — it authorises no new action, and the passive/no-raw-values guardrails carry through.
