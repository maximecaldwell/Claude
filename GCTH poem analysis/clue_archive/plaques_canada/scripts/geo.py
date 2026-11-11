import json,math,collections
from shapely.geometry import shape,Point
from shapely.strtree import STRtree
R='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/raw/'
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/'
_ne=[f for f in json.load(open(R+'ne_admin1.geojson'))['features'] if f['properties'].get('adm0_a3')=='CAN']
_geoms=[shape(f['geometry']) for f in _ne]; _codes=[(f['properties'].get('postal') or f['properties'].get('iso_3166_2','')[-2:]) for f in _ne]
_tree=STRtree(_geoms)
def prov(lat,lon,buf=0.05):
    p=Point(lon,lat)
    for i in _tree.query(p.buffer(buf)):
        if _geoms[i].distance(p)<=buf: return _codes[i]
    return None
def dist(lat1,lon1,lat2,lon2): return math.hypot((lon2-lon1)*111320*math.cos(math.radians(lat1)),(lat2-lat1)*110570)
occ=[]
for o in json.load(open(S+'shoremk/data/iron.json')):
    o=dict(o);o['prov']='QC' if o['src'].startswith('QC') else 'ON';occ.append(o)
occ+=json.load(open(S+'shoremk_canada/iron_canada.json'))
G=collections.defaultdict(list)
for o in occ: G[(int(math.floor(o['lat']*50)),int(math.floor(o['lon']*50)))].append(o)
def nearest(lat,lon,mag=False,r=2):
    best=(1e9,None);i,j=int(math.floor(lat*50)),int(math.floor(lon*50))
    for a in range(i-r,i+r+1):
        for b in range(j-r*2,j+r*2+1):
            for o in G[(a,b)]:
                if mag and not o['mag']: continue
                d=dist(lat,lon,o['lat'],o['lon'])
                if d<best[0]: best=(d,o)
    return best
import re
KW=re.compile(r'\b(iron|magnetite|magnetic|lodestone|compass|ore|ores|mine|mines|mining|miner|miners|mineshaft|furnace|forge|forges|fer|minerai|mine de fer|aimant|boussole|magnétite|ferrifère|haut[- ]fourneau)\b',re.I)
