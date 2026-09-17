## ADDED Requirements

### Requirement: Orchestrator fan-out follows real dependencies

`cyber-analyst` SHALL dispatch every independent, bounded specialist question without waiting for an unrelated specialist return. It MAY dispatch more than one instance of the same leg when it partitions a corpus or other input into disjoint, bounded slices. A specialist assignment SHALL name its question and input slice; the orchestrator SHALL retain responsibility for joining returns and SHALL NOT use fan-out to delegate that fusion.

A return SHALL block a later assignment only when the later assignment needs the return's information. In a directed credential sweep, Collection and Terrain orientation SHALL precede credential prioritisation, but their paired launch SHALL NOT imply a two-agent dispatch ceiling. Mission valuation SHALL wait only when it needs the oriented asset register, and Overwatch SHALL be dispatched when its operating question is independently material.

#### Scenario: Independent specialist questions fan out together

- **WHEN** an operation contains multiple independent, bounded specialist questions
- **THEN** the orchestrator's prompt directs it to dispatch them together rather than serialising them by roster order or a fixed pair

#### Scenario: One specialist receives disjoint slices

- **WHEN** a bounded corpus question requires more than one slice owned by the same specialist
- **THEN** the orchestrator's prompt permits multiple assignments to that specialist, each carrying a disjoint bounded slice

#### Scenario: A real dependency keeps its barrier

- **WHEN** a later specialist question requires an earlier return to define its input
- **THEN** the orchestrator's prompt directs it to read that return before dispatching the dependent question

#### Scenario: Lead retains fusion

- **WHEN** parallel specialist returns arrive
- **THEN** the orchestrator's prompt directs it to reconcile and fuse them itself rather than assigning the joined operating picture to a leg
