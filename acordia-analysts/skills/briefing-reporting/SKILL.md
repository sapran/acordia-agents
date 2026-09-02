---
name: briefing-reporting
description: Compose a bottom-line-up-front product — judgement, action, confidence, gaps, a dated ask — when a read must be handed to a decision-maker and acted on directly.
metadata:
  acordia:
    family: analytic-spine
    grid_row: briefing-reporting
    grid_deep_in: [Core]
    grid_working_in: [Mission, Terrain, Def, Coll]
    row: briefing-reporting
    source: docs/roles/operational-analyst.md
---

# Briefing & Written Reporting

## Objective

Communicate the operational picture and the recommended course of action crisply, so the recipient can decide and act without reconstructing your analysis or misreading your confidence.

## When to use

- Handing off a judgement, a target read, or a recommended move to a decision-maker or the next operator.
- Producing a written product (spot report, target package, after-action) others will act on.

## Method

- Lead with the bottom line: the judgement and the recommended action, before any supporting detail.
- Separate fact from inference from recommendation, and mark the confidence on each (see calibrated-confidence).
- Give only the evidence that changes the decision; push the rest to an annex, and name the key gaps and risks plainly.
- Match depth to the audience and the clock — a two-line spot report and a full target package are different products.
- State what you need from the reader: a decision, a resource, or an acknowledgement, with the deadline.
- **Render with a parser, never a regex.** When the product must also exist in a second format — HTML, PDF, a deck — convert the source with a real parser for that format rather than a hand-written line-prefix pass. Inline emphasis, code spans, tables and inline links are exactly what a regex converter drops, and it drops them without erroring. Probe for an available parser, and say which one you used. Render only your own prose as markup: turn the parser's raw-HTML passthrough off and escape any markup inside quoted evidence, because the product carries verbatim material from the corpus and a real parser will render what a regex pass left inert — into the browser of the person you are briefing.
- **Cite identifiers in full.** A shortened hash or a truncated id reads as a citation and cannot be looked up. Carry the whole identifier into the product however long it is, and let the rendering shorten what is *displayed* rather than what is recorded. This governs identifiers that exist to be resolved — an entity or document id, a content hash, a case or ticket reference. It is never a licence to reproduce a secret or a subject's personal data: a credential, token or key is not cited at all, whatever its length, and a personal identifier is carried only as far as the judgement requires. Those are cited by classification and fingerprint, per `credential-harvest-triage`.

## Signals / outputs

- A bottom-line-up-front judgement and recommendation.
- Confidence, key assumptions, and gaps flagged inline.
- An explicit ask: the decision or action required, by when.
- When the product is written to disk it lands in `.acordia/reports/`, the convention every analyst follows; returning it in-message instead is equally correct when the caller only needs the judgement.
- A rendered product verified twice over: no source-format tokens survive in the output, and a sample of its evidence references has been resolved against the system that issued them — the instance, casefile or store you already read from, using the same read call that produced the reference. Resolve nothing else: not a URL that appears inside the material you are citing, and nothing target-owned or third-party, which would turn writing the report into an active touch. A reference that renders is not a reference that works — a truncated identifier produces a well-formed link to nothing, and counting links detects neither failure.
