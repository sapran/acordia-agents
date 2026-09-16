## ADDED Requirements

### Requirement: `.acordia/` is the workspace root for everything an analyst generates

`.acordia/` SHALL be the root under which an analyst's **own** generated files belong — notes, the
task `README.md`, working drafts, the credential file and the finished product alike — and not the
destination of the product alone. Every agent prompt SHALL give each kind of file it tells the agent
to write a destination under that root, naming the sink where the prompt states the instruction: a
prompt that directs notes, working files and drafts to a task directory SHALL name `.acordia/work/`
there, and a prompt that states where a finished product belongs SHALL name `.acordia/reports/`.
Naming both sinks names the root; a prompt is not required to repeat one sink in the section that
states the other. The root exists so that what the analyst writes stays out of the material it was
given to analyse, which is the same separation the write-posture requirement states from the other
side.

The root SHALL hold exactly two sinks:

- `.acordia/work/` — one directory per task, holding that task's `README.md`, notes, drafts and
  credential file.
- `.acordia/reports/` — the finished product.

A prompt SHALL NOT direct an analyst to create a working file, a notes file or a task directory in
the current directory, or in any location outside `.acordia/`, when its brief names no directory.
Writing beside the corpus is the outcome the root exists to prevent, so the brief-names-none case
SHALL resolve into `.acordia/work/` rather than into whatever directory the agent happens to be in.

Like the sink it contains, the root is a **convention and not a permission**. No prompt, frontmatter
or spec SHALL present it as an enforced scope, because no harness in the distribution restricts a
write to it and a claim otherwise would describe an enforcement that does not exist.

#### Scenario: The root covers working files, not only the product

- **WHEN** an agent prompt tells the agent to write a notes file, a working file or a draft
- **THEN** it gives that file a destination under `.acordia/` — the task directory under
  `.acordia/work/` — rather than leaving the parent unstated

#### Scenario: The product sink is still named

- **WHEN** an agent prompt states where a finished product belongs
- **THEN** it names `.acordia/reports/`, so the prompt names both sinks and therefore the root

#### Scenario: An unbriefed dispatch does not write beside the corpus

- **WHEN** a prompt or skill describes what to do when the brief names no working directory
- **THEN** it directs the agent to create the directory under `.acordia/work/`, and no prompt or
  skill instructs the agent to create it in the current directory or under a bare slug

#### Scenario: The root is worded as a convention

- **WHEN** a prompt or skill names `.acordia/` or either of its two sinks
- **THEN** it presents the path as where the material belongs, without claiming any harness
  restricts writes to it

### Requirement: A task directory and its product are addressed by corpus, then date

A task directory and the report produced from it SHALL share one stem of the form
`<corpus>-<YYYY-MM-DD>-<task-slug>`: the directory is `.acordia/work/<stem>/` and the product is
`.acordia/reports/<stem>.<ext>`. A date alone SHALL NOT be the sole discriminator in either name.

The **corpus token** SHALL be derived from the material under analysis rather than from the wording
of the request, so that two differently-worded dispatches against one corpus address the same
directory. It SHALL be derived as:

- an Aleph collection's `foreign_id`, where the instance supplies one;
- otherwise a slug of that collection's label;
- for a file corpus, a slug of the name of the directory or archive analysed.

Where a stem is already taken — the same corpus, the same date and the same task slug — the new
directory SHALL take a numeric suffix (`-2`, `-3`) and its product SHALL take the same suffixed
stem. No run SHALL overwrite another run's directory or product.

The reason is stated rather than only the rule: a write to a colliding name **succeeds**. Nothing in
either harness detects it, so a sweep of a second corpus silently replaces the first day's product
and the loss surfaces only when a reader opens the report and finds the wrong corpus inside it.

#### Scenario: The stem carries the corpus ahead of the date

- **WHEN** a prompt or skill states how a task directory or a report file is named
- **THEN** it gives the form `<corpus>-<YYYY-MM-DD>-<task-slug>` and states that the report takes the
  same stem under `.acordia/reports/`

#### Scenario: The corpus token comes from the material

- **WHEN** the derivation of the corpus token is stated
- **THEN** it names the Aleph `foreign_id`, the collection label as its fallback, and the analysed
  directory or archive name for a file corpus — and does not derive the token from the request text

#### Scenario: Two corpora on one day do not collide

- **WHEN** two tasks run on the same date against two different corpora
- **THEN** their stems differ by the corpus token, and neither directory nor report overwrites the
  other

#### Scenario: A repeated run is suffixed rather than overwritten

