## ADDED Requirements

### Requirement: The orchestrator is entered by a route that leaves it able to dispatch

`cyber-analyst` exists to direct four legs, so any route that delivers its doctrine while removing its
ability to dispatch delivers a lead that cannot lead. The pillar's command wrappers SHALL therefore
carry the orchestrator's prompt body into the invoking session rather than instruct a harness to
dispatch the orchestrator as a subagent. A wrapper SHALL NOT describe switching a session to an agent,
because no harness the pillar targets provides that operation.

The orchestrator's prompt body SHALL appear byte-identically in `agents/cyber-analyst.md` and in every
command wrapper that enters the pillar, and the repository's drift gate SHALL fail when they diverge,
in the same manner as the byte-identity check on the two marketplace catalogs.

#### Scenario: A wrapper carries the doctrine rather than delegating it

- **WHEN** a command wrapper that enters the analysis pillar is read
- **THEN** it contains the orchestrator's prompt body, and instructs no harness to dispatch the
  orchestrator as a subagent

#### Scenario: No wrapper claims a session can become an agent

- **WHEN** any command wrapper in the pillar is read
- **THEN** it describes no operation that switches the current session to a named agent

#### Scenario: Wrapper and agent bodies are checked for drift

- **WHEN** a command wrapper's copy of the orchestrator body differs from `agents/cyber-analyst.md`
- **THEN** the drift gate fails, naming the wrapper and the divergence

### Requirement: The orchestrator refuses to act as a lead when it cannot dispatch

An orchestrator that finds itself unable to dispatch has been entered by the wrong route. It SHALL stop
and report that, naming the correct route, rather than proceeding to do the legs' work itself. The
failure this prevents is silent: a dispatched orchestrator receives its full doctrine, keeps every
other tool, and produces a confident product assembled from no specialist reads.

#### Scenario: Orchestrator entered as a subagent

- **WHEN** `cyber-analyst` is dispatched as a subagent and cannot spawn further agents
- **THEN** its prompt directs it to stop and report the wrong entry route rather than continue as a lead

#### Scenario: Refusal names the working route

- **WHEN** the orchestrator reports that it cannot dispatch
- **THEN** it names the command wrapper as the route that leaves it able to
