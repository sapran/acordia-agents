---
name: exhaustive-data-processing
description: Use when bulk collected material lands for analysis — a file dump, archive, log bundle, memory capture, or dataset too large for a single read to capture — and it must be processed in full: cover 100% of it with a script-first tool pass, read only located regions into context, and prove coverage rather than concluding from the opening portion.
metadata:
  acordia:
    grid_row: null
    procedural: true
    source: openspec/changes/exhaustive-data-processing/proposal.md
---

# Exhaustive Data Processing

## Cross-cutting notice

This skill is **procedural and cross-cutting**. It does not correspond to a row in the competency-grid appendix of `docs/roles/operational-analyst.md` — it names a *workflow* that composes competencies, not a competency of its own. It builds on `analytic-tooling-scripting` (the scripting baseline) and drives the three legs' evidence reads; it lands under the same procedural-skill exception that `credential-harvest-triage` and `analyst-loop` use. It is **not** one of the fifteen evidence-reading skills bound by the `## Method` contract — it *defines* the reading discipline those skills follow.

## Objective

Turn a pile of collected material into answers derived from **all** of it. Sampling the opening portion of an artefact and concluding from it manufactures false negatives — the credential on line 5,000 of a 20,000-line export, the one anomalous record in the tail — and reports "clean" on data that was never read. Exhaustion is the default; a partial pass is a named, justified exception, never a silent one.

## When to use

- Bulk material lands: a file dump, disk/memory image, archive, log bundle, cloud-state export, config directory, or dataset.
- Any artefact large enough that a single `read` captures only part of it.
- Any time a conclusion would otherwise rest on the first screenful of a file.

## The sampling trap

Head-and-stop is a mechanical default, not a choice — name it so you catch it:

- **The read window is bounded.** `read` (and `head`/`cat` into a fixed context) returns the opening slice of a large file. Read it, conclude, and everything past the window is invisible.
- **Tool hits get eyeballed partial.** `grep` returns 500 matches; reading the first ten and generalising ("looks like all the same") is sampling by another name.
- **Fan-out alone does not fix it.** Splitting the material across subagents only *distributes* the sampling if each leaf still reads a head. Exhaustion has to hold at the leaf, or it does not hold at all.

## Method — script-first exhaustion

Completeness comes from the tool, not from loading raw bytes into a context window that cannot hold them.

1. **Do not read bulk material into context.** Run a tool over 100% of the bytes or records — `rg` / `grep -c` for counts and located hits, `awk` / `sort` / `uniq -c` for aggregates, a real parser (`jq`, `csv`, `sqlite`, Python) for structured or nested formats. Iterate *every* record, not a page.
2. **Consume results, not raw.** The model reads the tool's aggregates and located hits (`path:line`), then reads into context only the specific located regions that need judgement — bounded by the hits, never the head.
3. **Validate the pass.** Confirm the tool covered the whole input (line / record / byte counts reconcile — see the ledger) and that a parsing bug is not silently dropping records. Validate transforms against a known-good sample before trusting their output.
4. **Fan out only for judgement a script cannot make.** When the question needs the model to *read* content a pattern cannot classify, partition into bounded slices (orchestrator only) and dispatch each for full reading. The script pass still runs first, so fan-out is the exception, not the engine.

## Coverage ledger

Completeness is proven, not asserted.

- **Declare the input scope up front** — the denominator: number of files × total bytes, or record / line counts. Enumerate with `find` / `glob` / `ls`, `wc -l`, or the parser's record count.
- **Account for every step** against that denominator: N scanned / N parsed / N deferred-with-reason. A numerator that does not reconcile to the denominator is a sampled result.
- **Emit a coverage receipt** per unit of work: `{scope declared, scope covered, method, deferred + why}`. The *method* field is load-bearing — a receipt whose method is "read the file" over a multi-megabyte artefact is self-evidently a sample.
- **Reconcile before compiling.** The orchestrator checks each leg's receipt against the slice it dispatched; a receipt that does not cover its slice is rejected and re-dispatched or sub-partitioned. Compile only from reconciled receipts.
- **State total coverage in the output** — "X of X files, Y of Y records processed, 0 deferred" — or name the deferred remainder explicitly. No silent short returns.

## Fan-out contract

- **Only the orchestrator fans out.** Legs are `task: deny` leaf specialists; they cannot dispatch.
- **Slices are disjoint and bounded** to full-processability, each dispatched with only its slice.
- **A leg that overflows surfaces back.** If a slice still exceeds full processing, the leg script-exhausts what it can and surfaces the un-processable remainder back to the orchestrator for sub-partition — it does not sample the remainder, and it does not fan out. (Mirrors `analyst-loop`: a leg surfaces the need back rather than assuming the orchestrator's role.)
- **The orchestrator sub-partitions deterministically** — by file, then by byte / line range — so each round strictly shrinks the slice and overflow cannot ping-pong.

## Signals / outputs

- A reconciled coverage ledger: declared scope = covered scope, or a named deferred remainder.
- Answers traceable to located source (`path:line` or `path:offset`), derived from a pass over the whole input.
- For fan-out work: one coverage receipt per slice, reconciled by the orchestrator before compilation.

## Guardrails

- **Passive posture.** Read, model, judge — no file edits, no payloads, no credential validation. Execution belongs to the operators the analyst advises.
- **No raw credential values** in output — classifications, sources, and priorities only (see `credential-harvest-triage`).
- **No silent truncation.** Any bound on coverage (a deferred slice, an unparseable artefact) is named in the output, never dropped.