- **WHEN** a task directory's stem is already taken
- **THEN** the convention states a numeric suffix for both the directory and its product, and states
  that a colliding write would otherwise succeed undetected

## MODIFIED Requirements

### Requirement: The report sink is a convention, not a permission

`.acordia/reports/` SHALL remain the suggested destination for an analyst product, stated as a
convention. No prompt or frontmatter SHALL present it as an enforced scope.

It is one of the two sinks under the `.acordia/` workspace root, the other being `.acordia/work/`
for task directories. The two are siblings with distinct contents — finished product on one side,
the working behind it on the other — and a product SHALL be addressable from its working by the
shared stem rather than by a path recorded anywhere.

`.acordia/ops/` SHALL NOT be named by any shipped artifact. It was the root of the operator journal,
and the pillar that recorded state there is removed; the analysis pillar records no operation state
and needs no journal root, which is a separate question from how many sinks its workspace holds.

#### Scenario: Sink is worded as a convention

- **WHEN** a prompt names `.acordia/reports/`
- **THEN** it presents the path as where the product belongs, without claiming any harness restricts writes to it

#### Scenario: The journal root goes with its pillar

- **WHEN** every agent prompt, command wrapper and skill in the distribution is searched for `.acordia/ops/`
- **THEN** no match is found

#### Scenario: The product is reachable from its working

- **WHEN** a finished product exists in `.acordia/reports/`
- **THEN** its filename stem equals the name of the `.acordia/work/` directory the working was done
  in, so one is found from the other without a recorded path

### Requirement: The orchestrator supplies the task directory and the bound

`cyber-analyst` SHALL state the task-directory convention: each task gets its own directory under
`.acordia/work/`, named and shaped as `briefing-reporting` states — the stem
`<corpus>-<YYYY-MM-DD>-<task-slug>`, and a `README.md` carrying the originating request
**verbatim**, the date, and one line on what is being settled. The prompt SHALL name the parent
itself, because that is the part whose absence sends an unbriefed task into the current directory,
and SHALL defer the stem and the `README.md` shape to the skill rather than restating them, per the
requirement that a prompt routes to a skill instead of restating its technique. The analysts' notes
files belong in that same directory, and the orchestrator SHALL read them before it fuses.

Where the orchestrator's own brief names a directory, it SHALL use that directory exactly as given
and SHALL NOT substitute a path of its own: a lead and a sandboxed leg can reach one directory under
two different names, so a constructed path is wrong on one side of that boundary. Where the brief
names none, the orchestrator SHALL create one under `.acordia/work/` with that stem and state where
it is, so the convention has a defined outcome in both cases rather than only when a deployment
supplies the input.

No **absolute or deployment-specific** directory path SHALL be written into any prompt: such a path
is exactly what a brief exists to supply, and baking one in is wrong on one side of a sandbox
boundary. The relative convention roots `.acordia/work/` and `.acordia/reports/` are not paths of
that kind and SHALL be named in the prompts, because a convention nobody states resolves to the
current directory by default.

`cyber-analyst` SHALL supply **both** the directory and the reply bound in every dispatch, alongside
the objective, operating logic, stage, tempo and risk tolerance it already carries. An unstated bound
is the orchestrator's defect and not the leg's, because a leg told nothing cannot size a reply it was
never given the size of.

The convention exists so an operation is navigable afterwards — by the human operator the pillar
hands its product to, or by the orchestrator itself once its own context has been compacted. The
request is kept verbatim because a paraphrase is already an analytic judgement, made at the moment
least is known. The corpus token is part of the name for the same reason: a directory identified only
by its date is navigable on the day it was made and ambiguous on every day after.

#### Scenario: Convention stated in the lead prompt

- **WHEN** `cyber-analyst`'s prompt is read
- **THEN** it states the per-task directory under `.acordia/work/`, names `briefing-reporting` as
  carrying that directory's stem and `README.md` shape, and states that the legs' notes go in the
  same directory

#### Scenario: Both are supplied on dispatch

- **WHEN** `cyber-analyst` dispatches any leg
- **THEN** its prompt requires the brief to state the working directory and the bound on the reply

#### Scenario: No path is baked into a prompt

- **WHEN** the five prompts are searched for an absolute or deployment-specific task-directory path
- **THEN** none is found, and the specific directory is attributed to the dispatching brief while the
  relative convention root is stated

#### Scenario: The lead reads the notes before fusing

- **WHEN** the legs have returned and the orchestrator fuses their reads
- **THEN** its prompt requires it to read the notes files in the task directory, not to fuse from the
  bounded summaries alone
