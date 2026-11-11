import json,subprocess,re,html,sys,csv
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/scripts')
import geo
from concurrent.futures import ThreadPoolExecutor
u=json.load(open(geo.R+'hp_union.json'))
byname={}
for x in u['all']: byname.setdefault(re.sub(r'\W+',' ',x['name'].lower()).strip(),[]).append(x['id'])
rows=list(csv.DictReader(open(geo.R+'fhd_2026.csv',encoding='utf-8-sig',errors='ignore')))
fhdk=[r for r in rows if re.search(r'\b(iron|magnetite|lodestone|compass|ore|mine|mines|mining|furnace|forge|forges)\b',(r['Commemorative inscription'] or '')+' '+r['Designation name'],re.I) and r['Designation type'].startswith('National Historic Site')]
extra=[]
for r in fhdk:
    k=re.sub(r'\W+',' ',(r['Designation name']+' National Historic Site of Canada').lower()).strip()
    for n,ids in byname.items():
        if n.startswith(re.sub(r'\W+',' ',r['Designation name'].lower()).strip()) and 'national historic site' in n: extra+=ids
ids=list(dict.fromkeys(u['near']+u['kw']+extra))
print('fetch',len(ids),'fhd-matched',len(set(extra)),flush=True)
def get(i):
    t=subprocess.run(['curl','-sS','-m','60','-A','gcth-desk-research/1.0','https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=%s'%i],capture_output=True).stdout.decode('utf8','ignore')
    lat=re.search(r'Latitude" content="([-0-9.]+)',t);lon=re.search(r'Longitude" content="([-0-9.]+)',t)
    title=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.S)
    txt=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>','',t,flags=re.S))))
    m=re.search(r'Description of Historic Place(.*?)(Other Name|Location of Documentation|Recognition)',txt)
    body=m.group(1) if m else ''
    th=re.search(r'Theme\s*-\s*Category and Type(.*?)(Historic Function|Architect|Builder|Location of)',txt)
    return dict(id=i,url='https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=%s'%i,title=html.unescape(re.sub('<[^>]+>','',title.group(1))).strip() if title else '',
                lat=float(lat.group(1)) if lat else None,lon=float(lon.group(1)) if lon else None,text=body.strip()[:4000],theme=th.group(1).strip()[:300] if th else '')
with ThreadPoolExecutor(3) as ex: out=list(ex.map(get,ids))
json.dump(dict(details=out,fhd_kw=[{k:r[k] for k in ('Designation name','Designation type','Commemorative inscription','Local area','Province or territory')} for r in fhdk]),open(geo.R+'hp_details.json','w'))
print('done',len(out),sum(1 for o in out if o['text']))
