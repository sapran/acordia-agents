## Design

### The failure in one line

An extension is a property of a *filename*; `q` searches *text*. The query an analyst reaches for
therefore measures the wrong population, and on a document-heavy corpus the wrong population is two
to three orders of magnitude larger than the right one.

```text
question asked:     which files in this collection are VPN / RDP / key-store configs?
query written:      q = ".ovpn OR .rdp OR .ppk OR .pfx OR .p12 OR .dst"   -> 13,607, capped
question answered:  which documents in this collection mention those words?
query that answers: filters = {"schema": ["VPNConfig","RDP","KeePassDB"]} -> 36
```

### Recall ladder, in the order it should be climbed

1. **Schema** — exact, enumerable, true facet counts. Answers every format Aleph's ingest recognises.
2. **Structural marker** — for a format with no schema, or an artefact pasted into a message rather
   than attached. Two or more format tokens ANDed, at least one of them rare.
3. **Extension / format word** — a cross-check on a set already in hand, never the recall step.

The ladder is the design: each rung exists because the rung above it cannot reach a specific class of
artefact, and the note that prompted this change had only the bottom rung.

### Measurements, collection `874`, 2026-09-13

Read-only, `limit=0`, faceted on `schema`. Obtained through an `aleph-mcp` build predating the
`collection` scope argument, so scope was passed as `filters={"collection_id": "874"}`; on the current
server the same scope is the required `collection` argument, and the figures are properties of the
corpus rather than of either build.

| Query | Reported total | What it actually is |
|---|---|---|
| `.ovpn OR .rdp OR .ppk OR .pfx OR .p12 OR .dst` | 10,000 (cap); facets sum 13,607 | 10,577 HyperText + 2,259 Table + 352 PlainText + 224 Image + 148 Pages + 30 Document + **17 RDP** |
| `filters={"schema": ["VPNConfig","RDP","KeePassDB"]}` | **36** | 19 KeePassDB + 17 RDP + 0 VPNConfig |
| `kdbx OR KeePass` | 2,684 | 19 of them KeePassDB |
| `"[Interface]" AND "PrivateKey ="` | **9** | 7 HyperText + 2 PlainText, all config bodies |
| `(PrivateKey OR PresharedKey OR "[Interface]") AND (впн OR vpn OR amnezia OR wireguard OR туннел)` | 4,406 | 3,592 HyperText — vocabulary noise |
| `"[Interface]" AND ("Jc" OR "S1" OR "H1")` | 10,000 (cap) | punctuation discarded, tokens too common |
| `"</key>"` family | 10,000 (cap) | reduces to the token `key` |
| `file_name:*.ovpn OR file_name:*.rdp OR file_name:*.kdbx` | **0** | `file_name` is a filter value, not a wildcard field |
| `facets=["mime_type","extension"]` | 0 buckets each | instance indexing property, not evidence |

### Why the guidance is split across two files

The Aleph-specific reasoning — facets, tokenisation, the cap — belongs in `aleph-entity-graph`, which
owns the platform. The per-format marker strings belong in `credential-patterns.md`, which the spec
already names as the single source of truth for detection patterns and which three other skills
inherit. Putting the strings in the Aleph skill would fork that source; putting the tokenisation rule
in the pattern file would bind a general pattern library to one platform.

The one sentence that must appear in **both** is that a pattern behaves differently in the two paths:
over raw bytes the full structural regex applies, as an Aleph `q` term only its rare token survives.
A reader arriving from either direction has to be told, so it is stated twice by design rather than by
oversight.

### Markers: what ships and why

Every string was checked against upstream format documentation, against the live corpus, or both. A
string that could not be established was dropped rather than shipped from recall:

- **WireGuard / AmneziaWG** — `[Interface]`, `PrivateKey =`, `PresharedKey =`; the obfuscation
  parameters `Jc/Jmin/Jmax`, `S1/S2`, `H1`–`H4` per Amnezia's own documentation, shipped as a
  file-level discriminator and explicitly **not** as a search term, because they are two-character
  tokens that return the cap.
- **OpenVPN** — `auth-user-pass`, `remote-cert-tls server`, `key-direction`, `tls-auth`, and the
  inline `<cert>`/`<key>`/`<tls-auth>`/`<tls-crypt>` block.
- **PuTTY** — `PuTTY-User-Key-File-[23]:`, `Private-Lines:`, `Private-MAC:`, from PuTTY's own PPK
  appendix (formats 2 and 3; format 1 never shipped in a release).
- **IPsec / IKE** — `crypto isakmp key`, `pre-shared-key`, `crypto ikev2 keyring`, each present in the
  live corpus.
- **Windows RDP** — `full address:s:`, `username:s:`. The encrypted-password field was **dropped**: it
  returned nothing in the corpus and could not be established from a source, so the honest cost is one
  missing line rather than one invented pattern.

### Literature position

Per `openspec/specs/doctrinal-provenance`, technique detail traces to its grid row and carries no
literature attribution, because a citation there would falsely imply a work prescribes the procedure.
The search was run anyway, because the repository's rule is that prose is not authored from memory:

- `Heuer` p. 81 — the handicapper and clinical-psychologist experiments: accuracy stayed flat or fell
  as information increased while confidence rose steadily. This grounds the *analytic* claim that
  volume is not quality, which `credential-harvest-triage` already cites as
  `Heuer#information-quantity`.
- `Monte` pp. 26–27 — directed collection knows the class of information wanted from the outset, as
  against strategic collection's bulk. This grounds *targeting*, not query syntax.

Neither addresses how a search is phrased against an index. The finding is therefore recorded in
`docs/roles/sources.md` as searched-and-not-found, and the new prose carries the skills' own procedural
anchors with no `doctrine_source` added. Adding one would misattribute measured platform behaviour to
a 1999 monograph.

### Rejected alternatives

- **Forbid extension search outright.** It has a legitimate residual use as a cross-check on a set
  already bounded by schema, and a prohibition an analyst can see is wrong gets ignored wholesale.
- **Put the covering-message queries in as recommended patterns.** The obvious forms do not work on
  real data: `"пароль от конфига"` returned 0, a `конфиг` + password-vocabulary form 1,911 and an
  attachment form 7,084, effectively all chat noise. Shipping them would have codified the same
  mention-versus-artefact error one level up. The rule that ships instead is to pivot from the located
  artefact to its carrier.
- **Regenerate `acordia-map.html`.** It was last rebuilt for 6.7.0 and 6.9.0–6.12.0 all shipped
  without it; it is a periodic rebuild rather than a per-change obligation, and folding a full
  re-derivation into a content change would couple unrelated risk.
