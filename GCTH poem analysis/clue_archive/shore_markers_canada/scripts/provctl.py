import sys,json;sys.path.insert(0,'.');from agq import agq,getj
D='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada/dl/'
occ=json.load(open(D+'../iron_canada.json'))
NS='https://nsgiwa2.novascotia.ca/arcgis/rest/services/LOC/LOC_NSCRS_Stations_WM84/MapServer/'
ns=[]
for l in (0,1,4):
    try:
        fs=agq(NS+str(l),'1=1','STATIONNUM,STATIONNAM,DESCRIPT,MONTYPE,CURRSTATUS,STATUSDATE,CONSTDATE,COMMENTS',geom=True,page=1000)
        for f in fs: f['layer']=l
        ns+=fs;print('NS',l,len(fs),flush=True)
    except Exception as e: print('NS',l,'ERR',e)
json.dump(ns,open(D+'ns_ctl.json','w'))
AB='https://services.arcgis.com/xYjDUN35YwdCEcMm/ArcGIS/rest/services/ASCM/FeatureServer/0'
ab={}
for o in occ:
    if o['prov']!='AB': continue
    try:
        fs=agq(AB,'1=1','ASCM_NO,TABLET_MARKING,MARKER_CONDITION,HORIZONTAL_ORDER,METHOD',geom=True,page=1000,
           extra=dict(geometry=f"{o['lon']},{o['lat']}",geometryType='esriGeometryPoint',inSR=4326,distance=3200,units='esriSRUnit_Meter',spatialRel='esriSpatialRelIntersects'))
        for f in fs: ab[f['attributes']['ASCM_NO']]=f
    except Exception as e: print('AB ERR',e)
print('AB',len(ab));json.dump(list(ab.values()),open(D+'ab_ctl.json','w'))
