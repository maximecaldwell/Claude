import json,math,sys,collections,os
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada/scripts')
from concurrent.futures import ThreadPoolExecutor
from wmsdist import mindist
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada'
occ=json.load(open(S+'/iron_canada.json'))
raw=json.load(open(S+'/data_markers_raw.json'))
def dist(lat1,lon1,lat2,lon2): return math.hypot((lon2-lon1)*111320*math.cos(math.radians(lat1)),(lat2-lat1)*110570)
G=collections.defaultdict(list)
for o in occ: G[(int(o['lat']*20),int(o['lon']*20))].append(o)
def nearest(lat,lon):
    best=(1e9,None);i,j=int(lat*20),int(lon*20)
    for a in range(i-2,i+3):
        for b in range(j-2,j+3):
            for o in G[(a,b)]:
                d=dist(lat,lon,o['lat'],o['lon'])
                if d<best[0]: best=(d,o)
    return best
def nearest_mag(lat,lon):
    best=(1e9,None);i,j=int(lat*20),int(lon*20)
    for a in range(i-2,i+3):
        for b in range(j-2,j+3):
            for o in G[(a,b)]:
                if not o['mag']: continue
                d=dist(lat,lon,o['lat'],o['lon'])
                if d<best[0]: best=(d,o)
    return best
mk={}
for cell,r in raw.items():
    for s in r['nrcan']:
        if isinstance(s,list): continue
        mk[s['id']]=dict(src='NRCan-'+s['net'],id=s['id'],name=s.get('n'),prov=s.get('p'),status=s.get('status'),lat=s['lat'],lon=s['lon'])

D=S+'/dl/'
nr=list(mk.values())
NG=collections.defaultdict(list)
for m in nr: NG[(int(m['lat']*200),int(m['lon']*200))].append(m)
def dup(lat,lon):
    i,j=int(lat*200),int(lon*200)
    for a in (i-1,i,i+1):
        for b in (j-1,j,j+1):
            for m in NG[(a,b)]:
                if dist(lat,lon,m['lat'],m['lon'])<10: return m['id']
    return None
nadd=collections.Counter()
for f in json.load(open(D+'bc_gcm_all.json')):
    p=f['properties'];lon,lat=f['geometry']['coordinates'][:2]
    d=dup(lat,lon)
    if d: mk[d]['alt_id']='BC-GCM %s (%s)'%(p['GCM_NUMBER'],(p['TABLET_MARKING'] or '').strip()); continue
    k='BCGCM:%s'%p['GCM_NUMBER'];nadd['BC']+=1
    mk[k]=dict(src='BC-GCM-'+(p['MARKER_TAG'] or 'NA'),id='BCGCM-%s'%p['GCM_NUMBER'],name=(p['TABLET_MARKING'] or '').strip(),prov='BC',status='',lat=lat,lon=lon,url=p['GEONETBC_GCM_QUERY_URL'])
for f in json.load(open(D+'ns_ctl.json')):
    a=f['attributes'];g=f.get('geometry')
    if not g: continue
    lat,lon=g['y'],g['x'];d=dup(lat,lon)
    if d: mk[d]['alt_id']='NSCRS %s'%a['STATIONNUM']; continue
    k='NS:%s'%a['STATIONNUM'];nadd['NS']+=1
    mk[k]=dict(src='NSCRS-L%d'%f['layer'],id='NS-%s'%a['STATIONNUM'],name=a['STATIONNAM'] or '',prov='NS',status=a['CURRSTATUS'] or '',lat=lat,lon=lon,
               desc_prov='%s | MONTYPE=%s | %s'%(a['DESCRIPT'] or '',a['MONTYPE'] or '',a['COMMENTS'] or ''))
for f in json.load(open(D+'ab_ctl.json')):
    a=f['attributes'];g=f['geometry'];lat,lon=g['y'],g['x']
    d=dup(lat,lon)
    if d: mk[d]['alt_id']='ASCM %s'%a['ASCM_NO']; continue
    nadd['AB']+=1
    mk['AB:%s'%a['ASCM_NO']]=dict(src='AB-ASCM',id='ASCM-%s'%a['ASCM_NO'],name=a['TABLET_MARKING'] or '',prov='AB',status=a['MARKER_CONDITION'] or '',lat=lat,lon=lon)
print('provincial added',nadd,flush=True)
print('markers total',len(mk))
cand=[]
for m in mk.values():
    d,o=nearest(m['lat'],m['lon'])
    if d<=3000:
        m['iron_d']=round(d);m['iron']=o
        dm,om=nearest_mag(m['lat'],m['lon'])
        m['mag_d']=round(dm) if om else None;m['mag_occ']=om
        cand.append(m)
print('within 3km',len(cand),flush=True)
json.dump(cand,open(S+'/data_cand3km.json','w'))
def job(m):
    m['wb_m']=mindist('waterbody_50k',m['lat'],m['lon'])
    m['wc_m']=mindist('watercourse_50k',m['lat'],m['lon'])
    return m
prev={m['id']:m for m in json.load(open(S+'/data_cand_shore.json'))} if os.path.exists(S+'/data_cand_shore.json') else {}
done=[];todo=[]
for m in cand:
    p=prev.get(m['id'])
    if p and p.get('wb_m')!='ERR': m['wb_m']=p['wb_m'];m['wc_m']=p['wc_m'];done.append(m)
    else: todo.append(m)
print('todo',len(todo),flush=True)
cand=todo
with ThreadPoolExecutor(8) as ex:
    out=list(done);
    for n,m in enumerate(ex.map(job,cand)):
        out.append(m)
        if n%100==0: print(n,flush=True)
json.dump(out,open(S+'/data_cand_shore.json','w'))
ok=[m for m in out if isinstance(m['wb_m'],float) and m['wb_m']<=40]
print('wb<=40',len(ok),'wc<=40',sum(1 for m in out if isinstance(m['wc_m'],float) and m['wc_m']<=40),'errs',sum(1 for m in out if m['wb_m']=='ERR'))
