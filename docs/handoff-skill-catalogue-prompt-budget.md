# Handoff — the skill catalogue outgrew a single agent's prompt budget

**Recorded** 2026-08-22, from operations work on a different project. **Not acted on.**
**Origin:** ACORDIA v5.0.0 installed on the `openclaw` gateway `openclaw-gdx-gateway` (OpenClaw
2026.7.1) on the host `mini`, running local models with a 131,072-token window. The finding is about
ACORDIA's packaging, not about that deployment, which is why it is written here.

## What happens

A host that loads the whole `acordia-analysts` bundle silently loses every skill description.

OpenClaw injects a skill *catalogue* into the system prompt — name, description and location per
skill — and the agent reads the `SKILL.md` body on demand only when it picks one. That part works
as intended and was verified live: the agent opened `analyst-loop/SKILL.md` by itself and reported
its heading. Bodies are never injected, so the 45 skills do **not** cost 45 skill-files of context.

But the catalogue has a character budget (`DEFAULT_MAX_SKILLS_PROMPT_CHARS = 18000` in OpenClaw
2026.7.1). When the rendered catalogue exceeds it, OpenClaw does not fail — it **drops all
descriptions** and renders names and file paths only, with one warning line the operator never sees
unless they read the compiled prompt:

```
⚠️ Skills catalog using compact format (descriptions omitted). Run `openclaw skills check` to audit.
```

That is the state on the live gateway today. The analyst is choosing among 62 skills by bare name.
`hypothesis-testing` and `deception-detection` survive that; `assessing-take-value`,
`take-domain-interpretation` and `change-cycle-forecasting` do not — they are exactly the skills
whose name does not tell you when to reach for them. The library still loads, still passes every
health check, and quietly stops steering selection.

## The numbers

Measured from the running gateway's own compiled-context trace and from this repo.

| Quantity | Value |
|---|---|
| Catalogue budget before degradation | 18,000 chars |
| ACORDIA's 45 skills, full format (name + description + location) | **24,639 chars** |
| ACORDIA's 45 skills, compact format (descriptions dropped) | 8,578 chars |
| Host's own remaining 17 skills, compact | ~3,953 chars |
| Rendered catalogue actually in the prompt (62 skills, compact) | 12,531 chars |
| Description length across the 45 | 16,061 total, **mean 356**, max 438 |

ACORDIA alone is over budget by 37% **before a host adds a single skill of its own**. No host
configuration fixes that; the library cannot be loaded whole with descriptions intact.

For scale, the whole catalogue is not the context problem people assume: on that deployment a fresh
session costs 18,253 tokens of 131,072 (14%), of which the skills block is roughly 3,100 tokens.
The cost is acceptable. The **silent loss of descriptions** is the defect.

## Why this is ACORDIA's to fix

Two things belong to this repo. Both are about how the library is packaged, not how a host is
configured.

**1. The role→skill mapping exists only as prose.** Each of the five analyst prompts already carries
its own list — a `Shared analytic spine (every analyst carries this)` line of twelve, plus a
`Your specialist depth (deep)` section. That is the correct decomposition and it is already authored.
Nothing can consume it: it is running text in the middle of a markdown body, so every host loads all
45 or none. Scanning that prose gives, indicatively:

| Analyst | skills | full-format catalogue cost |
|---|---|---|
| mission-analyst | 22 | 12,000 |
| collection-analyst | 25 | 13,616 |
| cyber-analyst | 28 | 15,016 |
| terrain-analyst | 31 | 16,878 |
| overwatch-analyst | 32 | 17,440 |

Every role fits under 18,000 on its own — which is the point. Making that mapping machine-readable
(a declared skill list per analyst) is what lets any host load one role's subset. Those counts come
from scanning prose with a regular expression and should be treated as indicative; producing the
authoritative list is precisely the task.

