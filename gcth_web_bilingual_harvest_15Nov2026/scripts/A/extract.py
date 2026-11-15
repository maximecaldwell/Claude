#!/usr/bin/env python3
"""Extract main content (title + body) from saved raw HTML.
usage: extract.py SITE RAW.html OUT.txt
SITE in: tce, hp (historicplaces), dfhd, generic:<css selector>
"""
import sys, re
from bs4 import BeautifulSoup, NavigableString

BLOCKS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li', 'blockquote', 'dt', 'dd', 'td', 'th', 'caption']


def clean(s):
    s = s.replace('\xa0', ' ')
    s = re.sub(r'[ \t\r\n]+', ' ', s)
    return s.strip()


def blocks_text(root, drop=()):
    for sel in ['script', 'style', 'noscript', 'iframe', 'figure', 'figcaption', 'img', 'form', 'button', 'nav'] + list(drop):
        for t in root.select(sel):
            t.decompose()
    for br in root.find_all('br'):
        br.replace_with(' ')
    out = []
    for el in root.find_all(BLOCKS):
        # skip if it contains nested block (take innermost)
        if el.find(BLOCKS):
            # still capture direct text in li/td containing nested p
            continue
        t = clean(el.get_text())
        if el.name == 'li':
            t = '- ' + t
        if t and t != '-':
            out.append(t)
    # also catch loose text directly in divs (e.g. <div>text<br>text</div>)
    return out


def tce(soup):
    title = clean(soup.select_one('h1#article-title').get_text())
    parts = [title]
    summ = soup.select_one('.article-content__summary')
    if summ:
        parts += blocks_text(summ)
    body = soup.select_one('.article-content-body')
    parts += blocks_text(body, drop=['.article-related', '.timeline'])
    # stop at 'See also'/'Voir aussi' lists? keep body only
    return parts


def hp(soup):
    root = soup.select_one('#wb-main-in') or soup.select_one('main') or soup.select_one('#wb-cont')
    return root


def generic(soup, sel):
    root = soup.select_one(sel)
    if root is None:
        raise SystemExit('selector not found: ' + sel)
    t = soup.find('h1')
    parts = []
    if t and not root.find('h1'):
        parts.append(clean(t.get_text(' ')))
    parts += blocks_text(root)
    return parts


def main():
    global DROP
    site, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    cut = [c for c in sys.argv[4:] if not c.startswith('--drop=')]  # optional stop markers
    DROP = [c[7:] for c in sys.argv[4:] if c.startswith('--drop=')]
    SKIP = [re.compile(c[7:]) for c in cut if c.startswith('--skip=')]
    cut = [c for c in cut if not c.startswith('--skip=')]
    global NN
    NN = '--nn' in cut
    cut = [c for c in cut if c != '--nn']
    soup = BeautifulSoup(open(src, 'rb').read(), 'html.parser')
    if site == 'tce':
        parts = tce(soup)
    elif site.startswith('blocks:'):
        root = soup.select_one(site[len('blocks:'):])
        if root is None:
            raise SystemExit('selector not found')
        for sel in ['script', 'style', 'noscript', 'iframe', 'img', '.aspNetHidden', 'input', 'select', 'button', '.thumbnails', '#imagewrapper', '#primaryImageCaption', 'nav', 'figure', 'figcaption'] + DROP:
            for t in root.select(sel):
                t.decompose()
        MARK = '\u2029'
        for br in root.find_all('br'):
            br.replace_with(MARK)
        for el in root.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'tr', 'center', 'hr', 'dt', 'dd', 'blockquote', 'section', 'ul', 'ol', 'table', 'span', 'label', 'header', 'article', 'dl', 'details', 'summary']):
            if el.name in ('span', 'label') and not (el.get('class') or el.get('id')):
                continue
            el.insert_before(MARK)
            el.append(MARK)
            if el.name == 'li':
                el.insert(0, '- ')
        raw = root.get_text()
        if NN:
            raw = re.sub(r'\r?\n[ \t]*\r?\n', MARK, raw)
        parts = []
        for ln in raw.split(MARK):
            ln = clean(ln)
            if not ln or ln == '-':
                continue
            if parts and parts[-1].endswith(':') and not ln.endswith(':') and len(parts[-1]) < 60:
                parts[-1] = parts[-1] + ' ' + ln
            else:
                parts.append(ln)
    elif site.startswith('lines:'):
        root = soup.select_one(site[len('lines:'):])
        if root is None:
            raise SystemExit('selector not found')
        for sel in ['script', 'style', 'noscript', 'iframe', 'img', 'form > .aspNetHidden', 'input', 'select', 'button', '.thumbnails', '#imagewrapper', '#primaryImageCaption']:
            for t in root.select(sel):
                t.decompose()
        for br in root.find_all('br'):
            br.replace_with('\n')
        raw = root.get_text('\n')
        parts = []
        for ln in raw.split('\n'):
            ln = clean(ln)
            if not ln:
                continue
            if parts and (parts[-1].endswith(':')) and not ln.endswith(':'):
                parts[-1] = parts[-1] + ' ' + ln
            else:
                parts.append(ln)
    elif site.startswith('generic:'):
        parts = generic(soup, site[len('generic:'):])
    else:
        raise SystemExit('unknown site')
    # cut at stop markers (exact block match, startswith)
    if cut:
        for i, p in enumerate(parts):
            if any(p.startswith(c) for c in cut) and i > 0:
                parts = parts[:i]
                break
    parts = [p for p in parts if not any(r.search(p) for r in SKIP)]
    # dedupe consecutive
    res = []
    for p in parts:
        if not res or res[-1] != p:
            res.append(p)
    text = '\n\n'.join(res) + '\n'
    open(dst, 'w', encoding='utf-8').write(text)
    print(dst, len(text.split()), 'words')


if __name__ == '__main__':
    main()
