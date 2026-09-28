#!/usr/bin/env python3
"""Check slides/references-ledger.md and slides/references.bib against the canonical dossier.

Checks:
 1. Every URL in Appendix A and in the E/D rows of the dossier appears exactly once in the URL map,
    and maps to a key of the reference table or to an entry of the Excluded table.
 2. Every E and D row of the dossier is in the row map, and either relies on at least one key or is
    listed under "Dossier rows with no citable source".
 3. The row map and the E/D IDs column of the reference table agree, and every URL in a row that maps
    to a key has that key in the row's keys.
 4. references.bib has exactly the keys of the reference table.
Prints counts per class. Exit status 1 on any failure.

Usage: python3 slides/check_references.py [--write]   (--write puts the output into references-ledger.md)
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOSSIER = os.path.join(ROOT, 'Agent-Acceleration-Consolidated-Dossier-v3-2026-09-27.md')
MD = os.path.join(HERE, 'references-ledger.md')
BIB = os.path.join(HERE, 'references.bib')

url_re = re.compile(r'https?://[^\s)\]|,;>"`]+')
def clean(u): return u.rstrip('.,;:)*_')

L = open(DOSSIER, encoding='utf-8').read().split('\n')
iA = next(n for n, l in enumerate(L) if l.startswith('# Appendix A'))
iB = next(n for n, l in enumerate(L) if l.startswith('# Appendix B'))
dossier_urls = set(clean(u) for l in L[iA:iB] for u in url_re.findall(l))
rows = collections.OrderedDict()
for l in L:
    m = re.match(r'^\| ([ED]\d+) \|', l)
    if m:
        rows[m.group(1)] = l
        dossier_urls.update(clean(u) for u in url_re.findall(l))

md = open(MD, encoding='utf-8').read()
def section(title):
    m = re.search(r'^## ' + re.escape(title) + r'.*?$(.*?)(?=^## |\Z)', md, re.M | re.S)
    return [l for l in m.group(1).split('\n') if l.startswith('| ') and not l.startswith('|---')][1:]
def cells(l): return [c.strip() for c in re.split(r'(?<!\\)\|', l)[1:-1]]

refs = {c[0]: c for c in map(cells, section('References'))}
excluded = {c[0]: c for c in map(cells, section('Excluded'))}
nocite = {cells(l)[0] for l in section('Dossier rows with no citable source')}
url_map = collections.Counter(); url_to = {}
for c in map(cells, section('URL map')):
    url_map[c[0]] += 1; url_to[c[0]] = c[1]
row_map = {}
for c in map(cells, section('Row map')):
    row_map[c[0]] = [k for k in c[1].split(', ') if k and k != '—']

fail = []
# 1. URLs
for u in sorted(dossier_urls):
    if url_map[u] != 1: fail.append('URL %s appears %d times in the URL map' % (u, url_map[u])); continue
    t = url_to[u]
    if t not in refs and t not in excluded: fail.append('URL %s maps to unknown target %s' % (u, t))
for u in url_map:
    if u not in dossier_urls: fail.append('URL map entry %s is not in the dossier' % u)
# 2. rows
for r in rows:
    if r not in row_map: fail.append('row %s missing from the row map' % r); continue
    for k in row_map[r]:
        if k not in refs: fail.append('row %s relies on unknown key %s' % (r, k))
    if not row_map[r] and r not in nocite: fail.append('row %s has no key and is not listed as having no citable source' % r)
    if row_map[r] and r in nocite: fail.append('row %s has keys but is listed as having no citable source' % r)
for r in row_map:
    if r not in rows: fail.append('row map entry %s is not a dossier row' % r)
# 3. consistency
for k, c in refs.items():
    listed = set(re.findall(r'\b[ED]\d+\b', c[5].split('; cited in')[0]))
    expect = {r for r, ks in row_map.items() if k in ks}
    if listed != expect: fail.append('key %s: E/D column %s differs from row map %s' % (k, sorted(listed ^ expect), ''))
for r, line in rows.items():
    for u in url_re.findall(line):
        t = url_to.get(clean(u))
        if t in refs and t not in row_map.get(r, []): fail.append('row %s cites %s (key %s) but the row map lacks it' % (r, clean(u), t))
# 4. bib
bib_keys = re.findall(r'^@\w+\{([^,]+),', open(BIB, encoding='utf-8').read(), re.M)
if collections.Counter(bib_keys) != collections.Counter(list(refs)): fail.append('bib keys differ from table keys: %s' % sorted(set(bib_keys) ^ set(refs)))

cls = collections.Counter(c[1] for c in refs.values())
keyed = sum(1 for r in rows if row_map.get(r))
out = [
    'Dossier URLs (Appendix A + E/D rows): %d; mapped to a key: %d; mapped to Excluded: %d; unmapped or duplicated: %d.' % (
        len(dossier_urls), sum(1 for u in dossier_urls if url_to.get(u) in refs), sum(1 for u in dossier_urls if url_to.get(u) in excluded),
        sum(1 for u in dossier_urls if url_map[u] != 1)),
    'Dossier rows: %d (E %d, D %d); relying on at least one key: %d; with no citable source (listed below): %d.' % (
        len(rows), sum(1 for r in rows if r[0] == 'E'), sum(1 for r in rows if r[0] == 'D'), keyed, len(rows) - keyed),
    'Entries per class: A %d, B %d, C %d, D %d (citable %d); E (excluded URLs) %d. BibTeX entries: %d.' % (
        cls['A'], cls['B'], cls['C'], cls['D'], len(refs), len(excluded), len(bib_keys)),
    'Failures: %d%s' % (len(fail), ''.join('\n  - ' + f for f in fail)),
]
text = '\n'.join(out)
print(text)
if '--write' in sys.argv:
    block = '<!-- CHECK-START -->\n```\n' + text + '\n```\n<!-- CHECK-END -->'
    md = re.sub(r'<!-- CHECK-START -->.*?<!-- CHECK-END -->', lambda m: block, md, flags=re.S)
    open(MD, 'w', encoding='utf-8').write(md)
sys.exit(1 if fail else 0)
