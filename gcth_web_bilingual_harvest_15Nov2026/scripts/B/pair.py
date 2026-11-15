# Usage: python3 -I pair.py BASE slug org EN_URL [FR_URL] [--sel CSS] [--note TEXT]
# Fetches EN (and FR via hreflang/language toggle if FR_URL omitted), saves raw HTML,
# extracts main content (title + body paragraphs) and records a row in pairs.jsonl.
import sys, os, re, json, subprocess, argparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
ap = argparse.ArgumentParser()
ap.add_argument('base'); ap.add_argument('slug'); ap.add_argument('org'); ap.add_argument('en'); ap.add_argument('fr', nargs='?')
ap.add_argument('--sel', default=None); ap.add_argument('--note', default=''); ap.add_argument('--drop', default='')
ap.add_argument('--title', default=None); ap.add_argument('--tsel', default=None)
a = ap.parse_args()
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
def get(url, out):
    r = subprocess.run(['curl','-sL','-A',UA,'-m','60','--compressed','-o',out,'-w','%{http_code} %{url_effective}',url],capture_output=True,text=True)
    code, eff = r.stdout.split(' ',1)
    return int(code), eff
def find_fr(soup, url):
    for l in soup.find_all(['link','a'], hreflang=True):
        if l['hreflang'].lower().startswith('fr') and l.get('href'): return urljoin(url, l['href'])
    for l in soup.find_all('a', href=True):
        t = l.get_text(' ', strip=True)
        if t in ('Français','French','FR','Fr','FRANÇAIS','français') : return urljoin(url, l['href'])
    return None
SELS = {'greatersudbury.ca':'main article','grandsudbury.ca':'main article','museums.greatersudbury.ca':'.wp-block-post-content','musees.grandsudbury.ca':'.wp-block-post-content'}
def extract(html, url, sel):
    s = BeautifulSoup(html, 'lxml')
    for t in s(['script','style','noscript','nav','footer','iframe','svg','button']): t.decompose()
    if a.drop:
        for d in a.drop.split('|'):
            for t in s.select(d): t.decompose()
    dom = re.sub(r'^www\.','',url.split('/')[2])
    sel = sel or SELS.get(dom)
    node = None
    for cand in ([sel] if sel else []) + ['main article','article','main','[role=main]','#content','body']:
        if cand:
            node = s.select_one(cand)
            if node: break
    title = None
    h1 = (s.select_one(a.tsel) if a.tsel else None) or node.find('h1') or s.find('h1')
    if h1: title = h1.get_text(' ', strip=True)
    paras = []
    for el in node.find_all(['h1','h2','h3','h4','h5','h6','p','li','blockquote','figcaption','td','dt','dd']):
        anc = False
        for par in el.parents:
            if par is node: break
            if par.name in ('p','li','blockquote','td','dd'): anc = True; break
        if anc and el.name != 'li': continue
        if el.name in ('li','td','dd','blockquote') and el.find(['p','li','h1','h2','h3','h4','h5','h6']): continue
        t = re.sub(r'\s+',' ', el.get_text(' ', strip=True)).strip()
        t = re.sub(r' ([,.;:)])', r'\1', t)
        if t and (not paras or paras[-1]!=t): paras.append(t)
    if title and paras and paras[0]==title: paras = paras[1:]
    if not paras:
        paras = [re.sub(r'\s+',' ',x).strip() for x in node.get_text('\n').split('\n\n') if x.strip()]
    return title, paras
raw = os.path.join(a.base,'raw')
code, eff = get(a.en, os.path.join(raw, a.slug+'_EN.html'))
if code != 200: print('EN fail', code, a.en); sys.exit(1)
enh = open(os.path.join(raw,a.slug+'_EN.html'),encoding='utf-8',errors='replace').read()
fr = a.fr or find_fr(BeautifulSoup(enh,'lxml'), eff)
if not fr: print('NO FR twin', a.en); sys.exit(2)
code2, eff2 = get(fr, os.path.join(raw, a.slug+'_FR.html'))
if code2 != 200: print('FR fail', code2, fr); sys.exit(1)
frh = open(os.path.join(raw,a.slug+'_FR.html'),encoding='utf-8',errors='replace').read()
te, pe = extract(enh, eff, a.sel); tf, pf = extract(frh, eff2, a.sel)
we = sum(len(p.split()) for p in pe); wf = sum(len(p.split()) for p in pf)
for lang,t,p in (('EN',te,pe),('FR',tf,pf)):
    open(os.path.join(a.base, f'{a.slug}_{lang}.txt'),'w').write((t or '')+'\n\n'+'\n\n'.join(p)+'\n')
print(f'{a.slug}: EN {we}w "{te}" | FR {wf}w "{tf}" | {eff2}')
if we < 40 or wf < 40: print('  TOO SHORT'); 
row = dict(slug=a.slug, title_en=a.title or te, url_en=eff, url_fr=eff2, org=a.org, we=we, wf=wf, note=a.note)
rows = [json.loads(l) for l in open(os.path.join(a.base,'scripts','pairs.jsonl'))] if os.path.exists(os.path.join(a.base,'scripts','pairs.jsonl')) else []
rows = [r for r in rows if r['slug']!=a.slug] + [row]
open(os.path.join(a.base,'scripts','pairs.jsonl'),'w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
