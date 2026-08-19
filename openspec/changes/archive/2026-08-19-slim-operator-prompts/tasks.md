## 1. Write the destination skills (wave 1 — nothing is cut before these exist)

- [ ] 1.1 `operation-journal`: build from `operator.md`'s journal section (the fullest, 1,783 chars) with sections Files · Scales · Logging discipline · Evidence quality · Finding file shape · Chaining
- [ ] 1.2 `gcp-postexploit`: follow `azure-postexploit` as the template; absorb the GCP technique text from `cloud-security.md`
- [ ] 1.3 `mobile-data-storage` from `mobile-application.md` lines 46–50 — SharedPreferences/Keychain, SQLite pull, logcat, clipboard and screenshots
- [ ] 1.4 `mobile-crypto-keys` from lines 57–59 — ECB/DES/MD5, hardcoded keys, runtime key capture by hooking
- [ ] 1.5 `mobile-platform-ipc` from lines 67–70 — exported activities and providers, deep links, WebView settings
- [ ] 1.6 `mobile-resilience-bypass` from lines 72–75 — root/jailbreak detection, anti-debug, repackaging, anti-tamper
- [ ] 1.7 `mobile-instrumentation` from the `frida`/`objection`/`drozer`/`jadx`/`apktool` invocations threaded through lines 47–75
- [ ] 1.8 Confirm the five mobile descriptions do not compete: pairwise overlap below 0.30, or merge two and record 36 skills

## 2. Append moved technique content into existing destinations (wave 1)

- [ ] 2.1 `ebpf-attacks` ← `internal-network.md` 91–103 and 104–126, appending only spans it lacks; extract the Phase-4 monitor table to `references/blind-spot-monitors.md` if the body passes ~14,000 chars
- [ ] 2.2 `windows-postexploit` ← 127–141, absent spans only
- [ ] 2.3 `macos-postexploit` ← 142–156, absent spans only
- [ ] 2.4 `aws-postexploit` ← 157–169, plus `cloud-security.md`'s AWS rows from `### IAM Enumeration`, `### IAM Privilege Escalation (AWS)`, `### Public Storage Exposure`, `### Network Exposure`, `### Secrets & Credentials in Code`
- [ ] 2.5 `azure-postexploit` ← 170–180, plus the Azure rows of the same four `cloud-security` sections
- [ ] 2.6 `k8s-postexploit` ← 181–190, plus `cloud-security.md`'s `### Kubernetes / Container`
- [ ] 2.7 `cicd-attacks` ← 191–198, absent spans only
- [ ] 2.8 `gcp-postexploit` ← the GCP rows of `cloud-security.md`'s enumeration and exposure sections

## 3. Cut the prompts (wave 2)

- [ ] 3.1 `internal-network.md`: replace the eight moved blocks with one routing line each in the form `- **Windows host, Administrator held** → \`windows-postexploit\``; keep the three situation blocks, `**Linux privilege escalation:**`, `**Internal services:**` and `**Pivoting:**` verbatim
- [ ] 3.2 `cloud-security.md`: replace the six moved sections with per-cloud routing lines; delete `### AWS / Azure / Kubernetes Post-Exploitation` outright (pure hand-off text); keep `### Logging & Monitoring Gaps`
- [ ] 3.3 `web-application.md`: reduce each `## Testing workflow` bullet to area plus skill name, keeping the workflow order; retain roughly 700 chars
- [ ] 3.4 `mobile-application.md`: cut `## Key techniques by area` into one routing line per new skill; delete the line admitting the pillar ships no mobile skill library
- [ ] 3.5 Add the new slugs to the naming prompts' skill lines: five `mobile-*` to `mobile-application.md`, `gcp-postexploit` to `cloud-security.md`, `operation-journal` to all five operator prompts

## 4. Replace the five journal sections with a pointer (wave 2)

- [ ] 4.1 `operator.md`: replace with one sentence naming `operation-journal`; it keeps nothing, it was the source
- [ ] 4.2 `internal-network.md`: keep *Affected hosts/accounts* and "Do not compose the final assessment report — that is composed by the primary orchestrator from this journal."
- [ ] 4.3 `cloud-security.md`: keep the cloud-account and region fields
- [ ] 4.4 `mobile-application.md`: keep the package and platform fields
- [ ] 4.5 `web-application.md`: keep *WSTG-ID*, *CWE* and *MITRE ATT&CK*
- [ ] 4.6 Budget roughly 250 chars per replacement section

## 5. Records and version

- [ ] 5.1 `docs/roles/operator.md`: record the seven authored-here skills as authored rather than ported, and that they carry no `metadata.cyberstrike`
- [ ] 5.2 `CLAUDE.md`: update the line describing the per-prompt `## Operation journal` section to name `operation-journal` instead
- [ ] 5.3 Bump both `plugin.json` files and both catalogs to 3.1.0, and update the operator skill count in both descriptions
- [ ] 5.4 Update `openspec/config.yaml` context where it states the 30-skill operator library

## 6. Verification

- [ ] 6.1 Prompt-size check prints nothing: no body over 10,000 chars
- [ ] 6.2 Slug-resolution one-liner prints nothing
- [ ] 6.3 Every backticked command span removed from a prompt is present in the destination skill it was routed to
- [ ] 6.4 `grep -rn 'ships no mobile-specific skill library' acordia-operators` → no hits
- [ ] 6.5 The severity and confidence scales appear once in the pillar, in `operation-journal`
- [ ] 6.6 Live dispatch: `internal-network` names the skill it would read for a Windows host and reads it; `mobile-application` names and reads one of the five new skills
- [ ] 6.7 `openspec validate --all --strict` passes
