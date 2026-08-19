---
name: web-api-authflow-analysis
description: Use when a web app or API is the target surface — reason about its application logic and authentication/authorization flows to find where identity, trust, or state can be broken.
metadata:
  acordia:
    family: target-modelling
    grid_row: web-api-authflow-analysis
    grid_deep_in: ['T&N']
    grid_working_in: [Def]
    source: docs/roles/operational-analyst.md#L86
---

# Web/API, App-Logic & Auth-Flow Analysis

## Objective
Model a target web application or API's business logic and auth flows to locate where authentication, authorization, or state assumptions can be subverted for access, data, or privilege.

## When to use
- When the target's exposed surface is a web app, API, or SSO/OAuth/SAML flow.
- When bugs are likely in logic and trust boundaries rather than memory-corruption territory.

## Method
- Inventory the collected web/API material with `ls` / `find` / `glob` — HAR archives, proxy transcripts (`.saz`/`.mitm`/Burp session files), captured JWTs, OpenAPI/Swagger exports, SAML metadata, source-code drops — before opening any single file.
- Map the app's roles, objects, and intended workflow — who may do what to which resource, and the state each action assumes. Drive reads with `grep`/`jq` for endpoint patterns, role-token claims, and state-machine transitions; open only the matched request/response pairs by line range, not the whole HAR.
- Trace auth flows end-to-end: login, token issuance/validation, session lifecycle, OAuth/OIDC/SAML exchanges, and federation trust. Decode tokens offline via `jwt-cli decode --no-verify` or an equivalent library in `verify_signature=False` mode; never replay live.
- Probe authorization at the object and function level (IDOR, missing checks, role confusion, tenant isolation) and multi-step logic (skipped steps, replay, race, negative/overflow values).
- Hunt token and trust weaknesses — signature/audience/expiry validation, secret handling, redirect and callback abuse, assertion forgery.
- Chain findings toward the crown jewels: from a logic flaw to account takeover, tenant crossover, or privileged function.
- Cite every finding by `<capture-file>@L<line>` (HAR/JSON/text) or `<capture-file>:<byte-offset>` (binary formats after parser conversion) so a peer can re-open the exact request, token, or assertion.
- If `jwt-cli`, `jq`, `mitmproxy`, or a similar named tool is unavailable, either substitute a documented equivalent (a Python one-liner using `PyJWT` in `verify_signature=False` mode, `yq`) or flag the gap and stop — never eyeball a base64 string for claim structure.

## Signals / outputs
- App-logic and auth-flow model with marked trust boundaries.
- Authz and logic-flaw findings with the assumption each breaks.
- Exploit chains from entry weakness to high-value objective.

## Credential extraction

Passive analysis of collected auth material — tokens, cookies, API-key strings — captured from proxies, logs, browser storage exports, or HAR archives. Never replays a token against the live service.

**JWTs**
- Split on `.`; base64url-decode header and payload (payload only for classification; do not archive contents that are themselves PII/credentials).
- Header fields to record: `alg` (flag `none` and `HS256` with weak-secret risk), `kid` (key identifier — useful for correlation), `typ`.
- Payload fields to record: `iss`, `aud`, `sub`, `iat`, `exp`, `scope`/`scp`, `roles`, `azp`. Compute `exp - now` for freshness; expired ≠ useless (still shows the auth model).
- Tooling: `jwt-cli decode --no-verify`, `python -c 'import jwt; print(jwt.decode(t, options={"verify_signature": False}))'`.

**OAuth 2 / OIDC**
- Access token — often opaque, sometimes JWT; if opaque, all classification comes from the surrounding context (endpoint used, `scope` claim on the introspection response if collected).
- Refresh token — high value (long-lived, exchangeable). Flag P0 when scope is broad or refresh window exceeds 30 days.
- ID token — always JWT; carries user identity claims (`email`, `sub`, `preferred_username`) — treat as PII, not just credential material.
- Authorization codes — short-lived (~60s); found in redirect URLs in referer headers and browser history; useless after the initial exchange but reveal client_id / redirect_uri.

**API keys by provider**
- Use the pattern-library prefixes from [`credential-harvest-triage/references/credential-patterns.md`](../credential-harvest-triage/references/credential-patterns.md): `AKIA`, `ghp_`, `sk-`, `sk-ant-`, `xox[baprs]-`, `AIza`, `glpat-`, `npm_`, `pypi-`, `dckr_pat_`.
- Provider-specific parse: GitHub PATs disclose scope via `X-OAuth-Scopes` on any `/user` GET (do not call; if the header was captured in a log, record it); AWS access keys carry the account ID in the ID via `sts:GetAccessKeyInfo` documentation (offline mapping only).

**Session cookies**
- Framework signatures: Django `sessionid` (opaque), Rails `_session` (base64 JSON+HMAC — decodable without secret, forgery needs secret), Flask `session` (itsdangerous — signed base64, decodable), Express `connect.sid` (`s:<sid>.<hmac>`).
- Cookie flags recorded: `Secure`, `HttpOnly`, `SameSite`, `Domain` (broad domain widens scope), `Expires`/`Max-Age` (freshness).
- Session-storage exports (browser `sessionStorage`/`localStorage` from a HAR or profile export) frequently hold access tokens outside cookies.

**SAML assertions**
- Base64-decode, XML-parse. Fields to record: `Issuer`, `NameID`, `AudienceRestriction`, `Conditions/@NotBefore` and `@NotOnOrAfter` (freshness), attribute statements (roles/groups).
- Signature validation is out of scope for passive triage; note whether a signature is present, not whether it verifies.

**Cross-cutting**
- Web/API credentials often have narrow `scope` but broad `reuse-potential` (same token works across many endpoints). Refresh tokens and long-lived PATs always mark P0 or P1 depending on scope. All classification and reporting flows through [`credential-harvest-triage`](../credential-harvest-triage/SKILL.md); the report cites cookie name / claim identifier, never the token itself.
