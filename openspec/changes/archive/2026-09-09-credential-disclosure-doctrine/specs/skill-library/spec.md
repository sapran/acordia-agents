## ADDED Requirements

### Requirement: Credential handling is a routing rule gated on ownership

`credential-harvest-triage` SHALL state where a credential value may go rather than forbidding it
everywhere, and SHALL gate every permission on whose credential it is.

It SHALL require **ownership** to be classified before any other handling decision, with four
values — `target`, `operation`, `third-party`, `unknown` — and SHALL state that `unknown` is handled
as `operation` until adjudicated, because one collected artefact holds both kinds and the error costs
are asymmetric.

It SHALL grant the following to a **target-owned** credential and to a corporate **third-party** one,
and to no other ownership value: the value may be recorded in a credential file and carried into the
finished product. It SHALL state that an **operation-owned** credential — the operation's own tooling,
C2 authentication, staging accounts — is written nowhere at all, because protecting the operation's
own material is operational security rather than evidence handling (`Monte`#operational-security). It
SHALL state that a **personal third-party** credential is carried by classification alone, because
disclosing an individual's own credential to their employer harms someone who is not party to the
operation.

It SHALL carry six handling rules, applying to every ownership value:

- A command reading credential-bearing material terminates in a file write rather than in standard
  output, and the analyst works from the receipt it returns — type, count and source location. It
  SHALL state the reason: a printed value reaches the session's displayed output, the model's context
  and the session transcript together, because one act feeds all three, and a redirected value
  reaches none of them.
- A value is read when a judgement needs it — reuse, strength, correlation against a value seen
  elsewhere — and not as the default way of handling material. It SHALL state the reason: acquiring
  awareness costs exposure (`Monte`#operational-security), and information past the minimum a
  judgement needs raises confidence without raising accuracy (`Heuer`#information-quantity).
- A value reaches another reader only as a file that reader opens, never in a reply, a dispatch, a
  hand-back or a summary, and never quoted into prose composed in-session. It SHALL state that this is
  what permits a product to disclose what its recipient owns: a product written to disk is a file and
  the same product returned in-message is not, so a product carrying values is written rather than
  returned.
- Values are held in a credential file distinct from the analyst's working notes, with the notes
  carrying the classification and a pointer to that file rather than the value, because those notes are
  read by whoever fuses the analyst's work.
- Values that ownership refused are purged from the extraction file once ownership is settled, because
  extraction runs before classification and its output therefore holds every ownership at once.
- Values live in the credential file and in the finished product, and nowhere else. It SHALL name
  durable memory, a commit, and any upstream destination — a network call, an API argument, a
  target-owned system, a third-party service — as excluded, with no ownership value exempt from the
  upstream exclusion.

It SHALL NOT claim that any of this is enforced. These are instructions to an analyst, and the
distribution ships no mechanism that inspects a value in flight.

#### Scenario: Ownership is classified before handling

- **WHEN** the triage skill's classification schema is read
- **THEN** it carries an `ownership` field taking `target`, `operation`, `third-party` or `unknown`,
  and states that `unknown` is handled as `operation` until adjudicated

#### Scenario: Ownership decides what may be written

- **WHEN** the triage skill's guardrails are read
- **THEN** a target-owned value and a corporate third-party one may be recorded in a credential file
  and carried into the product, an operation-owned value is written nowhere at all, an unsettled one is
  handled as operation-owned, and a personal third-party one is carried by classification alone

#### Scenario: The six handling rules are present

- **WHEN** the triage skill's guardrails are read
- **THEN** they require a credential-reading command to terminate in a file write rather than standard
  output and state that one act feeds displayed output, context and transcript together; require a
  value to be read when a judgement needs it rather than by default; permit a value to cross only as a
  file its reader opens and never in a reply, dispatch, hand-back or summary; hold values in a
  credential file distinct from the working notes; require values ownership refused to be purged from
  the extraction file; and confine values to that file and the product, naming durable memory, a commit
  and every upstream destination as excluded

#### Scenario: No enforcement is claimed

- **WHEN** the triage skill's guardrails are searched for a claim that a rule is enforced, blocked or
  prevented by the distribution
- **THEN** no such claim is found

### Requirement: Durable memory holds no credential value at any ownership

`operational-memory` SHALL continue to forbid writing a credential value into the memory record for
every ownership value, target-owned included, and SHALL state the reason that distinguishes it from
the working notes this change permits: the memory record is durable and is read by everyone who comes
next.

#### Scenario: Memory keeps the absolute prohibition

- **WHEN** `operational-memory` is read after this change
- **THEN** it still forbids writing a secret into the memory, carries the classification instead, and
  the prohibition is not qualified by ownership

## MODIFIED Requirements

### Requirement: Credential-extraction sections in credential-adjacent skills

Seven skills SHALL each carry a named `## Credential extraction` section covering, for that skill's domain: artefact locations, canonical extraction tools, and portable extraction patterns. The seven are `disk-memory-forensics`, `identity-directory-trust`, `log-artefact-interpretation`, `cloud-controlplane-analysis`, `web-api-authflow-analysis`, `os-host-internals`, and `implant-payload-re`. The section SHALL be additive — it does not replace the existing `Objective`, `When to use`, `Method`, or `Signals / outputs` sections.

Each section SHALL close by stating where its extraction output goes, deferring classification to
`credential-harvest-triage` and requiring the extraction to terminate in a file write rather than in
standard output. A section MAY additionally name the non-secret identifier that cites a finding in
its domain — an IAM path or ARN, a cookie name or claim identifier, a binary offset, a log file path
— and SHALL NOT state that a credential value may never be recorded, which the ownership-gated rule
replaces.

#### Scenario: Section present in each credential-adjacent skill

- **WHEN** any of the seven skills' `SKILL.md` is inspected
- **THEN** it contains a `## Credential extraction` H2 section with domain-specific artefact locations, tools, and patterns

#### Scenario: Enrichment is additive, not a rewrite

- **WHEN** an enriched skill is compared against its pre-enrichment content
- **THEN** the existing sections are unchanged and only the new `## Credential extraction` section is added

#### Scenario: Passive posture preserved

- **WHEN** a credential-extraction section is read
- **THEN** it describes analysis of already-collected material only, references no active credential validation, and stores no raw credential values in its examples

#### Scenario: Each section routes its output

- **WHEN** the closing paragraph of any of the seven `## Credential extraction` sections is read
- **THEN** it defers classification to `credential-harvest-triage` and requires the extraction to
  terminate in a file write rather than in standard output

### Requirement: `credential-harvest-triage` skill exists

The library SHALL contain a skill `acordia-analysts/skills/credential-harvest-triage/SKILL.md` providing (a) a classification schema for credential findings (ownership, type, subtype, status, scope, source, reuse potential, priority), (b) a triage procedure that begins with **inventory**, then performs a **bucket partition** step assigning material to a leg-owned bucket, then scans, classifies, correlates, prioritises, and reports, and (c) a **pointer** to a co-located pattern-library reference file for common credential material. It SHALL declare its cross-cutting/procedural nature in its body and SHALL NOT be added as a row to the competency grid.

The **bucket partition** step SHALL enumerate five buckets and their target legs:

- Bucket A — identity / directory / cloud-controlplane material → `terrain-analyst`
- Bucket B — host-forensic material (memory, SAM, DPAPI, keychain, shadow) → whichever leg holds the host under analysis
- Bucket C — web / API auth material → `terrain-analyst`
- Bucket D — log-artefact material → `overwatch-analyst`
- Bucket E — implant / payload RE material → cross-cutting via `implant-payload-re`, reported to `cyber-analyst`, which holds the fused picture itself

Each bucket's slice SHALL be dispatched with only that slice. The procedure SHALL state that per-leg classifications feed back into `multi-source-fusion` for cross-leg correlation.

#### Scenario: Triage skill loads in a harness

- **WHEN** a harness loads the analyst pillar
- **THEN** `credential-harvest-triage` is discovered from `acordia-analysts/skills/` and is invokable

#### Scenario: Body carries schema, procedure, and pattern library

- **WHEN** the triage skill is inspected
- **THEN** it contains a classification schema, a bucket-partition step, a numbered triage procedure downstream of the partition, and a pointer to the pattern library at `references/credential-patterns.md`

#### Scenario: Bucket partition maps to existing legs

- **WHEN** the bucket-partition step is read
- **THEN** every bucket routes to one of `terrain-analyst`, `overwatch-analyst`, `cyber-analyst`, or the cross-cutting `implant-payload-re` skill, and no bucket routes to a leg not on the current whitelist

#### Scenario: No bucket names a retired leg

- **WHEN** the bucket-partition step is searched for `target-analyst` or `fusion-analyst`
- **THEN** neither is found, because neither agent exists

#### Scenario: Not a grid row

- **WHEN** the competency grid in `docs/roles/operational-analyst.md` is inspected
- **THEN** no row corresponds to `credential-harvest-triage`

#### Scenario: Schema carries ownership

- **WHEN** the triage skill's classification schema is inspected
- **THEN** `ownership` is one of its fields

### Requirement: Reporting skills state a rendering and citation discipline

A skill that governs a written product handed to a decision-maker SHALL state the discipline for
rendering that product into a second format and for citing identifiers inside it. `briefing-reporting`
is that skill and SHALL carry all three of the following.

It SHALL require a second format — HTML, PDF, a deck — to be produced with a real parser for that
format, and SHALL name a hand-written line-prefix pass as the thing not to do. It SHALL state the
reason rather than only the rule: inline emphasis, code spans, tables and inline links are what a
regex converter drops, and it drops them without erroring, so the output is well-formed and wrong in
which one was used, and SHALL NOT name a specific parser, which is a property of the host rather than
of the distribution. Because the product carries verbatim corpus material, it SHALL also require the
parser's raw-HTML passthrough to be disabled and markup inside quoted evidence to be escaped rather
than rendered — a real parser renders what a regex pass left inert, into the reader's browser.

It SHALL require an identifier cited in the product to be carried whole, however long, and SHALL
state that a shortened hash or a truncated id reads as a citation while being unlookupable. It SHALL
separate display from record: the rendering may shorten what is *displayed*, never what is
*recorded*. It SHALL confine that requirement to identifiers whose purpose is to be resolved, and
SHALL state that a **target-owned** credential is carried into the product whole, per the ownership
gate in `credential-harvest-triage`, because the recipient owns it and cannot remediate from a
classification alone. It SHALL state that an operation-owned credential is never carried into a
product at any length, that an unadjudicated one is treated as operation-owned, and that a personal
identifier — including a personal third-party credential — is carried only as far as the judgement
requires.

It SHALL require a rendered product to be verified twice over — that no source-format tokens survive
in the output, and that a sample of its evidence references has been resolved against the system that
issued them — and SHALL name a link count as detecting neither failure, because a truncated
identifier produces a well-formed link to nothing and a count is satisfied identically by working and
broken references. It SHALL confine that resolution to the system the analyst already read from,
using the same read call that produced the reference, and SHALL forbid resolving a reference that
originates inside the cited material or that addresses a target-owned or third-party system, which
would make writing the report an active touch. Because a product may now carry credential values, it
SHALL require that verification to be performed against the draft or by a check that reports a
verdict, and SHALL forbid reading a rendered product carrying credential values back into the
session, which would place every value it carries into the transcript the routing rule keeps them out
of.

#### Scenario: A rendered product is converted with a parser

- **WHEN** the reporting skill's method is read by an analyst who must also produce HTML, PDF or a deck
- **THEN** it requires a real parser for that format, names a hand-written line-prefix or regex pass
  as dropping inline emphasis, code spans, tables and inline links without erroring, requires the
  parser actually used to be named, and requires raw-HTML passthrough to be off with markup inside
  quoted evidence escaped

#### Scenario: Identifiers are cited in full

- **WHEN** the reporting skill's method is read
- **THEN** it requires the whole identifier to be carried into the product however long it is, states
  that a truncated identifier cannot be looked up, confines shortening to what is displayed rather
  than what is recorded, and carries a target-owned credential into the product whole per the
  ownership gate

#### Scenario: Ownership decides what a product discloses

- **WHEN** the reporting skill's citation discipline is read
- **THEN** an operation-owned credential is excluded from the product at any length, an unadjudicated
  one is treated as operation-owned, and a personal identifier including a personal third-party
  credential is carried only as far as the judgement requires

#### Scenario: A rendered product's references are resolved, not counted

- **WHEN** the reporting skill's signals and outputs are read
- **THEN** a finished rendered product requires both that no source-format tokens survive and that a
  sample of its references has been resolved against the issuing system the analyst already read
  from, a link count is named as proving neither, and resolving a reference originating inside the
  cited material is forbidden

#### Scenario: A product carrying credentials is not read back into the session

- **WHEN** the reporting skill's verification discipline is read
- **THEN** verification is performed against the draft or by a check reporting a verdict, and reading
  a rendered product carrying credential values back into the session is forbidden
