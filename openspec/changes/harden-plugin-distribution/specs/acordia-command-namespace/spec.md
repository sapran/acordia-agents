## MODIFIED Requirements

### Requirement: A namespaced command wrapper for every dispatchable agent

The repository SHALL carry a **canonical** slash-command wrapper for every agent, at `commands/acordia/<stem>.md`, where `<stem>` is that agent's filename stem under `<pillar>/agents/`. Every agent SHALL have exactly one canonical wrapper, so each agent has one handle that is guaranteed to exist and is named for the thing it dispatches.

Both directions of that bijection SHALL be enforced by the build, not merely asserted. The generator already failed on a wrapper naming no live agent; it SHALL additionally fail when an agent has no wrapper whose stem is its own, because adding an agent could otherwise ship a roster with no handle for it and nothing would object.

A wrapper MAY additionally exist under a **short alias**, because the namespace exists to be typed and the stem form is the longest available spelling of each handle. An alias SHALL dispatch exactly one live agent and SHALL declare, in its frontmatter, which canonical wrapper it stands for. An alias name SHALL NOT equal any agent's filename stem, so an alias can never shadow a different agent's canonical wrapper.

Every wrapper, canonical or alias, SHALL name a live agent: a wrapper dispatching a name no agent answers to is a defect. This check — not a prohibition on second names — is what protects the namespace from a renamed agent, and it covers the canonical wrappers too, which a prohibition never did.

Each wrapper SHALL carry `description` frontmatter conveying that agent's operating question, and a body that dispatches the named agent passing `$ARGUMENTS` as the brief. `$ARGUMENTS` SHALL be the only argument placeholder used, because it is the one form every target harness honours. A wrapper for an agent whose `mode` is `primary` SHALL name the session-switch fallback for harnesses that cannot dispatch a primary agent as a subagent.

An alias SHALL be derived from its canonical wrapper rather than authored separately, so that description, argument hint, and dispatch body cannot diverge between the two.

A wrapper SHALL NOT restate the agent's prompt, redefine its scope, or grant it capability — it is an entry point, and the agent file remains the source of behaviour.

#### Scenario: Every agent has a canonical wrapper named for it

- **WHEN** `commands/acordia/` is compared with the union of `analysts/agents/*.md` and `operators/agents/*.md`
- **THEN** every agent has a wrapper whose filename stem equals the agent's filename stem

#### Scenario: A missing canonical wrapper fails the build

- **WHEN** an agent exists with no wrapper whose stem equals its own
- **THEN** the generator exits non-zero naming that agent
- **AND** no plugin tree is written

#### Scenario: Every wrapper dispatches a live agent

- **WHEN** any wrapper in `commands/acordia/` is read
- **THEN** the agent it names exists under some pillar's `agents/` directory

#### Scenario: Aliases do not shadow canonical wrappers

- **WHEN** the alias wrappers are compared with the set of agent filename stems
- **THEN** no alias name equals any agent's filename stem

#### Scenario: Alias declares its canonical wrapper

- **WHEN** an alias wrapper is read
- **THEN** its frontmatter names the canonical wrapper it stands for

#### Scenario: Orchestrator wrappers name the fallback

- **WHEN** the wrapper for an agent whose `mode` is `primary` is read
- **THEN** it states that the agent is dispatched where the harness allows it, and names switching the session agent as the fallback where it does not
