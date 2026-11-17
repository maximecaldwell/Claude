import json,math,sys,os,time,urllib.request,urllib.parse,subprocess
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad'
O=S+'/cachesites_gp/raw/'
sys.path.insert(0,S+'/shoremk_canada/scripts')
from wmsdist import mindist
SITES=[
 ('S1','Dawson YT - Bonanza Creek discovery claim','YT',63.9168,-139.317,'found'),
 ('S2','Cobalt ON - Nipissing Hill Lookout','ON',47.3913,-79.6801,'found'),
 ('S3','Kleanza Creek PP BC','BC',54.59767,-128.3962,'found'),
 ('S4','Dover NL (town label)','NL',48.887,-53.954,'found'),
 ('S5','Britannia BC - Hwy 99 lookout','BC',49.63455,-123.21023,'found'),
 ('S6','Toronto Island ON (centroid)','ON',43.62,-79.378,'found'),
 ('S7','Tetagouche Falls NB - hydro structure','NB',47.617286,-65.825141,'found'),
 ('S8',"Cape d'Or NS - viewing platform",'NS',45.2914,-64.774,'found'),
 ('S9','Chibougamau QC - Parc regional Obalski (community guess, unverified)','QC',49.8908,-74.3622,'found-site-withheld'),
 ('L1','Sudbury - McMahon Point, Whitewater Lake (Azilda)','ON',46.5395,-81.1324,'live'),
 ('L2','Saskatchewan - Dana Recreation Site','SK',52.2517,-105.7550,'live'),
 ('L3','Manitoba - Star Lake / Penniac Bay (Star Lake centre)','MB',49.7552,-95.2426,'live'),
 ('L4',"Val-d'Or - Parc de la Cote-de-Cent-Pieds",'QC',48.09472,-77.77861,'live'),
]
def get(u,data=None,t=120):
    for i in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,data=data,headers={'User-Agent':'desk-check'}),timeout=t);return r.read()
        except Exception as e: err=e;time.sleep(4)
    raise err
OV='https://maps.mail.ru/osm/tools/overpass/api/interpreter'
def overpass(lat,lon,r=2000):
    q=f"""[out:json][timeout:120];
(way(around:{r},{lat},{lon})[natural=water];relation(around:{r},{lat},{lon})[natural=water];way(around:{r},{lat},{lon})[landuse=reservoir];
 way(around:{r},{lat},{lon})[natural=coastline];way(around:{r},{lat},{lon})[waterway~"river|stream"];)->.w;
.w out geom tags;
(way(around:{r},{lat},{lon})[highway~"path|footway|track|bridleway"];relation(around:{r},{lat},{lon})[route~"hiking|foot"];)->.t;
.t out geom tags;
(nwr(around:{r},{lat},{lon})[natural~"wood|tree|grassland|scrub|heath|wetland"];nwr(around:{r},{lat},{lon})[landuse~"forest|meadow|grass"];)->.v;
.v out center tags;
(node(around:{r},{lat},{lon})[man_made=survey_point];node(around:{r},{lat},{lon})[historic~"boundary_stone|milestone|memorial|monument|marker"];node(around:{r},{lat},{lon})[tourism~"viewpoint|information"];node(around:{r},{lat},{lon})[man_made~"obelisk|marker"];)->.m;
.m out tags;"""
    return json.loads(get(OV,urllib.parse.urlencode({'data':q}).encode(),180))
U='https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/process/getStations.php'
def nrcan(lat,lon):
    out=[]
    for m in ('cbn','pvc','hc','hp3d'):
        data=urllib.parse.urlencode(dict(map=m,maxlatitude=lat+0.022,minlatitude=lat-0.022,minlongitude=lon-0.022/math.cos(math.radians(lat)),maxlongitude=lon+0.022/math.cos(math.radians(lat)))).encode()
        try: r=json.loads(get(U,data))
        except Exception as e: out.append({'err':str(e),'net':m});continue
        if r.get('warningHTML'): out.append({'warn':r['warningHTML'][:200],'net':m})
        out+=[s for g in r.get('networks',{}).get('stations',[]) for s in g]
    return out
QB='https://servicescarto.mrnf.gouv.qc.ca/pes/rest/services/Territoire/RESEAU_GEODESIQUE_WMS/MapServer/%d/query'
def qcmk(lat,lon):
    out=[];dl=0.022;dx=dl/math.cos(math.radians(lat))
    for l in (0,2,4,5,6):
        p=dict(geometry=f'{lon-dx},{lat-dl},{lon+dx},{lat+dl}',geometryType='esriGeometryEnvelope',inSR=4326,outSR=4326,spatialRel='esriSpatialRelIntersects',outFields='MATRICULE,DESCR_ETAT_CONSV,ANNEE_INSPECT,FICHE_83_URL',returnGeometry='true',f='json')
        try: r=json.loads(get(QB%l+'?'+urllib.parse.urlencode(p)))
        except Exception as e: out.append({'err':str(e)});continue
        for f in r.get('features',[]):
            x=f['attributes'];x['lat']=f['geometry']['y'];x['lon']=f['geometry']['x'];x['layer']=l;out.append(x)
    return out
