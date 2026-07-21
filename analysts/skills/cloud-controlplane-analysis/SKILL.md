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

## Credential extraction

Passive extraction from cloud artefacts already collected — instance-metadata snapshots, state files, exported configuration, service-account key files. No live cloud API calls to validate; no probing of IMDS endpoints on running targets.

**Instance metadata (IMDS captures)**
- AWS IMDSv1/v2 capture — parse `iam/security-credentials/<role>/` JSON for `AccessKeyId`, `SecretAccessKey`, `Token`, `Expiration`. Session tokens are short-lived; check `Expiration` before ranking priority.
- GCP metadata capture — `computeMetadata/v1/instance/service-accounts/default/token` yields an OAuth2 bearer with scope list; `identity` endpoint yields a signed JWT.
- Azure IMDS — `metadata/identity/oauth2/token?resource=...` yields a JWT bound to a system- or user-assigned managed identity.

**Service-account key files**
- GCP `type: service_account` JSON — contains `private_key` PEM + `client_email`; scope inferred from IAM bindings collected separately. `-----BEGIN PRIVATE KEY-----` is the anchor.
- AWS `~/.aws/credentials` / `~/.aws/config` INI — `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`, plus role-assumption chains via `source_profile` / `role_arn`.
- Azure Service Principal JSON — `appId`, `password` (or `clientSecret`), `tenant`. Certificate-based SPs carry a PFX reference.

**Infrastructure-as-code state**
- Terraform state (`terraform.tfstate`, `terraform.tfstate.d/`, S3-backend copies) — resources of type `aws_iam_access_key`, `aws_db_instance` (master_password), `random_password`, `vault_generic_secret` write plaintext to state. Search: `"sensitive": true` blocks and any `password`/`secret`/`key` attribute.
- CloudFormation exported templates — `NoEcho: true` parameters land in state but not stack outputs; drift detection can surface them.
- Pulumi state — encrypted by default with a passphrase or KMS key; if the passphrase is in the environment (`PULUMI_CONFIG_PASSPHRASE`) collected alongside state, extraction becomes a passive offline decrypt.

**Cloud secret stores (exported)**
- AWS Secrets Manager / Systems Manager Parameter Store — exports typically JSON with `Name`, `Value`, `Version`. Value is plaintext.
- Azure Key Vault secret/certificate exports — `.pem` / `.pfx`; certificate exports include private key if the vault permission included it.
- GCP Secret Manager exports — plaintext payload after `gcloud secrets versions access`.

**Cross-cutting**
- Cloud-plane credentials frequently have session/time bounds — record `Expiration` in `freshness`; expired credentials still classify for correlation but priority drops to P3. Root/organisation-level keys (`arn:aws:iam::*:root`, GCP `roles/owner`, Azure `Global Administrator`) always mark P0. Reporting via [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); IAM path or ARN identifies the credential, never the secret value.
