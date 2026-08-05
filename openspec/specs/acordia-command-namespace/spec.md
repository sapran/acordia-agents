# acordia-command-namespace Specification

## Purpose
How this distribution is invoked: one slash-command wrapper per agent, namespaced as `/acordia:<agent>` by directory placement rather than by renaming any artifact, the per-harness shapes that placement takes, how the wrappers deploy under the same ownership and idempotence guarantees as agents and skills, and the standing guarantee that agent names and skill slugs stay unprefixed.
## Requirements
### Requirement: A namespaced command wrapper for every dispatchable agent

The repository SHALL carry a **canonical** slash-command wrapper for every agent, at `commands/acordia/<stem>.md`, where `<stem>` is that agent's filename stem under `<pillar>/agents/`. Every agent SHALL have exactly one canonical wrapper, so each agent has one handle that is guaranteed to exist and is named for the thing it dispatches.

A wrapper MAY additionally exist under a **short alias**, because the namespace exists to be typed and the stem form is the longest available spelling of each handle. An alias SHALL dispatch exactly one live agent and SHALL declare, in its frontmatter, which canonical wrapper it stands for. An alias name SHALL NOT equal any agent's filename stem, so an alias can never shadow a different agent's canonical wrapper.

Every wrapper, canonical or alias, SHALL name a live agent: a wrapper dispatching a name no agent answers to is a defect. This check — not a prohibition on second names — is what protects the namespace from a renamed agent, and it covers the canonical wrappers too, which a prohibition never did.

Each wrapper SHALL carry `description` frontmatter conveying that agent's operating question, and a body that dispatches the named agent passing `$ARGUMENTS` as the brief. `$ARGUMENTS` SHALL be the only argument placeholder used, because it is the one form both target harnesses honour. A wrapper for an agent whose `mode` is `primary` SHALL name the session-switch fallback for harnesses that cannot dispatch a primary agent as a subagent.

An alias SHALL be derived from its canonical wrapper rather than authored separately, so that description, argument hint, and dispatch body cannot diverge between the two.

A wrapper SHALL NOT restate the agent's prompt, redefine its scope, or grant it capability — it is an entry point, and the agent file remains the source of behaviour.

#### Scenario: Every agent has a canonical wrapper named for it

- **WHEN** `commands/acordia/` is compared with the union of `analysts/agents/*.md` and `operators/agents/*.md`
- **THEN** every agent has a wrapper whose filename stem equals the agent's filename stem

#### Scenario: Every wrapper dispatches a live agent

- **WHEN** any wrapper in `commands/acordia/` is read
- **THEN** the agent it names exists under some pillar's `agents/` directory

#### Scenario: Aliases do not shadow canonical wrappers

- **WHEN** the alias wrappers are compared with the set of agent filename stems
- **THEN** no alias name equals any agent's filename stem

#### Scenario: Alias declares its canonical wrapper

- **WHEN** an alias wrapper is read
- **THEN** its frontmatter names the canonical wrapper it stands for
- **AND** its description, argument hint, and dispatch body match that canonical wrapper

#### Scenario: Wrapper dispatches its agent with the user's brief

- **WHEN** any wrapper body is read
- **THEN** it names the agent it dispatches and passes `$ARGUMENTS` as the brief

#### Scenario: Orchestrator wrappers name the fallback

- **WHEN** the wrapper for an agent whose `mode` is `primary` is read
- **THEN** it states that the agent is dispatched where the harness allows it, and names switching the session agent as the fallback where it does not

### Requirement: Namespace shape is per harness, because discovery differs

The namespace SHALL be realised by directory placement, never by renaming an artifact. Because the two target harnesses discover commands differently, one source tree SHALL produce two deployed shapes:

- A **Claude-format command tree** receives `<commands-root>/acordia/<stem>.md`, yielding `/acordia:<stem>`. A harness scanning that tree recursively registers the subdirectory alias (`foo/bar.md` → both `bar` and `foo:bar`), so a single deployment serves Claude Code and omp alike.
- **opencode** receives `<opencode-root>/commands/acordia-<stem>.md`, yielding `/acordia-<stem>`, because opencode command discovery is flat. This matches the convention this repository already uses for its own OpenSpec commands (`.opencode/commands/opsx-apply.md` beside `.claude/commands/opsx/apply.md`) rather than introducing a second one.

