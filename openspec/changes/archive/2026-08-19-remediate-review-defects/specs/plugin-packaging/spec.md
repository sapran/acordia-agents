## ADDED Requirements

### Requirement: Agent metadata anchors are validated before packaging

The generator SHALL validate the `metadata.acordia` block of every agent file it translates, and SHALL fail the build rather than emit an agent whose anchor is missing or malformed. The validation SHALL require:

- `metadata.acordia` is a mapping;
- `pillar` equals the name of the source pillar directory the file was discovered in, so a file copied into the wrong pillar fails rather than shipping mislabelled;
- `role` is either `orchestrator` or `specialist`, and is `orchestrator` if and only if `mode` is `primary`;
- no `leg` key is present, that key having been replaced by `pillar` + `role`.

The anchor is not decorative: the generator derives each agent's `color` from `role`, so an unreadable anchor silently produces a mislabelled agent in the picker rather than a build failure. The failure SHALL name the source file and the specific violation.

#### Scenario: A missing or non-mapping anchor fails the build

- **WHEN** an agent file carries no `metadata.acordia` block, or carries one that is not a mapping
- **THEN** the generator exits non-zero naming that source file

#### Scenario: Pillar mismatch fails the build

- **WHEN** an agent under `analysts/agents/` declares `pillar: operators`, or the converse
- **THEN** the generator exits non-zero naming both the declared and the expected pillar

#### Scenario: Role and mode must agree

- **WHEN** an agent declares `mode: primary` with `role: specialist`, or `mode: subagent` with `role: orchestrator`
- **THEN** the generator exits non-zero naming that source file

#### Scenario: The removed key fails the build

- **WHEN** an agent still declares `metadata.acordia.leg`
- **THEN** the generator exits non-zero naming that key, because its presence means the source predates the unified schema

### Requirement: Every skill an agent names resolves in its own pillar

Each agent prompt declares the skills it draws on as one or more single lines of `·`-separated slugs beneath a heading, because no harness in this distribution offers a per-agent `skills:` binding. The generator SHALL resolve every slug on every such line to an existing `<pillar>/skills/<slug>/SKILL.md` in that agent's own pillar, and SHALL fail the build naming the agent, the slug, and the pillar when one does not resolve.

A skill line SHALL be recognised by its shape — kebab-case slugs joined by ` · ` — rather than by matching a fixed set of heading strings, so that a newly introduced heading cannot escape the check by not being on a list.

This closes the gap between a declaration and its referent. The generator already parsed one such line and discarded the result, so a prompt could name a skill that does not exist, or one that exists only in the other pillar, and ship: the prompt would instruct the agent toward a slug the harness cannot resolve, and nothing would report it.

#### Scenario: A dangling slug fails the build

- **WHEN** an agent prompt names a skill slug with no corresponding directory in that agent's pillar
- **THEN** the generator exits non-zero naming the agent, the slug, and the pillar

#### Scenario: A cross-pillar slug fails the build

- **WHEN** an analyst prompt names a skill that exists only under `operators/skills/`, or the converse
- **THEN** the generator exits non-zero, because the two plugins are independently installable and a cross-pillar reference is unresolvable wherever only one is installed

#### Scenario: A new heading is checked without being enumerated

- **WHEN** a prompt introduces a skill list under a heading the generator has never seen
- **THEN** every slug on that line is resolved anyway, because the line is recognised by shape

### Requirement: The destructive-bash denylist has one canonical source

The per-pattern `bash` deny rules carried by write-capable agents SHALL be declared once, in the generator, and the generator SHALL fail the build when any write-capable agent's deny set differs from that canonical set.

The rules SHALL remain present in every agent source. opencode is the only harness that enforces them, and it enforces them by reading the source file; hoisting them out of the sources would trade a drift risk for a capability regression in the one harness where they bite. The generator holds the canonical copy because it is the only place that sees all of the sources at once.

The failure SHALL name the agent and the pattern that is missing or unexpected.

#### Scenario: A drifted denylist fails the build

- **WHEN** one write-capable agent's `bash` deny set gains, loses, or alters a pattern relative to the canonical set
- **THEN** the generator exits non-zero naming that agent and that pattern

#### Scenario: The rules stay in the sources

- **WHEN** the gate passes
- **THEN** every write-capable source file still carries the full deny map, so opencode's enforcement is unchanged by the gate's existence

### Requirement: Generated-tree drift ignores operating-system artefacts

Drift detection walks the filesystem rather than the index, so a file the repository ignores but the filesystem carries is reported as generated-tree drift. The comparison SHALL skip operating-system artefacts — at minimum `.DS_Store` — because the gate exists to detect divergence between the committed trees and the generator, not to detect a file manager.

#### Scenario: A Finder artefact does not fail the gate

