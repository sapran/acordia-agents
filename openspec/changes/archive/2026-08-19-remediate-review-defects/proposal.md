## Why

An architecture review of this distribution found eleven defects. Nine are structural or mechanical and are fixed here; two are content redesign (the operator prompts that re-type their own skills, and the absence of a selection layer over 73 skills) and are deliberately deferred, because they change what the agents say rather than whether the distribution is correct.

The review's most serious finding was outside the repository and has already been remediated by hand: on the maintainer's workstation all nine agents sat in `~/.omp/agent/agents/` as copies made on 2026-07-31 by the since-deleted `tools/translate-omp.py`. omp resolves that directory *before* plugin roots and dedups first-wins, so those copies were the agents actually running — including the four analyst prompts as they read before `loosen-analyst-interagent` trimmed roughly 1,380 words of duplicated protocol from them on 2026-08-05. The installed plugin recorded 2.0.0 against a repository at 2.4.0, and `acordia-operators` was installed in no registry at all while being fully live from the shadow. The 73 skill entries beside them were symlinks into the checkout, so skills tracked the working tree while agents were frozen two weeks stale.

Nothing in the repository could have detected that. The generator sees only its own inputs and outputs; `--check` compares the committed tree against a rebuild and is blind to what a machine actually loads. Current behavior: a maintainer can carry stale agents, a stale plugin version, and an uninstalled-but-live pillar simultaneously, with every install-state command reporting success. Desired behavior: one command reports install skew, native shadowing, and the prompt-size and duplication figures that the deferred content phase will act on.

The remaining defects share a shape: contracts this repository states in prose and nothing executes.

- Five operator agents carry a byte-identical destructive-bash deny map, hand-synced across five frontmatters — 24 globs as the review found it, and 29 once the single-cased SQL-to-RCE patterns gain the case variants a literal glob match needs. An edit to one leaves a bypass in four.
- An agent may name a skill slug that does not exist. Nothing resolves the `·`-separated lists the prompts use to declare their skill sets, and `deep_skills()` already parses one of those lines and throws the result away.
- `metadata.acordia` forks by pillar — `{leg, column, source_paragraph}` for analysts, `{pillar, role}` for operators — under one key name, so `agent_color()` has to accept either.
- A path-scoped `edit` posture yields opposite capability per harness: no write tool at all in omp, `Write` still allowed in Claude Code. The source states one intent; the two targets disagree about it.
- `browser: allow` is translated for omp and dropped for Claude Code with no note, unlike every other unmappable posture.
- `--check` reports a macOS `.DS_Store` under `plugins/` as generator drift and exits 1.
- `operational-analyst` names `analyst-loop` in prose as the skill formalising its own cycle, and declares it in neither of its own skill lists.
- All four analysts hold `web_search` in omp through the generator's `BASE_TOOLS`, while their opencode sources declare no web permission at all and rely on opencode's `allow` default to supply one. Nothing is denied there, but nothing is stated either: `fusion-analyst`'s body claims responsibility for open sources under a frontmatter that says nothing about fetching.
- Three published specs still carry the literal placeholder `TBD - created by archiving change <slug>. Update Purpose after archive.`, and `docs/implementation-notes.md` parks a note about a script that no longer exists.

## What Changes

### The generator gains four gates, one report, and two translation corrections

`tools/build-plugins.py`:

- **Fatal** — every agent's `metadata.acordia` declares `pillar` matching its source directory and `role` in `{orchestrator, specialist}`, with `role: orchestrator` if and only if `mode: primary`, and no `leg` key.
- **Fatal** — every skill slug named in a `·`-separated prompt line resolves to `<pillar>/skills/<slug>/SKILL.md` in that agent's own pillar. Skill lines are recognised by their shape, not by a hardcoded list of headings.
- **Fatal** — every write-capable agent's `bash` deny set equals one canonical constant in the generator. The lists stay in the sources, because opencode enforces them from there; the generator is simply the only place that sees all five at once.
- **Fatal** — no agent carries the removed `leg` key (folded into the metadata gate).
- `--doctor` reports install-state skew against both plugin registries, native shadowing under `~/.omp/agent/`, per-agent prompt size against the 10,000-character ceiling, orphan skills, skill-description proximity, and prompt/skill line duplication. It exits 0; `--strict` makes the first two findings fatal. Sections three through six stay report-only in every mode, because the phase that fixes them has not run.
- A path-scoped `edit` now appends `write` in omp, matching Claude Code, and the `write_access` note states the outcome rather than implying a scope.
- `browser: allow` gets a Claude-side comment note in the style of the other unmappable-posture notes.
- `relative_files()` skips `.DS_Store`, so a Finder artifact is no longer reported as generator drift.
- `agent_color()` reads `role` alone.

