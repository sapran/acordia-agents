## MODIFIED Requirements

### Requirement: Unmappable permissions are surfaced, not silently resolved

omp allowlists whole tools, cannot scope a tool to a path, and cannot remove `write` at all while its `tools.xdev` setting is on, because `read` and `write` are the transport for every `xd://` device. The source files' `".acordia/reports/**": allow` write exception therefore has no faithful translation, and neither does a blanket write denial. The translator SHALL emit the narrower allowlist regardless and SHALL record in the generated file that the harness does not enforce it.

The recorded note SHALL state the report sink as a **prompt-level convention that no harness enforces**, and SHALL NOT frame it as a capability omp lacks relative to opencode. The source's scoped `edit` rule is not enforced in opencode either: every analyst carries `bash: allow`, an unrestricted write channel at any path (see `analyst-agent-roster`). A note reading "omp cannot express a path-scoped permission" invites the reading that some harness does express one, which is false in effect.

The mechanically accurate facts SHALL be retained in the note: that omp exposes `write` as an `xd://` transport tool irrespective of the allowlist, and that the agent can therefore write anywhere. What changes is the attribution, not the disclosure.

#### Scenario: Write access is never silently claimed

- **WHEN** any agent is translated
- **THEN** the output frontmatter records, under generated metadata, that omp exposes `write` as an `xd://` transport tool irrespective of the allowlist

#### Scenario: Scoped report sink is reported as an unenforced convention

- **WHEN** an agent carrying the scoped report-sink exception is translated
- **THEN** the output frontmatter records that the sink is a prompt-level convention enforced by no harness
- **AND** the record states that the agent can write anywhere
- **AND** the record does not present the gap as specific to omp

#### Scenario: Dispatch denial is enforced

- **WHEN** a translated leaf agent runs in omp
- **THEN** it has no `task` tool and cannot dispatch any agent

### Requirement: Write-capable pillars are translated without a false read-only claim

Because omp cannot deny `write` while `tools.xdev` is on, the generated metadata note about write access SHALL distinguish three source postures: a blanket denial, a path-scoped exception, and an outright `allow`. A write-capable source SHALL NOT be stamped with the read-only note.

The path-scoped note's wording is **no longer frozen**. `harden-plugin-distribution` fixed a scenario requiring the analysts' generated write-access note to be unchanged from before that change; its purpose was to prove that change did not disturb the note, not to make the wording permanent. This change rewords it deliberately, per the reframing requirement above.

#### Scenario: Write-capable source stamped accurately

- **WHEN** an agent whose source grants `edit: allow` is translated
- **THEN** the generated metadata states that the source granted write access and that the allowlist carries `edit` and `write`
- **AND** it does not claim a read-only posture

#### Scenario: Blanket read-only note is unchanged by this change

- **WHEN** an agent whose source denies `edit` outright is translated
- **THEN** its generated write-access note still states that omp exposes `write` as an `xd://` transport tool and that read-only is prompt-level for writes

#### Scenario: Path-scoped note is reworded

- **WHEN** an agent whose source carries the scoped report-sink exception is translated
- **THEN** its generated write-access note differs from the pre-change wording
- **AND** it no longer attributes the gap to omp's inability to express a path scope
