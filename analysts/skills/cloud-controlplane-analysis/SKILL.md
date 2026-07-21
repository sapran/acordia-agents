---
name: cloud-controlplane-analysis
description: Use when the target lives in AWS/Azure/GCP — analyze the cloud control plane, services, and the trust between them to find where API-level access, roles, or misconfiguration yield control.
---

# Cloud Control-Plane & Service Analysis

## Objective
Model a target's cloud estate at the control-plane level — services, identities, roles, and inter-service trust — to find where an API call or a misconfigured grant converts into meaningful control or data.

## When to use
- When the target's assets and administration live in a cloud provider rather than (or alongside) on-prem.
- When the real attack surface is IAM policy, service config, and metadata — not network ports.

## Method
- Inventory the estate: accounts/subscriptions/projects, key services, and the control-plane APIs that govern them.
- Map identity and trust: IAM roles/policies, service principals, workload identities, assume-role/federation chains, and cross-account trust.
- Hunt control-plane misconfiguration — over-permissive policies, public resources, exposed secrets/keys, metadata/SSRF paths, logging gaps.
- Trace privilege-escalation and pivot chains through the control plane (role chaining, service-to-service trust, CI/CD and infra-as-code paths).
- Tie control-plane access to mission effect: which grant reaches the crown-jewel data, key vault, or production workload.

## Signals / outputs
- Estate and identity/trust map with cross-account and federation edges.
- Misconfiguration and exposed-credential findings.
- Control-plane escalation/pivot chains reaching high-value assets.
