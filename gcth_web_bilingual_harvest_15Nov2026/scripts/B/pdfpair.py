# Usage: python3 -I pdfpair.py BASE slug org EN_PDF_URL FR_PDF_URL title_en note
# Downloads both PDFs into raw/, extracts text with pdftotext, reflows wrapped lines into paragraphs.
import sys, os, re, json, subprocess
B, slug, org, en, fr, title, note = sys.argv[1:8]
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
def txt(url, lang):
    p = os.path.join(B, 'raw', f'{slug}_{lang}.pdf')
    subprocess.run(['curl','-sL','-A',UA,'-m','120','-o',p,url], check=True)
    t = subprocess.run(['pdftotext','-enc','UTF-8',p,'-'],capture_output=True,text=True).stdout
    paras = []
    for block in re.split(r'\n\s*\n', t.replace('\f','\n\n')):
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines: continue
        s = ''
        for l in lines:
            if s.endswith('-') and not s.endswith(' -'): s = s[:-1] + l
            else: s = (s + ' ' + l).strip()
        s = re.sub(r'\s+', ' ', s)
        if re.fullmatch(r'\d{1,3}', s): continue   # page numbers
        paras.append(s)
    open(os.path.join(B, f'{slug}_{lang}.txt'), 'w').write('\n\n'.join(paras) + '\n')
    return sum(len(x.split()) for x in paras)
we = txt(en, 'EN'); wf = txt(fr, 'FR')
print(slug, we, wf)
pj = os.path.join(B,'scripts','pairs.jsonl')
rows = [json.loads(l) for l in open(pj)]
rows = [r for r in rows if r['slug'] != slug] + [dict(slug=slug, title_en=title, url_en=en, url_fr=fr, org=org, we=we, wf=wf, note=note)]
open(pj,'w').write(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows))
