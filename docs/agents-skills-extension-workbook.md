# Agents & Skills Extension Workbook (Markdown)

How to extend CyberStrike with **custom agents** and **custom skills** using
markdown files only — no source changes, no rebuild. Drop a file in the right
directory and CyberStrike loads it on next start.

> **Scope:** this workbook covers the markdown/config extension path exclusively.
> A handful of built-in behaviors require editing TypeScript in
> `packages/cyberstrike/src/agent/agent.ts` and are **out of scope** here. See
> [Markdown-only limits](#markdown-only-limits) for what those are and the
> markdown equivalent.

Agents and skills are **two independent systems** loaded by **two different code
paths**. An agent works with zero skills; a skill ships without any agent. They
meet at exactly one point: an agent's `skills:` list *references* skills by name.

```
AGENT track (always):   pick mode ─▶ set permissions ─▶ write prompt ─▶ (reference skills, optional)
SKILL track (optional): only if the methodology doesn't exist yet ─▶ author SKILL.md ─▶ agent references it
```

---

## 1. What loads from where

### 1.1 Agents

Agent markdown is discovered by `loadAgent()`
(`packages/cyberstrike/src/config/config.ts`) with the glob
`{agent,agents}/**/*.md`, scanned in every **config directory**:

| Directory | Scope |
| --------- | ----- |
| `~/.config/cyberstrike/agent/<name>.md` | Global (your machine, not in git) |
| `<repo>/.cyberstrike/agent/<name>.md` | Project (committed to the repo, walked up from cwd to worktree root) |
| `~/.cyberstrike/agent/<name>.md` | Home-scoped |
| `$CYBERSTRIKE_CONFIG_DIR/agent/<name>.md` | Explicit override dir, if the env var is set |

Loaded agents are merged **over** the built-in (native) registry, so a markdown
file can override or extend a native agent — or add a brand-new one.

- **Agent name** = the file path relative to `agent/` (nested dirs joined,
  extension trimmed). A frontmatter `name:` overrides the filename.
- **Prompt** = the markdown body (everything after the frontmatter).
- **Duplicate name** across config dirs → the **last-scanned** directory wins.
  Scan order (each overrides the previous): `~/.config/cyberstrike` → project
  `.cyberstrike` from cwd upward to the worktree root → `~/.cyberstrike`. So a
  home `~/.cyberstrike` agent overrides a project one of the same name.

Sibling directories `{command,commands}/` and `{mode,modes}/` in the same config
dirs load slash-commands and legacy modes; `mode/*.md` files become `primary`
agents. This workbook focuses on `agent/`.

### 1.2 Skills

Skill markdown is discovered by `Skill.state()`
(`packages/cyberstrike/src/skill/skill.ts`). Files are named **`SKILL.md`** and
live in a folder named after the skill. Load order (later entries win on a name
collision):

```
1. External (Claude Code compatible)   glob: skills/**/SKILL.md
     global:  ~/.claude/skills/**        ~/.agents/skills/**
     project: <up-tree>/.claude/skills/** <up-tree>/.agents/skills/**
2. CyberStrike config dirs             glob: {skill,skills}/**/SKILL.md
     ~/.config/cyberstrike/  +  <up-tree>/.cyberstrike/  +  ~/.cyberstrike/
3. Built-in                            repo-root .cyberstrike/skill  OR  $XDG_DATA/cyberstrike/skill/
4. config skills.paths[]               glob: **/SKILL.md   (any folder you list)
5. config skills.urls[]                downloaded skill bundles
```

**Where to put a custom skill** (any of these; pick by scope):

| Location | Scope |
| -------- | ----- |
| `<repo>/.cyberstrike/skill/<name>/SKILL.md` | Project, committed (recommended) |
| `~/.claude/skills/<name>/SKILL.md` | Global, shared with Claude Code |
| `~/.config/cyberstrike/skill/<name>/SKILL.md` | Global CyberStrike |
| a folder listed in `skills.paths` | Anywhere you point config at |

Config knobs (`cyberstrike.json{c}`):

```jsonc
{
  "skills": {
    "paths": ["~/my-skills"],                 // extra roots, globbed for **/SKILL.md
    "urls":  ["https://example.com/.well-known/skills/"], // remote bundles
    "disabled": ["skill-name"]                // managed via the skill panel / API
  }
}
```

The env flag `CYBERSTRIKE_DISABLE_EXTERNAL_SKILLS` turns off step 1
(`.claude` / `.agents` scanning).

> **Overriding a built-in skill by name:** built-in skills (step 3) are scanned
> **after** `.cyberstrike/skill` (step 2), so a same-named skill placed in
> `.cyberstrike/skill` will be overwritten by the built-in — it does **not** win.
> Only `skills.paths` (step 4) and `skills.urls` (step 5) scan later than built-in
> and can override one. For a brand-new skill, just use a unique name and this
> never applies.

---

## 2. Format contract

### 2.1 Agent frontmatter

Schema: `Config.Agent` in `packages/cyberstrike/src/config/config.ts`. All fields
optional except that the body (prompt) should be non-empty.

```markdown
---
description: <ONE sharp sentence — WHEN to use this agent>   # dispatch signal for subagents
mode: all                     # subagent | primary | all   (default "all" for custom agents)
steps: 30                     # max agentic iterations before a forced text-only reply
temperature: 0.2
top_p: 0.9
color: error                  # theme name ONLY: primary/secondary/accent/success/warning/error/info — or a quoted hex "#RRGGBB"
hidden: false                 # hide a subagent from the @ autocomplete menu
# model: anthropic/claude-sonnet-5   # provider/modelID; omit to ride the session model
skills:                       # recommend-list: grants runtime skill-tool access + "load these first" hint
#  - attack-jwt
#  - wstg-auth-session
permission:                   # PermissionNext ruleset; merges OVER defaults + user config
  "*": deny
  read: allow
  bash: allow
# disable: true               # skip/remove this agent (e.g. to disable a native one)
---

You are <persona>. <system prompt body — becomes agent.prompt verbatim>
```

Notes:

- `mode`: `subagent` (dispatched by an orchestrator via the `task` tool),
  `primary` (you select it for a whole session), `all` (both).
- Unknown frontmatter keys fall into `options`.
- The legacy `tools: { name: bool }` map is **deprecated** — use `permission`.
- **Invalid frontmatter throws.** A bad field (e.g. `color: red` — not a hex or a
  theme name) fails schema validation and aborts config loading, not just that
  one agent. Keep `color` to the theme enum or a **quoted** hex.

### 2.2 Skill `SKILL.md` frontmatter

Schema: `Skill.Info` in `packages/cyberstrike/src/skill/skill.ts`. Only `name`
and `description` are required.

```markdown
---
name: attack-jwt                        # REQUIRED — convention: match the folder name
description: "JWT attacks — alg:none, key confusion, claim tampering"   # REQUIRED
category: "web-application"             # groups the skill in the skill-tool UI
version: "1.0"
author: "you"
tags: [jwt, authentication, token]
tech_stack: [web]                       # search filter (skill tool `tech`)
cwe_ids: [CWE-287, CWE-347]             # search filter (skill tool `cwe`)
owasp_id: "A07"
chains_with: [attack-idor-automation]   # kill-chain graph edges
prerequisites: []
severity_boost:
  attack-idor-automation: "JWT tamper + IDOR = full account takeover"
# --- signing (see caveat below) ---
# sha256: "<hex>"
# signature: "<base64>"
# signed_by: "cyberstrike-official"
---

# Skill Title
## Objective
## Testing Methodology
### Phase 1 …
```

The body is the content the `skill` tool loads on demand. Sibling files
(`scripts/`, `reference/`) are surfaced to the agent as `<file>` paths relative
to the skill folder.

#### Signing caveat (important)

Verification (`SkillSigning.verify`) resolves a status per skill:

```
no sha256                                   → "unverified"   (loads normally)
sha256 present, mismatches body             → "tampered"     ⚠ SKIPPED — not loaded
sha256 matches, signed_by ≠ official        → "community"
sha256 matches + valid Ed25519 official sig → "official"
sha256 matches, bad/invalid signature       → "tampered"     ⚠ SKIPPED
```

**For hand-authored skills, omit `sha256`.** If you add a hash and later edit the
body without recomputing it, the skill silently fails its integrity check and
will not load. Only add `sha256`/`signature` if you run the signing flow (see
`docs/skill-signing.md`).

---

## 3. Runbook — add a custom agent

Path is fixed to markdown. Walk the steps in order — four decisions, then verify.

### Step 1 — Location

| Put file in | Effect |
| ----------- | ------ |
| `.cyberstrike/agent/<name>.md` | Committed to repo; everyone on this checkout gets it |
| `~/.config/cyberstrike/agent/<name>.md` | Personal machine only, not in git |

Filename (kebab-case) becomes the agent name unless frontmatter `name:` overrides.

### Step 2 — Mode

- **Subagent** — dispatched by the `cyberstrike` orchestrator via `task`. Its
  `description` is the **only** routing signal; make it sharp and specific.
- **Primary** — you pick it as the session's top-level agent.
- **All** — both; good while iterating.

### Step 3 — Permissions (deny-by-default)

Start locked down, then allow only what the job needs. A brand-new agent inherits
the base defaults (`*: allow`, `doom_loop: ask`, `question: deny`, `.env` reads
prompt) and then your `permission` block on top, so setting `"*": deny` first is
what actually locks it down. Anything not explicitly allowed is blocked.

> Note: the built-in `proxy-tester-injection` agent carries extra
> **specific** deny patterns (SQL DDL / RCE strings under `bash`). Those only
> apply if you *override that specific native agent* by reusing its name — a new
> custom agent does not inherit them. A broad `bash: allow` will not override a
> more-specific deny pattern (permissions evaluate by specificity).

Common tool grants for offensive specialists:

```yaml
permission:
  "*": deny
  read: allow
  grep: allow
  glob: allow
  bash: allow
  # web:        webfetch: allow   websearch: allow   browser: allow
  # findings:   report_vulnerability: allow   triage_vulnerability: allow
  # methodology: add_intel: allow  update_vrt_check: allow  methodology_status: allow  scope_check: allow
  # tooling:    attack_script: allow   ensure_tools: allow
  # writes:     edit: allow   write: allow          # OFF by default — enable only if it must modify files
```

If the agent is a variant of a native specialist, clone that specialist's
permission block (`web-application`, `mobile-application`, `cloud-security`,
`internal-network` in `agent.ts`) rather than hand-picking.

### Step 4 — Prompt + skills

- Write the system prompt as the markdown body. Optionally bootstrap it with the
  agent generator (`Agent.generate()`), then hand-tune.
- Reference existing skills via `skills:` (a recommend-list, not a copy). Only
  author a new skill if the methodology is genuinely missing (Section 4).

### Full example

`.cyberstrike/agent/graphql-hunter.md`:

```markdown
---
description: Use for GraphQL-specific testing — introspection, batching/aliasing abuse, field-level authz. Dispatch when a target exposes a GraphQL endpoint.
mode: all
steps: 30
color: "#c026d3"                        # hex must be quoted — a bare #... is a YAML comment
skills:
  - attack-graphql
  - wstg-authz-01
permission:
  "*": deny
  read: allow
  grep: allow
  glob: allow
  bash: allow
  webfetch: allow
  report_vulnerability: allow
  triage_vulnerability: allow
  methodology_status: allow
  scope_check: allow
---

You are a GraphQL security specialist. You test GraphQL APIs for introspection
exposure, query batching and alias-based rate-limit bypass, injection through
resolvers, and field-level authorization gaps.

Methodology:
1. Enumerate the schema (introspection, or infer it if disabled).
2. Map every query/mutation to its authorization expectation.
3. Test batching/aliasing for rate-limit and cost-control bypass.
4. Probe resolver arguments for injection.
5. Report confirmed findings via report_vulnerability; log coverage as you go.
```

### Step 5 — Verify (evidence, not assumptions)

- Start CyberStrike; the agent appears in `agent list` / the `@` menu (unless
  `hidden`).
- Select or dispatch it; confirm the router picks it. If a subagent isn't
  chosen, sharpen the `description`.
- Trip a denied tool and confirm the allowlist blocks it.

---

## 4. Runbook — add a custom skill

Do this **only** when the methodology you need isn't among the built-in skills
(search first: the `skill` tool's `search`/`list` actions, or grep
`.cyberstrike/skill/`).

1. `mkdir .cyberstrike/skill/<my-skill>/` and create `SKILL.md`.
2. Frontmatter: `name` (match the folder), `description` (this is what the skill
   tool searches — make it triggering-quality). Add `category`, `tech_stack`,
   `cwe_ids` so search and filters find it.
3. Body: Objective → Methodology (phased) → payloads. Put scripts in `scripts/`,
   references in `reference/` (auto-surfaced to the agent).
4. Wire relationships: `chains_with` + `severity_boost` feed kill-chain
   suggestions.
5. **Do not** add `sha256` unless you sign it (Section 2.2 caveat).
6. Verify it loads: launch CyberStrike, run the `skill` tool `search`/`list`.
7. Optionally reference it from an agent's `skills:` list.

### Skill example

`.cyberstrike/skill/attack-graphql-cost/SKILL.md`:

```markdown
---
name: attack-graphql-cost
description: "GraphQL cost/complexity abuse — deep nesting, aliasing, batching to bypass rate limits and exhaust resources"
category: "web-application"
tech_stack: [web, graphql]
cwe_ids: [CWE-770, CWE-400]
chains_with: [attack-graphql]
---

# GraphQL Cost & Complexity Abuse

## Objective
Bypass rate limiting and exhaust backend resources via expensive GraphQL queries.

## Testing Methodology
### Phase 1: Measure cost controls
...
### Phase 2: Alias/batch amplification
...
```

---

## 5. Gotchas & verification

- **Subagent routing** depends entirely on `description`. Vague description →
  never dispatched.
- **Overriding a native agent:** reuse its name (markdown merges over the native
  registry), or set `disable: true` to remove it — both verified in `agent.ts`.
- **Overriding a built-in skill** by name does **not** work from `.cyberstrike/skill`
  (built-in scans later and wins); use `skills.paths`/`urls`. A `skills.disabled`
  config field exists (managed by the skill panel/API), but its load-time
  enforcement was not confirmed in the loader — don't rely on it to hide a skill.
- **Stale `sha256`** on a skill → silently dropped as `tampered`. Omit the hash
  for hand-authored skills.
- **Duplicate names** → the last-scanned source wins. Agents: see the scan order
  in §1.1 (home `~/.cyberstrike` wins last). Skills: see the load-order list in
  §1.2 (built-in beats `.cyberstrike/skill`; only `skills.paths`/`urls` beat
  built-in).
- **Permissions:** a new custom agent starts from the base defaults, then your
  block applies on top — lead with `"*": deny` to lock it down. Specific deny
  patterns (like the injection tester's) outrank a broad allow only when you
  inherit them by overriding that native agent.
- No type check needed for the markdown path (no TypeScript changes).

<a name="markdown-only-limits"></a>
### Markdown-only limits

These require editing `agent.ts` (native path) and are **not achievable** in
markdown — with the markdown equivalent noted:

| Native-only behavior | Markdown equivalent |
| -------------------- | ------------------- |
| Static skill embedding (inline skill content into the prompt, like the built-in vuln testers) | Reference via `skills:` recommend-list + the runtime `skill` tool |
| `useSmallModel` (route to the provider's cheap tier) | Pin a specific cheaper `model` if desired |
| `prependRequestContext` | n/a |
| Hidden pipeline plumbing agents (compaction/title/proxy pipeline) | Out of scope |

Everything else — primary/subagent/all, deny-allowlist permissions, `model`,
`steps`, `color`, `hidden`, referencing any built-in skill, and authoring new
skills — is fully available in markdown.

---

## 6. Upstream opencode — verified locations & conventions

CyberStrike is a fork of **opencode**. When you author agents and skills meant to
run in **plain opencode** (portable, not CyberStrike-specific), target opencode's
own config tree, which differs from CyberStrike's. The paths and fields below are
verified against opencode's docs (`opencode.ai/docs/agents`, `/docs/skills`).

### 6.1 Discovery paths

| Artifact | Global | Project |
| -------- | ------ | ------- |
| **Agents** | `~/.config/opencode/agents/<name>.md` | `.opencode/agents/<name>.md` |
| **Skills** | `~/.config/opencode/skills/<name>/SKILL.md` — and also `~/.claude/skills/`, `~/.agents/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` |

opencode scans **six** skill dirs (three homes × global/project) and reads the
Claude-compatible `.claude/skills` and `.agents/skills` families too. The agent
**filename is the agent name**.

### 6.2 opencode frontmatter

- **Agent** (only `description` needed): `description`, `mode`
  (`subagent`/`primary`/`all`), `model`, `temperature`, `permission`, `steps`.
  The body is the system prompt.
- **Skill** (`SKILL.md`): **required** `name` (lowercase-hyphen, `^[a-z0-9]+(-[a-z0-9]+)*$`, 1–64 chars) and
  `description` (1–1024). **Optional** `license`, `compatibility`, `metadata`
  (string→string map). **Unknown fields are ignored** — so CyberStrike-only skill
  fields degrade gracefully but do nothing in opencode.

### 6.3 opencode vs CyberStrike — the differences that bite

| | opencode | CyberStrike |
| --- | -------- | ----------- |
| Dir names | **plural** `agents/`, `skills/` under `~/.config/opencode` and `.opencode` | `{agent,agents}` / `{skill,skills}` globs under `~/.config/cyberstrike` and `.cyberstrike` |
| Agent→skill binding | **none** — skills fire by `description`; there is **no `skills:` field** | agent `skills:` recommend-list references skills by name |
| Skill frontmatter | `name` + `description` (+ optional `license`/`compatibility`/`metadata`) | superset: `category`, `cwe_ids`, `chains_with`, `severity_boost`, signing, … |
| Claude-compatible dirs | reads `.claude/skills` + `.agents/skills` | reads `.claude/skills` + `.agents/skills` |
| Agent permissions | default **allow**; `edit` governs edit/write/patch (there is **no** `write` key); a top-level `"*": deny` is **accepted but overridden** by per-tool built-in defaults (e.g. `read` stays `allow`), so it does **not** deny-default — express read-only as `edit: deny` (+ `task: deny` for leaf subagents) | deny-default via `"*": deny` then an allowlist |

opencode agent `permission` keys (verified): `read`, `edit`, `glob`, `grep`, `list`,
`bash`, `task`, `skill`, `lsp`, `question`, `webfetch`, `websearch`,
`external_directory`, `doom_loop`. Values `allow`/`ask`/`deny`; unlisted tools
default to `allow` (except `external_directory`/`doom_loop` → `ask`, and `.env`
reads → `deny`). Verify a resolved agent with `opencode debug agent <name>`.

**Path-scoped `edit`.** Like `bash`, the `edit` permission accepts glob rules with
**last-match-wins** precedence, so a read-only agent can be granted a single
writable sink without opening up the rest of the tree:
`edit: { "*": deny, ".acordia/reports/**": allow }`. In this repo that block is
reserved for the two agents holding the *Briefing & written reporting* grid
competency (`operational-analyst`, `fusion-analyst`), which write their reports to
`.acordia/reports/`; every other analyst uses a blanket `edit: deny`. Note this is
a **posture** control, not a sandbox — `bash: "*": allow` already permits scripted
writes — so the scoped block declares the sanctioned output path rather than
granting a new capability class.

The load-bearing one: in opencode an agent **cannot** list its skills. Composition
is by (a) triggering-quality skill `description`s and (b) the agent **prompt**
naming the skills it draws on.

### 6.4 Conventions (onwards)

For portable / opencode-native agents and skills:

- Skills → `~/.config/opencode/skills/<name>/SKILL.md`; agents →
  `~/.config/opencode/agents/<name>.md`.
- **Plain kebab-case slugs, no prefix.** `name` equals the folder slug.
- **No symlinks** and no canonical-source-plus-symlink schemes — author the file
  once, in place, in the opencode dir.
- **Compose by description + prompt**, not a `skills:` list: write the skill
  `description` to trigger, and have the agent prompt name its skill set.

## 7. omp (`oh-my-pi`) — the second harness

omp is the other harness this repo deploys to. Verified against omp 17.1.8
(`omp://task-agent-discovery.md`, `omp://skills.md`,
`omp://system-prompt-customization.md`). The two halves behave very differently.

### 7.1 Skills need no translation

omp registers an `opencode` skill provider (priority 55) that scans
`~/.config/opencode/skills` using the same non-recursive `<name>/SKILL.md`
layout. Skills installed for opencode are therefore already live in omp. The
omp-native user location is `~/.omp/agent/skills`; installing to both is
harmless because omp de-duplicates by `realpath` before it de-duplicates by
name.

omp reads more frontmatter than opencode does — `globs`, `alwaysApply`, `hide`,
`disableModelInvocation` — and ignores the rest. `name` defaults to the
directory name. Nothing in this repo's skill files needs to change, which is
why the plugin trees carry a verbatim copy of each pillar's `skills/` rather
than a translated one: the same bytes are valid in opencode, omp, and Claude
Code.

### 7.2 Agents need translation

omp discovers task agents from `<project>/.omp/agents`, `~/.omp/agent/agents`,
and installed plugin roots' `agents/` directories. It **deliberately skips**
`.claude/agents`, `.codex/agents`, and `.gemini/agents` because their
frontmatter is not the omp contract, and it does not look at
`~/.config/opencode/agents` at all. An opencode agent file is invisible to omp
no matter where it sits.

This repository reaches omp through the plugin path: `tools/build-plugins.py`
generates the omp-form agents into `plugins/omp/<plugin>/agents/`, and omp's
marketplace installer places that tree. **Plugin agents are surfaced only while
the `claude-plugins` capability provider is enabled** — listed in
`disabledProviders`, the plugin installs cleanly and contributes nothing.

The mapping `tools/build-plugins.py` implements for omp:

| Concern | opencode | omp |
| --- | --- | --- |
| Name | filename stem | **required** `name:` field — a file missing `name` or `description` is skipped with a logged warning |
| Role | `mode: primary` / `subagent` / `all` | no modes; every file-defined agent is a subagent reached through the `task` tool |
| Tool access | `permission:` map, allow-by-default with denies | `tools:` allowlist; an absent tool does not exist for that agent — **except** the xd:// transport tools, see 7.3. omp appends `yield` automatically |
| Read-only | `edit: deny` | omit `edit` from `tools:`; `edit` really does disappear, `write` does not |
| Path-scoped write | `edit: { "*": deny, ".acordia/reports/**": allow }` | **no equivalent** — omp scopes per tool, never per path, and cannot deny `write` at all under default settings |
| Delegation | `permission.task` map naming allowed agents | `task` in `tools:` **plus** `spawns:` listing allowed agent names (`*` for any) |
| Leaf specialist | `task: deny` | omit `task` from `tools:`; leave `spawns` unset |
| Skill binding | none — the prompt names its skills in prose | optional `autoloadSkills:` injects the named skills' full bodies at subagent start |
| Model | `model: provider/id` | `model:` (accepts role aliases such as `@smol`), plus `thinkingLevel:` |
| Extra metadata | ignored | preserved as unknown keys |

Two more omp-only fields worth knowing: `output:` declares a structured-output
schema, and `readSummarize: false` makes the agent's `read` return verbatim file
content instead of a structural summary.

### 7.3 Tool differences that reach into the prompt and the allowlist

omp has **no `list` tool** — a directory path handed to `read` enumerates it.
Any prompt that instructs an agent to use `list` is wrong under omp, which is
why the translator rewrites that paragraph and then asserts that no `` `list` ``
token survives. `read`, `grep`, `glob`, `bash`, `web_search`, and `task` carry
over unchanged.

**The allowlist has one hole.** omp's `XDEV_TRANSPORT_TOOLS` are `read` and
`write`: they are the channel every `xd://` device is invoked through, so both
are present whenever the `tools.xdev` setting is on, which is the default —
regardless of what the agent's `tools:` list says. Verified on omp 17.1.8 by
asking a translated leg agent, whose allowlist has no `write`, to create a
scratch file with the `write` tool; it succeeded and a read-back confirmed the
file. `edit` and `task` were correctly absent from the same agent, so the
allowlist is enforced in general.

The consequence for a read-only agent: omitting `edit` and `task` works;
omitting `write` does not. Under omp, "read-only" means no editing tool and no
dispatch, with writes constrained by the prompt rather than by the harness.
Disabling `tools.xdev` restores full allowlist enforcement at the cost of
moving every discoverable tool back into the top-level schema.

### 7.4 There is no file-defined primary agent

omp has no `mode: primary`. An opencode primary agent has two possible landings:

- **Spawnable orchestrator** (what this repo does) — give it `task` in `tools:`
  and name its legs in `spawns:`. It keeps its own prompt and, like any
  subagent, inherits the session's discovered-skills list.
- **Session persona** — `~/.omp/agent/SYSTEM.md` or `<project>/.omp/SYSTEM.md`.
  Beware: `SYSTEM.md` **replaces prompt block 0**, and block 0 is where omp
  injects the discovered-skills list. A persona installed this way must hard-code
  the skill names it wants the model to know about, which reintroduces drift.
  `APPEND_SYSTEM.md` keeps block 0 but layers onto omp's coding-agent prompt
  rather than replacing it.

### 7.5 Deploy and verify

```sh
tools/build-plugins.py                                    # regenerate the plugin trees
omp plugin marketplace add <owner>/acordia-agents         # or ./. for a local checkout
omp plugin install acordia-analysts@acordia --scope user  # acordia-operators for the offensive pillar
```

`/reload-plugins` refreshes skills and commands in a running session; new tools
or hooks need a restart.

The omp-form agents live at `plugins/omp/<plugin>/agents/` and are **committed
build output** — a marketplace install clones the repository and performs no
build on the installing machine. Edit `analysts/agents/*.md` and rebuild, never
the generated file; `tools/build-plugins.py --check` is the drift gate.

`autoloadSkills` is left unset unconditionally. A prebuilt plugin is installed
by the harness rather than by a user-invoked command, so there is no invocation
to carry a flag; the `(deep)` heading is still parsed on every build, and a
broken one still fails it.

To verify, start omp and check that the four analysts appear in the agent
roster the `task` tool advertises, that `/acordia-analysts:fusion` is
registered, and that `operational-analyst` can spawn its three legs while the
legs cannot spawn anything.

---

## 8. CyberStrike substitution contract — for future ports

`operators/` is the first pillar ported from a CyberStrike-derived fork rather than
derived from an ACORDIA competency map. Its prompts and skill bodies called twelve
platform tools that exist only inside CyberStrike (methodology engine, vulnerability
reporting, attack-script runner, hackbrowser crawler, `skill` CLI). This section is
the one place that mapping is documented, so a future pillar ported from the same
fork reuses it instead of inventing a second one — see
[`docs/roles/operator.md`](roles/operator.md), which references this section rather
than restating the table.

### 8.1 Tool substitution table

Every ported prompt and skill body SHALL name only tools the target harness
provides. Each CyberStrike platform tool below is replaced exactly as follows,
at every occurrence, preserving the upstream intent — the same information
recorded, the same test performed — rather than deleting the step:

| CyberStrike tool | Portable substitution |
| --- | --- |
| `add_intel` | append an entry to `.acordia/ops/intel.md` |
| `update_vrt_check`, `record_coverage_note` | append an entry to `.acordia/ops/coverage.md` |
| `methodology_status`, `get_coverage_notes` | read `.acordia/ops/coverage.md` and `.acordia/ops/intel.md` |
| `scope_check` | read `.acordia/ops/scope.md` before touching a new host, domain, account, or subnet |
| `report_vulnerability`, `triage_vulnerability` | write `.acordia/ops/findings/<slug>.md` |
| `generate_report` | compose the report from the journal into `.acordia/ops/reports/<name>.md` |
| `ensure_tools` | install with `bash`, after asking the user first |
| `attack_script <name>` | the equivalent standard tool (`jwt_tool`, `ffuf`, `sqlmap`, `nuclei`) or an explicit inline command (`curl`, `python3 -c`), preserving the same test |
| `hackbrowser` | the `browser` tool where the harness provides it (omp does; stock opencode does not); otherwise scripted HTTP requests — always ask the user before an automated crawl |
| `skill search`/`load`/`unload` | nothing — skills fire by description match, and the prompt already names the skill set it draws on |

Intel entries carry a severity (`critical`/`high`/`medium`/`low`/`informational`)
and a confidence (`confirmed`/`high`/`medium`/`low`). Coverage entries carry the
request sent, the response summary, and the reasoning that proves or disproves
the issue — CyberStrike's own coverage discipline, kept intact.

A prompt that would need a tool present in one harness but not the other
(`browser` exists in omp and CyberStrike, not in stock opencode; `list` exists in
opencode, not in omp) states the condition and names the fallback, rather than
assuming the tool is there.

### 8.2 The `.acordia/ops/` operation journal

CyberStrike keeps operation state — intel, coverage, findings, reports — in its
own methodology-engine database. Neither opencode nor omp has an equivalent, so
the state moves to files, in a fixed layout every ported prompt names the same
way:

| Path | Content |
| --- | --- |
| `.acordia/ops/scope.md` | authorised targets, exclusions, rules of engagement |
| `.acordia/ops/intel.md` | append-only intel log — endpoints, credentials, technologies, parameters, configuration, auth flows, with severity and confidence |
| `.acordia/ops/coverage.md` | append-only coverage log — what was tested, the request sent, the response summary, and the reasoning |
| `.acordia/ops/findings/<slug>.md` | one confirmed finding per file, with evidence |
| `.acordia/ops/reports/<name>.md` | composed engagement reports |

The path mirrors the analyst pillar's existing `.acordia/reports/` sink, so the
two pillars share one operator-visible convention. The journal is **discipline,
not a permission scope**: it is described in every operator prompt's body, but
no `edit` rule attempts to confine writes to it — omp scopes a tool by name
only, never by path, so a scoped rule would hold in opencode and silently
evaporate in omp. `scope_check`'s substitution follows the same logic as the
analyst pillar's read-only posture: an absent or silent scope file means a
target is **untested**, never implicitly in scope.

