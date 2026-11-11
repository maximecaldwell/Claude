import osmium,json,sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/scripts')
HIST={'memorial','monument','marker','wayside_shrine','mine','mine_shaft','heritage','boundary_stone','plaque','cairn','mine_adit','adit'}
def want(t):
    if t.get('historic') in HIST: return True
    if t.get('memorial') in ('plaque','cairn','stone','blue_plaque'): return True
    if t.get('man_made') in ('cairn','mineshaft','adit'): return True
    if t.get('tourism')=='information' and t.get('information') in ('board','plaque'): return True
    return False
out=[]
fp=osmium.FileProcessor(sys.argv[1],osmium.osm.NODE|osmium.osm.WAY).with_locations('flex_mem').with_filter(osmium.filter.KeyFilter('historic','memorial','man_made','information'))
for o in fp:
    t=dict(o.tags)
    if not want(t): continue
    if o.is_node(): out.append(dict(osm='n%d'%o.id,lat=o.location.lat,lon=o.location.lon,tags=t))
    else:
        pts=[(x.lat,x.lon) for x in o.nodes if x.location.valid()]
        if pts: out.append(dict(osm='w%d'%o.id,lat=sum(p[0] for p in pts)/len(pts),lon=sum(p[1] for p in pts)/len(pts),tags=t))
json.dump(out,open(sys.argv[2],'w'))
print(sys.argv[1],len(out),flush=True)
