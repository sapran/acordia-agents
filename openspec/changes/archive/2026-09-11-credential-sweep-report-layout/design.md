## Context

An access-credential sweep delivered on 2026-09-11 produced an HTML product whose structure the
operator wants to reuse for every future sweep. Nothing in the distribution describes that
structure. Step 8 of `credential-harvest-triage` — "**Report**: emit the classified inventory" —
owns the moment the product is written and says nothing about its form, so the form is reinvented
per run and is therefore also unchecked per run.

The delivered file cannot be read back into a session: it carries real private-key material, and
the published spec (`skill-library`, the reporting requirement) forbids reading a rendered product
carrying credential values back in, because that places every value into the transcript the routing
rule keeps out of it. Everything used here was extracted structurally — counts of elements, class
names, the stylesheet — by scripts printing verdicts and shapes rather than content.

## Goals / Non-Goals

**Goals.**

- Fix the shape of the HTML sweep product so it is reproduced rather than reinvented.
- Make that shape checkable, by a script that prints a verdict and no report content.
- Correct the three defects the delivered report actually carried, in the codified version.

**Non-Goals.**

- Redesigning the visual language. The delivered structure is what was asked for; only the three
  named corrections are made.
- Generating reports. The distribution ships no executing code and gains none here.
- Widening what may be disclosed. The layout decides presentation; ownership decides disclosure.
- Regenerating `acordia-map.html`, which is stale by a full release for unrelated reasons.

## Decisions

### Where the layout lives: a reference file under `credential-harvest-triage`

Chosen: `acordia-analysts/skills/credential-harvest-triage/references/report-layout.md`.

Step 8 of that skill's triage procedure is the exact hook — it already owns emitting the product and
already gates what the product may disclose. The skill is `procedural: true` with `grid_row: null`,
and the published `skill-library` spec permits a `references/` subdirectory **only** on a procedural
cross-cutting skill, and forbids one to a grid row. So the home is available without widening
anything, and the competency grid does not move. The skill already ships
`references/credential-patterns.md`, so both the naming-pointer shape in the body and the register
of the reference file itself exist to be matched rather than invented.

**Rejected: `briefing-reporting`.** It is a grid-row skill (`row: briefing-reporting`) and cannot
carry a `references/` directory without widening the spec's own restriction. Its remit is also
wrong: any product handed to a decision-maker, not a credential sweep. Its rendering and citation
discipline already governs this layout from above, so the new file cites it rather than restating
it, and `briefing-reporting` is left untouched. A one-line cross-pointer there is defensible, but it
would edit a grid-row skill body and trigger the literature rule for a signpost — a worse trade than
leaving the pointer to run in one direction.

**Rejected: a new skill.** A report layout is a workflow artefact, not a competency. Adding it as a
skill would either require a grid row — inflating the competency map with a workflow, which is the
precise reason `credential-harvest-triage` itself is procedural — or create a second procedural
skill whose only content is the presentation of the first one's output.

### No `doctrine_source` on the reference file

The repository rule is that shipped prose is grounded in the lib.ai canon before it is written. This
file makes no doctrinal claim. It is a layout contract of the same category as its sibling
`credential-patterns.md`, which carries no literature attribution either, and every normative
statement in it is a rendering of a claim the distribution already ships: bottom-line-up-front
ordering and the display-versus-record rule from `briefing-reporting`, the coverage denominator from
`exhaustive-data-processing`, the ownership gate from `credential-harvest-triage`'s own guardrails.
Each is cited by skill slug. A `doctrine_source` here would assert that a registered work prescribes
a CSS class, which is the false-attribution failure the provenance capability exists to prevent.

The stop condition is written into the work rather than trusted to judgement: a sentence asserting
*why* an analytic product should be shaped a given way — an argument rather than a rule — is a
doctrinal claim, and authoring it requires the literature pass first.

### Three corrections, then a fourth round from review

The layout was codified **as delivered**, with three changes:

1. `.mono` is defined — and, after review, actually used, on the key fingerprint. Defining a rule
   nothing reaches leaves the "every class is defined" probe unable to exercise it.
2. `.cred.sys` replaces an inline `style="border-left:4px solid var(--accent)"` that one system
   block carried and another did not. This is not a tidy-up: it turns "no element carries a
   `style=` attribute" into a property the self-check can assert.
3. No unsubstituted placeholder. The template's own slots are a **closed vocabulary** the self-check
   carries by name, alongside the `{BRACED}` probe.

