import json,sys,os
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada/scripts')
from wmsdist import mindist
from agq import getj
from concurrent.futures import ThreadPoolExecutor
P='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/'
K=json.load(open(P+'data_keep.json'))
C=P+'data_water_cache.json'
cache=json.load(open(C)) if os.path.exists(C) else {}
def key(m): return '%.6f,%.6f'%(m['lat'],m['lon'])
def w(m):
    k=key(m);c=cache.get(k,{})
    for lay,f in (('waterbody_50k','wb_m'),('watercourse_50k','wc_m'),('shoreline_50k','coast_m')):
        if f not in c or c[f]=='ERR': c[f]=mindist(lay,m['lat'],m['lon'])
    return k,c
with ThreadPoolExecutor(8) as ex:
    for n,(k,c) in enumerate(ex.map(w,K)):
        cache[k]=c
        if n%200==0: print(n,flush=True);json.dump(cache,open(C,'w'))
json.dump(cache,open(C,'w'))
def num(v): return v if isinstance(v,(int,float)) else None
sel=[]
for m in K:
    c=cache[key(m)];m.update(c)
    ds=[num(c[f]) for f in ('wb_m','wc_m','coast_m') if num(c[f]) is not None]
    m['water_m']=min(ds) if ds else None
    if m['water_m'] is not None and m['water_m']<=60: sel.append(m)
print('errs',sum(1 for m in K if 'ERR' in (m['wb_m'],m['wc_m'],m['coast_m'])),'<=60m',len(sel),flush=True)
CP='https://maps-cartes.ec.gc.ca/arcgis/rest/services/CWS_SCF/CPCAD/MapServer/0/query'
def e(m):
    lat,lon=m['lat'],m['lon']
    m['road_m']=mindist('road_segment_50k',lat,lon,half=300,px=2.0)
    m['road2k_m']=m['road_m'] if isinstance(m['road_m'],float) else mindist('road_segment_50k',lat,lon,half=2000,px=10.0)
    d=getj(CP,dict(geometry=f'{lon},{lat}',geometryType='esriGeometryPoint',inSR=4326,spatialRel='esriSpatialRelIntersects',outFields='NAME_E,TYPE_E,MGMT_E',returnGeometry='false',f='json'))
    m['cpcad']='ERR' if 'error' in d else ['/'.join(str(v) for v in f['attributes'].values() if v) for f in d.get('features',[])]
    g=getj('https://geogratis.gc.ca/services/geoname/en/geonames.json',dict(lat=lat,lon=lon,radius=2,concise='LAKE,RIV,BAY,SEA,CHAN,RAP',num=1))
    try: it=g['items'][0];m['water_name']=f"{it['name']} ({it['concise']['code']})"
    except Exception: m['water_name']=''
    return m
with ThreadPoolExecutor(8) as ex: sel=list(ex.map(e,sel))
json.dump(dict(all=K,sel=sel),open(P+'data_enriched.json','w'))
print('done')