**2. Descriptions are long enough that role subsets still crowd the budget.** At a mean of 356 chars,
the two largest roles land within ~1,000 chars of the ceiling with nothing left for the host's own
skills. To keep any single role under 12,000 chars — leaving real headroom — the mean has to fall to
between 184 (overwatch) and 353 (mission). **A uniform target of ≤180 chars per description** clears
every role with room to spare, and costs nothing analytically: the description's whole job is to let
a model decide whether to open the file.

## What is *not* ACORDIA's to fix

Recorded so the next person does not chase them here. All of these are host-side and are being
handled where the deployment lives: per-agent skill allowlists, delegation to sub-agents so
retrieved document text stays out of the coordinator's transcript, collapsing tool schemas behind
tool-search, and a cosmetic mismatch where the catalogue advertises a gateway-side path while the
agent reads the same file through its sandbox mount (the agent resolves this by itself).

Also worth knowing, because it shapes what the five analyst files are *for*: OpenClaw has no registry
that consumes a plugin's `agents/*.md` as named personas, and its slash commands are a separate
mechanism from Claude's. On that host the bundle delivers the 45 skills; the five personas and ten
commands load nothing and cost nothing. Any packaging change should keep the personas useful to hosts
that *do* read them rather than optimising them away.

## Acceptance criteria

1. Each analyst declares its skill set in a machine-readable field, and the declared set matches the
   prose spine and specialist-depth sections in the same file.
2. No single analyst's full-format catalogue cost exceeds 12,000 chars.
3. Description mean ≤180 chars across all 45 skills, with no description exceeding ~250.
4. A host loading one analyst's subset renders the catalogue **with** descriptions — verified by
   reading the compiled prompt and confirming the compact-format warning is absent, not by the
   install reporting success.

## How to re-measure

The character cost of a catalogue entry is `97 + len(name) + len(description) + len(location)`, where
`location` is the absolute `SKILL.md` path on the host. Compare the total against the host's budget.
On OpenClaw, read the rendered block directly rather than trusting a health check — it is cached
per-agent under the session directory as `skills-prompts/sha256/<..>.txt`, and the compact-format
warning is its first line.

---

## Status — partly answered in 6.1.0

`openspec/changes/archive/*-compress-skill-descriptions/` compressed all 45 descriptions. Measured on
that tree, using this document's own cost formula and the 40-character host prefix that reproduces
its 24,639 figure exactly:

| | before | after |
|---|--:|--:|
| description total / mean / max | 16,061 / 357 / 438 | 8,099 / 180 / 192 |
| largest analyst's catalogue (`overwatch-analyst`, 30 skills) | 16,331 | **11,114** |
| whole 45-skill library | 24,639 | 16,677 |

**Criterion 2 — no analyst over 12,000 — met.** The largest is 11,114, and the spec now carries a
hard 200-character per-description ceiling rather than a mean, because a mean bounds the library
without bounding any single role.

**Criterion 3 — mean ≤180, none over ~250 — met**, at mean 180.0 and max 192.

**Criterion 1 — a machine-readable per-analyst skill set — not done**, and deliberately. Producing
that list surfaced two defects this document did not know about, both parked in
`docs/implementation-notes.md` under *Parked in 6.1.0*: the grid marks the 12-skill shared spine in
the `Core` column alone while all four legs carry it in prose, so generating the list from the
prompts would harden a source-of-truth drift into a declared field; and three skills
(`aleph-entity-graph`, `credential-harvest-triage`, `exhaustive-data-processing`) are named in no
prompt at all. Both turn on how analytic work is divided, which this repository requires be selected
from the literature first, and the lib.ai library was returning `database disk image is malformed`
throughout.

**Criterion 4 — verify against a compiled prompt — not done here.** It cannot be: it is a reading
taken on the host, not in this repository. The figures above are arithmetic on this document's
formula, which is a projection and not the compiled-prompt evidence the criterion asks for. Read the
rendered block on the gateway after upgrading, and confirm the compact-format warning is absent.

Note that the whole 45-skill library still costs 16,677 and so still leaves too little of an
18,000-character budget for a host's own skills. That is by design — role-scoping is the fix, and
this change is what makes role-scoping sufficient once criterion 1 exists.
