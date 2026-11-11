import json,glob,csv,re,sys,collections
sys.path.insert(0,'/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/plaques_canada/scripts')
import geo
R=geo.R; recs=[]
def add(src,id,name,typ,lat,lon,text,url,extra=None):
    if lat is None or lon is None: return
    recs.append(dict(src=src,id=str(id),name=(name or '').strip(),type=typ,lat=float(lat),lon=float(lon),text=re.sub(r'\s+',' ',text or '').strip(),url=url,**(extra or {})))
# OSM
TXT=('name','name:en','name:fr','inscription','inscription:en','inscription:fr','description','description:en','description:fr','memorial:text','subject','old_name','note','website','wikipedia','wikidata','operator','resource','mineral')
for f in glob.glob(R+'osm_*.json'):
    for o in json.load(open(f)):
        t=o['tags']
        typ='/'.join(x for x in [('historic='+t['historic']) if 'historic' in t else '',('memorial='+t['memorial']) if 'memorial' in t else '',('man_made='+t['man_made']) if 'man_made' in t else '',('information='+t['information']) if t.get('tourism')=='information' else '',('material='+t['material']) if 'material' in t else ''] if x)
        text=' | '.join('%s=%s'%(k,t[k]) for k in TXT if k in t and k not in ('name',))
        add('OSM',o['osm'],t.get('name') or t.get('name:en') or t.get('name:fr') or '',typ,o['lat'],o['lon'],text,'https://www.openstreetmap.org/%s/%s'%({'n':'node','w':'way'}[o['osm'][0]],o['osm'][1:]),dict(osm_tags=json.dumps(t,ensure_ascii=False)))
# OHT
for p in json.load(open(R+'oht_locations.json'))['data']['plaques']:
    add('OHT',p['uuid'],p['title_en'],'Ontario Heritage Trust provincial plaque (%s)'%(p.get('plaque_status_en') or ''),p['latitude'],p['longitude'],(p.get('plaque_text_en') or '')+' || Location: '+(p.get('location_en') or ''),'https://maps.heritagetrust.on.ca/search?view=plaques (uuid %s)'%p['uuid'])
# BC SOI
for r in csv.DictReader(open(R+'bc_stop_of_interest.csv',encoding='utf-8-sig')):
    try: add('BC-SOI',r['Sign ID'],r['Sign Name'],'BC Stop of Interest sign',float(r['Latitude']),float(r['Longitude']),r['Current Text']+' || Location: '+r['Specific Location'],'https://catalogue.data.gov.bc.ca/dataset/bc-stop-of-interest-signs (sign %s)'%r['Sign ID'])
    except ValueError: pass
# MHS
for m in json.load(open(R+'mhs_monuments.json')):
    add('MHS',m['url'].split('/')[-1],m['name'],'Manitoba Historical Society monument/site',m['lat'],m['lon'],m['text']+' || '+m['addr']+', '+m['muni'],m['url'])
# RTP
for p in json.load(open(R+'rtp_canada.json')):
    if 'err' in p: continue
    add('RTP',p['id'],p['title'],'Read the Plaque plaque',p['latitude'],p['longitude'],p.get('description') or '','https://readtheplaque.com/plaque/'+p['slug'])
# HP details (fetched) + other HP (coords only)
det={d['id']:d for d in json.load(open(R+'hp_details.json'))['details']}
for x in json.load(open(R+'hp_union.json'))['all']:
    d=det.get(x['id'])
    add('CRHP',x['id'],x['name'],'Canadian Register of Historic Places'+((' / '+d['theme'][:80]) if d and d['theme'] else ''),x['posn'][0],x['posn'][1],(d['text'] if d else '')+' || '+x.get('location',''),'https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=%s'%x['id'],dict(hp_detail=bool(d)))
# QC MCC
import io
for f in glob.glob(R+'qc_*.csv'):
    raw=open(f,encoding='utf-8-sig',errors='ignore').read()
    dl=';' if raw.split('\n')[0].count(';')>raw.split('\n')[0].count(',') else ','
    for r in csv.DictReader(io.StringIO(raw),delimiter=dl):
        lat=r.get('latitude');lon=r.get('longitude')
        if not lat:
            w=r.get('Wkt_Multipoint_XY') or ''
            m=re.search(r'(-?\d+\.\d+)\s+(-?\d+\.\d+)',w)
            if m: lon,lat=m.group(1),m.group(2)
        try: lat=float(str(lat).replace(',','.'));lon=float(str(lon).replace(',','.'))
        except Exception: continue
        add('QC-RPCQ',r['bien_id'],r['nom_bien'],'Quebec '+(r.get('statut_juridique') or r.get('statut_juridique_princ') or '')+' / '+(r.get('categorie') or ''),lat,lon,(r.get('description_bien') or '')[:1500]+' || '+(r.get('synthese_historique') or '')[:1500],r.get('url_rpcq') or '')
print(collections.Counter(r['src'] for r in recs))
# filter
keep=[]
for r in recs:
    d,o=geo.nearest(r['lat'],r['lon'])
    dm,om=geo.nearest(r['lat'],r['lon'],mag=True)
    kw=sorted(set(m.lower() for m in geo.KW.findall(r['name']+' '+r['text'])))
    # OSM website/wikidata fields shouldn't count for keywords
    if r['src']=='OSM':
        t=json.loads(r['osm_tags']);s=' '.join(str(t.get(k,'')) for k in ('name','name:en','name:fr','inscription','inscription:en','inscription:fr','description','description:en','description:fr','memorial:text','subject','old_name','resource','mineral'))
        kw=sorted(set(m.lower() for m in geo.KW.findall(s)))
        if t.get('historic') in ('mine','mine_shaft') or t.get('man_made') in ('mineshaft','adit'): kw=sorted(set(kw)|{'(mine feature)'})
    r['prov']=geo.prov(r['lat'],r['lon'],0.02)
    if r['prov'] is None: continue
    if d<=1500 or kw:
        r.update(iron_d_m=round(d),iron_name=o['name'] if o else '',iron_id=o['id'] if o else '',iron_src=o['src'] if o else '',iron_prim=o['prim'] if o else '',iron_mag=o['mag'] if o else '',iron_url=o['url'] if o else '',
                 mag_d_m=round(dm) if om else None,mag_name=om['name'] if om else '',mag_url=om['url'] if om else '',kw=';'.join(kw),near_iron=d<=1500)
        keep.append(r)
print('kept',len(keep),collections.Counter((r['src'],r['near_iron']) for r in keep))
json.dump(keep,open(R+'../data_keep.json','w'))
json.dump(collections.Counter(r['src'] for r in recs),open(R+'../counts_all.json','w'))
