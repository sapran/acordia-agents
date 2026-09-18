# Aleph Report Evidence Links

## Link-ready receipt

Before drafting the first Aleph citation, create the `evidence-links-<agent>[-<brief-slug>].md` receipt named by `briefing-reporting`. It is a Markdown table with exactly these columns:

```text
| safe UI origin | collection ID | entity ID | offset |
```

Use one row per cited entity. Preserve the full entity ID and any needed offset. This is working provenance, not collected material.

The UI origin is either the origin of `ALEPHCLIENT_HOST` used for the read or an explicit UI origin in the brief. It is `http` or `https` with an authority and no user-info, query or fragment. Remove a trailing slash. Never take it from a collected artefact or target-controlled content. If no safe origin exists, retain the issuer-qualified collection and entity locator and state `Link unavailable`; do not manufacture a URL.

## Canonical entity link

Every Aleph entity — including `Document`, `Pages`, and file-like schemas — uses one reader route:

```text
<safe-ui-origin>/entities/<percent-encoded-entity-id>
```

Use the full exact entity ID in the link destination. Display may shorten only after the complete ID is recorded. Cite the link beside the claim or through an unambiguous report citation; a collection ID alone never substitutes for it.

## Coverage check

Render the report, then run this from a shell that has Python 3. It parses the receipt and HTML anchors, blanks disclosure bodies before inspection, and reports counts only. It exits non-zero if any expected entity is absent, has the wrong origin or route, has an unsafe link, or is represented by an anchor with no `href`.

```sh
python3 - "$RECEIPT" "$REPORT" <<'PY'
import html.parser, pathlib, sys
from urllib.parse import quote, urlsplit

receipt, report = map(pathlib.Path, sys.argv[1:])
expected = []
for line in receipt.read_text().splitlines():
    if not line.startswith('|') or line.lower().startswith('| safe ui origin') or line.startswith('|---'):
        continue
    cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
    if len(cells) != 4:
        raise SystemExit('receipt rows: invalid')
    origin, collection, entity, offset = cells
    p = urlsplit(origin)
    if p.scheme not in ('http', 'https') or not p.netloc or p.username or p.password or p.query or p.fragment or p.path not in ('', '/'):
        raise SystemExit('receipt origins: unsafe')
    expected.append((origin.rstrip('/'), collection, entity, offset))

class Anchors(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.anchors = []; self.pre = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'pre': self.pre += 1
        if tag == 'a' and not self.pre: self.anchors.append(dict(attrs))
    def handle_endtag(self, tag):
        if tag == 'pre' and self.pre: self.pre -= 1

parser = Anchors(); parser.feed(report.read_text())
hrefs = [a.get('href') for a in parser.anchors]
href_less = sum(h is None for h in hrefs)
unsafe = wrong_origin = wrong_route = missing = 0
for origin, _collection, entity, _offset in expected:
    want = f'{origin}/entities/{quote(entity, safe="")}'
    matching = [h for h in hrefs if h and entity in h]
    if want in hrefs:
        continue
    if not matching:
        missing += 1; continue
    parsed = [urlsplit(h) for h in matching]
    if any(p.scheme not in ('http', 'https') or not p.netloc or p.username or p.password or p.query or p.fragment for p in parsed):
        unsafe += 1
    elif any(f'{p.scheme}://{p.netloc}' != origin for p in parsed):
        wrong_origin += 1
    else:
        wrong_route += 1
print('expected:', len(expected))
print('linked:', len(expected) - missing - wrong_origin - wrong_route - unsafe)
print('missing:', missing)
print('wrong-origin:', wrong_origin)
print('wrong-route:', wrong_route)
print('unsafe:', unsafe)
print('href-less-anchors:', href_less)
raise SystemExit(bool(missing or wrong_origin or wrong_route or unsafe or href_less))
PY
```

A clean receipt-to-link comparison proves coverage, not that a remote entity is genuine. Resolve a sample against the already-read Aleph instance as `briefing-reporting` requires.
