# skill-library

## ADDED Requirements

### Requirement: `bolts` skill exists

`acordia-operators/skills/bolts/SKILL.md` SHALL exist, defining remote tool execution as an operating
posture: a bolt is a named remote server holding the offensive toolkit and the network position, driven
over SSH, while the local machine holds the conversation, the notes and the report.

The skill SHALL state which work runs on the bolt — scanners and probes, web and API tooling,
credential and directory tooling, any fetch aimed at an engagement target, and a headless browser when
the page must load from the bolt's position — and which stays local. It SHALL define the registry that
records each bolt, how a bolt is verified before first use, how a long-running scan survives a dropped
connection, and how artifacts return.

The skill SHALL be authored rather than cloned and SHALL carry no `metadata.cyberstrike`. The concept
descends from CyberStrike's Bolt remote tool servers; none of its code does, and SSH replaces the
pairing protocol because this repository ships no runtime that could pair.

Nothing SHALL claim to enforce the posture. It is a discipline stated in a prompt, not a sandbox:
no harness can bind a tool call to a remote host.

#### Scenario: The skill is present and authored
- **WHEN** `acordia-operators/skills/bolts/SKILL.md` is read
- **THEN** it declares `family: operations-discipline`, carries no `metadata.cyberstrike`, and names its CyberStrike ancestor in prose

#### Scenario: The posture separates remote from local
- **WHEN** the skill body is read
- **THEN** it names the tooling that runs on the bolt and the work that stays on the local machine, as two explicit lists

#### Scenario: No enforcement is claimed
- **WHEN** the skill's `## The operating rule` section is read
- **THEN** it states that nothing enforces the posture and that a local invocation would succeed, claiming no guarantee that tooling cannot run locally

#### Scenario: The four operating mechanics are present
- **WHEN** the skill body is read
- **THEN** it defines the registry that records each bolt, how a bolt is verified before first use, how a long-running scan survives a dropped connection, and where retrieved artifacts land

#### Scenario: The bolt is distinguished from a target
- **WHEN** the skill is read alongside the prompts' scope guardrail
- **THEN** it states that the bolt is operator infrastructure exempt from the scope file, and that everything it is aimed at must appear in `.acordia/ops/scope.md`

## MODIFIED Requirements

### Requirement: Thirty operations skills cloned from CyberStrike

`acordia-operators/skills/` SHALL contain the thirty skill directories cloned from CyberStrike, each
holding a `SKILL.md`:

- **26 standalone technique skills** cloned from `.cyberstrike/skill/<name>/SKILL.md`: `ad-security`,
  `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`,
  `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`,
  `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-ssrf`,
  `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`, `aws-postexploit`,
  `azure-postexploit`, `cicd-attacks`, `ebpf-attacks`, `k8s-postexploit`, `kerberos-attacks`,
  `macos-postexploit`, `recon-methodology`, `windows-postexploit`.
- **4 OWASP WSTG bundle skills** cloned from
  `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/<name>/SKILL.md`: `wstg-recon-config`, `wstg-auth-session`,
  `wstg-injection`, `wstg-logic-client-api`.

`bun-file-io`, the twenty-seventh standalone CyberStrike skill, SHALL NOT be cloned: it documents Bun
file APIs for CyberStrike's own development and carries no security capability.

The library MAY additionally contain skills **authored in this repository** rather than cloned. Such a
skill SHALL NOT carry `metadata.cyberstrike`, because that block is upstream attribution and claiming
it for local text would corrupt the port record. Nine exist as of 4.1.0: `operation-journal`,
`gcp-postexploit`, `linux-postexploit`, the five `mobile-*` skills, and `bolts`.
`docs/roles/operator.md` SHALL record them as authored here, so the provenance record stays a
complete account of what the pillar contains.

#### Scenario: Library membership is exact

- **WHEN** `acordia-operators/skills/` is listed
- **THEN** the thirty cloned directories are present, each containing a `SKILL.md`, alongside the skills authored here

#### Scenario: Development skill excluded

- **WHEN** the library is inspected for `bun-file-io`
- **THEN** it is absent

#### Scenario: Authored skills are not dressed as ported

- **WHEN** a skill authored in this repository is inspected
- **THEN** it carries no `metadata.cyberstrike`, and `docs/roles/operator.md` lists it as authored here

### Requirement: Every skill declares its family

Every `SKILL.md` in both pillars SHALL declare `metadata.acordia.family`, naming exactly one of twelve
families: `analytic-spine`, `target-modelling`, `defender-reading`, `evidence-forensics`,
`take-handling`, `web-attack`, `web-methodology`, `host-postexploit`, `cloud-postexploit`,
`directory-attack`, `mobile`, `operations-discipline`. The tag is documentation, not a gate: nothing
enforces it and no harness reads it. It exists so a reader can see which skills compete for selection,
and so the description contract below has a defined set of siblings to discriminate against.

The field SHALL sit inside the existing `metadata.acordia` block on an analyst skill, and SHALL be
added as an `acordia` key beside the untouched `metadata.cyberstrike` block on a ported operations skill.

#### Scenario: Every skill lands in exactly one family

- **WHEN** all 82 skills' `metadata.acordia.family` values are collected
- **THEN** each skill declares exactly one, every value is one of the twelve, and every family has at least one member

#### Scenario: Provenance is untouched

- **WHEN** a ported operations skill's frontmatter is read after the family tag is added
- **THEN** its `metadata.cyberstrike` block is unchanged

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
- **THEN** the analyst pillar holds 42 skills and the operations pillar holds 40, 82 in total

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

- **WHEN** all 82 descriptions are read
- **THEN** none begins with `Use when`, `Apply when`, `Use to`, `Use this skill` or an equivalent selection-boilerplate clause

#### Scenario: The worked collision is separated

- **WHEN** `macos-postexploit` and `windows-postexploit` descriptions are compared
- **THEN** each names its platform's own mechanisms — TCC and keychain against LSASS and DPAPI — rather than a shared "host post-exploitation" phrasing
