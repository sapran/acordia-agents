---
name: web-api-authflow-analysis
description: Use when a web app or API is the target surface — reason about its application logic and authentication/authorization flows to find where identity, trust, or state can be broken.
---

# Web/API, App-Logic & Auth-Flow Analysis

## Objective
Model a target web application or API's business logic and auth flows to locate where authentication, authorization, or state assumptions can be subverted for access, data, or privilege.

## When to use
- When the target's exposed surface is a web app, API, or SSO/OAuth/SAML flow.
- When bugs are likely in logic and trust boundaries rather than memory-corruption territory.

## Method
- Map the app's roles, objects, and intended workflow — who may do what to which resource, and the state each action assumes.
- Trace auth flows end-to-end: login, token issuance/validation, session lifecycle, OAuth/OIDC/SAML exchanges, and federation trust.
- Probe authorization at the object and function level (IDOR, missing checks, role confusion, tenant isolation) and multi-step logic (skipped steps, replay, race, negative/overflow values).
- Hunt token and trust weaknesses — signature/audience/expiry validation, secret handling, redirect and callback abuse, assertion forgery.
- Chain findings toward the crown jewels: from a logic flaw to account takeover, tenant crossover, or privileged function.

## Signals / outputs
- App-logic and auth-flow model with marked trust boundaries.
- Authz and logic-flaw findings with the assumption each breaks.
- Exploit chains from entry weakness to high-value objective.
