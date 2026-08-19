## ADDED Requirements

### Requirement: A technique has exactly one owning skill

Every technique the operator pillar ships SHALL have exactly one owning skill. Two skills SHALL NOT
carry the same technique, and a prompt SHALL NOT carry a technique a skill owns. Where a technique
plausibly belongs to two skills, the owner SHALL be stated in both bodies as an explicit boundary
sentence rather than left to the reader.

#### Scenario: No technique has two owners

- **WHEN** a command or payload appears in one operator skill
- **THEN** it does not appear in another, unless one of the two names the other as the owner

#### Scenario: Boundary is written down

- **WHEN** two skills border on the same ground
- **THEN** each body states which of them owns what

### Requirement: `operation-journal` skill exists

`acordia-operators/skills/operation-journal/SKILL.md` SHALL carry the `.acordia/ops/` contract that
the five operator prompts previously restated: the file layout (`scope.md`, `intel.md`, `coverage.md`,
`findings/<slug>.md`, `reports/<name>.md`), the severity scale
(`critical`/`high`/`medium`/`low`/`informational`), the confidence scale
(`confirmed`/`high`/`medium`/`low`), the logging discipline (log intel on discovery rather than in a
batch; read `coverage.md` before claiming a category complete; read `scope.md` before touching a new
target), the evidence-quality rule (the request sent, a concrete response summary, and the reasoning
that proves or disproves the finding), the finding-file shape, and the chaining rule that a chain's
severity is the chain's own, not the maximum of its parts.

#### Scenario: Skill carries the whole contract

- **WHEN** `operation-journal` is read
- **THEN** it states the five file paths, both scales, the logging discipline, the evidence-quality rule, the finding-file shape and the chaining rule

#### Scenario: Prompts stop restating it

- **WHEN** the five operator prompts are searched for the severity or confidence scale
- **THEN** only domain-specific additions remain, and the scales themselves appear once, in the skill

### Requirement: `gcp-postexploit` skill exists

`acordia-operators/skills/gcp-postexploit/SKILL.md` SHALL cover Google Cloud post-exploitation on the
pattern the pillar already uses for `aws-`, `azure-` and `k8s-postexploit`: enumeration of the
identity and project surface, privilege-escalation paths, data and secret access, persistence, and
the logging surface the actions touch. It exists because `cloud-security` claims GCP in its
description and carries GCP technique text; a claim with no skill behind it is the defect this closes.

#### Scenario: GCP claim has a skill behind it

- **WHEN** `cloud-security`'s description and technique lines name GCP
- **THEN** `gcp-postexploit` resolves in the same pillar and carries the GCP technique detail

#### Scenario: Shape matches its siblings

- **WHEN** `gcp-postexploit` is compared with `azure-postexploit`
- **THEN** it follows the same section order and depth

### Requirement: Five mobile skills exist

The operator library SHALL contain `mobile-data-storage`, `mobile-crypto-keys`,
`mobile-platform-ipc`, `mobile-resilience-bypass` and `mobile-instrumentation`, carrying the technique
detail previously held in `mobile-application`'s `## Key techniques by area`. Each SHALL state what it
owns and SHALL NOT compete with its siblings on description. Network, authentication and
business-logic testing for mobile targets SHALL be pointed at the skills that already own them
(`attack-jwt`, `attack-idor-automation`, the `wstg-*` bundles) rather than duplicated.

#### Scenario: Five directories present

- **WHEN** `acordia-operators/skills/` is listed
- **THEN** the five `mobile-*` skills are present, each with a `SKILL.md`

#### Scenario: The admission is gone

- **WHEN** `mobile-application`'s prompt is searched for a claim that the pillar ships no mobile skill library
- **THEN** none is found, and the five slugs appear on its skill lines

#### Scenario: Siblings do not compete

- **WHEN** the five descriptions are compared pairwise
- **THEN** each names work the other four do not cover

## MODIFIED Requirements

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
- **THEN** the analyst pillar holds 43 skills and the operator pillar holds 37

### Requirement: Thirty operator skills cloned from CyberStrike

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
it for local text would corrupt the port record. Seven exist as of 3.1.0: `operation-journal`,
`gcp-postexploit`, and the five `mobile-*` skills. `docs/roles/operator.md` SHALL record them as
authored here, so the provenance record stays a complete account of what the pillar contains.

#### Scenario: Library membership is exact

- **WHEN** `acordia-operators/skills/` is listed
- **THEN** the thirty cloned directories are present, each containing a `SKILL.md`, alongside the skills authored here

#### Scenario: Development skill excluded

- **WHEN** the library is inspected for `bun-file-io`
- **THEN** it is absent

#### Scenario: Authored skills are not dressed as ported

- **WHEN** a skill authored in this repository is inspected
- **THEN** it carries no `metadata.cyberstrike`, and `docs/roles/operator.md` lists it as authored here
