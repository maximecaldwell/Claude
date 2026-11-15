#!/usr/bin/env python3
"""Generic main-content extractor.
usage: extract.py in.html out.txt "css selector[,css selector...]" ["drop selectors"]
Keeps title (h1 or <title>) + block text from first matching container(s)."""
import sys, re
from bs4 import BeautifulSoup, NavigableString

BLOCKS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'td', 'th', 'dt', 'dd', 'figcaption', 'pre']
DROP = ['script', 'style', 'noscript', 'nav', 'header', 'footer', 'form', 'iframe', 'svg', 'button', 'select', 'aside']


def clean(s):
    s = s.replace('\xa0', ' ').replace('​', '')
    return re.sub(r'\s+', ' ', s).strip()


def extract(html, sel, drop_extra=None, keep_header=False):
    soup = BeautifulSoup(html, 'lxml')
    drops = list(DROP)
    if keep_header:
        drops.remove('header')
    for t in soup(drops):
        t.decompose()
    if drop_extra:
        for d in drop_extra.split(','):
            for t in soup.select(d.strip()):
                t.decompose()
    conts = []
    for s in sel.split(','):
        conts += soup.select(s.strip())
    # remove nested duplicates
    conts = [c for c in conts if not any(c is not o and c in o.descendants for o in conts)]
    out = []
    for c in conts:
        # treat br as newline in block
        for br in c.find_all('br'):
            br.replace_with('\n')
        for el in c.find_all(BLOCKS + ['div']):
            if el.name == 'div':
                # only divs with direct text and no block children
                if el.find(BLOCKS + ['div']):
                    continue
            if el.name in BLOCKS and el.find_parent(BLOCKS) is not None and el.name not in ('li',):
                # nested block within a block (e.g. p in li): skip, parent handles
                if el.find_parent(BLOCKS).name != 'li' or el.name == 'p':
                    pass
            if el.name == 'li' and el.find(['p', 'ul', 'ol']):
                continue
            if el.name != 'li' and el.find_parent(['p']) is not None:
                continue
            txt = '\n'.join(clean(x) for x in el.get_text('').split('\n'))
            txt = re.sub(r'\n+', '\n', txt).strip()
            if txt:
                out.append(('- ' if el.name == 'li' else '') + txt)
    # dedupe consecutive
    res = []
    seen = set()
    for o in out:
        if o in seen:
            continue
        seen.add(o)
        res.append(o)
    # drop multi-line blocks whose every line also appears as its own block (duplicated containers)
    singles = set(res)
    res = [r for r in res if not ('\n' in r and all(x.strip() in singles or x.strip().lstrip('- ') in singles for x in r.split('\n') if x.strip()))]
    # drop teaser-link boilerplate
    res = [r for r in res if r.strip() not in ('Read more', 'Lire la suite', 'Learn more', 'En savoir plus', 'Read More')]
    res = [re.sub(r'\n(Read more|Lire la suite)$', '', r) for r in res]
    return '\n\n'.join(res)


if __name__ == '__main__':
    html = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    drop = sys.argv[4] if len(sys.argv) > 4 else None
    txt = extract(html, sys.argv[3], drop)
    open(sys.argv[2], 'w', encoding='utf-8').write(txt + '\n')
    print(sys.argv[2], len(txt.split()))
