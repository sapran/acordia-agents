# skill-library

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
