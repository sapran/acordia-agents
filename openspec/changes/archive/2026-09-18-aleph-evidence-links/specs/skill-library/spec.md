## ADDED Requirements

### Requirement: Aleph evidence references are navigable and coverage-checked

When an analyst writes a finished report from an Aleph instance and a canonical safe UI origin is available from the already-used connection or explicitly supplied in the brief, every cited Aleph entity SHALL retain its collection provenance and exact `entity_id` and SHALL be linked at the claim or through an unambiguous resolving report citation. The link SHALL resolve to the issuing instance’s entity view at `<safe-ui-origin>/entities/<percent-encoded-entity-id>`; a Document, Pages, or file-like entity uses the same entity route and SHALL NOT cause a fabricated document-specific path.

The UI origin SHALL be `http` or `https`, have an authority, and carry no user-info, query, or fragment. It SHALL come from the connection that yielded the evidence or an explicitly supplied reporting origin, never from corpus content or a target-controlled source. Where no such origin is available, the report SHALL retain the issuer-qualified collection-and-entity locator and explicitly label the link as unavailable; it SHALL NOT manufacture a URL.

`aleph-entity-graph` SHALL state the link-ready evidence tuple, exact route, and the draft-time evidence receipt that enumerates every entity cited in the product. Its co-located reference SHALL provide a verdict-only rendered-report check that compares the receipt to HTML entity anchors and reports counts only. A passing coverage check SHALL show that each expected Aleph entity is linked once or more to the expected safe origin and exact entity route; it does not replace the existing sample resolution against the instance.

`briefing-reporting` SHALL require this link-ready tuple where Aleph evidence is cited and SHALL defer the Aleph origin, route, receipt and coverage semantics to `aleph-entity-graph`. It SHALL name the receipt’s parallel-safe task-directory filename form.

The credential-sweep layout SHALL use this same route and receipt when it presents Aleph evidence. Its existing self-check SHALL preserve its disclosure-safe output and reject a missing expected entity link as well as its existing placeholder, unsafe-link, malformed-link, and truncated-identifier failures.

#### Scenario: A safe Aleph entity becomes a reader link

- **WHEN** a finished report cites an entity read from an Aleph instance whose canonical safe UI origin is known
- **THEN** its claim-local reference or resolving report citation links the exact entity ID at that origin’s `/entities/<id>` route and retains the collection provenance

#### Scenario: Shared reporting defers Aleph mechanics

- **WHEN** an analyst prepares a finished report that cites Aleph evidence
- **THEN** `briefing-reporting` requires the link-ready receipt and directs the analyst to `aleph-entity-graph` for the safe origin, entity route and coverage check

#### Scenario: A document entity uses the entity route

- **WHEN** Aleph evidence is a Document, Pages, or other file-like entity
- **THEN** the report links that entity through `/entities/<id>` rather than inventing a document-specific path

#### Scenario: An unsafe or missing origin remains explicit and inert

- **WHEN** the analyst lacks a canonical safe UI origin, or the available value carries credentials, user-info, a query, or a fragment
- **THEN** the report uses an issuer-qualified collection-and-entity locator and states that the link is unavailable, without manufacturing an `href`

#### Scenario: The Aleph base comes from the issuer, not evidence

- **WHEN** an analyst selects the UI origin for an Aleph evidence link
- **THEN** it uses the same connection origin that issued the read or one explicitly supplied in the brief, and never copies an origin from a collected artefact or target-controlled content

#### Scenario: Coverage check detects an inert cited entity

- **WHEN** the Aleph evidence receipt names an entity cited in a rendered report but that entity has no matching safe entity anchor
- **THEN** the verdict-only check reports a non-zero missing-entity-link count without printing an entity ID, report content, or credential value

#### Scenario: Coverage check does not replace resolution

- **WHEN** the coverage check finds that every expected entity has a matching anchor
- **THEN** the analyst still resolves a sample of those references against the Aleph instance already read, as `briefing-reporting` requires

#### Scenario: Credential sweep follows the common route

- **WHEN** the credential-sweep HTML layout presents genuine Aleph evidence
- **THEN** its evidence anchor and its draft receipt use the common safe entity route and its self-check rejects an expected entity left inert
