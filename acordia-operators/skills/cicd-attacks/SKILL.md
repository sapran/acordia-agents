---
name: cicd-attacks
description: Attack the build pipeline rather than what it ships — read workflow definitions for injectable triggers and inputs, extract secrets from logs, environments and runner state, inject a job into GitHub Actions, GitLab CI or Jenkins, and abuse self-hosted runner and artefact trust. Reach for it when pipeline configuration, a runner or a build token is in scope.
metadata:
  acordia:
    family: cloud-postexploit
  cyberstrike:
    source: .cyberstrike/skill/cicd-attacks/SKILL.md
    commit: 359655518
---

# CI/CD Pipeline Attack Methodology

CI/CD pipeline attacks target the software delivery infrastructure to extract secrets, inject malicious code, and establish persistence. After gaining access to GitHub, Jenkins, or GitLab, these tools extract stored credentials, inject pipeline steps for secret exfiltration, and manipulate workflow configurations.

## Prerequisites

1. **CI/CD access** — API token, personal access token, or service account credentials
2. **Python packages** — `pip3 install requests`
3. **API access** — Valid token with appropriate scopes (repo, admin, workflow)

```bash
# Quick prerequisite check — GitHub
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user | jq .login

# Quick prerequisite check — Jenkins
curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" "$JENKINS_URL/api/json" | jq .nodeDescription

# Quick prerequisite check — GitLab
curl -s -H "Private-Token: $GITLAB_TOKEN" "$GITLAB_URL/api/v4/user" | jq .username
```

## Kill Chain Phases

### Phase 1 — Reconnaissance

| Action | Command | Purpose |
|--------|---------|---------|
| List GitHub secrets | `gh api repos/OWNER/REPO/actions/secrets, environments, and org secrets` | Enumerate repository and environment secret names |
| Jenkins credentials | `curl URL/credentials/store/system/domain/_/api/json` | List credential store entries |
| GitLab variables | `curl --header PRIVATE-TOKEN URL/api/v4/projects/ID/variables` | Enumerate CI/CD variables and tokens |

### Phase 2 — Secret Extraction

| Action | Command | Purpose |
|--------|---------|---------|
| GitHub dispatch | `create workflow_dispatch.yml that echoes secrets to an external URL` | Exfiltrate secrets via workflow dispatch |
| Jenkins console | `curl -X POST URL/scriptText -d 'script=com.cloudbees.plugins.credentials...'` | Extract credentials via Groovy Script Console |
| GitHub logs | `gh run list / gh run view --log and grep for leaked secrets` | Search workflow logs for leaked secrets |

### Phase 3 — Pipeline Injection

| Action | Command | Purpose |
|--------|---------|---------|
| Inject pipeline | `add exfiltration step to CI config (e.g. .github/workflows, .gitlab-ci.yml, Jenkinsfile)` | Add exfiltration step to CI/CD pipeline |

### Phase 4 — Cleanup (MANDATORY)

```text
revert injected pipeline steps, delete dispatch workflows, revoke leaked tokens
```

## Detection Considerations

- **GitHub Audit Log** — Workflow creation, secret access, branch creation
- **Jenkins Audit Trail Plugin** — Script console access, credential reads
- **GitLab Audit Events** — Variable access, runner token reads, pipeline modifications
- **Branch Protection Rules** — Prevent direct push to main/protected branches
- **Required Reviews** — PR approval requirements block unauthorized workflow changes
- **Secret Scanning** — GitHub/GitLab native scanning for leaked credentials

## Program Reference

| Program | Technique | MITRE ATT&CK |
|---------|-----------|---------------|
| gh_secrets | GitHub Actions secret extraction | T1552.004 — Private Keys |
| jenkins_creds | Jenkins credential dump | T1555 — Credentials from Password Stores |
| pipeline_inject | CI/CD pipeline injection | T1195.002 — Compromise Software Supply Chain |
| gitlab_tokens | GitLab CI/CD variable extraction | T1552.004 — Private Keys |
| cleanup_ci | Pipeline modification rollback | T1070 — Indicator Removal |
