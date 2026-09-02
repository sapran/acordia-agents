## ADDED Requirements

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
SHALL state that a credential, token or key is not cited at all whatever its length and that a
personal identifier is carried only as far as the judgement requires — cited by classification and
fingerprint, per `credential-harvest-triage`.

It SHALL require a rendered product to be verified twice over — that no source-format tokens survive
in the output, and that a sample of its evidence references has been resolved against the system that
issued them — and SHALL name a link count as detecting neither failure, because a truncated
identifier produces a well-formed link to nothing and a count is satisfied identically by working and
broken references. It SHALL confine that resolution to the system the analyst already read from,
using the same read call that produced the reference, and SHALL forbid resolving a reference that
originates inside the cited material or that addresses a target-owned or third-party system, which
would make writing the report an active touch.

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
  than what is recorded, and excludes a credential, token or key from being cited at all

#### Scenario: A rendered product's references are resolved, not counted

- **WHEN** the reporting skill's signals and outputs are read
- **THEN** a finished rendered product requires both that no source-format tokens survive and that a
  sample of its references has been resolved against the issuing system the analyst already read
  from, a link count is named as proving neither, and resolving a reference originating inside the
  cited material is forbidden

### Requirement: Aleph tool calls name the identifier argument and are built in code

`aleph-entity-graph` SHALL state how a call to the Aleph tools is constructed, in a subsection placed
with its tooling paragraph rather than inside its numbered method, because argument construction
applies to every call at every step rather than once per investigation.

It SHALL name `entity_id` as the identifier argument on every tool that takes one — `get_entity`,
`get_entity_text`, `expand_entity`, `entity_tags`, `similar_entities` — SHALL name `profile_id` for a
profile, and SHALL name `id` and `entity` as the wrong keys. It SHALL state that a wrong key is
refused rather than dropped, because the tool's input schema is closed, so validation fails before
the call reaches Aleph and the reply carries two errors — one naming the missing `entity_id` and one
naming the unexpected key. It SHALL require the whole error text to be read, and SHALL state that the
diagnosis was lost in the measured run because the loop around the call parsed the error as JSON and
discarded the line naming the key. It SHALL distinguish that refusal from a genuine `not found (404)`,
which means the identifier itself is wrong rather than the call.

It SHALL require the argument object to be built with a JSON serialiser inside a script rather than
written by hand, SHALL name quoted-phrase escaping as the failure — a `q` joining quoted phrases with
`OR` needs every inner quote escaped, and a hand-written object escapes the first phrase and then
stops — and SHALL cross-reference `analytic-tooling-scripting` as the same path already recommended
for replacing many interactive calls with one loop. It SHALL state that on the HTTP fallback the same
discipline is met by the client's own parameter encoding rather than by shell interpolation, and
SHALL forbid interpolating a corpus-derived value into a shell command string.

Every argument name stated SHALL be traceable to the `aleph-mcp` server's own tool signatures rather
than to recollection of them.

#### Scenario: The identifier argument is named

- **WHEN** the tooling section of `aleph-entity-graph` is read
- **THEN** `entity_id` is named as the identifier argument on `get_entity`, `get_entity_text`,
  `expand_entity`, `entity_tags` and `similar_entities`, `profile_id` is named for a profile, and
  `id` and `entity` are named as wrong

#### Scenario: An unrecognised argument key is named as refused by name

- **WHEN** the same section is read
- **THEN** it states that a wrong key is refused rather than dropped, names the two validation errors
  the closed schema produces, requires the whole error text to be read, and distinguishes that
  refusal from a genuine not-found meaning a wrong identifier

#### Scenario: Query arguments are serialised rather than hand-written

- **WHEN** an analyst must issue a search whose `q` carries more than one quoted phrase
- **THEN** the skill requires the argument object to be serialised in code, names inner-quote
  escaping past the first phrase as the failure, points at `analytic-tooling-scripting`, and states
  that the `curl` path meets the rule by the client's parameter encoding rather than by shell
  interpolation
