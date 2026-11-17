import json,math,csv,sys,collections
from shapely.geometry import Point,Polygon,LineString
from shapely.ops import transform
S='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad'
sys.path.insert(0,S+'/cachesites_gp'); sys.argv=[sys.argv[0]]
import importlib.util
sp=importlib.util.spec_from_file_location("f",S+"/cachesites_gp/fetch.py");F=importlib.util.module_from_spec(sp)
try: sp.loader.exec_module(F)
except SystemExit: pass
SITES=F.SITES
def hav(a,b,c,d):
    R=6371000;p1,p2=math.radians(a),math.radians(c);dp=p2-p1;dl=math.radians(d-b)
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2;return 2*R*math.asin(math.sqrt(h))
iron=json.load(open(S+'/shoremk/data/iron.json'))+json.load(open(S+'/shoremk_canada/iron_canada.json'))
bcg=json.load(open(S+'/shoremk_canada/dl/bc_gcm_all.json'))
nsc=json.load(open(S+'/shoremk_canada/dl/ns_ctl.json'))
cands=[]
for fn,src in [('/boundary_monuments/candidates.csv','boundary_monuments'),('/plaques_canada/candidates.csv','plaques_canada'),('/shoremk/nearshore_markers.csv','shoremk'),('/shoremk_canada/nearshore_markers_canada.csv','shoremk_canada')]:
    for r in csv.DictReader(open(S+fn)): cands.append((src,r.get('id'),r.get('name',r.get('desc','')[:60]),float(r['lat']),float(r['lon'])))
