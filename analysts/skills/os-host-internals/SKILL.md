---
name: os-host-internals
description: Use when you are on or reasoning about a specific host and need to command Windows/Linux/macOS internals — to understand its state, escalate, persist, and move without tripping the host's own defenses.
---

# OS & Host Internals

## Objective
Apply deep operating-system knowledge to a target host so you can read its true state, find privilege and persistence footholds, and operate within its native mechanisms rather than against them.

## When to use
- When you have a foothold and must escalate, persist, or pivot from a specific host.
- When you need to predict how a host will respond to an action — logging, EDR, integrity controls, isolation.

## Method
- Establish host context: OS/version, patch level, privilege model, running processes/services, scheduled tasks/daemons, and installed security tooling.
- Identify escalation vectors native to the platform — token/privilege abuse, SUID/sudo, service and DLL/dylib hijacks, misconfigured ACLs, kernel/driver exposure.
- Locate credential and secret material at rest and in memory (LSASS/keyring/keychain, tokens, caches, config).
- Choose persistence that matches the platform's legitimate mechanisms and survives reboot without standing out.
- Model the host's observation surface: what is logged, what EDR sees, and how to act inside normal process behaviour.

## Signals / outputs
- Host state and privilege map with concrete escalation candidates.
- Credential/secret locations and access method.
- Persistence options ranked by durability vs detectability, plus the host's logging/EDR blind spots.
