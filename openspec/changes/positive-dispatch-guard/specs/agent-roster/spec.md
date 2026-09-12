## MODIFIED Requirements

### Requirement: The orchestrator establishes its dispatch capability positively

The orchestrator SHALL determine whether it can dispatch, and report that determination, before any
other work. Its prompt SHALL direct it to enumerate its own tools, look for the dispatch tool by name,
and open with an explicit verdict — available or unavailable — read from what it holds rather than from
what it expects to hold. An orchestrator that finds itself unable to dispatch has been entered by the
wrong route: it SHALL then stop and report that, naming the correct route, rather than proceeding to do
the legs' work itself.

The guard SHALL NOT be phrased as a condition on the absence of a tool. A guard so phrased does not
fire: a dispatched orchestrator enumerated its tools, held no dispatch tool, and produced 391,251
characters without once reaching for the guard, because a model does not notice an absence it was not
asked to look for. The failure this prevents is silent in both directions — a dispatched orchestrator
receives its full doctrine, keeps every other tool, and produces a confident product assembled from no
specialist reads.

#### Scenario: Orchestrator states its verdict before working

- **WHEN** `cyber-analyst` begins any session
- **THEN** its prompt directs it to enumerate its tools and open with an explicit dispatch verdict,
  before analysis, dispatch or any other work

#### Scenario: Orchestrator entered as a subagent

- **WHEN** `cyber-analyst` is dispatched as a subagent and cannot spawn further agents
- **THEN** its prompt directs it to stop and report the wrong entry route rather than continue as a lead

#### Scenario: Refusal names the working route

- **WHEN** the orchestrator reports that it cannot dispatch
- **THEN** it names the command wrapper as the route that leaves it able to

#### Scenario: The verdict is read, not assumed

- **WHEN** the orchestrator reports that it can dispatch
- **THEN** its prompt requires that verdict to come from the tools it observed holding, not from the
  capability its role implies
