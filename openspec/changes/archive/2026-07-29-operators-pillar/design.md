## Context

Two repositories are involved. This one distributes opencode-schema markdown to two harnesses (opencode natively, omp via `tools/translate-omp.py`) and currently holds a single read-only pillar, `analysts/`. The other, `~/git/CyberStrike`, is a fork of opencode carrying a compiled offensive roster (16 agents, of which 6 are harness plumbing) and 7,656 skills.

Three properties of the source make the port tractable:

1. CyberStrike is an opencode fork, so its agent frontmatter is a **superset** of the schema this repo authors to — `name`, `description`, `mode`, `permission` all carry over; `skills:`, `native`, `hidden`, `color`, `useSmallModel`, `prependRequestContext` are fork extensions to drop.
2. Its skill files already use the `<slug>/SKILL.md` layout both harnesses discover, with `name` + `description` frontmatter.
3. `install.sh` discovers pillars by scanning for top-level non-dot directories carrying `agents/` or `skills/`, so a new pillar needs no installer change.

Two properties make it non-trivial:

1. The prompts and skill bodies call twelve platform tools that exist only in the fork (methodology engine, vulnerability reporting, attack-script runner, hackbrowser crawler, skill CLI). Copying them verbatim would ship agents that call nothing.
2. The bulk of the skill library is generated compliance corpora. Skill discovery in both harnesses puts every discovered skill's name and description into the system prompt, so library size is a per-session token cost, not a disk cost.

## Goals / Non-Goals

**Goals:**

- A second pillar, `operators/`, that runs in both harnesses with no fork-specific dependency.
- Faithful preservation of CyberStrike's technique content — payload tables, command sequences, phase structure — since that is the value being ported.
- One documented substitution table for fork tools, reusable by any future CyberStrike-derived pillar.
- Provenance for every artifact, so upstream drift is a mechanical diff.
- Zero change to the analyst pillar's behaviour.

**Non-Goals:**

- Reproducing CyberStrike's methodology engine, its coverage database, or its Liyakat agent-scoring loop. The journal is a flat-file stand-in for state, not a re-implementation.
- Porting the web-proxy pipeline (`proxy-agent`, `proxy-analyzer`, eight `proxy-tester-*`). Their inputs come from the fork's proxy database via `web_get_*`; without it the agents have nothing to read.
- Publishing the generated corpora.
- Vendoring the Python attack scripts. This repository stays markdown-only.

## Decisions

**Five agents, not fifteen.** The ported set is the primary plus the four domain specialists — the agents whose value is methodology rather than pipeline plumbing. The eight proxy testers are excellent prompts wired to a database this repo cannot supply; shipping them adapted would mean rewriting their input contract, which is a different change with a different reviewable surface. The six harness-internal CyberStrike agents (`general`, `explore`, `compaction`, `title`, `summary`, `normalize-request`) duplicate what both target harnesses already do natively.

*Alternative considered:* port all fifteen and mark the testers "requires captured traffic". Rejected — an agent that cannot read its own inputs is a stub, and the roster spec would have to describe a capability the pillar does not have.

**Thirty skills, not 7,656.** The 26 standalone technique skills plus the 4 WSTG bundles are hand-authored, self-contained methodology. The corpora are generated one-control-per-file reference material: 5,000 CIS + 1,606 NIST + 898 MITRE + 121 WSTG leaves. At roughly 25 tokens per prompt-listed skill entry, publishing them costs about 190k tokens per session in either harness — more than most context windows.

*Alternatives considered:* (a) publish with `hide: true`, which omp honours by excluding a skill from the prompt list while keeping `skill://` reachable — rejected because opencode has no equivalent, so the pillar would behave differently per harness, and a hidden skill the model cannot see the name of is unreachable in practice; (b) ship each corpus as one index skill with the tree as sibling assets under it (non-recursive discovery means nested `SKILL.md` files are never enumerated) — genuinely attractive, ~6 prompt lines for 43 MB of reference material, but it makes this a 43 MB markdown repository and needs its own lookup contract. Recorded as a candidate follow-up change rather than folded in here.

