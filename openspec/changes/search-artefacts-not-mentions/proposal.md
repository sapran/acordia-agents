## Why

`aleph-entity-graph` teaches an analyst to facet before pulling rows, and `credential-harvest-triage`
teaches a first-pass scan over a pattern library. Neither says how to find a *configuration file* in a
corpus, and the gap has a default answer that does not work: search the file extension.

An extension in `q` is free text, so it matches every document that **mentions** the format — wiki
pages, inventory spreadsheets, vendor manuals — rather than the files that **are** one. Measured on
collection `874` of the operator's instance (2026-09-13): `.ovpn OR .rdp OR .ppk OR .pfx OR .p12 OR
.dst` returned 13,607 hits, of which 10,577 were web pages and 2,259 spreadsheets, and the reported
total sat at the 10,000 cap — an unenumerated set, which this skill already teaches the analyst to
treat as unreadable. The same collection holds 36 files of those classes. `kdbx OR KeePass` returned
2,684 against 19 actual KeePass databases.

Three separate defects made that the analyst's best available move, and each is a sentence the skills
do not carry:

1. **The file-class discriminator was believed absent.** The `mime_type` and `extension` facets return
   zero buckets on this instance, and the analyst reasonably read that as "no way to slice by file
   type here". It is an indexing property of the instance, not evidence about the corpus, and it
   removes nothing: Aleph's ingest assigns every file an FtM **schema**, the `schema` facet is
   populated, and it carries true counts. `filters={"schema": ["VPNConfig","RDP","KeePassDB"]}`
   returned exactly 36 rows — 19 KeePass databases and 17 RDP profiles — where the extension query
   returned an unenumerable 13,607.

2. **No guidance existed for a format with no schema.** A config pasted into a chat message is a
   `HyperText` page like any other, so no facet isolates it, and a WireGuard or AmneziaWG config
   carries no extension at all. What distinguishes it is the skeleton of the format:
   `"[Interface]" AND "PrivateKey ="` returned 9 rows, every one a configuration body, seven of them
   inside chat pages. The pattern library held no structural marker for any config format.

3. **A marker's discriminating power was never attributed to the right thing.** Aleph's index discards
   punctuation, so a marker that looks distinctive to a reader can collapse to a common word:
   `"</key>"` reduces to `key`, and `"[Interface]" AND ("Jc" OR "S1" OR "H1")` both returned the
   10,000 cap. `PrivateKey` works because the token is rare, not because of the bracket. Nothing said
   so, and the neighbouring correct instinct — add more vocabulary, in the corpus's own language —
   makes it worse: the same intent spread across synonyms
   (`(PrivateKey OR PresharedKey OR "[Interface]") AND (впн OR vpn OR amnezia OR wireguard OR туннел)`)
   returned 4,406. The 66% rule already in the skill is why, and it was never connected to this.

The cost was not only volume. An AmneziaWG deployment — the DPI-resistant WireGuard fork widely
deployed in Russia — was reachable only by the structural form, and an extension-only sweep would have
missed that credential class entirely.

## What Changes

- **`aleph-entity-graph`** gains a `### Searching for artefacts rather than mentions` subsection:
  schema is the file-class discriminator; empty `mime_type`/`extension` facets are an indexing
  property rather than evidence; a format word in `q` measures mentions, with the measured figures;
  `file_name` is a filter value and not a wildcard-searchable field; structural markers for formats no
  facet can isolate; the punctuation-is-discarded rule and the instruction to price a candidate marker
  at `limit=0` before building on it; and the connection from the existing 66% rule to why added
  vocabulary widens in any language.
- **`credential-patterns.md`** gains a non-secret `## Config-file structural markers` section —
  WireGuard/AmneziaWG, OpenVPN, PuTTY, IPsec/IKE and Windows RDP — plus the statement that the same
  pattern behaves differently over raw bytes than as an Aleph `q` term, and a carrier-pivot rule for
  the passphrase that lives in a different document from the config.
- **`credential-harvest-triage`** step 3 establishes file class by schema before scanning an Aleph
  slice, and names the extension form as a cross-check rather than the recall mechanism.
- **`docs/roles/sources.md`** records the literature search as a gap: the canon grounds the adjacent
  analytic claim and holds nothing on query construction, so the addition carries no attribution.
- Version `6.12.0` → `6.13.0` across the three JSON files.

Capability touched: `skill-library` — two ADDED requirements. Nothing published is falsified: the
`aleph-entity-graph` and pattern-reference requirements enumerate body sections additively, and no
published requirement or scenario asserts anything about extensions, MIME types or file class.

## Impact

`acordia-analysts/skills/aleph-entity-graph/SKILL.md`,
`acordia-analysts/skills/credential-harvest-triage/SKILL.md` and its
`references/credential-patterns.md`, `docs/roles/sources.md`, the three version literals.

The competency grid does not move. Both edited skills are `procedural` with `grid_row: null`, so the
bijection is untouched and no column gains or loses a mark — this is technique detail inside existing
competencies rather than a new one.

The change is passive throughout. Every figure quoted was obtained with read-only search and faceting
at `limit=0`; no credential value was read, printed or recorded, and the markers locate material
without conferring permission to validate it.
