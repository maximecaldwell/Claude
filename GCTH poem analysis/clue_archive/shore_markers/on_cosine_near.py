import json, sys, math, urllib.request, urllib.parse, concurrent.futures as cf
from shapely.geometry import shape, Point, Polygon
rows=json.load(open(sys.argv[1]))
U="https://ws.lioservices.lrc.gov.on.ca/arcgis2/rest/services/LIO_OPEN_DATA/LIO_Open01/MapServer/25/query"
def shore(r):
    la,lo=float(r[0]),float(r[1]); d=0.004
    q=dict(geometry=f"{lo-d*1.4},{la-d},{lo+d*1.4},{la+d}",geometryType="esriGeometryEnvelope",inSR=4326,spatialRel="esriSpatialRelIntersects",
           outFields="OFFICIAL_NAME_LABEL,WATERBODY_TYPE",returnGeometry="true",outSR=4326,f="json")
    for _ in range(3):
        try:
            j=json.load(urllib.request.urlopen(U+"?"+urllib.parse.urlencode(q),timeout=60)); break
        except Exception as e: j={"features":[]}
    k=111320*math.cos(math.radians(la)); best=None
    for f in j.get("features",[]):
        for ring in f["geometry"].get("rings",[]):
            pts=[((x-lo)*k,(y-la)*111320) for x,y in ring]
            from shapely.geometry import LineString
            dd=LineString(pts).distance(Point(0,0))
            if best is None or dd<best[0]: best=(dd,f["attributes"].get("OFFICIAL_NAME_LABEL") or "")
    return r+[round(best[0],1) if best else None, best[1] if best else ""]
with cf.ThreadPoolExecutor(8) as ex: out=list(ex.map(shore,rows))
json.dump(out,open(sys.argv[2],"w"))
near=[o for o in out if o[8] is not None and o[8]<=40]
print(len(out),"with water within 40m:",len(near))
for o in sorted(near,key=lambda o:o[8]): print(o)
