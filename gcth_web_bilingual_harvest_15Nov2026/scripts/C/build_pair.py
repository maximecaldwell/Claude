#!/usr/bin/env python3
"""Build one EN/FR pair from two raw HTML files.
usage: build_pair.py slug en.html fr.html selector url_en url_fr org notes [drop_selectors] [title_suffix_regex]
Writes <slug>_EN.txt/<slug>_FR.txt in cwd (title + body) and appends to pairs.tsv."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import extract
from bs4 import BeautifulSoup

slug, fen, ffr, sel, uen, ufr, org, notes = sys.argv[1:9]
drop = sys.argv[9] if len(sys.argv) > 9 and sys.argv[9] else None
suf = sys.argv[10] if len(sys.argv) > 10 else r'\s*[|\-–—]\s*[^|\-–—]*$'


def title_of(html):
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('h1')
    if h1 and h1.get_text(strip=True):
        return re.sub(r'\s+', ' ', h1.get_text(' ', strip=True))
    t = soup.title.get_text(strip=True) if soup.title else ''
    return re.sub(suf, '', t).strip()


titles = []
for lang, f in (('EN', fen), ('FR', ffr)):
    html = open(f, encoding='utf-8', errors='replace').read()
    body = extract(html, sel, drop)
    t = title_of(html)
    if t and not body.startswith(t):
        body = t + '\n\n' + body
    open(f'{slug}_{lang}.txt', 'w', encoding='utf-8').write(body.strip() + '\n')
    titles.append(t)
    print(slug, lang, len(body.split()))
with open('pairs.tsv', 'a', encoding='utf-8') as o:
    o.write('\t'.join([slug, titles[0], uen, ufr, org, notes]) + '\n')
