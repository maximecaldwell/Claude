# Build one combined pair from Place des Arts "la-collection" item pages: EN pages carry only a
# short caption; FR pages carry the same caption followed by a long FR-only essay. We keep the
# caption (first paragraph after the repeated item title) from each side. On the Sacré-Coeur
# stained-glass item the site serves the captions in swapped languages; we swap them back.
import sys, os, json, glob, re
B = sys.argv[1]
from bs4 import BeautifulSoup
rows = [json.loads(l) for l in open(os.path.join(B,'scripts','pairs.jsonl'))]
items = [r for r in rows if r['slug'].startswith('pda_')]
def cap(path):
    L = [l for l in open(path).read().split('\n\n') if l.strip()]
    title = L[0].strip()
    # skip breadcrumb lines until the repeated title
    i = [k for k,l in enumerate(L) if l.strip()==title][1]
    return title, L[i+1].strip()
out = {'EN':[], 'FR':[]}
urls = []
for r in sorted(items, key=lambda r: r['slug']):
    te, ce = cap(os.path.join(B, r['slug']+'_EN.txt'))
    tf, cf = cap(os.path.join(B, r['slug']+'_FR.txt'))
    if 'vitrail' in r['slug']: ce, cf = cf, ce
    out['EN'].append(te+'\n\n'+ce); out['FR'].append(tf+'\n\n'+cf)
    urls.append((r['url_en'], r['url_fr']))
for L in out:
    head = 'The Collection – Place des Arts (object captions)' if L=='EN' else 'La collection – Place des Arts (légendes des objets)'
    open(os.path.join(B, f'pda_collection_captions_{L}.txt'),'w').write(head+'\n\n'+'\n\n'.join(out[L])+'\n')
    # keep per-item raw html (already in raw/); remove per-item txt files
for r in items:
    for L in ('EN','FR'): os.remove(os.path.join(B, r['slug']+f'_{L}.txt'))
we = sum(len(x.split()) for x in out['EN']); wf = sum(len(x.split()) for x in out['FR'])
rows = [r for r in rows if not r['slug'].startswith('pda_')]
rows.append(dict(slug='pda_collection_captions', title_en='The Collection – Place des Arts (object captions, 10 items)',
  url_en=' ; '.join(u[0] for u in urls), url_fr=' ; '.join(u[1] for u in urls), org='Place des Arts du Grand Sudbury', we=we, wf=wf,
  note='Captions for 10 physical objects built into Place des Arts (27 Larch St, former King Edward Hotel site): salvaged items in the building collection. Bricks page excluded. FR pages also carry long FR-only essays (not included). Sacré-Coeur stained-glass captions were language-swapped on site; corrected.'))
open(os.path.join(B,'scripts','pairs.jsonl'),'w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
print(we, wf)
