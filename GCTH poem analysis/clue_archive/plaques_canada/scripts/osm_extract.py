import osmium,json,sys
HIST={'memorial','monument','marker','wayside_shrine','mine','mine_shaft','heritage','boundary_stone','memorial;plaque','plaque','cairn','mine_adit','adit'}
def want(t):
    h=t.get('historic')
    if h in HIST: return True
    if t.get('memorial') in ('plaque','cairn','stone','blue_plaque'): return True
    if t.get('man_made') in ('cairn','mineshaft','adit'): return True
    if t.get('tourism')=='information' and t.get('information') in ('board','plaque'): return True
    return False
out=[]
class H(osmium.SimpleHandler):
    def node(self,n):
        t=dict(n.tags)
        if t and want(t): out.append(dict(osm='n%d'%n.id,lat=n.location.lat,lon=n.location.lon,tags=t))
    def way(self,w):
        t=dict(w.tags)
        if t and want(t):
            pts=[(x.lat,x.lon) for x in w.nodes if x.location.valid()]
            if pts: out.append(dict(osm='w%d'%w.id,lat=sum(p[0] for p in pts)/len(pts),lon=sum(p[1] for p in pts)/len(pts),tags=t))
H().apply_file(sys.argv[1],locations=True,idx='flex_mem')
json.dump(out,open(sys.argv[2],'w'))
print(sys.argv[1],len(out))