**Flat-file journal under `.acordia/ops/`.** CyberStrike's prompts are built around state calls: log intel, check coverage, verify scope, report a finding. Dropping those instructions would gut the methodology; faking them would be worse. Files are the one state mechanism both harnesses have. The path mirrors the analyst pillar's existing `.acordia/reports/` sink, so the two pillars share one operator-visible convention.

*Alternative considered:* keep state in the conversation only. Rejected — CyberStrike's own forced-continuation prompt exists because coverage claims need to survive across turns and across subagent boundaries; a subagent's context is gone when it returns, but a file it appended is not.

**`edit: allow`, unscoped.** Operators write scripts, evidence, and journal entries. A path-scoped `edit` (as the two reporting analysts carry) would be enforced in opencode and silently absent in omp, which scopes per tool and never per path — a posture that holds in one harness and evaporates in the other is worse than an honest `allow` plus prompt discipline. The destructive-command denies go on `bash` instead, where CyberStrike itself puts them, and the specs record that omp has no per-command equivalent.

**Permission-derived allowlist in the translator.** `BASE_TOOLS` is currently a constant expressing the analyst read-only posture; a second pillar with a different posture makes it wrong. Deriving `tools` from the source `permission` map keeps one translator honest for both pillars, and makes the write-access metadata note a three-way choice (denied / path-scoped / allowed) instead of a two-way one.

**Conditional Tool-discipline rewrite.** The exact-match paragraph assertion is a good tripwire for the analyst files it was written against, but it is an analyst convention, not a repository invariant. Operator prompts are authored without a `list` reference in the first place. The unconditional post-rewrite assertion (no surviving `` `list` `` token) is what actually protects omp, so it stays for every pillar.

**Skill descriptions rewritten where they are topic labels.** Several upstream descriptions read as titles ("Active Directory security testing and attack techniques"). Both harnesses select skills by description match, so a label triggers poorly. Descriptions are rewritten into when-clauses; bodies are not touched beyond the tool substitutions.

## Risks / Trade-offs

- **A substitution silently changes a technique's meaning** → the substitution table is fixed and mechanical, applied per occurrence rather than per file, and the skill-library spec requires the replaced step to perform the same test. Each ported skill is diffed against its source, and the diff is expected to be confined to frontmatter, tool calls, and the sections those calls belonged to.
- **`attack_script` replacements assume tooling that is not installed** (`jwt_tool`, `ffuf`, `sqlmap`) → replacements prefer an explicit inline command (`curl`, `python3 -c`) where one is short, and the prompts carry the ask-before-installing rule inherited from `ensure_tools`.
- **Write-capable agents in omp can write anywhere** → true, and unavoidable: omp exposes `write` as an `xd://` transport tool regardless of the allowlist. For operators this is the intended posture rather than a gap, but the generated metadata still states it plainly.
- **Destructive-command denies are prompt-level under omp** → recorded in the delta spec and in the generated metadata. Operators inherit CyberStrike's prompt-level safety rules (no destructive actions, no exfiltration beyond proof, no persistence) as the primary control.
- **The journal is advisory** → an operator can ignore it; nothing enforces an append. Mitigated by naming the journal in every prompt's `## Operation journal` section and by making coverage claims contingent on the coverage file, exactly as CyberStrike makes them contingent on `methodology_status`.
- **Upstream drift** → CyberStrike prompts change independently. `docs/roles/operator.md` records source paths and the commit the port was taken from, so a re-port is a diff rather than an archaeology exercise.
- **A future pillar re-invents the substitution table** → the table lands in `docs/agents-skills-extension-workbook.md`, the file the repo already treats as the extension contract, and the pillar doc references it instead of copying it.

## Migration Plan

Additive. No existing artifact changes except `tools/translate-omp.py`, whose behaviour for analyst files must stay byte-identical — verified by translating the analyst pillar before and after the change and diffing the generated output. Deployment is `./install.sh --pillar operators --harness both`; rollback is `./uninstall.sh --pillar operators` plus reverting the translator.

## Open Questions

- Whether the corpus-as-sibling-assets design (43 MB, six index skills) becomes its own change or stays out of the repository entirely.
- Whether the eight proxy testers are worth re-pointing at a file-based request-context convention, or belong in CyberStrike only.
