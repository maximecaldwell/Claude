import json,subprocess,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/scripts')
import geo
from concurrent.futures import ThreadPoolExecutor
d=json.load(open(geo.R+'rtp_geo.json'))['features']
ca=[]
for f in d:
    lon,lat=f['geometry']['coordinates']
    if lat>41.6 and -141<lon<-52.5:
        p=geo.prov(lat,lon,0.01)
        if p: ca.append((f['properties']['id'],p))
print('canada',len(ca),flush=True)
def get(x):
    r=subprocess.run(['curl','-sS','-m','40','-A','gcth-desk-research/1.0','https://readtheplaque.com/api/plaques/%d'%x[0]],capture_output=True).stdout
    try: j=json.loads(r);j['prov']=x[1];return j
    except Exception: return dict(id=x[0],err=r[:200].decode('latin1'),prov=x[1])
with ThreadPoolExecutor(3) as ex: out=list(ex.map(get,ca))
json.dump(out,open(geo.R+'rtp_canada.json','w'))
print('done',len(out),sum(1 for o in out if 'err' in o))
