## ADDED Requirements

### Requirement: Thirty operator skills cloned from CyberStrike

`operators/skills/` SHALL contain exactly thirty skill directories, each holding a `SKILL.md`:

- **26 standalone technique skills** cloned from `.cyberstrike/skill/<name>/SKILL.md`: `ad-security`, `attack-cache-poison`, `attack-cors`, `attack-graphql`, `attack-host-header`, `attack-idor-automation`, `attack-jwt`, `attack-open-redirect`, `attack-prototype-pollution`, `attack-race-condition`, `attack-rate-limit-bypass`, `attack-request-smuggling`, `attack-ssrf`, `attack-ssti`, `attack-subdomain-takeover`, `attack-websocket`, `attack-xxe`, `aws-postexploit`, `azure-postexploit`, `cicd-attacks`, `ebpf-attacks`, `k8s-postexploit`, `kerberos-attacks`, `macos-postexploit`, `recon-methodology`, `windows-postexploit`.
- **4 OWASP WSTG bundle skills** cloned from `.cyberstrike/skill/WEB/OWASP_WSTG_4.2/<name>/SKILL.md`: `wstg-recon-config`, `wstg-auth-session`, `wstg-injection`, `wstg-logic-client-api`.

`bun-file-io`, the twenty-seventh standalone CyberStrike skill, SHALL NOT be cloned: it documents Bun file APIs for CyberStrike's own development and carries no security capability.

#### Scenario: Library membership is exact

- **WHEN** `operators/skills/` is listed
- **THEN** exactly those thirty directories are present, each containing a `SKILL.md`

#### Scenario: Development skill excluded

- **WHEN** the library is inspected for `bun-file-io`
- **THEN** it is absent

### Requirement: Folder slug equals frontmatter name

Each skill's `name` SHALL be kebab-case matching `^[a-z0-9]+(-[a-z0-9.]*)*$`, SHALL equal its folder slug, and SHALL carry no pillar prefix — the same rule the analyst library follows, because both harnesses default a skill's name to its directory name.

#### Scenario: Slug and name agree

- **WHEN** any operator skill is inspected
- **THEN** its frontmatter `name` is identical to its containing directory's name

### Requirement: Frontmatter reduced to the opencode contract

A cloned skill's frontmatter SHALL contain `name`, `description`, and optionally `metadata`. Every CyberStrike-only field SHALL be dropped: `category`, `version`, `author`, `tags`, `owasp_id`, `cis_id`, `cis_benchmark`, `tech_stack`, `cwe_ids`, `chains_with`, `prerequisites`, `severity_boost`.

The signing triple `sha256` / `signature` / `signed_by` SHALL also be dropped, because a hash that no longer matches the edited body makes CyberStrike drop the skill as `tampered` while opencode and omp ignore the field entirely — a stale hash is worse than no hash.

#### Scenario: Only contract fields survive

- **WHEN** any operator skill's frontmatter is parsed
- **THEN** its keys are a subset of `name`, `description`, `metadata`

#### Scenario: No signing fields

- **WHEN** any operator skill's frontmatter is inspected
- **THEN** it carries no `sha256`, `signature`, or `signed_by`

### Requirement: Provenance recorded in metadata

Each cloned skill SHALL record its origin under `metadata.cyberstrike` as the repository-relative source path it was cloned from, so a diff against upstream is mechanical.

#### Scenario: Source path recorded

- **WHEN** any operator skill's `metadata.cyberstrike` block is read
- **THEN** it names the `.cyberstrike/skill/...` path the body was cloned from

### Requirement: Triggering-quality descriptions

Each `description` SHALL be a single sentence stating **when** the skill applies, in 1–1024 characters, because both harnesses select skills by description match. Where the upstream CyberStrike description is a bare topic label, it SHALL be rewritten into a when-clause; where it already states applicability, it SHALL be preserved.

#### Scenario: Description states applicability

- **WHEN** any operator skill's description is read
- **THEN** it states the situation in which the skill applies, not merely its topic

### Requirement: Bodies carry no tool the harness lacks

A cloned skill body SHALL name no CyberStrike platform tool. Every `attack_script <name>` invocation SHALL be replaced per the `harness-tool-translation` substitution table, and no body SHALL reference `add_intel`, `report_vulnerability`, `update_vrt_check`, `methodology_status`, `scope_check`, `ensure_tools`, `hackbrowser`, or the `skill` CLI.

The eleven skills that invoke `attack_script` upstream — `attack-jwt`, `attack-idor-automation`, `attack-race-condition`, `attack-subdomain-takeover`, `attack-ssti`, `attack-rate-limit-bypass`, `attack-xxe`, `attack-graphql`, `attack-ssrf`, `attack-open-redirect`, `attack-cors` — SHALL retain the same testing intent, expressed as a standard tool invocation or an explicit inline command.

#### Scenario: No platform tool named

- **WHEN** the thirty skill bodies are searched for CyberStrike platform tool names
- **THEN** none is found

#### Scenario: Replaced invocation keeps the intent

- **WHEN** a former `attack_script` step is compared to its replacement
- **THEN** the replacement performs the same test using a standard tool or an explicit command, rather than dropping the step

#### Scenario: Attack scripts are not vendored

- **WHEN** the repository is inspected after the change
- **THEN** no Python or other executable attack script has been added — the repository remains markdown-only

### Requirement: Bodies otherwise preserve upstream methodology

Apart from the frontmatter reduction and the tool substitutions, a cloned body SHALL preserve its upstream payloads, commands, tables, and phase structure. Cloning SHALL NOT be an occasion to rewrite technique content, because the upstream body is the reviewed artifact.

#### Scenario: Technique content unchanged

- **WHEN** a cloned body is diffed against its CyberStrike source
- **THEN** the differences are confined to frontmatter reduction, tool substitutions, and the section removals required by them

### Requirement: Corpus skills are not published

The generated compliance and technique corpora under `.cyberstrike/skill/` — CIS benchmarks (5,000 skills), NIST control families (1,606), MITRE ATT&CK enterprise, mobile, and ICS (898 combined), and the 121 individual WSTG leaf skills — SHALL NOT be cloned into this pillar. Both harnesses list every discovered skill's name and description in the system prompt, so publishing them would add roughly 190,000 tokens to every session.

#### Scenario: Corpus absent from the library

- **WHEN** `operators/skills/` is listed
- **THEN** no `cis-*`, NIST-control, or MITRE-technique skill directory is present, and the only `wstg-*` entries are the four bundles

#### Scenario: Exclusion is recorded

- **WHEN** `docs/roles/operator.md` is read
- **THEN** it records the corpora that were not published and the prompt-cost reason
