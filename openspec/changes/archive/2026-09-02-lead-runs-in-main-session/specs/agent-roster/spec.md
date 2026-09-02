## ADDED Requirements

### Requirement: The orchestrator is entered by a route that leaves it able to dispatch

`cyber-analyst` exists to direct four legs, so any route that delivers its doctrine while removing its
ability to dispatch delivers a lead that cannot lead. The pillar's lead wrappers SHALL therefore carry
the orchestrator's prompt body into the invoking session rather than instruct a harness to dispatch the
orchestrator as a subagent. A wrapper SHALL NOT describe switching a session to an agent, because no
harness the pillar targets provides that operation.

The orchestrator's prompt body SHALL appear byte-identically in `agents/cyber-analyst.md` and in every
wrapper that carries it, and the repository's drift gate SHALL fail when they diverge, in the same
manner as the byte-identity check on the two marketplace catalogs.

#### Scenario: A lead wrapper carries the doctrine rather than delegating it

- **WHEN** a lead wrapper is read
- **THEN** it contains the orchestrator's prompt body, and instructs no harness to dispatch the
  orchestrator as a subagent

#### Scenario: No wrapper claims a session can become an agent

- **WHEN** any command wrapper in the pillar is read
- **THEN** it describes no operation that switches the current session to a named agent

#### Scenario: Wrapper and agent bodies are checked for drift

- **WHEN** a lead wrapper's copy of the orchestrator body differs from `agents/cyber-analyst.md`
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

### Requirement: A carried brief is framed as material, not instruction

A wrapper that carries doctrine into the invoking session interpolates the caller's brief into the same
document as that doctrine, at its end, where recency weights it most heavily. The wrapper SHALL
therefore label the brief as material to act on rather than instructions to obey, and SHALL state
before the brief appears that a directive found inside it — to change the doctrine, the entry route, or
tool use — is reported to the caller rather than followed. This extends the retained guardrail on
retrieved content, which names fetched pages and tool output but not the brief.

#### Scenario: Brief is labelled as material

- **WHEN** a lead wrapper is read
- **THEN** the brief is introduced as material rather than instruction, and the sentence saying so
  appears before the interpolation point

## MODIFIED Requirements

### Requirement: Prompt bodies stay under a measured ceiling

No agent prompt body SHALL exceed 10,500 characters, measured after the frontmatter. A prompt that
crosses the ceiling SHALL be reduced by moving technique detail to the skill that owns it, never by
deleting the routing or the guardrails.

The ceiling SHALL be enforced by the repository's drift gate rather than by inspection. An unenforced
ceiling is how the orchestrator was allowed to sit at 9,921 of 10,000 characters with no signal, so
that a 353-character entry guard crossed it silently while every other invariant reported clean.

#### Scenario: Ceiling holds across the roster

- **WHEN** every agent prompt body in the roster is measured
- **THEN** none exceeds 10,500 characters

#### Scenario: A crossed ceiling fails the gate

- **WHEN** an agent prompt body exceeds the ceiling
- **THEN** the drift gate fails, naming the agent and its measured size

### Requirement: A namespaced command wrapper for every dispatchable agent

The distribution SHALL ship 10 slash-command wrappers: one canonical wrapper named after each of the
five agents, plus five short aliases. All ten SHALL live in the pillar's flat
`acordia-analysts/commands/` directory, because a harness discovers plugin commands from
`<pluginRoot>/commands/*.md` without recursion and namespaces them by plugin name. Each wrapper SHALL
carry `description` and `argument-hint` frontmatter, SHALL pass the caller's argument through as the
brief, and SHALL ask for a brief when none is supplied.

A wrapper SHALL resolve to exactly one agent, the one it is named or aliased for. **How it does so
depends on whether that agent dispatches.** A leg wrapper SHALL dispatch its agent as a subagent. A
lead wrapper SHALL instead carry its agent's prompt body into the invoking session, because a
dispatched agent cannot itself dispatch and the lead's work is directing four legs.

The canonical stems SHALL be the five agent names, and the aliases SHALL be `analyst`, `mission`,
`terrain`, `overwatch` and `collection`. An alias stem SHALL NOT equal any agent stem: the canonical
wrapper already holds that stem, so such an alias is a filename collision in one flat directory rather
than a second handle.

Where renaming a lead agent lengthens its canonical wrapper, the previous single-word wrapper SHALL be
retained as that agent's short alias, so that an existing invocation keeps working.

#### Scenario: Wrapper count and split

- **WHEN** the pillar's `commands/` directory is enumerated
- **THEN** ten wrappers are present, five canonical and five aliases, each a flat `.md` file, and no
  second `commands/` directory ships

#### Scenario: Wrapper dispatches its own agent

- **WHEN** any wrapper is read
- **THEN** it resolves to exactly one agent, the one it is named or aliased for

#### Scenario: A leg wrapper dispatches, a lead wrapper carries

- **WHEN** a leg wrapper and a lead wrapper are compared
- **THEN** the leg wrapper dispatches its agent as a subagent, and the lead wrapper carries the agent's
  prompt body into the invoking session

#### Scenario: A renamed lead keeps its old handle

- **WHEN** `/analyst` is invoked
- **THEN** it enters `cyber-analyst`, carrying its prompt body into the invoking session

#### Scenario: Empty brief is refused

- **WHEN** a wrapper is invoked with no argument
- **THEN** it asks what to look at before proceeding

#### Scenario: No alias collides with a canonical wrapper

- **WHEN** the ten wrapper stems are compared with the five agent names
- **THEN** no alias stem equals any agent stem
