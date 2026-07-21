---
name: implant-payload-re
description: Use to reverse-engineer an implant or payload's real behavior — ours, a competitor's, or a captured sample — to understand exactly what it does, what it emits, and how it would be detected.
---

# Implant/Payload Behaviour & Reverse-Engineering

## Objective
Reverse-engineer implant/payload behavior to ground-truth what it actually does on a host and over the wire. This is a CROSS-CUTTING deep skill: it attaches to whichever leg needs it — Target & Network (understanding a target's malware or a tool you'll deploy) or Defender & Detection (predicting the artifacts and signatures a payload emits) — for a given operation.

## When to use
- Validating your own tooling's real footprint before deployment, or triaging unexpected behavior in the field.
- Analyzing a captured, third-party, or competitor sample to understand capability, indicators, and attribution.

## Method
- Triage statically first: file type, packing, imports, strings, embedded config, and signing — cheap signal before you run anything.
- Analyze safely in an isolated, instrumented environment; assume anti-analysis and sandbox-evasion and account for it.
- Recover behavior dynamically: process/thread activity, injection, persistence, file/registry changes, and full network/C2 behavior.
- Extract config and IOCs — keys, domains, mutexes, campaign markers — and map behavior to ATT&CK techniques and the telemetry each would produce.
- Feed findings to the leg that needs them: detection-signature prediction for blue-side reasoning, or capability/attribution for target work.

## Signals / outputs
- A behavior profile: what it does on host and network, plus its anti-analysis tricks.
- Extracted config, IOCs, and an emitted-signature map tied to detection sources.
- Attribution and capability notes routed to the relevant operational leg.

## Credential extraction

Credential material embedded in payloads — hardcoded strings, encrypted config blocks, keys embedded for C2 auth or lateral movement. Extraction is static or sandboxed-dynamic; never runs the sample against a live target to prove reuse.

**Static extraction from binaries**
- `strings -a -n 8` (and `strings -e l` for UTF-16 on Windows PE), then pattern-library grep from [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md). Hits often surface C2 auth keys, hardcoded RDP/SMB credentials, hardcoded API tokens for stagers pulling from paste sites.
- `.rsrc` (PE resources) — embedded config blobs, sometimes XOR- or RC4-obfuscated with a key also present in the binary. Extract with `pefile` / `pyresource` + a short deobfuscator.
- `.rdata` / `.data` — hardcoded strings the compiler could not deduplicate; C2 URLs and hex-encoded key material.
- .NET assemblies — decompile with `ILSpy` / `dnSpyEx`; hardcoded credentials often live as string literals in obfuscated fields. `de4dot` normalises common obfuscators.
- ELF and Mach-O — `objdump -s -j .rodata`, `otool -s __TEXT __cstring`.

**Configuration blocks**
- Malware families with known config formats — dedicated parsers (`malwareconfig.com` / `CAPE` community parsers). Feeds directly into `type`/`subtype` schema fields.
- Custom/unknown configs — locate the decryptor stub statically; extract the algorithm and key; decrypt offline in a scratch buffer; record the plaintext structure without storing the raw config file.

**Packed payloads**
- Recognise packer (UPX, Themida, VMProtect, Enigma) from entropy + section names. Unpack in an isolated instrumented environment (Cuckoo/CAPE/x64dbg script), dump the unpacked image, then apply static extraction to the dump.
- Loader → shellcode → payload chains: extract each stage's embedded material separately; correlate keys reused across stages (common attribution signal).

**Cross-cutting**
- Payload-embedded credentials frequently have *very* broad `reuse-potential` inside their intended deployment scope (all bots authenticating to the same C2, all sample instances sharing an XOR key) but classifying reuse against the target requires input from `target-network-analyst`. Classification and reporting via [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); the report cites offset within the binary and a decryption-method identifier, never the raw credential.
