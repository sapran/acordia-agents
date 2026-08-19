## ADDED Requirements

### Requirement: `attack-sqli` skill exists

`acordia-operators/skills/attack-sqli/SKILL.md` SHALL carry SQL injection as a first-class skill,
holding the detection payloads, database fingerprinting, union-based extraction, blind-SQLi and
`sqlmap` reference content that `wstg-injection` carried at lines 12–104. It SHALL follow the shape of
`attack-ssrf` and `attack-xxe`, and SHALL carry the `metadata.cyberstrike` `source` and `commit` of the
bundle the text came from, because the text is moved rather than authored.

#### Scenario: SQLi has its own skill

- **WHEN** the `attack-*` family is enumerated
- **THEN** `attack-sqli` is present alongside the other seventeen

#### Scenario: Provenance follows the text

- **WHEN** `attack-sqli`'s frontmatter is read
- **THEN** its `metadata.cyberstrike` names the same `source` path and `commit` as `wstg-injection`

#### Scenario: The bundle no longer carries the method

- **WHEN** `wstg-injection` is read
- **THEN** its SQL-injection entry is a one-line pointer to `attack-sqli`, carrying no payload table

### Requirement: `linux-postexploit` skill exists

`acordia-operators/skills/linux-postexploit/SKILL.md` SHALL cover Linux post-exploitation reachable
with ordinary userland access: SUID/SGID and capability abuse, sudo-rule abuse, cron and
systemd-timer persistence, SSH key and agent-socket theft, shadow handling, container-escape checks
from the host, and kernel-exploit triage. It SHALL follow the shape of `windows-postexploit`.

The boundary with `ebpf-attacks` SHALL be stated in both bodies: `ebpf-attacks` owns anything needing
`CAP_BPF`/`CAP_SYS_ADMIN` and a loaded BPF program; `linux-postexploit` owns what ordinary userland
access reaches.

#### Scenario: Linux userland has a home

- **WHEN** an operator holds a shell on a Linux host without loading a BPF program
- **THEN** `linux-postexploit` resolves and carries the escalation and persistence paths

#### Scenario: Boundary is written in both bodies

- **WHEN** `linux-postexploit` and `ebpf-attacks` are read
- **THEN** each states which of the two owns kernel-instrumentation work and which owns ordinary userland work

### Requirement: Every skill declares its family

Every `SKILL.md` in both pillars SHALL declare `metadata.acordia.family`, naming exactly one of twelve
families: `analytic-spine`, `target-modelling`, `defender-reading`, `evidence-forensics`,
`take-handling`, `web-attack`, `web-methodology`, `host-postexploit`, `cloud-postexploit`,
`directory-attack`, `mobile`, `operations-discipline`. The tag is documentation, not a gate: nothing
enforces it and no harness reads it. It exists so a reader can see which skills compete for selection,
and so the description contract below has a defined set of siblings to discriminate against.

The field SHALL sit inside the existing `metadata.acordia` block on an analyst skill, and SHALL be
added as an `acordia` key beside the untouched `metadata.cyberstrike` block on a ported operator skill.

#### Scenario: Every skill lands in exactly one family

- **WHEN** all 81 skills' `metadata.acordia.family` values are collected
- **THEN** each skill declares exactly one, every value is one of the twelve, and every family has at least one member

#### Scenario: Provenance is untouched

- **WHEN** a ported operator skill's frontmatter is read after the family tag is added
- **THEN** its `metadata.cyberstrike` block is unchanged

### Requirement: A bundle points at a dedicated skill rather than restating it

Where a WSTG bundle covers ground a dedicated skill owns, the bundle SHALL carry a one-line pointer to
that skill instead of the Method. Before a section becomes a pointer, the destination skill SHALL be
confirmed to carry the Method, and any payload, flag or table row the bundle holds and the skill lacks
SHALL be appended to the skill first.

A bundle SHALL keep its WSTG identity, its provenance block, its routing, and every section for which
no dedicated skill exists.

#### Scenario: Duplicated section becomes a pointer

- **WHEN** a bundle section's Method is carried by a dedicated skill
- **THEN** the bundle holds a pointer line naming that skill, and no payload table for it

