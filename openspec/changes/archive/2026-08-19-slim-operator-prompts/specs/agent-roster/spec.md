## ADDED Requirements

### Requirement: A prompt routes to a skill rather than restating its technique

An agent prompt SHALL carry the judgement its agent exists to make — the situation-to-technique
routing, the phase order, the return contract — and SHALL NOT restate technique detail that a skill
it names already carries. Where a prompt needs to reach a technique, it SHALL name the situation and
the owning skill on one line, in the form `- **<situation>** → \`<skill-slug>\``.

Moving technique text out of a prompt SHALL NOT lose it: before a block leaves a prompt, every
command, payload, flag and table row in it SHALL be present in the destination skill, appended there
first where it is absent.

#### Scenario: Prompt names a skill instead of repeating it

- **WHEN** an operator prompt reaches a technique that a named skill carries
- **THEN** the prompt gives the situation and the skill slug, and does not repeat the skill's commands

#### Scenario: A moved command survives the move

- **WHEN** a technique block is removed from a prompt
- **THEN** every command and payload it contained is present in the skill the prompt now routes to

#### Scenario: Routing blocks stay in the prompt

- **WHEN** a block reads "situation → technique → skill" rather than carrying the technique itself
- **THEN** it stays in the prompt, because routing is the agent's own work

### Requirement: Prompt bodies stay under a measured ceiling

No agent prompt body SHALL exceed 10,000 characters, measured after the frontmatter. A prompt that
crosses the ceiling SHALL be reduced by moving technique detail to the skill that owns it, never by
deleting the routing or the guardrails.

#### Scenario: Ceiling holds across the roster

- **WHEN** every agent prompt body in both pillars is measured
- **THEN** none exceeds 10,000 characters

### Requirement: The journal contract is named once, not restated per prompt

The `.acordia/ops/` operation-journal contract — the file layout, the severity and confidence scales,
the log-on-discovery and check-coverage-before-claiming rules, the finding-file shape — SHALL live in
the `operation-journal` skill. Each of the five operator prompts SHALL name that skill in one sentence
and SHALL carry only the journal fields specific to its own domain, which the shared contract does not
cover.

#### Scenario: Prompt points at the skill

- **WHEN** an operator prompt's journal section is read
- **THEN** it names `operation-journal` and does not restate the scales or the file layout

#### Scenario: Domain-specific fields survive

- **WHEN** `web-application`'s journal section is read
- **THEN** it still requires WSTG-ID, CWE and MITRE ATT&CK on a finding, because those are its own additions

#### Scenario: Composition boundary stays stated

- **WHEN** `internal-network`'s journal section is read
- **THEN** it still states that the final assessment report is composed by the orchestrator from this journal, not by the specialist

## MODIFIED Requirements

### Requirement: Operator prompts state the authorization gate and journal discipline

Each of the five operator prompts SHALL state that work proceeds only inside authorized scope,
naming `.acordia/ops/scope.md` as where scope is recorded, and SHALL name the `operation-journal`
skill as the contract for how operation state is recorded. Each SHALL also carry a guardrails section
requiring evidence-backed findings, minimal noise and blast radius, least privilege, no fabrication,
no destructive action beyond a proof of concept, no exfiltration beyond proof, and no persistence.

#### Scenario: Scope gate present

- **WHEN** any operator prompt is read
- **THEN** it names `.acordia/ops/scope.md` and refuses work on a target absent from it

#### Scenario: Guardrails present

- **WHEN** any operator prompt is read
- **THEN** it carries the evidence-first, minimal-noise, least-privilege, no-fabrication, no-destruction, no-exfiltration and no-persistence rules

#### Scenario: Journal discipline reachable

- **WHEN** any operator prompt is read
- **THEN** it names `operation-journal`, so the recording contract is one read away rather than restated in the prompt