omp's own commands directory SHALL NOT be used for the namespace, because it is scanned non-recursively and therefore cannot express one. An omp deployment writing outside the omp harness root SHALL be reported in the installer's output rather than performed silently.

#### Scenario: Claude-format tree carries the colon namespace

- **WHEN** the command set is deployed to a Claude-format command root
- **THEN** each wrapper lands at `<root>/acordia/<stem>.md`
- **AND** the invocable name is `acordia:<stem>`

#### Scenario: opencode carries the flat namespace

- **WHEN** the command set is deployed for the opencode harness
- **THEN** each wrapper lands at `<opencode-root>/commands/acordia-<stem>.md`
- **AND** no subdirectory is created, because opencode command discovery is flat

#### Scenario: omp destination is reported, not silent

- **WHEN** commands are deployed for the omp harness
- **THEN** the installer reports the Claude-format destination path
- **AND** states that omp's own commands directory cannot carry a namespace

### Requirement: Agent names and skill slugs stay unprefixed

The command namespace SHALL be the only prefixed surface this repository publishes. No agent filename, agent name, skill slug, or competency-grid row SHALL carry a distribution prefix, because agent dispatch and skill selection are flat exact-name and description-match surfaces on which a prefix isolates nothing while breaking the grid bijection and the autoload lines the omp translator parses.

#### Scenario: No slug gains a prefix

- **WHEN** the agent files, both orchestrators' `task` whitelists, and the skill slugs are inspected after this change
- **THEN** none carries a distribution prefix
- **AND** the only place `acordia` appears as a name prefix is the deployed command namespace

### Requirement: Commands deploy under the same guarantees as agents and skills

`install.sh` and `uninstall.sh` SHALL carry the command set by default, and SHALL apply to it the guarantees they already apply to agents and skills: ownership evidence before overwrite or removal, preflight abort before anything is written, `--dry-run` that writes nothing, and idempotent re-invocation.

The scripts SHALL accept `--no-commands` to skip the step and `--commands-target DIR` to place the tree explicitly. Because a command root cannot be inferred from an overridden harness root, a run combining `--target` with a harness whose command root lies outside that root SHALL skip the command step with an explanatory message rather than guess.

Ownership evidence for a command SHALL be defined in the same shared file as the existing evidence, as a symlink resolving inside this repository or a byte-identical copy, so the installer and uninstaller cannot drift.

#### Scenario: Foreign command file is refused

- **WHEN** a file this repository did not deploy occupies a command destination
- **AND** `./install.sh` runs
- **THEN** the run exits non-zero naming the conflicting path
- **AND** the foreign file is left byte-for-byte unchanged

#### Scenario: Commands can be skipped

- **WHEN** `./install.sh --no-commands` runs
- **THEN** agents and skills are deployed
- **AND** no command file is written

#### Scenario: Dry run writes no command

- **WHEN** `./install.sh --dry-run` runs
- **THEN** the intended command actions are printed
- **AND** no command file is created, removed, or modified

#### Scenario: Uninstall removes owned commands only

- **WHEN** `./uninstall.sh` runs after an install
- **THEN** the command files this repository deployed are removed
- **AND** a name-matching command file it did not deploy is left in place and reported
- **AND** the `acordia/` namespace directory is removed only if it is left empty

### Requirement: The command directory is not a pillar

`commands/` is a visible top-level directory carrying neither `agents/` nor `skills/`, so pillar auto-discovery SHALL continue to exclude it under the existing rule, without an exclusion list. Commands SHALL be deployed by their own step rather than as a pillar's artifacts.

#### Scenario: Auto-discovery still finds exactly the artifact pillars

- **WHEN** `./install.sh` runs with no `--pillar` argument
- **THEN** the discovered pillars are exactly `analysts` and `operators`
- **AND** `commands` is not among them
