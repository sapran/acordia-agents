## ADDED Requirements

### Requirement: Aleph file class is discriminated by schema, not by filename text

`aleph-entity-graph` SHALL state how the class of a file is established in an Aleph corpus, because the
default move — searching the file extension — measures a different population from the one asked
about, and does so without any symptom other than a result count.

The skill SHALL state that Aleph's ingest assigns every file a FollowTheMoney schema, so file class is
answered by the same faceting the skill already teaches: `schemata="Document"` with
`facets=["schema"]`, whose buckets carry true counts, and a `filters={"schema": [...]}` constraint to
enumerate the slice. It SHALL name the purpose-built classes an analyst hunting configuration material
is looking for — `VPNConfig`, `RDP`, `KeePassDB` — alongside the generic ones.

The skill SHALL state that the `mime_type` and `extension` facets MAY return zero buckets on an
instance, that this is an indexing property of the instance rather than evidence about the corpus, and
that it removes no discriminator because `schema` is populated regardless. The inference it must
forbid is explicit: "there is no way to slice by file type here" is the wrong reading, and it is the
reading that sends an analyst to the filename.

The skill SHALL state that a format word or extension in `q` measures **mentions rather than
artefacts**, because `q` searches text and matches every document that names the format. It SHALL
carry the measured evidence rather than asserting the effect: on one collection an extension query
across six config formats returned 13,607 hits — 10,577 web pages and 2,259 spreadsheets — with the
reported total at the 10,000 cap, where the schema filter for the same classes returned 36 files, 19
KeePass databases and 17 RDP profiles; and a `kdbx OR KeePass` text query returned 2,684 against those
same 19. It SHALL place the extension form as a cross-check on a set already in hand and SHALL NOT
present it as a recall mechanism.

The skill SHALL state that a fielded filename query is not a rescue: `file_name` is a filter value
rather than a wildcard-searchable field, a `file_name:*.ext` form returned nothing, and the analyst
SHALL filter it exactly when the name is known and scope by schema otherwise.

The skill SHALL state the structural-marker route for material no facet can isolate — a configuration
pasted into a chat message is an ordinary `HyperText` page, and a WireGuard or AmneziaWG config carries
no extension at all — as two or more format tokens ANDed, with the measured example returning 9 rows
of which 7 sat inside chat pages. It SHALL point at `credential-harvest-triage`'s
`references/credential-patterns.md` as the marker set rather than restating the strings.

The skill SHALL state that a marker discriminates by its **rarest token and never by its
punctuation**, because the index discards punctuation: a `"</key>"` form reduces to the token `key`
and returned the cap, as did a bracketed-section marker ANDed with two-character parameter names. It
SHALL instruct the analyst to price a candidate marker at `limit=0` and read its `schema` facet before
building on it, and SHALL state that a marker whose count looks like the cap is not a marker.

The skill SHALL connect its existing 66% rule to this failure: adding vocabulary widens a result set
because only two-thirds of the terms need match, so the same intent spread across synonyms returned
4,406 where the tight structural form returned 9. It SHALL state that this is language-independent —
translating a synonym list does not rescue it, and a corpus in another language raises the temptation
rather than the yield.

The coverage statement the skill already requires SHALL additionally separate the classes enumerated
by schema from the formats reached only by marker, and SHALL name any marker whose result set hit the
cap as sampled rather than enumerated.

#### Scenario: File class is established by schema before any filename search

- **WHEN** an analyst must find the configuration files in an Aleph collection
- **THEN** the skill directs a `schema` facet and a `filters={"schema": [...]}` enumeration first, and places the extension form as a cross-check rather than the recall step

#### Scenario: Empty MIME facet does not imply an absent discriminator

- **WHEN** the `mime_type` or `extension` facet returns zero buckets on an instance
- **THEN** the skill has already stated that this is an instance indexing property rather than evidence, and that `schema` remains the populated discriminator

#### Scenario: Mention counts are not artefact counts

- **WHEN** the subsection's evidence is read
- **THEN** it carries the measured contrast between an extension query's 13,607 mention hits at the reported cap and the 36 files the schema filter enumerates for the same classes

#### Scenario: A format with no schema is reached by structural marker

