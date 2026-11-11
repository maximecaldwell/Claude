import json,csv,re,collections,math
P='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/'
D=json.load(open(P+'data_enriched.json'));sel=D['sel']
def n(v): return v if isinstance(v,(int,float)) else None
STRONG={'iron','magnetite','magnetic','lodestone','compass','fer','minerai','aimant','boussole','magnétite','ferrifère','haut fourneau','haut-fourneau','mine de fer'}
rows=[]
for m in sel:
    sc=0;why=[]
    wb,wc,co=n(m['wb_m']),n(m['wc_m']),n(m['coast_m'])
    inland=[x for x in (wb,wc) if x is not None]
    dw=min(inland) if inland else None
    if dw is not None and dw<=60:
        sc+=4 if dw<=15 else 3 if dw<=30 else 2
        why.append('lake/river %s m (%s)'%(round(dw),'polygon shore' if wb is not None and wb==dw else 'stream line'))
    elif co is not None:
        sc+=1;why.append('marine coastline %s m'%round(co))
    marine=(co is not None and (dw is None or co<dw))
    # iron
    if m['near_iron']:
        d=m['iron_d_m'];sc+=3 if d<=1000 else 2;why.append('iron occ %d m'%d)
        if re.search(r'iron|magnet',m['iron_prim'] or '',re.I): sc+=1;why.append('Fe is primary commodity')
    md=m.get('mag_d_m')
    if md is not None and md<=1000: sc+=2;why.append('magnetite occ %d m'%md)
    elif md is not None and md<=1500: sc+=1;why.append('magnetite occ %d m'%md)
    # type
    t=m['type'];kind='other'
    if re.search(r'memorial|monument|marker|plaque|cairn|wayside|Stop of Interest|Heritage Trust|Read the Plaque|Historical Society',t,re.I) and 'boundary_stone' not in t:
        kind='marker';sc+=2;why.append('plaque/cairn/memorial type')
    elif 'information=board' in t: kind='board';sc+=1;why.append('interpretive board')
    elif 'boundary_stone' in t: kind='boundary monument'; why.append('international boundary monument (survey-type)')
    elif re.search(r'mineshaft|adit|historic=mine',t): kind='mine feature'; why.append('mine shaft/adit/mine site')
    elif m['src'] in ('CRHP','QC-RPCQ'): kind='heritage place record'
    if 'cairn' in t.lower() or re.search(r'\bcairn\b',m['name'],re.I): sc+=1;why.append('cairn')
    # text
    import sys;sys.path.insert(0,P+'scripts');import geo
    base=m['name']+' '+(m['text'] or '')
    if m['src']=='OSM':
        t=json.loads(m['osm_tags']);base=' '.join(str(t.get(k,'')) for k in ('name','name:en','name:fr','inscription','inscription:en','inscription:fr','description','description:en','description:fr','memorial:text','subject','old_name','resource','mineral'))
    base=re.sub(r'chemins? de fer|fer à cheval|fer forgé','',base,flags=re.I)
    base=re.sub(r'<[^>]+>',' ',base)
    kws=set(x.lower() for x in geo.KW.findall(base))
    if '(mine feature)' in m['kw']: kws.add('(mine feature)')
    m['kw']=';'.join(sorted(kws))
    if kws & STRONG: sc+=3;why.append('text mentions '+','.join(sorted(kws&STRONG)))
    elif kws: sc+=1;why.append('text mentions '+','.join(sorted(kws)))
    # land / access
    cp=m.get('cpcad') or []
    if cp and cp!='ERR': sc+=2;why.append('in protected area')
    r=n(m.get('road_m'));r2=n(m.get('road2k_m'))
    if r is not None and r<=25: sc-=1;why.append('roadside (%d m to road)'%r)
    elif r is not None: sc+=1;why.append('%d m from road (walk-in)'%r)
    elif r2 is not None: why.append('nearest road %d m'%r2)
    else: sc-=1;why.append('no road within 2 km')
    if m['src']=='BC-SOI': sc-=1;why.append('highway sign')
    txt=m['text'] or ''
    rows.append(dict(score=sc,src=m['src'],id=m['id'],name=m['name'],kind=kind,type=t,prov=m['prov'],lat=round(m['lat'],6),lon=round(m['lon'],6),
        water_m=m['water_m'],waterbody_m=wb,watercourse_m=wc,coast_m=co,marine=marine,water_name=m.get('water_name',''),
        iron_d_m=m['iron_d_m'] if m['iron_d_m']<1e8 else None,iron_name=m['iron_name'],iron_id=m['iron_id'],iron_src=m['iron_src'],iron_prim=m['iron_prim'],iron_url=m['iron_url'],
        mag_d_m=md,mag_name=m.get('mag_name',''),mag_url=m.get('mag_url',''),kw=m['kw'],
        land='; '.join(cp) if isinstance(cp,list) else cp,road_m=r,road2k_m=r2,text=txt[:1500],url=m['url'],why='; '.join(why)))
rows.sort(key=lambda x:(-x['score'],x['water_m'] or 999))
grp=[]
for x in rows:
    g=None
    for i,(la,lo) in enumerate(grp):
        if math.hypot((x['lon']-lo)*111320*math.cos(math.radians(la)),(x['lat']-la)*110570)<60: g=i;break
    if g is None: grp.append((x['lat'],x['lon']));g=len(grp)-1
    x['site_group']=g+1
with open(P+'candidates.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
# also keyword/near list without water filter
allk=D['all']
with open(P+'all_kept_unfiltered.csv','w',newline='') as f:
    ks=['src','id','name','type','prov','lat','lon','near_iron','iron_d_m','iron_name','mag_d_m','mag_name','kw','wb_m','wc_m','coast_m','water_m','url']
    w=csv.DictWriter(f,fieldnames=ks,extrasaction='ignore');w.writeheader();w.writerows(allk)
print('candidates',len(rows))
print(collections.Counter(r['src'] for r in rows));print(collections.Counter(r['prov'] for r in rows))
print('near-iron cands',sum(1 for r in rows if (r['iron_d_m'] or 9e9)<=1500))
for r in rows[:0]: print(r['score'],r['src'],r['prov'],r['name'][:40],'|',r['kind'],'|w',r['water_m'],'|fe',r['iron_d_m'],r['iron_name'][:20],'|mag',r['mag_d_m'],'|',r['land'][:30],'|',r['why'][:150])