The original reasoning for a braces-only probe — that `ANGLE_CAPS` examples would never fire on the
template — was wrong, and review caught it: the check runs against the draft report, never against
this file, so the only placeholder vocabulary a real report can contain is the one the template
teaches. A braces-only probe closed the 2026-09-11 defect for the form that report used and left it
open for the form the template teaches. The vocabulary is an explicit allowlist rather than a
general all-caps pattern so that legitimate report text — `UNENUMERATED` in the coverage note, an
environment-variable name in an excluded-material verdict — does not fire it. A probe that fires on
legitimate content trains the author to ignore it, which is the same failure as no probe at all.

Review then found three more, all folded in before merge:

4. **Ownership had no place on the page.** The guardrails make ownership the first decision and the
   one that governs whether a value may be written at all, and the anatomies rendered a value slot
   unconditionally. Both credential blocks now carry an `Ownership` row, an eighth non-cosmetic rule
   gates the `<details>` on it, and the document order says where an ownership-refused finding
   lives — its own system section, as a block with no disclosure element.
5. **The key tag contradicted rule 1.** "The tag carries the key's own header line" is safe for PEM
   armour and unsafe for a JWT or a prefixed API key, whose first bytes are the secret. The tag now
   carries a derived key-type label, with the PEM armour line named as the one permitted literal.
6. **`REPORT_MODE` was named once and never defined**, while the layout required operation-side
   working-file detail on a page that leaves the analyst's control. Two modes are defined, the
   holder is named by role rather than by individual, the footer author is a role designator, and
   every working file is named relative to the brief's working directory.

### The self-check reports a verdict, not content

Verification of a product carrying credential values may only run against the draft or through a
check that reports a verdict — the disclosure doctrine's carve-out. Review showed the first draft
overstated this: three of its prints echoed report-derived substrings, and one of them scanned
`pre` bodies, so a captured artefact quoted inside a disclosure could put its own class names and
braced tokens into the analyst's context as tool output — an injection channel opened by the very
check meant to keep content out. The shipped script blanks every `<pre>` body before the class and
placeholder scans, and the file states what the verdict includes rather than claiming it prints
nothing.

Review also found the check blind in five ways, each of which let a real defect through clean, and
two of which had a disclosure cost:

- `<pre class="key">` matched as an exact literal, so `<pre class="key" id="k9">` or
  `class="mono key"` was counted in neither total and a credential rendered open on the page
  reported `0`.
- `<details>.*?<pre class="key">` under `re.S` crossed `</details>`, so one keyless `<details>` —
  which the file's own certificate rule invites — masked a later orphan value.
- `class="…"` and `style="…"` matched double quotes only, so the single-quoted spelling defeated two
  of the non-cosmetic rules, including the one `.cred.sys` exists to make checkable.
- `<a href="…"` required `href` to be the anchor's first attribute, so a link with any attribute
  before it escaped the short-link count entirely, and an anchor with no `href` was invisible.
- A `<details open>` was detected only accidentally, and reported as the wrong fault.

All five are fixed, each is mutation-proved, and the old patterns were re-run against the same five
documents to confirm they reported clean. The output gains a `details shipped open` line and an
anchor triple, and `pre.key outside <details>` is renamed `pre.key not collapsed`, which is true of
both faults it now detects.

### The delta keeps the published scenario title and adds beside it

The plan called for retitling the published scenario
`#### Scenario: \`credential-harvest-triage\` carries \`credential-patterns.md\`` to cover both
reference files. OpenSpec joins scenarios between a `MODIFIED` block and the published spec **by
title**, so a retitle is read as a deletion and `--strict` fails naming the omitted scenario. The
published title is still true, so the honest move is the second of the two available: keep it
verbatim and add a new scenario alongside it for the new file. The end state is identical and the
scenario history survives.

## Risks / Trade-offs

- **A fixed layout can outlive its fit.** A sweep whose findings do not decompose into systems —
  a corpus of hashes with no endpoints — would strain the spine. Mitigated by the residual section,
  which is part of the contract rather than an escape hatch, and by the layout being a reference
  file the operator can change in one place.
- **The self-check is a lint, not a proof.** It cannot tell a correct system attribution from a
  wrong one, or a real evidence id from a syntactically valid invention. It catches exactly the
  class of defect that shipped: undefined classes, inline styles, surviving placeholders, open
  values, shortened hrefs. The analytic checks stay with `briefing-reporting`.
- **Two reference files in one skill raises the cost of reading it whole.** Accepted: the body
  carries a naming pointer to each, so a session that reads only `SKILL.md` knows both exist and
  what class of content each holds, which is what the co-location requirement asks for.
