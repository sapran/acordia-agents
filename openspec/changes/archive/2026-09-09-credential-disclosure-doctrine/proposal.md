## Why

The distribution forbids a credential value from appearing anywhere. The prohibition is stated
eleven times across the shipped tree — `credential-harvest-triage` guardrails, seven
`## Credential extraction` sections, four leg prompts, `briefing-reporting`,
`exhaustive-data-processing`, `packet-traffic-analysis`, `aleph-entity-graph` — and in two spec
requirements. It is one rule applied to one undifferentiated destination called "output".

That rule breaks the product it governs. A finished analytic product handed to a human operator is
the place a credential finding legitimately lands: the recipient owns the credential, needs it to
remediate, and cannot act on `type: password, scope: domain, priority: P0` alone. The rule also
forbids an analyst from writing a value into its own working notes, which makes correlation across a
large corpus — step 6 of the triage procedure — a workflow the skill demands and its own guardrail
denies.

The rule is also imprecise about what it protects against. Three destinations that behave very
differently are collapsed into one word: a value printed to stdout reaches the model's context, the
terminal, and the session transcript on disk simultaneously, while a value redirected to a file
reaches none of them. Naming the destinations separately turns a blanket prohibition into a routing
rule, and routing is what an analyst can actually follow.

The prohibition's one genuinely load-bearing case is currently the weakest-stated: the operation's
own credentials. `overwatch-analyst` alone draws the target-owned / operation-owned line, as a
footprint observation in one prompt. That line is the change's red line and belongs in the
classification schema, not in one prompt's prose.

## What Changes

**Current behaviour.** Every credential value is forbidden in every destination, for every kind of
credential, with no field recording whose credential it is. `cyber-analyst` — the orchestrator that
fuses findings and writes the product — is the one prompt of five that does not carry the "report
classifications, not raw values" sentence at all, so the strictest role states the rule the least.

**Desired behaviour.** A four-rule routing doctrine, gated on a required `ownership` classification:

- **Don't print.** A command reading credential-bearing material terminates in a file write, not in
  stdout. The analyst receives a receipt — type, count, source location — not the value. This single
  discipline keeps values off the console, out of the model's context, and out of the session
  transcript together, because all three are fed by the same act.
- **Look deliberately.** An analyst may read a value when a judgement needs it — reuse, strength,
  correlation against a value seen elsewhere — and not as a default way of handling material.
- **Files, not messages.** A value reaches another reader only as a file that reader opens — never in
  a reply, a dispatch, a hand-back or a summary. This is what lets a product disclose what its
  recipient owns: a product written to disk is a file, the same product returned in-message is not.
- **A credential file, and a purge.** Values sit in a credential file beside the analyst's notes, which
  carry the classification and a pointer instead, because those notes are read by whoever fuses the
  work. Extraction runs before ownership is settled, so whatever ownership refuses is purged from the
  files extraction wrote.
- **Two destinations only.** Values live in that credential file and in the finished product. Never in
  `operational-memory`, never in a commit, and never upstream — no network call, no API argument, no
  target system, no third-party service.

**The red line.** The relaxation applies to **target-owned** credentials only. Operation-owned
material — the operation's own tooling, C2 authentication, staging accounts — keeps the absolute
prohibition in every destination including the working notes. Ownership is a required field with
four values (`target`, `operation`, `third-party`, `unknown`) and fails safe: `unknown` is handled as
operation-owned until adjudicated, because a memory capture holds both kinds and the error costs are
asymmetric — over-protecting a target credential costs a re-run, under-protecting an operation
credential burns infrastructure.

Layered by artifact type:

- **Skill bodies** — `credential-harvest-triage` gains the `ownership` field and the four rules in
  place of its five guardrail bullets; the seven `## Credential extraction` sections change their
  closing line from "never the raw value" to the redirect discipline; `briefing-reporting` inverts
  its carve-out so a target credential may be cited in a product; `exhaustive-data-processing`,
  `packet-traffic-analysis`, `aleph-entity-graph` and `web-api-authflow-analysis` follow.
  `operational-memory` is deliberately unchanged — memory is durable and spans engagements, so it
  stays the one place a value never goes.
- **Agent prompts** — all five `## Credential harvest` sections state ownership-first classification
  and the don't-print / never-restate pair, which also closes the `cyber-analyst` omission.
- **Command wrappers** — the two lead wrappers carry the orchestrator body byte-identically and
  follow it.
- **Docs** — `docs/roles/sources.md` records the empty literature result as a gap.
- **Marketplace metadata** — three version occurrences move 6.7.0 → 6.8.0.

No competency-grid change. The grid's rows carry a skill name, a row id and column marks and no
prose, so guardrail wording inside a skill cannot drift from it, and no competency changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `skill-library`: the credential-extraction requirement's "stores no raw credential values"
  scenario is scoped to the skill file's own examples rather than to analyst output; a new
  requirement states the four-rule doctrine and the `ownership` field on `credential-harvest-triage`;
  the `briefing-reporting` requirement's exclusion of credentials from citation is replaced by
  ownership-gated disclosure.
- `agent-roster`: the cross-cutting-sections requirement gains ownership-first classification and the
  don't-print / never-restate pair as content every credential-harvest section carries, in all five
  prompts rather than four.

## Impact

- `acordia-analysts/skills/credential-harvest-triage/SKILL.md` — schema, triage steps 5 and 8,
  guardrails.
- `acordia-analysts/skills/{disk-memory-forensics,identity-directory-trust,log-artefact-interpretation,cloud-controlplane-analysis,web-api-authflow-analysis,os-host-internals,implant-payload-re}/SKILL.md`
  — the closing line of each `## Credential extraction` section.
- `acordia-analysts/skills/{briefing-reporting,exhaustive-data-processing,packet-traffic-analysis,aleph-entity-graph}/SKILL.md`.
- `acordia-analysts/agents/*.md` — five `## Credential harvest` sections.
- `acordia-analysts/commands/{analyst,cyber-analyst}.md` — orchestrator body, byte-identical.
- `docs/roles/sources.md` — one gap entry.
- `.claude-plugin/marketplace.json`, `.omp-plugin/marketplace.json`,
  `acordia-analysts/.claude-plugin/plugin.json` — 6.7.0 → 6.8.0.

Not affected: `docs/roles/operational-analyst.md` (no grid change),
`acordia-analysts/skills/operational-memory/SKILL.md` (deliberately unchanged),
`acordia-analysts/skill-sets.json` (no skill added or removed, no prompt gains or loses a slug).

Out of scope: enforcement. A prompt rule is not a control — it cannot stop a value reaching context
through tool output the agent did not author, nor survive prompt injection from the analysed
material. Real enforcement is a `PreToolUse` / `PostToolUse` masking hook, which is harness
configuration rather than distribution content. The distribution already ships the pattern source
such a hook would consume at
`acordia-analysts/skills/credential-harvest-triage/references/credential-patterns.md`.