#### Scenario: Unowned section stays whole

- **WHEN** a bundle section has no dedicated skill — XSS, command injection, LFI/path traversal, HTTP parameter pollution, mass assignment, privilege-escalation patterns
- **THEN** it stays in the bundle in full

#### Scenario: Nothing is lost to a pointer

- **WHEN** a section is reduced to a pointer
- **THEN** every payload and flag it held is present in the destination skill

## MODIFIED Requirements

### Requirement: The description is the selection surface

Because both harnesses select a skill by matching its `description`, each `description` SHALL open
with an imperative naming the work only that skill does, and SHALL then give the trigger — the
situation in which that work is wanted. It SHALL be 1–1024 characters.

A description SHALL NOT open with a selection-boilerplate clause: `Use when`, `Apply when`, `Use to`,
`Use this skill`, and their variants are prohibited openings, because they are common to every skill
and therefore discriminate between none of them. A bare topic label SHALL NOT be used either.

Within a family, no two descriptions SHALL compete: each SHALL name work its siblings do not cover.
Where two are inseparable, the two skills SHALL be merged rather than shipped as competing siblings.

#### Scenario: Description states applicability

- **WHEN** any skill's description is read
- **THEN** it states the situation the skill applies to, not merely its topic

#### Scenario: Description discriminates between siblings

- **WHEN** two skills in the same family are compared
- **THEN** each description names work the other does not cover

#### Scenario: Boilerplate openings are absent

- **WHEN** all 81 descriptions are read
- **THEN** none begins with `Use when`, `Apply when`, `Use to`, `Use this skill` or an equivalent selection-boilerplate clause

#### Scenario: The worked collision is separated

- **WHEN** `macos-postexploit` and `windows-postexploit` descriptions are compared
- **THEN** each names its platform's own mechanisms — TCC and keychain against LSASS and DPAPI — rather than a shared "host post-exploitation" phrasing

### Requirement: Skills live in their own pillar under a plain slug

Each skill SHALL live at `acordia-analysts/skills/<slug>/SKILL.md` or
`acordia-operators/skills/<slug>/SKILL.md`, one directory per skill. The slug SHALL be kebab-case
matching `^[a-z0-9]+(-[a-z0-9.]*)*$`, SHALL carry no pillar or distribution prefix, and SHALL equal
the frontmatter `name`, because both harnesses default a skill's name to its directory name. A skill
SHALL exist in exactly one pillar; no skill directory SHALL be duplicated across the two, and no
generated or translated copy of a skill SHALL exist in the repository.

#### Scenario: Slug, name and directory agree

- **WHEN** any skill directory is inspected
- **THEN** its `SKILL.md` frontmatter `name` equals the directory name and carries no prefix

#### Scenario: One copy per skill

- **WHEN** the repository is enumerated for `SKILL.md` files
- **THEN** every one lives under exactly one of the two pillars' `skills/` directories

#### Scenario: Library counts are what each pillar ships

- **WHEN** the two libraries are counted
- **THEN** the analyst pillar holds 42 skills and the operator pillar holds 39, 81 in total

### Requirement: Cross-cutting deep skills are ordinary skills

The two cross-cutting deep skills — reverse-engineering (implant/payload behaviour) and
operational-technology/embedded — SHALL be authored as ordinary `SKILL.md` files, not agents. Their
relationship to the legs that draw on them SHALL be stated in prose (skill body / agent prompt), not
via a `chains_with` frontmatter edge. Every skill SHALL be reachable by name from at least one agent
prompt: a skill no prompt names is unreachable in practice, because a prompt's `·`-separated lines are
the only agent-to-skill binding either harness offers.

#### Scenario: RE and OT are plain skills

- **WHEN** the reverse-engineering and operational-technology skills are inspected
- **THEN** each is a `SKILL.md` with contract frontmatter, no `chains_with` field, and neither has its own agent file

#### Scenario: No skill is orphaned

- **WHEN** every analyst skill slug is searched for in the four analyst prompts
- **THEN** each appears on at least one prompt's skill line
