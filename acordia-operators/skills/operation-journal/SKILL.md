---
name: operation-journal
description: Record intel, coverage and findings the way the whole operations pillar reads them back — the five files under .acordia/ops/, the severity and confidence scales, the evidence-quality bar, the finding-file shape, and how low-severity entries chain into one high or critical finding. Reach for it whenever an operator or specialist logs a discovery, records what was tested, or checks the journal before claiming ground is untested.
metadata:
  acordia:
    family: operations-discipline
---

# Operation journal

Operators work against a flat-file journal under `.acordia/ops/`. It is the state mechanism that survives across turns and across specialist dispatches, since a specialist's context is gone once it returns. Anything not written to the journal is lost.

This is prompt discipline, not an enforced scope: no harness restricts writes to these paths. The contract holds because the agent follows it.

## Files

| Path | Holds |
|---|---|
| `.acordia/ops/scope.md` | Authorised targets, exclusions, rules of engagement |
| `.acordia/ops/intel.md` | Append-only intel log — one entry per discovery |
| `.acordia/ops/coverage.md` | Append-only coverage log — what was tested, how, and with what result |
| `.acordia/ops/findings/<slug>.md` | One confirmed finding per file |
| `.acordia/ops/reports/<name>.md` | Composed engagement reports |

## Scales

Two scales, and only these two, across the whole pillar:

- **Severity** — `critical` / `high` / `medium` / `low` / `informational`
- **Confidence** — `confirmed` / `high` / `medium` / `low`

Every intel entry carries both. A finding carries a severity. Nothing unverified is presented as confirmed: label it with its confidence instead.

## Logging discipline

- **Log intel on discovery, immediately** — not batched at the end. Every endpoint, subdomain, technology, credential, injectable parameter, hidden parameter, exposed resource, IAM misconfiguration, hardcoded secret, directory object or edge, vulnerability hint, configuration or version disclosure, and authentication flow goes into `.acordia/ops/intel.md` the moment it is found.
- **Read `coverage.md` before claiming a testing category, phase or host complete.** Read `intel.md` alongside it, rather than re-deriving from memory what has already been tested and logged. Append the coverage entry after testing the area.
- **Read `scope.md` before touching a target not touched yet** — a host, domain, subnet, account, subscription, project, cluster, app or build. Never test outside the defined scope.
- **Respect phase order.** Do not skip to exploitation before reconnaissance is covered, and do not write a finding before its evidence quality is verified.

## Evidence quality

A coverage or intel entry carries three things:

1. The request sent or the command run, verbatim.
2. A concrete response summary — never "looked fine", never "appeared secure". State what came back.
3. The reasoning that proves or disproves the finding.

Treat roughly 100 characters as the floor for that reasoning: shorter than that is an assertion, not evidence. Redact sensitive values in captured output while keeping the output recognisable.

## Finding file shape

`.acordia/ops/findings/<slug>.md`, one confirmed finding per file:

- **Severity** — from the scale above
- **Title**
- **Attack vector** — the technique used (e.g. Kerberoasting, ESC1, IDOR via `user_id`, Redis unauthenticated write)
- **Description**
- **Evidence** — request/response or command output, sensitive values redacted
- **Impact** — what this enables, and for whom
- **Remediation** — specific guidance, a concrete command or configuration change where one exists

## Chaining

Individually low-severity intel entries can combine into a high or critical finding — a leaked key plus an endpoint that accepts it, a verbose error plus an unauthenticated debug path, read access to one account plus a trust that reaches another. When two or more entries chain, the combined finding's severity is **the chain's own severity**, not the maximum of its parts. Note the chain explicitly in the finding you write, naming the entries it is built from.

---

Per-agent additions to a journal entry — a specialist's own fields, and whether that specialist composes a report or leaves it to the orchestrator — live in that agent's prompt. This skill is the shared contract those additions extend, not a complete list of the fields any one agent writes.