CP='https://maps-cartes.ec.gc.ca/arcgis/rest/services/CWS_SCF/CPCAD/MapServer/0/query'
def cpcad(lat,lon,r):
    dl=r/110570;dx=r/(111320*math.cos(math.radians(lat)))
    p=dict(geometry=f'{lon-dx},{lat-dl},{lon+dx},{lat+dl}' if r else f'{lon},{lat}',geometryType='esriGeometryEnvelope' if r else 'esriGeometryPoint',inSR=4326,spatialRel='esriSpatialRelIntersects',outFields='NAME_E,TYPE_E,MGMT_E,OWNER_E',returnGeometry='false',f='json')
    try: d=json.loads(get(CP+'?'+urllib.parse.urlencode(p)))
    except Exception as e: return 'ERR '+str(e)
    return ['/'.join(str(v) for v in f['attributes'].values() if v) for f in d.get('features',[])]
def grid(lat,lon,step=700,R=2000):
    pts=[]
    for i in range(-3,4):
        for j in range(-3,4):
            if math.hypot(i*step,j*step)<=R: pts.append((lat+i*step/110570,lon+j*step/(111320*math.cos(math.radians(lat)))))
    return pts
def qctrees(lat,lon):
    out=[]
    for (a,b) in grid(lat,lon):
        d=0.002;u='https://geoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?'+urllib.parse.urlencode(dict(SERVICE='WMS',VERSION='1.1.1',REQUEST='GetFeatureInfo',LAYERS='ori_pee_close_scale',QUERY_LAYERS='ori_pee_close_scale',STYLES='',SRS='EPSG:4326',BBOX=f'{b-d},{a-d},{b+d},{a+d}',WIDTH=101,HEIGHT=101,X=50,Y=50,INFO_FORMAT='text/plain',FEATURE_COUNT=3))
        try: t=get(u).decode('utf-8','replace')
        except Exception as e: out.append(dict(lat=a,lon=b,err=str(e)));continue
        g=[l.split('=',1)[1].strip().strip("'") for l in t.splitlines() if l.strip().startswith(('gr_ess_desc','gr_ess ','type_couv_desc','co_ter_desc'))]
        out.append(dict(lat=a,lon=b,v=g))
    return out
def bctrees(lat,lon):
    out=[]
    for (a,b) in grid(lat,lon):
        d=0.002;u='https://openmaps.gov.bc.ca/geo/pub/wms?'+urllib.parse.urlencode(dict(SERVICE='WMS',VERSION='1.1.1',REQUEST='GetFeatureInfo',LAYERS='pub:WHSE_FOREST_VEGETATION.VEG_COMP_LYR_R1_POLY',QUERY_LAYERS='pub:WHSE_FOREST_VEGETATION.VEG_COMP_LYR_R1_POLY',STYLES='',SRS='EPSG:4326',BBOX=f'{b-d},{a-d},{b+d},{a+d}',WIDTH=101,HEIGHT=101,X=50,Y=50,INFO_FORMAT='application/json',FEATURE_COUNT=3))
        try: j=json.loads(get(u))
        except Exception as e: out.append(dict(lat=a,lon=b,err=str(e)));continue
        sp=[]
        for f in j.get('features',[]):
            p=f['properties'];sp+=[(p.get(f'SPECIES_CD_{k}'),p.get(f'SPECIES_PCT_{k}')) for k in range(1,7) if p.get(f'SPECIES_CD_{k}')]
            sp.append(('BCLCS',p.get('BCLCS_LEVEL_4')))
        out.append(dict(lat=a,lon=b,v=sp))
    return out
if __name__!="__main__": raise SystemExit
only=sys.argv[1:]
for sid,name,prov,lat,lon,kind in SITES:
    if only and sid not in only: continue
    f=O+sid+'.json'
    R=json.load(open(f)) if os.path.exists(f) else {}
    if 'osm' not in R:
        try: R['osm']=overpass(lat,lon)
        except Exception as e: print(sid,'overpass ERR',e)
    if 'nrcan' not in R: R['nrcan']=nrcan(lat,lon)
    if prov=='QC' and 'qcmk' not in R: R['qcmk']=qcmk(lat,lon)
    if 'cpcad_pt' not in R: R['cpcad_pt']=cpcad(lat,lon,0); R['cpcad_2km']=cpcad(lat,lon,2000)
    if prov=='QC' and 'trees' not in R: R['trees']=qctrees(lat,lon)
    if prov=='BC' and 'trees' not in R: R['trees']=bctrees(lat,lon)
    if 'canvec' not in R:
        R['canvec']=dict(waterbody=mindist('waterbody_50k',lat,lon,half=2000,px=8.0),watercourse=mindist('watercourse_50k',lat,lon,half=2000,px=8.0))
    if 'geonames' not in R:
        try: R['geonames']=json.loads(get('https://geogratis.gc.ca/services/geoname/en/geonames.json?'+urllib.parse.urlencode(dict(lat=lat,lon=lon,radius=2,num=100))))['items']
        except Exception as e: R['geonames']='ERR '+str(e)
    json.dump(R,open(f,'w'))
    print(sid,'osm' in R,len(R.get('nrcan',[])),len(R.get('qcmk',[])),R['cpcad_pt'],R['canvec'],len(R.get('trees',[])),flush=True)
    time.sleep(2)
