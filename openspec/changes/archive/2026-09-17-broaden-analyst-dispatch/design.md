## Context

The current credential-sweep passage makes Collection and Terrain the only initial pair, then requires a mission valuation after their fusion. The live `opwe` setting already allows four concurrent task agents, so the observed two-leg maximum is prompt behaviour rather than an execution limit.

## Goals / Non-Goals

**Goals:**

- Let the lead occupy available task capacity with independent, bounded specialist work.
- Preserve evidence hand-offs, dependency barriers, and lead-owned fusion.
- Permit same-specialist fan-out only for disjoint, bounded input slices.

**Non-Goals:**

- Do not set a numerical concurrency target or alter OMP profile configuration.
- Do not alter leg tool permissions, introduce a spawn allowlist, or delegate fusion.
- Do not change credential handling, source scope, or the analytic roster.

## Decisions

- Replace the fixed Collection-and-Terrain pair with a dependency rule: dispatch every independent orientation question in one batch; dispatch later work only when it needs a defined return.
- Keep Collection and Terrain mandatory before credential prioritisation. Mission waits for the asset register only when its valuation depends on it; Overwatch launches whenever its own question is independently material.
- Allow repeated leg instances only for explicit disjoint bounded slices. This reuses the library's existing exhaustive-processing contract and prevents overlapping work.
- Edit the operating-model prose first, then derive the canonical lead prompt from it. Regenerate rather than hand-edit the two wrappers that carry the lead body.

## Risks / Trade-offs

- Broader fan-out raises the number of returns the lead must reconcile. Bounded assignments, notes files, and explicit questions control that cost.
- A model may mistake unrelated work for a dependency. The revised wording must make the test explicit: wait only for information the next question consumes.
- More workers can duplicate corpus work. Slice identity and disjointness are therefore required for repeated instances of one leg.