- **WHEN** the material sought is a configuration pasted into a message, or a format Aleph's ingest assigns no schema of its own
- **THEN** the skill directs a structural marker of two or more ANDed format tokens and points at the pattern reference for the strings

#### Scenario: A candidate marker is priced before it is trusted

- **WHEN** an analyst proposes a new structural marker
- **THEN** the skill requires a `limit=0` check with its `schema` facet read first, and states that punctuation is discarded so the discriminating power must come from a rare token

#### Scenario: Added vocabulary is named as widening, in any language

- **WHEN** an analyst considers adding synonyms, including in the corpus's own language, to narrow a result set
- **THEN** the skill states that the 66% term rule makes this widen rather than narrow, with the measured 4,406-against-9 contrast, and that structure rather than vocabulary discriminates

#### Scenario: Coverage separates enumerated classes from marker-reached formats

- **WHEN** the coverage statement for an Aleph credential search is written
- **THEN** it names which classes were enumerated by schema, which formats were reached only by marker, and which markers hit the cap and were therefore sampled

### Requirement: Credential pattern reference carries config-file structural markers

The credential pattern reference at
`acordia-analysts/skills/credential-harvest-triage/references/credential-patterns.md` SHALL carry a
`## Config-file structural markers` section holding the skeleton a real configuration file carries, as
against the name it happens to have. The section SHALL cover WireGuard/AmneziaWG, OpenVPN, PuTTY,
IPsec/IKE and Windows RDP. Markers SHALL be treated as non-secret locators in the same way as the
asset fingerprints already in the file: they identify a file class or search context and SHALL NOT be
treated as credential values or as permission to validate access.

The section SHALL name the AmneziaWG obfuscation parameters (`Jc`/`Jmin`/`Jmax`, `S1`/`S2`,
`H1`–`H4`) as a file-level discriminator for the DPI-resistant WireGuard fork, and SHALL state that
they are not usable as search terms because they are short, common tokens.

The section SHALL state that a pattern behaves differently in the reference's two consumption paths,
because a reader arriving from either one must be told: over raw bytes the whole pattern applies,
punctuation included, while as an Aleph `q` term the index discards punctuation so only a rare token
survives. It SHALL name the subset whose tokens do survive and SHALL point at `aleph-entity-graph`
for the platform reasoning rather than restating it.

The section SHALL state that a configuration's passphrase commonly sits in a different document from
the configuration itself, that a located config is therefore the starting point for a pivot to its
carrier — container, thread or correspondent — and SHALL NOT recommend a corpus-wide
password-vocabulary query for that purpose. It SHALL carry the measured reason: the obvious forms
returned 1,911 and 7,084 hits of effectively pure chat noise, and the specific phrase an analyst
expects returned nothing at all.

Every marker string SHALL be traceable to upstream format documentation or to an observed corpus hit.
A string that cannot be established SHALL be omitted rather than included from recall.

#### Scenario: Structural markers are present alongside the existing sections

- **WHEN** the pattern reference is inspected
- **THEN** the existing credential-value sections and the asset-fingerprint section remain present, and the config-file structural-marker section is also present

#### Scenario: Markers are non-secret locators

- **WHEN** a structural marker is used in triage
- **THEN** it identifies a file class or search context, and does not constitute a credential value or trigger validation or live provider contact

#### Scenario: The two consumption paths are distinguished

- **WHEN** an analyst takes a marker from the reference to use as an Aleph query term
- **THEN** the section has already stated that punctuation is discarded in the index and named the subset of tokens that survive, rather than presenting the raw-bytes regex as a search string

#### Scenario: AmneziaWG is reachable and its parameters are not search terms

- **WHEN** the sought material is an AmneziaWG configuration, which carries no extension and no dedicated schema
- **THEN** the section supplies the `[Interface]`/`PrivateKey`/`PresharedKey` structural form and marks the obfuscation parameters as a file-level discriminator rather than a query

#### Scenario: The covering message is reached by pivot rather than by sweep

- **WHEN** the passphrase for a located configuration is sought
- **THEN** the section directs a pivot from the artefact to its carrier and states, with measured figures, why a corpus-wide password-vocabulary query is not the route
