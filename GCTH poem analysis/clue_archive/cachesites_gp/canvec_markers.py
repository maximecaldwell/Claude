import json,sys
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad'
sys.path.insert(0,S+'/shoremk_canada/scripts')
from wmsdist import mindist
A=json.load(open('raw/analysis.json'))
jobs=[]
for sid,o in A.items():
    seen=set()
    for m in o['markers']:
        k=(round(m['lat'],5),round(m['lon'],5))
        if k in seen: continue
        seen.add(k);jobs.append((sid,k))
def f(j):
    sid,(la,lo)=j
    return sid,la,lo,mindist('waterbody_50k',la,lo,half=300,px=2.0)
with ThreadPoolExecutor(6) as ex: res=list(ex.map(f,jobs))
json.dump(res,open('raw/marker_canvec.json','w'))
print(len(res))
