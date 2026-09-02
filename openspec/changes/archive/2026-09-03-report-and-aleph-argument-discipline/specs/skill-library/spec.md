## ADDED Requirements

### Requirement: Reporting skills state a rendering and citation discipline

A skill that governs a written product handed to a decision-maker SHALL state the discipline for
rendering that product into a second format and for citing identifiers inside it. `briefing-reporting`
is that skill and SHALL carry all three of the following.

It SHALL require a second format — HTML, PDF, a deck — to be produced with a real parser for that
format, and SHALL name a hand-written line-prefix pass as the thing not to do. It SHALL state the
reason rather than only the rule: inline emphasis, code spans, tables and inline links are what a
regex converter drops, and it drops them without erroring, so the output is well-formed and wrong in
the places nobody inspected. It SHALL require the analyst to probe for an available parser and to say
which one was used, and SHALL NOT name a specific parser, which is a property of the host rather than
of the distribution.

It SHALL require an identifier cited in the product to be carried whole, however long, and SHALL
state that a shortened hash or a truncated id reads as a citation while being unlookupable. It SHALL
separate display from record: the rendering may shorten what is *displayed*, never what is
*recorded*.

It SHALL require a rendered product to be verified twice over — that no source-format tokens survive
in the output, and that a sample of its evidence references has been resolved against the system that
issued them — and SHALL name a link count as detecting neither failure, because a truncated
identifier produces a well-formed link to nothing and a count is satisfied identically by working and
broken references.

#### Scenario: A rendered product is converted with a parser

- **WHEN** the reporting skill's method is read by an analyst who must also produce HTML, PDF or a deck
- **THEN** it requires a real parser for that format, names a hand-written line-prefix or regex pass
  as dropping inline emphasis, code spans, tables and inline links without erroring, and requires the
  parser actually used to be named

#### Scenario: Identifiers are cited in full

- **WHEN** the reporting skill's method is read
- **THEN** it requires the whole identifier to be carried into the product however long it is, states
  that a truncated identifier cannot be looked up, and confines shortening to what is displayed
  rather than what is recorded

#### Scenario: A rendered product's references are resolved, not counted

- **WHEN** the reporting skill's signals and outputs are read
- **THEN** a finished rendered product requires both that no source-format tokens survive and that a
  sample of its references has been resolved against the issuing system, and a link count is named as
  proving neither

### Requirement: Aleph tool calls name the identifier argument and are built in code

`aleph-entity-graph` SHALL state how a call to the Aleph tools is constructed, in a subsection placed
with its tooling paragraph rather than inside its numbered method, because argument construction
applies to every call at every step rather than once per investigation.

It SHALL name `entity_id` as the identifier argument on every tool that takes one — `get_entity`,
`get_entity_text`, `expand_entity`, `entity_tags`, `similar_entities` — SHALL name `profile_id` for a
profile, and SHALL name `id` and `entity` as the wrong keys. It SHALL state that an unrecognised
argument key is dropped rather than refused, and SHALL name both resulting outcomes: a failure naming
a missing `entity_id`, or a call that reaches the server and returns a not-found which reads as a bad
identifier rather than as a bad call. It SHALL state that the second outcome is why the mistake
repeats undetected.

It SHALL require the argument object to be built with a JSON serialiser inside a script rather than
written by hand, SHALL name quoted-phrase escaping as the failure — a `q` joining quoted phrases with
`OR` needs every inner quote escaped, and a hand-written object escapes the first phrase and then
stops — and SHALL cross-reference `analytic-tooling-scripting` as the same path already recommended
for replacing many interactive calls with one loop.

Every argument name stated SHALL be traceable to the `aleph-mcp` server's own tool signatures rather
than to recollection of them.

#### Scenario: The identifier argument is named

- **WHEN** the tooling section of `aleph-entity-graph` is read
- **THEN** `entity_id` is named as the identifier argument on `get_entity`, `get_entity_text`,
  `expand_entity`, `entity_tags` and `similar_entities`, `profile_id` is named for a profile, and
  `id` and `entity` are named as wrong

#### Scenario: An unrecognised argument key is named as silently dropped

- **WHEN** the same section is read
- **THEN** it states that an unrecognised key is dropped rather than refused, and names the
  not-found reply that reads as a bad identifier instead of a bad call as the reason the mistake
  survives repetition

#### Scenario: Query arguments are serialised rather than hand-written

- **WHEN** an analyst must issue a search whose `q` carries more than one quoted phrase
- **THEN** the skill requires the argument object to be serialised in code, names inner-quote
  escaping past the first phrase as the failure, and points at `analytic-tooling-scripting`
