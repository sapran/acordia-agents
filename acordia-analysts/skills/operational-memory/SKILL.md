---
name: operational-memory
description: Carry what the operation has established across sessions and dispatches — findings, discarded hypotheses, source reliability and the reasoning — so a returning analyst does not re-derive it.
metadata:
  acordia:
    family: take-handling
    grid_row: operational-memory
    grid_deep_in: [Coll]
    grid_working_in: [Core]
    row: operational-memory
    source: docs/roles/operational-analyst.md
    doctrine_source: [Lindsay#intelligence-performance]
---

# Operational Memory

## Objective

Keep the operation's accumulated understanding available to whoever needs it next. Analysis that has
to be re-derived every session is not analysis, it is repetition — and the second derivation
frequently disagrees with the first without anyone noticing.

## When to use

- Whenever a dispatched specialist returns and its context is about to be discarded.
- At the end of any session, before the working context is lost.
- When a claim in the operating picture is old enough that nobody now remembers what it rested on.
- When two strands of the operation appear to contradict each other.

## Method

- Write findings **with their basis attached**, not as bare conclusions. A recorded conclusion whose
  evidence is gone cannot be re-examined when it is later contradicted, and becomes an assumption
  nobody can audit.
- Record the **rejected** hypotheses and why they were rejected. This is the half most often skipped
  and the half that stops a later analyst spending a day re-walking a path already closed — or, worse,
  reopening it and reaching the opposite answer with no record of the disagreement.
- Keep **source reliability as a running record** rather than a per-item judgement: which feeds have
  produced, which have misled, which have gone quiet. Reliability is a track record and only exists
  if someone keeps it.
- Timestamp what is **perishable** and mark what it depends on. A target's posture, a credential's
  validity and a defender's tooling all decay, and a fact recorded without its decay assumption will
  be read as current long after it stopped being true.
- **Never write a secret into the memory.** The record is durable and is read by everyone who comes
  next, which is exactly what makes it the wrong place for a credential value. Carry the
  `credential-harvest-triage` classification — type, scope, source, priority, reuse potential — and a
  pointer to where the value lives, never the value. A memory entry is the longest-lived artefact the
  operation produces; treat anything written into it as permanently disclosed to every later reader.
- Treat the **return from a dispatch as the memory event**: the specialist's context is destroyed on
  return, so anything not written at that moment is lost. Capture what was done, what was learned,
  the confidence, what was deliberately not done, and what the specialist would look at next.
- Reconcile rather than append when a new finding contradicts a recorded one. Supersede the old entry
  explicitly, keeping it visible with its reason for retirement, so the contradiction is resolved once
  in the record rather than repeatedly in argument.
- Keep it **readable by the next analyst, not only by its author** — the test is whether someone
  arriving cold can act on it without asking a question only the author could answer.
- Degradation: where a full record cannot be written, prefer a short entry with the evidence pointer
  over a long one without it. A pointer survives; a summary without provenance does not.

## Signals / outputs

- A durable record of findings, each with its evidence and its confidence.
- The closed-off hypotheses, with the reasoning that closed them.
- A running source-reliability ledger.
- Explicit supersession entries where later work overturned earlier work.
- Perishability markers on anything time-bound, with the assumption it depends on.
