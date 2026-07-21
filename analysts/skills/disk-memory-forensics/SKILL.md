---
name: disk-memory-forensics
description: Use to perform forensic reads of disk and memory — to self-check what evidence your operation left on a host, or to understand a target system's state and history the way a responder would.
---

# Disk & Memory Forensics

## Objective
Apply forensic technique to disk and memory to see a host the way a responder would — either as a self-detection check on the evidence your own activity left behind, or to understand a target's state, history, and defensive posture.

## When to use
- Self-detection: verifying what artifacts your on-host actions actually left, and whether cleanup succeeded, before you rely on stealth.
- Target understanding: reconstructing a compromised or accessed host's history, defenses, and stored secrets.

## Method
- Memory: enumerate processes, injected regions, hooks, network connections, and in-memory artifacts to confirm what a live-response capture would reveal about you.
- Disk: examine filesystem timelines, prefetch/amcache/shimcache, event logs, registry, browser and shell history, and deletion/recovery traces.
- Build a timeline and diff it against your own action log to find residual indicators you did not expect to remain.
- For target work, mine the same sources for credentials, defensive tooling, prior-incident traces, and pivot opportunities.
- Judge what a responder arriving now would reconstruct, and prioritize cleanup or avoidance of the highest-fidelity remnants.

## Signals / outputs
- A forensic timeline of the host with your operation's residual artifacts flagged.
- A self-detection verdict: what cleanup missed and what a responder would find.
- For targets, extracted secrets, defensive-posture intel, and pivot leads.
