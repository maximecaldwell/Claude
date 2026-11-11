import math,io,subprocess,time,urllib.parse
from PIL import Image
W='https://maps.geogratis.gc.ca/wms/canvec_en'
def render(layer,lat,lon,half=300,px=2.0):
    n=int(2*half/px)
    dlat=half/110570; dlon=half/(111320*math.cos(math.radians(lat)))
    p=dict(SERVICE='WMS',VERSION='1.1.1',REQUEST='GetMap',LAYERS=layer,STYLES='',SRS='EPSG:4326',
           BBOX=f'{lon-dlon},{lat-dlat},{lon+dlon},{lat+dlat}',WIDTH=n,HEIGHT=n,FORMAT='image/png',TRANSPARENT='TRUE')
    for i in range(4):
        r=subprocess.run(['curl','-sS','-m','90',W+'?'+urllib.parse.urlencode(p)],capture_output=True)
        try:
            im=Image.open(io.BytesIO(r.stdout)).convert('RGBA');return im,n,px
        except Exception: time.sleep(3)
    return None,n,px
def mindist(layer,lat,lon,half=300,px=2.0,thr=128):
    im,n,px=render(layer,lat,lon,half,px)
    if im is None: return 'ERR'
    a=im.getchannel('A').load();c=(n-1)/2;best=None
    for y in range(n):
        for x in range(n):
            if a[x,y]>=thr:
                d=math.hypot(x-c,y-c)*px
                if best is None or d<best: best=d
    return None if best is None else round(best,1)
