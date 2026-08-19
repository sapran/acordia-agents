## Why

An agent prompt is read on every dispatch; a skill is read when it is needed. The five operator
prompts carry technique detail that belongs in skills, and they pay for it on every single dispatch.
Measured body sizes today: `internal-network` 22,265 · `operator` 11,289 · `cloud-security` 10,422 ·
`web-application` 7,493 · `mobile-application` 5,911 characters.

Most of the weight is technique text with a home elsewhere. `internal-network`'s
`## Key techniques by situation` alone is 14,908 characters, and eight of its fourteen blocks
duplicate a skill the same prompt already names — 69 of its 122 backticked command spans already
appear in a named skill. `cloud-security` carries per-cloud IAM, exposure and post-exploitation
tables, plus a section that is pure hand-off text to three skills. All five prompts restate the same
`.acordia/ops/` journal contract in different words.

Three destinations do not exist yet, so the moves have nowhere to land:

- **No journal skill.** The identical contract is written five times.
- **No GCP skill.** `cloud-security` claims GCP in its description and carries GCP technique text,
  while `aws-`, `azure-` and `k8s-postexploit` all exist. The claim stands with nothing behind it.
- **No mobile skills.** `mobile-application` says so outright: "this pillar ships no mobile-specific
  skill library … rely on the techniques above and general reverse-engineering judgment."

## What Changes

- Add seven operator skills: `operation-journal`, `gcp-postexploit`, `mobile-data-storage`,
  `mobile-crypto-keys`, `mobile-platform-ipc`, `mobile-resilience-bypass`,
  `mobile-instrumentation`. Operator library 30 → 37.
- `internal-network`: move eight technique blocks into the skills that own them — eBPF into
  `ebpf-attacks`, Windows into `windows-postexploit`, macOS into `macos-postexploit`, AWS/Azure/
  Kubernetes into `aws-`/`azure-`/`k8s-postexploit`, CI/CD into `cicd-attacks`. Each becomes one
  routing line. The three situation-routing blocks and the internal-services and pivoting blocks stay
  verbatim: routing is what the agent is for. `**Linux privilege escalation:**` stays until 3.2.0
  creates `linux-postexploit`.
- `cloud-security`: move the IAM-enumeration, IAM-privilege-escalation, storage-exposure,
  network-exposure, Kubernetes and secrets-in-code tables into the per-cloud skills, and delete the
  pure hand-off section. `### Logging & Monitoring Gaps` stays — CIS posture is this agent's own
  remit.
- `web-application`: reduce each `## Testing workflow` bullet to area plus skill name, keeping the
  workflow order. `mobile-application`: move `## Key techniques by area` into the five new mobile
  skills and delete the line admitting no mobile library exists.
- All five prompts: replace the `## Operation journal` section with one sentence naming
  `operation-journal`, keeping only the fields that prompt adds beyond the shared contract.
- Nothing moves that is not already covered, and nothing is deleted without a destination: a command
  or payload absent from the destination skill is appended to it before the prompt loses it.
- Version 3.0.0 → **3.1.0** in both manifests and both catalogs.

## Capabilities

### Modified Capabilities

- `agent-roster`: the prompt-content contract changes. A prompt routes to a skill rather than
  restating its technique; the journal contract is named once in a skill rather than restated per
  prompt; a measured prompt-body ceiling replaces the current silence on size.
- `skill-library`: seven new operator skills, the operator count moves 30 → 37, and the library gains
  the rule that a technique named in a prompt has exactly one owning skill.

## Impact

- Rewritten: five operator prompt bodies; seven new `SKILL.md` files; appended technique content in
  `ebpf-attacks`, `windows-postexploit`, `macos-postexploit`, `aws-postexploit`, `azure-postexploit`,
  `k8s-postexploit`, `cicd-attacks`.
- Updated: `docs/roles/operator.md` (the port grows by seven authored-here skills, which the
  provenance record must state as authored rather than ported), both `plugin.json` files, both
  catalogs, `CLAUDE.md` where it describes the per-prompt journal section.
- No behaviour is removed: every moved technique remains reachable through the skill the prompt now
  names.
