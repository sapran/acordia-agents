## Context

See proposal.md — Why. The measurements this design rests on, taken in this worktree at 3.0.0:

`internal-network`'s `## Key techniques by situation` spans lines 56–210, 14,909 characters. Its
subsections are **bold labels, not headings**, so any tooling must target the label text:

| label | lines | chars | disposition |
| --- | --- | --- | --- |
| `**No credentials → first credential:**` | 58–65 | 471 | keep — routing |
| `**Credential obtained → escalate:**` | 66–77 | 761 | keep — routing |
| `**Local admin → lateral movement…:**` | 78–83 | 336 | keep — routing |
| `**Linux privilege escalation:**` | 84–90 | 324 | keep until 3.2.0 creates `linux-postexploit` |
| `**eBPF post-exploitation…:**` | 91–103 | 1,175 | → `ebpf-attacks` |
| `**eBPF blind spot monitors…:**` | 104–126 | 2,556 | → `ebpf-attacks` |
| `**Windows post-exploitation…:**` | 127–141 | 1,744 | → `windows-postexploit` |
| `**macOS post-exploitation…:**` | 142–156 | 1,839 | → `macos-postexploit` |
| `**AWS post-exploitation…:**` | 157–169 | 1,669 | → `aws-postexploit` |
| `**Azure post-exploitation…:**` | 170–180 | 1,363 | → `azure-postexploit` |
| `**Kubernetes post-exploitation…:**` | 181–190 | 1,243 | → `k8s-postexploit` |
| `**CI/CD pipeline attacks…:**` | 191–198 | 793 | → `cicd-attacks` |
| `**Internal services:**` | 199–205 | 364 | keep |
| `**Pivoting:**` | 206–210 | 239 | keep |

`cloud-security` (10,422): `### IAM Enumeration` 50–77 (1,129) · `### IAM Privilege Escalation (AWS)`
78–88 (713) · `### Public Storage Exposure` 89–112 (692) · `### Network Exposure` 113–137 (664) ·
`### Kubernetes / Container` 138–156 (672) · `### Secrets & Credentials in Code` 157–165 (251) ·
`### Logging & Monitoring Gaps` 166–172 (338, **keep**) · `### AWS / Azure / Kubernetes
Post-Exploitation` 173–180 (1,144, pure hand-off text).

`web-application` (7,493): `## Testing workflow` 23–69 (2,138). `mobile-application` (5,911):
`## Key techniques by area` 44–81 (1,719). Journal sections: `operator` 144–154 (1,783) ·
`internal-network` 236–252 (1,406) · `cloud-security` 196–207 (1,123) · `mobile-application` 96–109
(1,216) · `web-application` 96–111 (940).

**69 of `internal-network`'s 122 backticked command spans already appear in a skill it names** — 26 in
`ebpf-attacks`, 11 in `windows-postexploit`, 10 in `macos-postexploit`. The moves are mostly
de-duplication, not transfer.

## Goals / Non-Goals

**Goals:**

- Every prompt body under 10,000 characters, with the routing and guardrails intact.
- One owner per technique, and a destination for every technique that leaves a prompt.
- The journal contract written once.
- The three claims with nothing behind them — GCP, the mobile library, the five journal restatements —
  closed.

**Non-Goals:**

- `linux-postexploit`, `attack-sqli`, the WSTG de-duplication, the description rewrite and the family
  taxonomy. Those are 3.2.0.
- Rewriting technique content. A move is a move: text lands in the destination as it was, adapted only
  where the destination's section order requires it.
- Touching the four analyst prompts. They are 3,533–4,868 characters and carry no technique tables.

## Decisions

**Append-only into destinations, checked span by span.** Before a block leaves a prompt, each
backticked command in it is checked against the destination skill; only genuinely absent spans are
appended. This is why the net loss is smaller than the block sizes suggest, and why a blind cut-and-paste
would inflate `ebpf-attacks` by 3,729 characters of mostly-duplicate text.

**`ebpf-attacks` gets a `references/` file if it crosses ~14,000 characters.** It is already the
largest operator skill at 12,581. The precedent is
`credential-harvest-triage/references/credential-patterns.md`; the candidate for extraction is its
Phase-4 blind-spot monitor table, which is a lookup rather than a method.

**The seven new skills land before any prompt is cut.** A prompt whose technique text is deleted while
its destination does not exist yet is a prompt that has lost the technique. Wave 1 writes the skills,
wave 2 cuts the prompts.

**`operation-journal` is built from `operator`'s version, the fullest at 1,783 characters.** Pairwise
similarity across the five sections is 0.06–0.24, so there is no shared wording to lift — but the
contract is identical: the same five paths, the same severity and confidence scales, the same
log-on-discovery and check-coverage rules. Each prompt keeps only its own additions: `internal-network`
its affected-hosts/accounts field and the "the orchestrator composes the report, not you" boundary;
`cloud-security` its account and region fields; `mobile-application` its package and platform fields;
`web-application` its WSTG-ID, CWE and MITRE ATT&CK fields. `operator` keeps nothing — it was the
source.

**Five mobile skills, not one.** The prompt's five technique areas map cleanly onto storage, crypto,
platform/IPC, resilience and instrumentation, and each is a different job on a different surface. The
risk is sibling descriptions that compete; the mitigation is a boundary sentence in each body and a
pairwise description check. If `mobile-crypto-keys` and `mobile-data-storage` cannot be separated below
0.30 description overlap, they merge into `mobile-storage-crypto` and the pillar records 36 skills
rather than 37.

**GCP is inferred from the agent's own claims, not from a request.** `cloud-security` claims GCP in its
description and carries GCP technique text at five points. Either the skill exists or the claim comes
out; leaving the claim with nothing behind it is the one outcome this change refuses.

**Seven authored-here skills do not get `metadata.cyberstrike`.** That block is upstream attribution.
`docs/roles/operator.md` records them as authored here instead, which keeps the provenance record a
complete account of the pillar rather than a record of only its ported half.

## Risks / Trade-offs

- **A move loses a command** → each moved span is checked against the destination before the prompt is
  cut, and the change is verified by grepping every removed command span against the destination skill.
- **`ebpf-attacks` becomes unreadably large** → `references/` extraction at ~14,000 characters.
- **The five mobile skills compete on description** → pairwise overlap check; merge to four if two
  cannot be separated.
- **A prompt loses routing along with technique** → the three situation-routing blocks and the
  internal-services and pivoting blocks are named as verbatim keeps in the task list, not left to
  judgement.
- **Slug lines fall out of date** → every new skill is added to the naming prompt's skill line in the
  same task, and the slug-resolution one-liner is run before commit.

## Migration Plan

1. Wave 1 — write the seven skills; append the moved technique content into the seven existing
   destination skills.
2. Wave 2 — cut the five prompts: `internal-network`, `cloud-security`, `web-application`,
   `mobile-application`, and the journal sections in all five including `operator`.
3. Update `docs/roles/operator.md`, both manifests and both catalogs to 3.1.0, and `CLAUDE.md` where it
   describes the per-prompt journal section.
4. Verify: prompt-size ceiling, slug resolution, moved-command survival, and a live dispatch of
   `internal-network` and `mobile-application` reading a moved technique out of its new skill.

Rollback is `git revert`; no external state changes.
