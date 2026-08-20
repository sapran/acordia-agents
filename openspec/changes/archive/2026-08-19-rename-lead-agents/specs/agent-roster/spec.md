## ADDED Requirements

### Requirement: A lead agent's name is distinct from its pillar's name

Neither pillar's lead agent SHALL be named with a word that also names the pillar, its skill library,
its prompts or its artifacts. The analyst lead SHALL be `cyber-analyst` and the operations lead SHALL
be `cyber-operator`, so that "the operations pillar" and "the operations prompts" can never be read as
naming an agent.

Prose SHALL keep the bare word `operator` only where it means a human or a driving session rather than
the agent — the analyst guardrail *"execution belongs to the operators you advise"*, an operator
journal, an operator session, operator-deployed artifacts, and technique content such as a
default-credential pair. Renaming SHALL NOT rewrite those sites.

An archived change SHALL NOT be rewritten to use a later name. It records what was true when it
shipped.

#### Scenario: Pillar word never resolves to an agent
- **WHEN** the live tree is searched for `operator` followed by pillar, library, skill, prompt, agent, wrapper, artifact or file
- **THEN** no match is found, because every such site reads `operations`

#### Scenario: The human sense survives the rename
- **WHEN** an analyst prompt's closing guardrail is read
- **THEN** it still says execution belongs to the operators it advises, naming no agent

#### Scenario: Archived changes keep their original names
- **WHEN** any file under `openspec/changes/archive/` is read
- **THEN** it still names `operational-analyst` and `operator` as they were at the time it shipped

#### Scenario: A provenance document keeps its filename and its anchors
- **WHEN** `docs/roles/operational-analyst.md` is read
- **THEN** its grid rows are still at lines L67–L108, every skill anchor still resolves to a row, and a
  closing note records that the shipped agent is now `cyber-analyst`

## MODIFIED Requirements

### Requirement: Nine agents, two pillars, one authored file each

The distribution SHALL ship exactly nine agent files, four under `acordia-analysts/agents/` and five
under `acordia-operators/agents/`, each the single editable source for every harness. The analyst
files SHALL be `cyber-analyst.md`, `target-network-analyst.md`,
`defender-detection-analyst.md`, `fusion-analyst.md`; the operations files SHALL be `cyber-operator.md`,
`web-application.md`, `mobile-application.md`, `cloud-security.md`, `internal-network.md`. Filename
stem SHALL equal frontmatter `name`. No generated or translated copy of an agent SHALL exist in the
repository.

#### Scenario: Roster is complete and named
- **WHEN** the two pillar `agents/` directories are enumerated
- **THEN** exactly those nine files are present, and each filename stem equals its frontmatter `name`

#### Scenario: No second copy of an agent exists
- **WHEN** the repository is searched for agent files carrying an ACORDIA description
- **THEN** the only matches are those nine files

### Requirement: A namespaced command wrapper for every dispatchable agent

The distribution SHALL ship 18 slash-command wrappers: one canonical wrapper named after each of the
nine agents, plus nine short aliases. Each wrapper SHALL live in its own pillar's flat `commands/`
directory — eight under `acordia-analysts/commands/`, ten under `acordia-operators/commands/` —
because a harness discovers plugin commands from `<pluginRoot>/commands/*.md` without recursion and
namespaces them by plugin name. Each wrapper SHALL carry `description` and `argument-hint`
frontmatter, SHALL dispatch exactly the agent it is named for, SHALL pass the caller's argument
through as the brief, and SHALL ask for a brief when none is supplied.

Where renaming a lead agent lengthens its canonical wrapper, the previous single-word wrapper SHALL be
retained as that agent's short alias, so that an existing invocation keeps working.

#### Scenario: Wrapper count and split
- **WHEN** the two `commands/` directories are enumerated
- **THEN** eight analyst and ten operations wrappers are present, 18 in total, each a flat `.md` file

#### Scenario: Wrapper dispatches its own agent
- **WHEN** any wrapper is read
- **THEN** it names exactly one agent, the one it is named or aliased for

#### Scenario: A renamed lead keeps its old handle
- **WHEN** `/operator` and `/analyst` are invoked
- **THEN** they dispatch `cyber-operator` and `cyber-analyst` respectively

#### Scenario: Empty brief is refused
- **WHEN** a wrapper is invoked with no argument
- **THEN** it asks what to look at before dispatching

### Requirement: Operations prompts state the authorization gate and journal discipline

Each of the five operations prompts SHALL state that work proceeds only inside authorized scope,
naming `.acordia/ops/scope.md` as where scope is recorded, and SHALL name the `operation-journal`
skill as the contract for how operation state is recorded. Each SHALL also carry a guardrails section
requiring evidence-backed findings, minimal noise and blast radius, least privilege, no fabrication,
no destructive action beyond a proof of concept, no exfiltration beyond proof, and no persistence.

#### Scenario: Scope gate present

- **WHEN** any operations prompt is read
- **THEN** it names `.acordia/ops/scope.md` and refuses work on a target absent from it

#### Scenario: Guardrails present

- **WHEN** any operations prompt is read
- **THEN** it carries the evidence-first, minimal-noise, least-privilege, no-fabrication, no-destruction, no-exfiltration and no-persistence rules

#### Scenario: Journal discipline reachable

- **WHEN** any operations prompt is read
- **THEN** it names `operation-journal`, so the recording contract is one read away rather than restated in the prompt
