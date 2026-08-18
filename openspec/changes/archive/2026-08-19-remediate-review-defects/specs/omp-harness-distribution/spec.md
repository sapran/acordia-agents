## MODIFIED Requirements

### Requirement: Unmappable permissions are surfaced, not silently resolved

omp allowlists whole tools, cannot scope a tool to a path, and cannot remove `write` at all while its `tools.xdev` setting is on, because `read` and `write` are the transport for every `xd://` device. The source files' `".acordia/reports/**": allow` write exception therefore has no faithful translation.

Where a source declares a path-scoped `edit`, the translator SHALL emit `write` and SHALL NOT emit `edit`, and SHALL record in the generated file that the path scope is a prompt-level convention no harness enforces. This resolves a divergence in which one source posture produced opposite capability in the two plugin harnesses: the omp emitter withheld every write tool while the Claude emitter kept `Write` allowed, so an agent whose prompt requires it to produce a report held the means to do so in one harness and not the other.

The emitted capability is the honest one. `write` survives in omp as an `xd://` transport tool whenever `tools.xdev` is on, and `bash: allow` is an open write channel at any path in all three harnesses, so an agent with a scoped `edit` can already write anywhere; the generated note SHALL state that outcome rather than imply a boundary the harness keeps.

A blanket `edit: deny` SHALL continue to emit neither `edit` nor `write`, with the note recording that omp exposes `write` regardless while `tools.xdev` is on.

#### Scenario: A path-scoped edit yields a write tool

- **WHEN** a source agent declares `edit` as `"*": deny` followed by a path-scoped `allow`
- **THEN** the generated omp agent's `tools` list includes `write` and excludes `edit`
- **AND** the generated note states that the path scope is an unenforced convention and that the agent can write anywhere

#### Scenario: The two plugin harnesses agree on the posture

- **WHEN** the same path-scoped source is translated for both harnesses
- **THEN** both generated agents hold a write capability and neither holds a general edit capability, so one source posture yields one capability

#### Scenario: A blanket denial is unchanged

- **WHEN** a source agent declares a bare `edit: deny`
- **THEN** the generated omp agent's `tools` list contains neither `edit` nor `write`, and the note records that omp exposes `write` anyway while `tools.xdev` is on

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
