## MODIFIED Requirements

### Requirement: The `.acordia/ops/` operation journal

Operation state that CyberStrike keeps in its methodology-engine database SHALL be kept as files under `.acordia/ops/`, relative to the working directory, with this fixed layout:

| Path | Content |
| --- | --- |
| `.acordia/ops/scope.md` | authorised targets, exclusions, rules of engagement |
| `.acordia/ops/intel.md` | append-only intel log — endpoints, credentials, technologies, parameters, configuration, auth flows, with severity and confidence |
| `.acordia/ops/coverage.md` | append-only coverage log — what was tested, the request sent, the response summary, and the reasoning |
| `.acordia/ops/findings/<slug>.md` | one confirmed finding per file, with evidence |
| `.acordia/ops/reports/<name>.md` | composed engagement reports |

The journal mirrors the analyst pillar's `.acordia/reports/` convention and SHALL be described in prompts as discipline, not enforced as a permission scope, **because a path scope on a write tool is unenforceable in every harness**: `bash: allow` is an open write channel at any path. That omp cannot scope a tool to a path is an additional limitation, and SHALL NOT be given as the reason on its own — doing so implies some harness enforces the journal, which none does.

#### Scenario: Layout named identically across artifacts

- **WHEN** the journal paths named in the five operator prompts are compared
- **THEN** they agree on the five paths above

#### Scenario: Intel entries carry severity and confidence

- **WHEN** a prompt describes an intel append
- **THEN** it requires a severity (critical / high / medium / low / informational) and a confidence (confirmed / high / medium / low)

#### Scenario: Coverage entries carry evidence

- **WHEN** a prompt describes a coverage append
- **THEN** it requires the request sent, the response summary, and the reasoning that proves or disproves the vulnerability

#### Scenario: Journal is not a permission scope

- **WHEN** an operator agent's `edit` permission is inspected
- **THEN** it is an unscoped `allow`, and the journal paths appear only in the prompt body

#### Scenario: Non-enforcement is stated as universal

- **WHEN** the reason the journal is discipline rather than a scope is read
- **THEN** it names `bash: allow` as the open write channel present in every harness
- **AND** omp's inability to scope a tool to a path appears as an additional limitation, not as the sole cause
