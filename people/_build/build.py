import csv,json,os,re,html,sys
sys.path.insert(0,os.path.dirname(__file__))
from people import P
meta=json.load(open(sys.argv[1])) if len(sys.argv)>1 and os.path.exists(sys.argv[1]) else {}
root='/home/user/Claude/people'
rows=[]
import urllib.parse
PENDING={l.split('\t')[0]:'https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(l.rstrip('\n').split('\t')[1].replace(' ','_')) for l in open(os.path.join(os.path.dirname(__file__),'picks.tsv'))}
for line in P.strip().split('\n'):
    f=line.split('|')
    assert len(f)==13,(len(f),line)
    name,slug,ch,quote,role,born,died,status,pflag,alt,licov,conf,notes=f
    pf=src=lic=''
    if pflag=='P':
        m=meta.get(slug)
        if m and os.path.exists(f'{root}/portraits/{slug}.jpg'):
            pf=f'portraits/{slug}.jpg'; src=m['page']; lic=re.sub('<[^>]+>','',m['lic'])
            art=html.unescape(re.sub('<[^>]+>','',m.get('artist',''))).strip()
            if art and 'Unknown' not in art: notes=(notes+f'; author: {art[:80]}').strip('; ')
        else:
            conf=conf+' (download pending/failed)'; notes=(notes+'; Commons file identified but not downloaded (rate-limited)').strip('; ')
            src=PENDING.get(slug,'')
    else:
        src=alt
    found='yes' if pf else ('identified-not-downloaded' if pflag=='P' else 'no')
    rows.append(dict(name=name,slug=slug,chapters=ch,context_quote=quote,role=role,born=born,died=died,status_historical_or_living=status,portrait_file=pf,portrait_source_url=src,licence=lic or licov,match_confidence=conf if (pf or pflag=='P') else 'n/a',notes=notes,_found=found))

cols='name,slug,chapters,context_quote,role,born,died,status_historical_or_living,portrait_file,portrait_source_url,licence,match_confidence,notes'.split(',')
with open(f'{root}/named_people.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
json.dump(rows,open(f'{root}/_build/rows.json','w'),indent=1,ensure_ascii=False)
print(len(rows),'rows;',sum(r['_found']=='yes' for r in rows),'portraits downloaded')
