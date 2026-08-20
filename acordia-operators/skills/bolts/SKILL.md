---
name: bolts
description: Run offensive tooling from a named remote server rather than from the machine holding the conversation — which commands must run there and which stay local, the bolt registry, how a bolt is verified before first use, how a long scan survives a dropped connection, and how artifacts come back. Reach for it whenever the traffic has to originate from a chosen network position, or before any scan, probe or exploitation step that would otherwise leave from the operator's own address.
metadata:
  acordia:
    family: operations-discipline
---

# Bolts — remote tool execution

A **bolt** is a named remote server that holds the offensive toolkit and the network position. The operator's machine holds the conversation, the notes, and the report; the bolt does the work. The concept descends from CyberStrike's Bolt remote tool servers (one client, many attack hosts), carried over plain SSH instead of a pairing protocol — no daemon, no extra keys beyond the ones already in the SSH agent.

## The operating rule

When a bolt is active, **every external tool runs on the bolt**, so the target only ever sees the bolt's address. Read that as the consequence of following this rule, not as a property of the system: nothing enforces it. It is a discipline stated in a prompt, not a sandbox — no harness can bind a tool call to a remote host, so a local invocation will succeed silently and only this rule stops it.

The bolt itself is **operator infrastructure, not a target**. It is exempt from the scope file: SSHing into it and running tooling there is not an engagement action. Everything the bolt is *aimed at* is a target, and must appear in `.acordia/ops/scope.md` before the first packet leaves.

**Runs on the bolt:**

- Scanners and probes: `nmap`, `masscan`, `arp-scan`, `fping`, `tcpdump`
- Web and API tooling: `nuclei`, `ffuf`, `feroxbuster`, `sqlmap`, `httpx`, `whatweb`
- Credential and AD tooling: `netexec`, `impacket-*`, `evil-winrm`, `bloodhound-python`, `responder`
- Any `curl`/`wget` aimed at an engagement target
- A headless browser when the page must load from the bolt's position

**Stays local:**

- Reading and writing files in the engagement directory
- `git`, package managers, documentation lookups, web search
- Parsing and analysing output already retrieved from the bolt

## Registry

Each engagement records its bolts at `.acordia/bolts.json`:

```json
{
  "default": "kali",
  "bolts": {
    "kali": {
      "ssh": "kali",
      "description": "Kali VM, arm64, local network position",
      "workdir": "~/bolt",
      "sudo": "nopasswd",
      "position": {
        "192.168.99.0/24": "eth1 192.168.99.180, bridged LAN",
        "internet": "wg0 tunnel, egress 203.0.113.26"
      }
    }
  }
}
```

The `ssh` value is an SSH destination — a host alias from `~/.ssh/config` or `user@host`. It MUST work with `BatchMode=yes` (key authentication, no password prompt).

## Verifying a bolt before use

Before sending any traffic to a target through a bolt, verify its identity and egress address:

```bash
ssh -o BatchMode=yes BOLT_SSH 'echo "host:   $(hostname) $(uname -srm)"
  echo "addrs:  $(ip -brief addr | awk "\$2==\"UP\" {printf \"%s=%s \", \$1, \$3}")"
  echo "sudo:   $(sudo -n true 2>/dev/null && echo nopasswd || echo needs-password)"
  echo "egress: $(curl -s -m 8 https://api.ipify.org || echo unreachable)"'
```

The `egress` line is the source address the target will record. If it does not match the operation's intended network position, do not proceed.

## Running a command on the bolt

### Quoting rule: base64 transport

A scan command routinely contains quotes, pipes, and `$` characters. Passing it through `ssh host "..."` mangles these — the failure is silent and produces artifacts named after the flags. Encode the command locally and decode it on the bolt:

```bash
# Short inline: base64-encode, transport, decode, execute
# RUN is computed once, locally. Two `date` calls would be two forks a second apart:
# when the boundary falls between them the names differ, `cd` fails, the && chain
# aborts, and an empty run directory is left looking like a completed prior run.
RUN="run-$(date +%Y%m%d-%H%M%S)"
ENC=$(printf '%s' 'sudo -n nmap -sS -p- 192.168.99.106 -oX scan.xml | grep "open"' | base64)
ssh -o BatchMode=yes BOLT_SSH "mkdir -p ~/bolt/$RUN && cd ~/bolt/$RUN && \
  printf '%s' '$ENC' | base64 -d > cmd.sh && sh cmd.sh 2>&1 | tee output.txt"
```

Every run gets its own timestamped directory containing:
- `cmd.sh` — exactly what was executed
- `output.txt` — everything it printed

### Long-running scans: detach with setsid

A foreground `ssh` run dies when the connection drops. For scans that take minutes or hours, detach:

```bash
RUN="run-$(date +%Y%m%d-%H%M%S)"
ENC=$(printf '%s' 'sudo -n nmap -sS -p- -sV -oX full.xml 10.0.0.0/24' | base64)
ssh -o BatchMode=yes BOLT_SSH "mkdir -p ~/bolt/$RUN && cd ~/bolt/$RUN && \
  printf '%s' '$ENC' | base64 -d > cmd.sh && \
  setsid nohup sh cmd.sh > output.txt 2>&1 < /dev/null &"
```

The scan survives a dropped connection, a closed laptop, or a session restart. Poll it:

```bash
# Check if still running
ssh -o BatchMode=yes BOLT_SSH "pgrep -af nmap"

# Tail the output
ssh -o BatchMode=yes BOLT_SSH "tail -40 ~/bolt/$RUN/output.txt"

# List what the run produced
ssh -o BatchMode=yes BOLT_SSH "ls -lh ~/bolt/$RUN/"
```

### Retrieving artifacts

Write output to files on the bolt (`-oA`, `-oX`, `-o`), then pull into the engagement directory, so a
later turn or a dispatched specialist can find it. Artifacts land under `.acordia/ops/artifacts/<run>/`
— a directory beside the journal's own files, not a sixth journal file:

```bash
mkdir -p ".acordia/ops/artifacts/$RUN"
scp -q -o BatchMode=yes "BOLT_SSH:~/bolt/$RUN/full.xml" ".acordia/ops/artifacts/$RUN/"
```

Do not pipe megabytes of scan text through the conversation. Pull the file, then read it locally.

## Discipline rules

1. **Check `egress` before the first packet.** The bolt's public address is what the target records.
2. **Write output to files on the bolt**, then pull what is needed. Save tools' native output formats (`-oX`, `-oA`) — they carry more data than stdout.
3. **Never re-run an expensive scan** before checking existing run directories on the bolt for an earlier one.
4. **Privileged scans:** where the bolt's sudo is `nopasswd`, use `sudo -n` so a password prompt fails loudly instead of hanging.
5. **Artifacts belong in the engagement directory**, not only on the bolt. Pull them as soon as a run finishes — a bolt is disposable.
6. **One bolt per network position.** If a target is reachable only from a different host, register that host as its own bolt rather than chaining.

## Listing available tools on a bolt

```bash
# Check for a specific tool
ssh -o BatchMode=yes BOLT_SSH "command -v nmap nuclei ffuf sqlmap netexec"

# Search the bolt's PATH by pattern
ssh -o BatchMode=yes BOLT_SSH \
  "ls /usr/bin /usr/sbin /usr/local/bin 2>/dev/null | sort -u | grep -i nmap"
```

## Listing previous runs

```bash
# Recent runs (newest first)
ssh -o BatchMode=yes BOLT_SSH "ls -1t ~/bolt/ | head -20"

# What a specific run produced
ssh -o BatchMode=yes BOLT_SSH "ls -lh ~/bolt/run-20260730-020449/"

# What command it ran
ssh -o BatchMode=yes BOLT_SSH "cat ~/bolt/run-20260730-020449/cmd.sh"
```
