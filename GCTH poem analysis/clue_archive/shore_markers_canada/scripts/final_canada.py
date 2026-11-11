import json,math,sys,re,html,os,csv,collections,subprocess,urllib.parse
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada/scripts')
from concurrent.futures import ThreadPoolExecutor
from wmsdist import mindist
from agq import getj
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada'
SH=S+'/sheets';os.makedirs(SH,exist_ok=True)
c=json.load(open(S+'/data_cand_shore.json'))
MAXS=40
def ok(v): return isinstance(v,float) and v<=MAXS
sel=[m for m in c if ok(m['wb_m']) or ok(m['wc_m'])]
print('selected',len(sel),flush=True)
CP='https://maps-cartes.ec.gc.ca/arcgis/rest/services/CWS_SCF/CPCAD/MapServer/0/query'
def nrcan_sheet(i):
    f=f'{SH}/{i}.html'
    if not os.path.exists(f) or os.path.getsize(f)<1000:
        subprocess.run(['curl','-sS','-m','90','-o',f,f'https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/station/report-rapport.php?id={i}'])
    s=open(f,encoding='utf-8',errors='replace').read()
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S);t=html.unescape(re.sub('<[^>]+>',' ',t));t=re.sub(r'\s+',' ',t)
    a=t.find('Station Marker');b=t.find('Use of Canadian Geodetic')
    return t[a:b] if a>=0 else ''
def job(m):
    lat,lon=m['lat'],m['lon']
    m['road_m']=mindist('road_segment_50k',lat,lon,half=300,px=2.0)
    d=getj(CP,dict(geometry=f'{lon},{lat}',geometryType='esriGeometryPoint',inSR=4326,spatialRel='esriSpatialRelIntersects',outFields='NAME_E,TYPE_E,MGMT_E',returnGeometry='false',f='json'))
    m['cpcad']='ERR' if 'error' in d else ['/'.join(str(v) for v in f['attributes'].values() if v) for f in d.get('features',[])]
    g=getj('https://geogratis.gc.ca/services/geoname/en/geonames.json',dict(lat=lat,lon=lon,radius=2,concise='LAKE,RIV,BAY,SEA,CHAN,RAP',num=1))
    try: it=g['items'][0];m['water_name']=f"{it['name']} ({it['concise']['code']}, CGNDB nearest named feature within 2 km)"
    except Exception: m['water_name']=''
    if m['src'].startswith('NRCan'): m['sheet']=nrcan_sheet(m['id'])
    elif m.get('desc_prov'): m['sheet']=m['desc_prov']
    else: m['sheet']=''
    return m
EN=S+'/data_enriched.json'
cache={m['id']:m for m in json.load(open(EN))} if os.path.exists(EN) else {}
def job2(m):
    c=cache.get(m['id'])
    if c and 'road2k_m' in c: return c
    m=job(m)
    m['road2k_m']=mindist('road_segment_50k',m['lat'],m['lon'],half=2000,px=10.0) if m['road_m'] is None else m['road_m']
    return m
with ThreadPoolExecutor(8) as ex: out=list(ex.map(job2,sel))
json.dump(out,open(EN,'w'))
if 'road2k_m' not in out[0]:
    def rj(m):
        m['road2k_m']=mindist('road_segment_50k',m['lat'],m['lon'],half=2000,px=10.0) if m['road_m'] is None else m['road_m'];return m
    with ThreadPoolExecutor(8) as ex: out=list(ex.map(rj,out))
    json.dump(out,open(EN,'w'))
if 'coast_m' not in out[0]:
    def cj(m):
        m['coast_m']=mindist('shoreline_50k',m['lat'],m['lon'],half=300,px=2.0);return m
    with ThreadPoolExecutor(8) as ex: out=list(ex.map(cj,out))
    json.dump(out,open(EN,'w'))
def g(rx,t):
    x=re.search(rx,t,re.I|re.S);return x.group(1).strip() if x else ''
