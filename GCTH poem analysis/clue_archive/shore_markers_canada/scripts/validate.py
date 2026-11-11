import csv,sys;sys.path.insert(0,'.')
from wmsdist import mindist
rows=list(csv.DictReader(open('/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk/nearshore_markers.csv')))
for r in rows[2:14]:
    lat,lon=float(r['lat']),float(r['lon'])
    print(r['id'],r['hydro_src'],r['shore_m'],r['water'],'| canvec wb',mindist('waterbody_50k',lat,lon),'wc',mindist('watercourse_50k',lat,lon))
