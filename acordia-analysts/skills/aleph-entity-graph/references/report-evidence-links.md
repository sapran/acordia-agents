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

Render the report, then run this from a shell that has Python 3. It parses the receipt and HTML anchors, ignores anchors inside disclosure `<pre>` blocks, and reports counts only. It exits non-zero if any expected entity is absent, has the wrong origin or route, has an unsafe link, or is represented by an anchor with no `href`.

```sh
python3 - "$RECEIPT" "$REPORT" <<'PY'
import html.parser, pathlib, sys
from urllib.parse import quote, urlsplit

receipt, report = map(pathlib.Path, sys.argv[1:])
expected = []
for line in receipt.read_text().splitlines():
    if (not line.startswith('|') or line.lower().startswith('| safe ui origin') or
            all(not cell.strip().replace('-', '') for cell in line.strip().strip('|').split('|'))):
        continue
    cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
    if len(cells) != 4:
        raise SystemExit('receipt rows: invalid')
    origin, collection, entity, offset = cells
    p = urlsplit(origin)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.query or p.fragment or p.path not in ('', '/'):
        raise SystemExit('receipt origins: unsafe')
    expected.append((origin.rstrip('/'), collection, entity, offset))

class Anchors(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.anchors = []; self.current = None; self.pre = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'pre': self.pre += 1
        if tag == 'a' and not self.pre:
            if self.current is not None: self.anchors.append(self.current)
            hrefs = [value for name, value in attrs if name.lower() == 'href']
            values = [value or '' for _name, value in attrs]
            self.current = [hrefs, values, []]
    def handle_data(self, data):
        if self.current is not None: self.current[2].append(data)
    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            self.anchors.append(self.current); self.current = None
        if tag == 'pre' and self.pre: self.pre -= 1

parser = Anchors(); parser.feed(report.read_text())
if parser.current is not None: parser.anchors.append(parser.current)
entity_values = [entity for _origin, _collection, entity, _offset in expected]
href_less = sum(
    not hrefs and any(entity in ' '.join(values + text) for entity in entity_values)
    for hrefs, values, text in parser.anchors
)
duplicate_href = sum(len(hrefs) > 1 for hrefs, _values, _text in parser.anchors)
hrefs = [hrefs[0] for hrefs, _values, _text in parser.anchors if hrefs]
unsafe = sum(bool(
    (p := urlsplit(h)).scheme not in ('http', 'https') or not p.hostname or
    p.username or p.password or p.query or p.fragment
) for h in hrefs)
wrong_origin = wrong_route = missing = 0
for origin, _collection, entity, _offset in expected:
    want = f'{origin}/entities/{quote(entity, safe="")}'
    matching = [h for h in hrefs if entity in h]
    if want in hrefs:
        continue
    if not matching:
        missing += 1; continue
    parsed = [urlsplit(h) for h in matching]
    if any(f'{p.scheme}://{p.netloc}' != origin for p in parsed):
        wrong_origin += 1
    else:
        wrong_route += 1
print('expected:', len(expected))
print('linked:', len(expected) - missing - wrong_origin - wrong_route)
print('missing:', missing)
print('wrong-origin:', wrong_origin)
print('wrong-route:', wrong_route)
print('unsafe:', unsafe)
print('href-less-anchors:', href_less)
print('duplicate-href-anchors:', duplicate_href)
raise SystemExit(bool(missing or wrong_origin or wrong_route or unsafe or href_less or duplicate_href))
PY
```

A clean receipt-to-link comparison proves coverage, not that a remote entity is genuine. Resolve a sample against the already-read Aleph instance as `briefing-reporting` requires.
