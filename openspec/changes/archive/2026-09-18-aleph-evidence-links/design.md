## Context

See `proposal.md` for the failure. The reporting contract is intentionally centralised in `briefing-reporting`; Aleph semantics and collection provenance belong to `aleph-entity-graph`; the credential sweep owns a fixed HTML form. The repository is markdown-only, so product verification must ship as an inspectable, fenced, verdict-only script in a markdown reference rather than a runtime or repository gate.

The selected ACORDIA passage supports protecting analysis as a core function. It does not prescribe URL construction. The entity route, UI-origin handling and receipt check are measured procedural details and have no `doctrine_source` attribution.

## Goals / Non-Goals

**Goals:**

- Make a safe, known Aleph evidence source directly navigable from a report.
- Capture the identifier, collection and safe origin at drafting time, so agents do not attempt error-prone post-hoc link wrapping.
- Mechanically detect an expected Aleph entity left inert in a rendered report without copying report or credential content into verifier output.
- Preserve source safety: no target-controlled, signed, credential-bearing or query/fragment URL becomes a link.

**Non-Goals:**

- No agent-prompt or command-wrapper duplication.
- No new runtime, dependency, report generator, universal report format, or repository-wide report-artifact gate.
- No request to Aleph beyond the existing read used to obtain and sample-resolve evidence.
- No document-specific Aleph route, because file-like material is represented by entities and the supplied reader route is `/entities/<id>`.

## Decisions

### One generic obligation, one Aleph implementation

`briefing-reporting` will require navigable evidence when a safe canonical source locator exists, and direct Aleph work to `aleph-entity-graph`. The latter will own the exact tuple and route. This keeps report policy central while placing platform mechanics beside the platform’s data model.

### The safe base has two authorised sources

The report base is the `ALEPHCLIENT_HOST` origin used by the direct HTTP path, or an explicitly supplied UI origin where the UI is separately hosted. The analyst removes any trailing slash and rejects a value with user-info, a query or a fragment. A base taken from collected material is never acceptable. This resolves the old `{ALEPH}` placeholder failure by making the base an input that must be established before the first report citation, not a token substituted at the end.

### One entity route covers documents and files

Aleph documents and file-like records are entities. The canonical reader link is `<base>/entities/<percent-encoded entity_id>`. The entity identifier remains exact in `href`; display may shorten only after the complete value is recorded.

### A receipt makes link coverage checkable

During drafting, the analyst creates a small task-directory receipt containing one row per cited Aleph entity: safe origin, collection ID, entity ID and optional offset. The report uses those records for its citations. A fenced Python check reads the receipt and rendered HTML, parses anchors, and reports only counts for expected, linked, missing, wrong-origin, wrong-route and unsafe links. It must blank disclosure bodies before any captured-string probe. A clean receipt-to-link comparison proves coverage, not that a remote entity is genuine; the existing sample resolution remains mandatory.

### Credential HTML reuses, rather than forks, the rule

The credential layout retains its fixed anatomy and disclosure constraints. Its evidence cells use the same receipt and entity route; its self-check gains the receipt input and a distinct missing-expected-link verdict. The generic Aleph reference owns the reusable procedure, while the specialist reference preserves its product-specific validation.

## Risks / Trade-offs

- An Aleph UI can be served at a different origin than its API. The explicit reporting-origin input covers that case; without it, the product reports an unavailable link rather than guessing.
- A receipt adds a small drafting artefact, but it replaces repetitive retrofitting and gives the checker an independent expected set.
- HTML parsing that relies on one literal anchor spelling would be blind to ordinary author variants. The check must parse anchors structurally enough to count elements and attributes, and mutation checks must exercise href-less anchors, reordered attributes, short IDs, wrong origins and report IDs left as inert text.
- The check cannot prove the reader is authorised or that an Aleph record is semantically correct. It deliberately limits itself to safe report construction and leaves live sample resolution to the already-authorised read path.