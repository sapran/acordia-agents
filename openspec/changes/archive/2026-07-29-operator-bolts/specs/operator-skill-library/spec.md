## MODIFIED Requirements

### Requirement: Thirty operator skills cloned from CyberStrike

`operators/skills/` SHALL contain exactly thirty-one skill directories, each holding a `SKILL.md`:

- **26 standalone technique skills** cloned from `.cyberstrike/skill/<name>/SKILL.md`: `ad-security`, `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`, `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`, `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-ssrf`, `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`, `aws-postexploit`, `azure-postexploit`, `cicd-attacks`, `ebpf-attacks`, `k8s-postexploit`, `kerberos-attacks`, `macos-postexploit`, `recon-methodology`, `windows-postexploit`.
- **4 OWASP WSTG bundle skills** cloned from `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/<name>/SKILL.md`: `wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api`.
- **1 locally-authored skill**: `bolts` — remote tool execution posture, descended from CyberStrike's Bolt concept but not cloned from any CyberStrike source.

`bun-file-io`, the twenty-seventh standalone CyberStrike skill, SHALL NOT be cloned: it documents Bun file APIs for CyberStrike's own development and carries no security capability.

#### Scenario: Library membership is exact

- **WHEN** `operators/skills/` is listed
- **THEN** exactly those thirty-one directories are present, each containing a `SKILL.md`

#### Scenario: Development skill excluded

- **WHEN** the library is inspected for `bun-file-io`
- **THEN** it is absent

## ADDED Requirements

### Requirement: Locally-authored skills record their own provenance

A locally-authored skill SHALL NOT carry `metadata.cyberstrike`, since it has no CyberStrike source to reference. Instead it SHALL record `metadata.acordia.authored` naming the OpenSpec change that introduced it, plus `metadata.acordia.ancestor` naming the concept or system it descends from when one exists.

#### Scenario: Local provenance is positive

- **WHEN** the `bolts` skill's frontmatter is inspected
- **THEN** it carries `metadata.acordia.authored` naming the originating change and `metadata.acordia.ancestor` naming "CyberStrike Bolt"

#### Scenario: No false CyberStrike provenance

- **WHEN** the `bolts` skill's frontmatter is inspected
- **THEN** it carries no `metadata.cyberstrike` block

### Requirement: Markdown-only constraint applies to locally-authored skills

A locally-authored skill, like a cloned one, SHALL ship no executable or helper script in its directory. The repository remains markdown-only: operational tooling documented in a skill body SHALL be expressed as command patterns the agent runs through `bash`, never as a vendored script that must be installed.

#### Scenario: No executable in the skill directory

- **WHEN** `operators/skills/bolts/` is listed
- **THEN** it contains only `SKILL.md`

### Requirement: Remote-execution skill describes the bolt posture

The `bolts` skill body SHALL define which classes of tooling MUST execute on a remote host (scanners, web/API tooling, credential and AD tooling, target-directed HTTP requests, headless browsers aimed at targets) and which stay local (file I/O, git, documentation, analysis of already-retrieved output).

It SHALL document:

- How to verify a bolt's network position and egress address before the first packet.
- How to run a command on the bolt with quoting preserved across the SSH hop (base64 transport).
- How to start a long-running scan detached so it survives a dropped SSH connection.
- How to poll output and retrieve artifacts from completed runs.
- That the engagement-scoped registry lives at `.acordia/bolts.json`.

#### Scenario: Posture split is stated

- **WHEN** the `bolts` skill body is read
- **THEN** it lists which tool classes run remotely and which stay local

#### Scenario: Egress verification is required

- **WHEN** the skill body's usage section is read
- **THEN** it states that the bolt's egress address MUST be checked before any tooling aimed at a target

#### Scenario: Command transport is documented

- **WHEN** the skill body describes running a command on a bolt
- **THEN** it documents the base64-encoding transport and explains why (quoting preservation)
