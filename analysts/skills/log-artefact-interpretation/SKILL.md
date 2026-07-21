---
name: log-artefact-interpretation
description: Use whenever you have raw logs or artefacts in hand — host, network, or cloud — and need to reconstruct what happened, what the environment is, and whether your own activity left marks.
---

# Log / Artefact Interpretation

## Objective
Read logs and artefacts across host, network, and cloud to reconstruct events, understand the environment, and see the target — and your own footprint — the way a defender's telemetry would.

## When to use
- When on-box or collected logs and artefacts hold the answer to what happened, what exists, or who did it.
- When assessing your own detectability — what evidence your actions wrote, and where it lives.

## Method
- Identify the artefact and its semantics: know what each log/event actually records, its fidelity, retention, and blind spots before trusting it.
- Reconstruct timelines by correlating artefacts across host, network, and cloud into one ordered account of events.
- Read the environment from its exhaust — installed tooling, agents, logging config, and coverage gaps revealed by what is and isn't recorded.
- Turn the lens on yourself: locate the artefacts your own operation generated and judge what a hunter reading them would conclude.
- Distinguish signal from routine noise, and flag artefacts that have been cleared, tampered, or are conspicuously absent.

## Signals / outputs
- A reconstructed timeline of events from correlated artefacts.
- A map of the environment's logging coverage, fidelity, and blind spots.
- Own-footprint assessment: what you left behind, where, and how visible it is.