### Nine agent sources converge on one metadata schema

`{pillar, role}` on every agent; analysts keep `column` and `source_paragraph`; `leg` is removed, since an agent's identity is already its filename.

### The analyst roster gains two declarations it already had in effect

`analyst-loop` joins `operational-analyst`'s defining spine, first in the line, because the other spine skills are steps inside it. All four analysts gain `webfetch: allow` and `websearch: allow` — which widens nothing, since omp's `BASE_TOOLS` already carries `web_search` and opencode's permission default is `allow`, and instead makes the posture explicit in the source, where it also survives a deployer whose global `opencode.json` denies those tools.

### Three heading capitalisations and four stale documents

`internal-network.md`'s three title-cased H2s move to the sentence case its four siblings use. The three placeholder Purposes are written from the requirements actually present in each spec. `docs/implementation-notes.md`'s entry is retired against the code that exists now. `CLAUDE.md` and `README.md` narrow "omp has no marketplace runtime of its own" to the claim the quoted omp documentation actually supports: no separate *discovery* path.

### The version — a MINOR bump

`2.4.0` → `2.5.0`. Agent frontmatter and generated output both reach users.

**Deliberately not done here**, each a separate finding from the same review:

- moving the operator prompts' embedded technique catalogues into the skills that already own them (~310 lines across `internal-network.md` and `cloud-security.md`);
- collapsing the four WSTG bundles' duplication of the dedicated `attack-*` skills (~600–800 lines), and the missing `linux-postexploit`, mobile, and `attack-sqli` skills;
- the selection layer: discriminator-first descriptions, a skill-family tag, per-agent family maps, and the two analyst skill merges that would move competency-grid rows;
- the cross-pillar handoff between an analyst product and an operation journal;
- renaming and splitting `omp-harness-distribution`, whose install-script half no longer concerns omp, and the wrapper-routing requirement split between `plugin-packaging` and `acordia-command-namespace`;
- making the prompt-ceiling and prompt/skill-duplication findings fatal, which is the last step of the content phase, not of this one.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `plugin-packaging`: four new build gates, the `--doctor` report, the `.DS_Store` exclusion from drift detection, and the Claude-side `browser` note. The contracts the gates enforce are not new — the metadata anchors, the prompt skill-set declarations, and the destructive-bash denylist are all already stated; this change executes them.
- `omp-harness-distribution`: a path-scoped `edit` translates to `write` in omp, so one source posture yields one capability across both plugin harnesses.
- `analyst-agent-roster`: the orchestrator declares `analyst-loop`; all four analysts declare the web permissions they already hold in omp; the metadata schema unifies.
- `operator-agent-roster`: the metadata schema unifies, and the destructive-bash denylist gains a single canonical source without leaving the sources opencode enforces from.
- `competency-map-derivation`: the `metadata.acordia` anchor schema replaces `leg` with `pillar` + `role`.

## Impact

- **Modified:** `tools/build-plugins.py` (gates, `--doctor`, two translation corrections, `VERSION`); all nine `*/agents/*.md` (metadata, and for analysts the spine line and web permissions); `internal-network.md` (three heading casings); three `openspec/specs/*/spec.md` Purpose lines; `docs/implementation-notes.md`; `CLAUDE.md`; `README.md`.
- **Regenerated:** both `plugins/` trees — every agent file (metadata, colour, and the two translation corrections) plus the six files carrying the version.
- **Unchanged:** all 73 skill bodies, all 17 command wrappers, `install.sh`, `uninstall.sh`, and every prompt body except three heading lines and one skill list.
- **Behavioral risk:** the four fatal gates run against sources that have never been checked. Each was evaluated against the current tree during the review, and the expected failures are exactly the ones this change repairs; a gate failing on anything else is new information and should be treated as a finding rather than worked around. The scoped-`edit` correction gives `operational-analyst` and `fusion-analyst` a `write` tool in omp that the previous translation withheld — a capability they already had in practice, on two grounds recorded rather than assumed: an omp agent whose allowlist omitted `write` still wrote a file when asked (verified against omp 17.1.8), and `bash: allow` is an open write channel in every harness. omp's own documentation describes a narrower mechanism than "omission does not remove a tool", so the claim rests on that observation and is not generalised past it.
- **Verified before this change:** the workstation shadow and its exact staleness (the four analyst prompts, pre-trim, 2026-07-31 vintage), the 2.0.0-against-2.4.0 registry skew, `acordia-operators` installed nowhere, the 73 skill symlinks, `--check` exiting 1 on `plugins/.DS_Store`, and the two divergent scoped-`edit` translation paths.