rows=[]
for m in out:
    t=m['sheet'];low=t.lower()
    loc=g(r'Location (.*)',t) if m['src'].startswith('NRCan') else t
    mtype=g(r'Comments (.*?) Location',t) if m['src'].startswith('NRCan') else ''
    rock=bool(re.search(r'affleurement|\bsur le dessus du roc|\brocher|outcrop|bedrock|in rock|rock surface|rock ledge|ledge of rock|ledge|boulder|in top of rock|on rock|rock knoll|rock point|granite|exposed rock|rock bluff|rock cut',low))
    post=bool(re.search(r'(iron|steel|aluminum|aluminium|galvanized|concrete|brass[- ]capped) (pipe|post|rod|bar|pillar|monument)|pipe with (a )?(brass|aluminum|bronze) cap|standpipe|survey post|\bpillar\b|rod mark|anchor rod|steel rod|copperweld',low))
    struct=sorted(set(x[1] for x in re.findall(r'\b(bolt|tablet|cap|plug|rivet|disc|disk)\b[^.;]{0,70}?\b(wall|abutment|bridge|pier|culvert|dam|foundation|building|step|steps|curb|sidewalk|church|wharf|concrete base|platform|lighthouse)\b',low)))
    m0=re.match(r'^[\w\. ]{0,40}?(?:c\.?n\.?r[\w\.]*|c\.?p\.?r[\w\.]*|w\.p\.and\s?y\.?ry\.?)?,?\s*(?:steel truss |steel |concrete |stone |highway |railway )?(bridge|culvert|dam|wall|church|building|abutment)',re.sub(r'^\s*(?:location\s+)?accessible by [^.]*\.\s*','',low))
    if m0: struct=sorted(set(struct+[m0.group(1)]))
    rail=bool(re.search(r'c\.?n\.?r|c\.?p\.?r|railway|rail lengths|\btrack\b|w\.p\.and',low))
    hwy=bool(re.search(r'highway|hwy|shoulder|right of way|road allowance|ditch|r\.o\.w|along [^.;]{0,70}?\b(?:road|rd)\b|side of [^.;]{0,60}?\b(?:road|rd)\b|roadside|road cut',low))
    pub=[x for x in m['cpcad']] if isinstance(m['cpcad'],list) else []
    o=m['iron'];om=m.get('mag_occ')
    shore=min([v for v in (m['wb_m'],m['wc_m']) if isinstance(v,float)])
    score=0;why=[]
    marine=bool(re.search(r'seaward|high tide|tidal|high water mark|\bwharf|\bsound\b|\binlet\b|harbour|harbor|ocean|strait|\bbight\b|salt water|sea level|marine',low+' '+m.get('water_name','').lower()))
    hasdesc=bool(re.sub(r'\|\s*MONTYPE=\S*|\|','',loc).strip())
    if marine: score-=3;why.append('marine/tidal wording (desc or CGNDB name)')
    if not hasdesc: score-=3;why.append('no monument description available')
    if ok(m['wb_m']): score+=2;why.append('lake/river polygon shore %.0fm'%m['wb_m'])
    elif ok(m['wc_m']): score+=1;why.append('stream line %.0fm'%m['wc_m'])
    if rock: score+=3;why.append('rock/outcrop/boulder monument')
    if post and not struct: score+=1;why.append('post/pipe/rod type')
    if struct: score-=2;why.append('structure: '+','.join(struct))
    if hwy: score-=1;why.append('road/hwy wording')
    if rail: score-=1;why.append('railway setting')
    r2=m.get('road2k_m')
    cls=[(float(a),b) for a,b in re.findall(r'(\d+(?:\.\d+)?) ?m [^.;]{0,40}?(?:of|from) (?:the )?(?:c/l|centre ?line|center ?line) of (?:the )?(?:main |paved |gravel )?(road|highway|hwy|track|railway|street)',low)]
    cls+=[(float(a),'road') for a in re.findall(r'(\d+(?:\.\d+)?) ?m [^.;]{0,30}?du (?:centre|c/l) de la (?:route|rue|chauss)',low)]
    rcl=min([a for a,b in cls if b in ('road','highway','hwy','street')],default=None)
    if re.search(r'walk of 50 to 500 m',low): score+=1;why.append('access: car + 50-500 m walk')
    elif re.search(r'by boat|helicopter|aircraft|float ?plane|by air',low): score-=1;why.append('REMOTE: boat/air access per report')
    if rcl is not None:
        if rcl<=30: score-=1;why.append('roadside: %.0f m from road centre line (report)'%rcl)
        else: score+=1;why.append('%.0f m from road centre line (report)'%rcl)
    elif isinstance(m['road_m'],float) and m['road_m']<25: score-=1;why.append('CanVec road %.0fm'%m['road_m'])
    elif isinstance(r2,float) and r2>=60: score+=1;why.append('CanVec road %.0fm away'%r2)
    elif r2 is None: why.append('REMOTE: no CanVec road within 2km')
    if m['mag_d'] is not None and m['mag_d']<=1000: score+=3;why.append('magnetite occ %dm'%m['mag_d'])
    elif m['iron_d']<=1000: score+=1;why.append('iron occ %dm'%m['iron_d'])
    if pub: score+=1;why.append('CPCAD: '+pub[0][:60])
    st=str(m.get('status') or '').upper()
    if st in ('DESTROYED','BAD','NOT FOUND','LOST') or 'DESTROY' in st: score-=3;why.append('status '+st)
    rows.append(dict(id=m['id'],src=m['src'],status=m.get('status',''),prov=m.get('prov',''),lat=round(m['lat'],6),lon=round(m['lon'],6),shore_m=shore,
        water=m.get('water_name',''),hydro_src='CanVec 1:50k WMS (waterbody_50k=%s m; watercourse_50k=%s m)'%(m['wb_m'],m['wc_m']),
        iron_d_m=m['iron_d'],iron_name=o['name'],iron_src=o['src'],iron_id=o['id'],iron_status=o['status'],magnetite=o['mag'],iron_url=o['url'],
        mag_occ_d_m=m['mag_d'] if m['mag_d'] is not None else '',mag_occ=(om['src']+' '+om['id']+' '+str(om['name'])) if om else '',
        land=json.dumps({'cpcad':m['cpcad']},ensure_ascii=False),desc=loc[:600],site=mtype[:200],owner='',struct=','.join(struct),
        road_m=m['road_m'],road_cl_desc_m=rcl,road2k_m=m.get('road2k_m'),rail=rail,marine=marine,has_desc=hasdesc,rock=rock,post=post,hwy_words=hwy,alt_id=m.get('alt_id',''),score=score,why='; '.join(why),
        report_url=('https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/data-donnees/station/report-rapport.php?id='+m['id']) if m['src'].startswith('NRCan') else m.get('url','')))
rows.sort(key=lambda r:(-r['score'],r['mag_occ_d_m'] if r['mag_occ_d_m']!='' else 9e9,r['shore_m']))
cols=['id','src','status','lat','lon','shore_m','water','hydro_src','iron_d_m','iron_name','iron_src','iron_id','iron_status','magnetite','iron_url','land','desc','site','owner','struct',
      'prov','mag_occ_d_m','mag_occ','road_m','road_cl_desc_m','road2k_m','rail','marine','has_desc','rock','post','hwy_words','alt_id','score','why','report_url']
with open(S+'/nearshore_markers_canada.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
json.dump(rows,open(S+'/data_final.json','w'),ensure_ascii=False)
print('written',len(rows))