- **WHEN** `plugins/.DS_Store` exists on disk and the committed trees otherwise match a fresh build
- **THEN** `tools/build-plugins.py --check` exits 0 and reports no drift

#### Scenario: Real drift is still reported

- **WHEN** a file under a generated path differs from, is missing from, or is extra to a fresh build, and is not an ignored artefact name
- **THEN** `--check` exits non-zero naming that path

### Requirement: The generator reports install state and prompt measurements

The generator SHALL offer a `--doctor` mode that reports what a build cannot see: the state of the machine the distribution is installed on, and the measurements that bound the distribution's own quality. It SHALL report

1. version skew between each installed `acordia-*` plugin recorded in omp's and Claude Code's plugin registries and the generator's `VERSION`, and any pillar recorded in neither registry;
2. any ACORDIA agent filename or skill slug present under `~/.omp/agent/agents/` or `~/.omp/agent/skills/`, whether file, directory, or symlink;
3. each agent's post-frontmatter body size, flagged against a 10,000-character ceiling;
4. skills named by no agent's skill line;
5. same-pillar skill `description` pairs whose content-word overlap is high enough to compete, both harnesses selecting skills by description match;
6. per-agent counts of prompt body lines duplicated verbatim in a `SKILL.md` that agent names.

Report (1) is the version signal the harnesses act on; report (2) is the failure it hides. A native agent or skill directory takes precedence over every plugin root in omp and dedups first-wins, so a copy there is what actually runs, at whatever vintage it was copied, and no install-state command reveals it.

`--doctor` SHALL exit 0, because a report that fails a build is a report that gets skipped. With `--strict`, findings (1) and (2) SHALL exit non-zero. Findings (3) through (6) SHALL remain advisory in every mode: they measure a backlog rather than a defect, and a gate that fails on the current tree would be disabled rather than obeyed.

#### Scenario: Version skew is named

- **WHEN** a plugin registry records an installed ACORDIA plugin at a version below `VERSION`
- **THEN** `--doctor` names the plugin, the installed version, and the current one

#### Scenario: A shadowing copy is named

- **WHEN** an ACORDIA agent file or skill slug is present under `~/.omp/agent/`
- **THEN** `--doctor` names it and states that it takes precedence over the installed plugin

#### Scenario: Absent registries are not an error

- **WHEN** neither plugin registry file exists on the machine
- **THEN** `--doctor` says so and continues, because a checkout with nothing installed is a valid state

#### Scenario: A report does not fail a build

- **WHEN** `--doctor` runs without `--strict` and every section has findings
- **THEN** it exits 0

## MODIFIED Requirements

### Requirement: Postures Claude Code cannot express are recorded in the generated file

Claude Code plugin agents silently ignore `metadata`, `hooks`, `mcpServers`, and `permissionMode`, so the provenance and permission-gap record the omp emitter places in `metadata.generated` has no frontmatter home. The Claude emitter SHALL therefore write comment lines above the frontmatter keys: always the generating tool and the repo-relative source path, and conditionally one note per posture the harness cannot express — the spawn allowlist, the path-scoped write, the per-command bash denies, and a granted `browser` permission.

Every unmappable posture SHALL be recorded. A posture that is dropped silently is indistinguishable, in the generated artifact, from a posture the source never granted: `browser: allow` translates to an omp tool and has no Claude Code counterpart, so without a note the two generated trees disagree about the agent's capability with nothing to say why.

#### Scenario: Each unmappable posture leaves a note

- **WHEN** a source agent declares a spawn allowlist, a path-scoped write, per-command bash denies, or `browser: allow`
- **THEN** the generated Claude agent carries one comment line per such posture, naming what the harness does not express

#### Scenario: A granted browser permission is not dropped silently

- **WHEN** a source agent declares `browser: allow`
- **THEN** the generated Claude agent records that the harness has no counterpart for it, matching how the other unmappable postures are recorded

#### Scenario: Provenance is always present

- **WHEN** any Claude plugin agent file is read
- **THEN** its first comment line names the repo-relative source path and `tools/build-plugins.py`, and states that the file is not to be edited

#### Scenario: Spawn allowlist gap recorded

- **WHEN** an agent whose source allows dispatch to named agents is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express a spawn allowlist and that the prompt names the agents this one dispatches

#### Scenario: Path scope gap recorded as a universal convention

- **WHEN** an agent whose source scopes writes to a report path is emitted for Claude Code
- **THEN** a comment states that the sink is a prompt-level convention enforced by no harness
- **AND** the comment does not contrast Claude Code against the source harness

#### Scenario: Bash deny gap recorded

- **WHEN** an agent whose source carries per-pattern bash denies is emitted for Claude Code
- **THEN** a comment states that plugin agents cannot express per-command bash rules and that those denies are prompt-level
