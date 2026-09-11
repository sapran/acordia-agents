## Why

Step 8 of `credential-harvest-triage` says "emit the classified inventory" and stops. Everything
about the shape of the product it emits — what the reader sees first, how findings are grouped,
where a credential value may appear on the page — is left to whoever is writing that run's report.
So each sweep reinvents the layout, and the reinvention is not free: the organising choice decides
what the reader comes away believing. A report grouped by artefact or by collection hands over a
list of strings; a report grouped by the system each credential opens hands over an inventory of
accesses. Only the second is an analytic product.

The 2026-09-11 access-credential sweep produced a layout worth keeping, and shipped two defects
that show why an unwritten layout is also an unchecked one:

- one `<span class="mono">` with **no `.mono` rule in the stylesheet**, so the span rendered
  unstyled and nothing said so;
- one evidence link emitted as `href="{ALEPH}/entities/<id>…"` — an **unsubstituted template
  placeholder**, a well-formed link to nothing. This is exactly the failure `briefing-reporting`
  already names: "a truncated identifier produces a well-formed link to nothing, and counting links
  detects neither failure." The skill names the failure; nothing in the distribution catches it.

A third inconsistency was cosmetic but blocked checking: one system block carried
`style="border-left:4px solid var(--accent)"` inline and another did not, so "no inline styles" was
not a property the document had.

Codifying the layout fixes all three at once. The shape becomes a contract rather than a habit, and
because it is written down it can carry a self-check — one that reports a verdict and prints no
report content, which is what the disclosure doctrine requires of any verification run against a
product that carries credential values.

## What Changes

**Current behaviour.** `credential-harvest-triage` specifies what goes into the report (the
classified inventory, the coverage statement, the owner and reuse hypothesis per P0/P1) and nothing
about its form. The skill ships one reference file, `references/credential-patterns.md`, for
detection patterns.

**Desired behaviour.** The skill ships a second reference file,
`references/report-layout.md`, fixing the presentation of the HTML sweep product:

- **The organising principle** — by the system each credential opens, never by artefact, file or
  collection. A credential whose system could not be identified goes to a residual section rather
  than being filed under a guess, because a wrong system attribution reads as an access that does
  not exist.
- **The document order** — dateline, bottom line, numbered system sections ordered by consequence,
  residual, excluded and borderline, coverage, gaps, hand-off, footer.
- **The stylesheet**, verbatim, with `.cred.sys` replacing the inline border and `.mono` given the
  rule it was missing.
- **Four `div.cred` anatomies** — system dossier, credential (login variant), credential (key
  variant), excluded/borderline — each with its field labels, so the artefact, the account and the
  holder role stay three distinguishable things, and each credential block carrying an `Ownership`
  row.
- **A closed placeholder vocabulary** the self-check carries, so a slot left unsubstituted in a real
  report is named rather than shipped.
- **Two report modes** — `exact` for the credential owner's own responder, `classified` for any
  other reader — deciding whether a disclosure element appears at all and whether working-file
  locations are named.
- **What fills the fixed blocks** — the dateline's fields, the bottom line's counted clauses, the
  coverage probe grid and its three `p.meta` (scoping receipt, unenumerated sets, legs and note
  files), the gaps list, the hand-off ask and standing record, the footer's assertions.
- **Eight rules that are not cosmetic** — a value only ever inside a collapsed `<details>`; that
  `<details>` written **only where ownership permits the value into the product**, so an
  ownership-refused finding is a credential block with no disclosure element rather than an empty
  one; `(exact)` on a summary hiding a verbatim secret; the whole identifier in `href` with only the
  display text shortened; no placeholder token surviving into the product, braced or from the
  vocabulary; every class defined and no `style=` attribute; no count without a denominator, and an
  unenumerable set labelled unenumerated; the product written to disk and never read back into the
  session.
- **A self-check** run against the draft before hand-over, printing a verdict — class names,
  integer counts and truncated section titles — and never a `pre` body, a `summary` body, an
  attribute value or an evidence identifier. A precursor of it, run verdict-only against the
  delivered 2026-09-11 report, printed both real defects and the inline-style inconsistency; the
  shipped version is stricter and is mutation-proved against a substituted skeleton instead, because
  the delivered report may not be read again.
- **A stated limit** — a clean verdict is a lint result, not a proof, and a sample of the evidence
  references must still be resolved against the issuing system per `briefing-reporting`.

**Presentation only.** The reference decides how a finding is shown, never whether it may be shown.
What may be disclosed remains decided by `## Guardrails` in `SKILL.md`, gated on ownership. The file
states this in its lede and again in its closing paragraph.

**No grid change.** `credential-harvest-triage` is `procedural: true` with `grid_row: null`, and the
published spec permits a `references/` subdirectory only on a procedural cross-cutting skill. No
row, no mark and no `grid_deep_in`/`grid_working_in` list moves.

**No literature attribution.** The file makes no doctrinal claim. Every normative statement in it is
a *rendering* of a claim already shipped — bottom-line-up-front ordering and the display-versus-record
rule from `briefing-reporting`, the coverage denominator from `exhaustive-data-processing`, the
ownership gate from this skill's own guardrails — and each is cited by skill slug rather than by a
work. It therefore carries no `doctrine_source`, matching its sibling `credential-patterns.md`, and
the skill's existing `doctrine_source: [Monte#operational-security, Heuer#information-quantity]` is
unchanged.

**Version.** Three occurrences move 6.8.0 → 6.9.0. MINOR — content that reaches a user.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `skill-library`: the co-located-reference requirement gains a scenario asserting
  `credential-harvest-triage` carries `references/report-layout.md` and names it in the body; the
  `credential-harvest-triage` requirement gains a clause (d) for the report-layout pointer, extends
  its body scenario to require that pointer, and gains a scenario asserting the layout fixes
  presentation without widening disclosure.

## Impact

- `acordia-analysts/skills/credential-harvest-triage/references/report-layout.md` — new file.
- `acordia-analysts/skills/credential-harvest-triage/SKILL.md` — one sentence appended to triage
  step 8, and one new `## Report layout` pointer section between `## Pattern library` and
  `## Signals / outputs`.
- `.claude-plugin/marketplace.json`, `.omp-plugin/marketplace.json`,
  `acordia-analysts/.claude-plugin/plugin.json` — 6.8.0 → 6.9.0.
- `docs/implementation-notes.md` — one line recording measured `acordia-map.html` drift, parked.

Not affected: `docs/roles/operational-analyst.md` (no grid change), `docs/roles/sources.md` (no
doctrinal claim, so no register entry), `acordia-analysts/skill-sets.json` (no skill added or
removed, no prompt gains or loses a slug), `acordia-analysts/skills/briefing-reporting/SKILL.md`
(deliberately untouched — see `design.md`).

Out of scope: `acordia-map.html`, already stale by a full release independently of this change; and
any generator that would emit a report from the layout, which the distribution does not have and
which would be a change to the shape of the distribution rather than to its content.
