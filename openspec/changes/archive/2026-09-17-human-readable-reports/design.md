## Context

See `proposal.md` for motivation. `briefing-reporting` owns the shared shape of a written analyst product, while the credential-sweep layout fixes a specialist HTML form. The competency map is normative for the shared skill's prose. The map is a tracked, derived display of the authored tree.

The selected library material supports the reporting rationale but not a universal mechanical format rule: `SAT` §5.3 (library p.149) describes matrices as a means to sort and compare; `Heuer` (library p.44) calls for visible assumptions, inference chains, and uncertainty; `grugq-Ukraine` (library pp.11,26) supplies a practitioner example of a glossary and acronym reference. The search used routing and hybrid searches for intelligence writing, report sources/references, tables, acronyms and glossaries, then keyword searches for `acronyms`, `first use`, `sources` with `reader`, and `tables` with `present`. It was bounded rather than exhaustive. No retrieved passage prescribes both first-use expansions and claim-level URL/path references. Those exact rules are user-directed report-production practice, not literary doctrine.

## Goals / Non-Goals

**Goals:**

- Make every finished report understandable, comparable where comparison helps, and traceable at the point of each evidence-backed claim.
- Keep one shared policy in `briefing-reporting` and add only the necessary specialist-layout integration.
- Preserve the existing identifier, disclosure, passive-verification, and no-target-contact boundaries.
- Regenerate the map from the completed tree instead of hand-patching its derived record.

**Non-Goals:**

- No agent-prompt, command-wrapper, or skill-set binding duplication.
- No citation engine, automatic acronym detector, universal report template, translation service, or runtime enforcement.
- No source-register repair for the retired ACORDIA identifier, no less restrictive disclosure policy, installed-profile change, release tag, or deployment.

## Decisions

### One shared contract with a finished-report boundary

The reporting skill instructs first-use expansion, a dedicated glossary chapter, useful comparative tables, and claim-local evidence references. It expressly distinguishes a finished product from a short dispatch hand-back: both explain terms and map evidence, but only a finished report needs the chapter. This prevents a short reply from becoming a false document template while preventing a short finished report from evading reader aids.

### Place specialist integration where the form is fixed

The credential layout adds the acronym chapter after Hand-off and before the footer, keeps the existing `table.grid` style, and permits either genuine source anchors or escaped source-root-relative paths plus locators. It does not synthesize URLs for local evidence or record identifiers. Narrative and dossier claims retain their own reference mapping; a credential link is not generic support for a system-level assertion.

### Narrow the existing link heuristic, not the safety check

The embedded self-check counts only parsed `/entities/<id>` paths for short Aleph identifiers. General source URLs, local paths, and href-less anchors remain distinct. Malformed URLs fail with a content-free diagnostic, so a bad value cannot enter checker output.

### Derive the map after authored changes

Use the established markdown transform and model rules against the worktree tree, validate the baseline transform against the last map-producing commit, then replace all model records with derived data. Static version text is updated as part of the same regeneration.

## Risks / Trade-offs

- Models can still omit a rule; the isolated, same-model before/after runs inspect the actual written products and tool events rather than accepting a self-report.
- A detailed reader contract enlarges an already long skill. The change is kept grouped and does not repeat it in five prompts.
- Link parsing can be confused by hostile values; the self-check reports only a fixed malformed-URL message and never emits the value.
- The regenerated map covers a broader current tree, so its model drift is reconciled by record-set and source-derived comparison rather than presented as unrelated hand edits.