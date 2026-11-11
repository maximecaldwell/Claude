import json,urllib.request,urllib.parse,math,os,sys,time
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada'
occ=json.load(open(S+'/iron_canada.json'))
T=0.25
cells=set()
for o in occ:
    for dy in (-0.03,0,0.03):
        for dx in (-0.045,0,0.045):
            cells.add((math.floor((o['lat']+dy)/T),math.floor((o['lon']+dx)/T)))
print('cells',len(cells),flush=True)
U='https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/process/getStations.php'
def nrcan(m,a,b,c,d,depth=0):
    data=urllib.parse.urlencode(dict(map=m,maxlatitude=b,minlatitude=a,minlongitude=c,maxlongitude=d)).encode()
    for i in range(3):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(U,data=data),timeout=120));break
        except Exception as e:
            time.sleep(3);r={'err':str(e)}
    if 'err' in r: return [('ERR',m,a,c)]
    if r.get('warningHTML') and 'Too many' in r['warningHTML'] and depth<4:
        ma=(a+b)/2;mc=(c+d)/2;out=[]
        for (aa,bb) in ((a,ma),(ma,b)):
            for (cc,dd) in ((c,mc),(mc,d)):
                out+=nrcan(m,aa,bb,cc,dd,depth+1)
        return out
    return [s for g in r.get('networks',{}).get('stations',[]) for s in g]
def job(cell):
    i,j=cell;a=i*T;b=a+T;c=j*T;d=c+T
    res={'nrcan':[]}
    for m in ('cbn','pvc','hc','hp3d'):
        res['nrcan']+=nrcan(m,a,b,c,d)
    return cell,res
allr=json.load(open(S+'/data_markers_raw.json')) if os.path.exists(S+'/data_markers_raw.json') else {}
cells=[c for c in cells if '%d_%d'%c not in allr]
print('new cells',len(cells),flush=True)
with ThreadPoolExecutor(8) as ex:
    for n,(cell,res) in enumerate(ex.map(job,sorted(cells))):
        allr['%d_%d'%cell]=res
        if n%200==0: print(n,flush=True)
json.dump(allr,open(S+'/data_markers_raw.json','w'))
print('done',sum(len(r['nrcan']) for r in allr.values()),'errs',sum(1 for r in allr.values() for s in r['nrcan'] if isinstance(s,(list,tuple))))
