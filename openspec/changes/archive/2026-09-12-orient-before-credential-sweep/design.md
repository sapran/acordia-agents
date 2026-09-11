## Design

### Operational sequence

The lead runs a collection-planning preflight before directed credential collection:

```text
carried-memory refresh
    -> Aleph corpus and technical terrain orientation
    -> mission/crown-jewel valuation
    -> asset-and-credential hypothesis register
    -> targeted credential triage and specialist extraction
    -> residual sweep for unexplained systems
    -> correlation, ranking and operator hand-off
```

Collection and Terrain may run in parallel because memory/corpus orientation and technical terrain orientation are independent reads. The lead must read both returns and fuse them. Mission valuation follows the technical asset register. Overwatch may be added when own-footprint or defender exposure is material. Credential work is blocked until the lead has a current orientation packet.

The general analyst loop remains end-neutral and retains its six existing steps. The new preflight is a collection-planning gate, not a seventh universal leg read and not a replacement for the existing mission, terrain, defender, take, judgement and next-move sequence.

### Orientation packet

The lead's packet is a working brief, not a secret store. It contains:

- scoped Aleph collection identifiers and coverage limitations;
- prior assets, aliases, domains, providers, prior searches and unresolved gaps;
- asset/system class and non-secret technical fingerprints;
- entity identifiers, source collection, observed/inferred status, freshness and confidence;
- mission relevance and likely organisational process/crown-jewel relationship;
- expected credential forms and planned specialist bucket owner;
- gaps that the targeted sweep or a later residual sweep must close.

No raw credential value belongs in this packet or in operational memory.

### Asset-aware triage

`credential-harvest-triage` keeps its existing ownership gate and coverage discipline. It gains four non-secret associations on each finding: `asset`, `asset-class`, `mission-relevance` and `credential-hypothesis`. The existing fields remain authoritative for credential handling.

P0–P3 priority is assessed from scope, reuse potential, freshness, confidence, asset criticality and mission relevance. Ease of use remains a tie-breaker. The asset register supplies the context; triage does not independently invent target value.

For Aleph, triage first validates that the packet exists and that its collection scope matches the work. It then inventories and partitions only the selected material, runs system-specific patterns over the declared slice, performs the existing deep passes, correlates findings back to assets and mission threads, and runs a residual sweep for unexplained endpoints or system classes. A missing or incomplete packet stops prioritisation and returns an orientation gap to the lead.

For raw archives, the existing local artefact inventory remains the first step because the archive itself is the available source of shape. An orientation packet, when supplied, still steers bucket selection and pattern choice.

### Asset fingerprints

The existing credential pattern reference gains a separate non-secret fingerprint section. Fingerprints are search selectors, not credentials and not permission to validate anything. They cover MinIO/S3-compatible storage, databases, SMB/NFS, Kubernetes/container systems, CI/CD, VPN/remote access, identity systems and SSH. Existing credential-value patterns remain unchanged.

### Source-of-truth and delivery

The role-model prose is updated first to state the orientation-before-directed-collection relationship. Prompt bodies and skill bodies then derive from that role model. No competency-grid mark changes. The OpenSpec delta modifies `agent-roster` and `skill-library`; no new capability directory is created.

The plugin version becomes `6.10.0` in `acordia-analysts/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `.omp-plugin/marketplace.json`, with the two catalogs byte-identical.

### Verification design

Verification combines strict OpenSpec validation, the ACORDIA drift gate, catalog/JSON checks, a focused ordering assertion, and a real harness smoke run if available. The focused synthetic scenario contains a MinIO endpoint and a generic VPN/SSH-shaped observation but no credential value. The expected plan first creates the asset orientation, associates object-storage credential hypotheses with MinIO, ranks them using mission/asset relevance, and reserves generic scanning for the residual pass. No live credential validation or target contact is permitted.