OUT={}
for sid,name,prov,lat,lon,kind in SITES:
    R=json.load(open(S+'/cachesites_gp/raw/'+sid+'.json'))
    k=math.cos(math.radians(lat))
    proj=lambda x,y: ((x-lon)*111320*k,(y-lat)*110570)
    def P(la,lo): return Point(proj(lo,la))
    o={'sid':sid,'name':name,'prov':prov,'lat':lat,'lon':lon,'kind':kind}
    els=(R.get('osm') or {}).get('elements') or []
    o['osm_ok']=bool(R.get('osm'))
    waters=[];lines=[];paths=[];veg=[];mk_osm=[]
    for e in els:
        t=e.get('tags',{})
        if e['type']=='way' and 'geometry' in e:
            pts=[proj(g['lon'],g['lat']) for g in e['geometry']]
            if t.get('natural')=='water' or t.get('landuse')=='reservoir':
                if len(pts)>=4 and pts[0]==pts[-1]: waters.append((Polygon(pts).buffer(0),t,e['id']))
                else: lines.append((LineString(pts),t,e['id']))
            elif t.get('natural')=='coastline': lines.append((LineString(pts),{'natural':'coastline'},e['id']))
            elif 'waterway' in t: lines.append((LineString(pts),t,e['id']))
            elif 'highway' in t: paths.append((LineString(pts),t))
        elif e['type']=='relation' and t.get('natural')=='water':
            for m in e.get('members',[]):
                if m.get('role')=='outer' and 'geometry' in m:
                    lines.append((LineString([proj(g['lon'],g['lat']) for g in m['geometry']]),t,e['id']))
        elif e['type']=='relation' and 'route' in t:
            paths.append((None,t))
        if e['type'] in('node','way','relation') and (t.get('natural') in('wood','tree','grassland','scrub','heath','wetland') or t.get('landuse') in('forest','meadow','grass')):
            c=e.get('center') or {'lat':e.get('lat'),'lon':e.get('lon')}
            if c.get('lat'): veg.append((round(hav(lat,lon,c['lat'],c['lon'])),{x:t[x] for x in t if x in('natural','landuse','leaf_type','leaf_cycle','species','genus','species:en','wetland','name','taxon')}))
        if e['type']=='node' and 'lat' in e and (t.get('man_made') in('survey_point','obelisk','marker') or t.get('historic') or t.get('tourism')):
            mk_osm.append((round(hav(lat,lon,e['lat'],e['lon'])),e['lat'],e['lon'],{x:t[x] for x in t if x in('man_made','historic','tourism','name','information','memorial','ref','inscription','material','survey_point:structure')}))
    site=Point(0,0)
    lakes=[]
    for g,t,i in waters+[(l,t,i) for l,t,i in lines if t.get('natural')=='water']:
        wt=t.get('water','(none)')
        lakes.append((round(g.distance(site)) if g.geom_type!='LineString' else round(g.distance(site)),wt,t.get('name',''),i,round(g.area/1e4,2) if g.geom_type=='Polygon' else None))
    lakes.sort()
    o['osm_water']=lakes[:15]
    calm=[x for x in lakes if x[1] in('lake','pond','reservoir','lagoon','oxbow','(none)','basin')]
    o['osm_calm_nearest']=calm[:5]
    o['coast_m']=min([round(l.distance(site)) for l,t,i in lines if t.get('natural')=='coastline'] or [None]) if any(t.get('natural')=='coastline' for l,t,i in lines) else None
    o['river_m']=min([round(l.distance(site)) for l,t,i in lines if 'waterway' in t] or [None])
    o['canvec']=R['canvec']
    gn=R.get('geonames') if isinstance(R.get('geonames'),list) else []
    o['cgndb_water']=sorted([(round(hav(lat,lon,g['latitude'],g['longitude'])),g['name'],g['concise']['code']) for g in gn if g['concise']['code'] in('LAKE','RIV','BAY','SEA','CHAN','RAP','FALL','LAKEP' ) or 'Lake' in g['name'] or 'Lac' in g['name'] or 'Pond' in g['name']])[:12]
    o['cgndb_all']=sorted([(round(hav(lat,lon,g['latitude'],g['longitude'])),g['name'],g['concise']['code']) for g in gn])[:40]
    # paths
    pd=[(round(l.distance(site)),t.get('highway'),t.get('name','')) for l,t in paths if l is not None]
    pd.sort();o['paths_n']=len(pd);o['path_nearest']=pd[:3];o['paths_named']=sorted(set(x[2] for x in pd if x[2]))[:12]
    o['routes']=sorted(set(t.get('name','?') for l,t in paths if l is None))
    o['veg']=sorted(veg,key=lambda x:x[0])
    o['grass_m']=min([d for d,t in veg if t.get('natural') in('grassland','heath','scrub') or t.get('landuse') in('meadow','grass')] or [None])
    # trees
    tr=R.get('trees') or []
    o['trees_raw']=tr
    # iron
    ir=sorted(((round(hav(lat,lon,x['lat'],x['lon'])),x['src'],x['id'],x['name'],x.get('mag'),x.get('prim','')[:60]) for x in iron),key=lambda z:z[0])
    o['iron_nearest']=ir[:3];o['iron_2km']=[x for x in ir if x[0]<=2000]
    o['mag_nearest']=[x for x in ir if x[4]][:1]
    # markers
    mk=[]
    for s in R.get('nrcan',[]):
        if 'lat' in s: mk.append(('NRCan-'+s.get('net',''),s['id'],s.get('status',''),s['lat'],s['lon']))
    for s in R.get('qcmk',[]):
        if 'lat' in s: mk.append(('QC-RG-L%s'%s['layer'],str(s.get('MATRICULE')),str(s.get('DESCR_ETAT_CONSV')),s['lat'],s['lon']))
    if prov=='BC':
        for f in bcg:
            lo,la=f['geometry']['coordinates'][:2]
            if abs(la-lat)<0.03 and abs(lo-lon)<0.05: mk.append(('BC-GCM-'+str(f['properties'].get('MARKER_TAG')),str(f['properties']['GCM_NUMBER']),(f['properties'].get('TABLET_MARKING') or '').strip(),la,lo))
    if prov=='NS':
        for f in nsc:
            g=f.get('geometry')
            if g and abs(g['y']-lat)<0.03 and abs(g['x']-lon)<0.05: a=f['attributes'];mk.append(('NSCRS',str(a['STATIONNUM']),'%s %s'%(a.get('MONTYPE') or '',a.get('CURRSTATUS') or ''),g['y'],g['x']))
    for d,la,lo,t in mk_osm:
        if t.get('man_made') in('survey_point','marker','obelisk') or t.get('historic') in('boundary_stone','milestone','marker'): mk.append(('OSM',str(t.get('ref',t.get('name',''))),json.dumps(t,ensure_ascii=False)[:120],la,lo))
    for src,i,nm,la,lo in cands:
        if abs(la-lat)<0.03 and abs(lo-lon)<0.05: mk.append(('cand:'+src,str(i),str(nm)[:80],la,lo))
    allw=[g for g,t,i in waters]+[l for l,t,i in lines if t.get('natural') in('water','coastline') or t.get('waterway')=='river']
    mko=[]
    seen=set()
    for src,i,st,la,lo in mk:
        key=(round(la,4),round(lo,4))
        d=hav(lat,lon,la,lo)
        if d>2000 or (key in seen and src.startswith('cand')): continue
        seen.add(key)
        p=P(la,lo);wd=min([g.distance(p) for g in allw] or [None]) if allw else None
        calmd=min([g.distance(p) for g,t,ii in waters if t.get('water','(none)') in('lake','pond','reservoir','lagoon','oxbow','(none)','basin')] or [9e9])
        mko.append(dict(src=src,id=i,info=st,lat=la,lon=lo,d_site=round(d),d_water_osm=None if wd is None else round(wd),d_calm_osm=None if calmd>8e9 else round(calmd)))
    mko.sort(key=lambda m:m['d_site'])
    o['markers']=mko
    o['markers_le200_water']=[m for m in mko if m['d_water_osm'] is not None and m['d_water_osm']<=200]
    o['osm_poi']=sorted(mk_osm)[:40]
    o['cpcad_pt']=R.get('cpcad_pt');o['cpcad_2km']=R.get('cpcad_2km')
    OUT[sid]=o
json.dump(OUT,open(S+'/cachesites_gp/raw/analysis.json','w'),indent=1,ensure_ascii=False)
for sid,o in OUT.items():
    print('\n#####',sid,o['name'],'osm_ok',o['osm_ok'])
    for k in ['canvec','osm_calm_nearest','coast_m','river_m','cgndb_water','paths_n','path_nearest','paths_named','routes','grass_m','iron_nearest','iron_2km','mag_nearest','cpcad_pt','cpcad_2km']:
        print(' ',k,':',str(o[k])[:400])
    print('  veg:',str([v for v in o['veg'] if len(v[1])>1 and any(x in v[1] for x in('leaf_type','species','genus'))][:8])[:500])
    print('  markers n',len(o['markers']),'<=200m water:',len(o['markers_le200_water']))
    for m in o['markers'][:12]: print('   ',m)
