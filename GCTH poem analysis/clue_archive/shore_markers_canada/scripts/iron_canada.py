import json,re,csv,collections
from pyproj import Transformer
D='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada/dl/'
OUT='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/shoremk_canada/iron_canada.json'
occ=[]
M=lambda s: bool(re.search('magnet',s or '',re.I))
def add(**k): occ.append(k)
# BC MINFILE
for f in json.load(open(D+'bc.json'))['features']:
    p=f['properties'];cs=[(p['COMMODITY_CODE%d'%i] or '').strip() for i in range(1,9)]
    if not ({'FE','MA'}&set(cs)): continue
    desc=', '.join((p['COMMODITY_DESCRIPTION%d'%i] or '').strip() for i in range(1,9) if p['COMMODITY_DESCRIPTION%d'%i])
    add(prov='BC',src='BC-MINFILE',id=p['MINFILE_NUMBER'].replace('  ',' ').strip(),name=(p['MINFILE_NAME1'] or '').strip(),status=(p['STATUS_DESCRIPTION'] or '').strip(),
        prim=desc,sec=(p['DEPOSIT_TYPE_DESCRIPTION1'] or '').strip(),lat=p['LATITUDE_DECIMAL'],lon=p['LONGITUDE_DECIMAL'],mag='MA' in cs,
        url=p['MINFILE_SUMMARY_URL'])
# Yukon MINFILE
for f in json.load(open(D+'yt_all.json')):
    a=f['attributes'];c=a['MAIN_COMMODITY'] or ''
    if not re.search('iron|magnet',c,re.I): continue
    add(prov='YT',src='YT-MINFILE',id=a['MINFILE_NUMBER'],name=a['MINFILE_NAME'],status=a['DEPOSIT_STATUS'],prim=c,sec=a['DEPOSIT_TYPE'] or '',
        lat=a['LATITUDE_DD'],lon=a['LONGITUDE_DD'],mag=M(c),url=a['LINK_TO_DOCUMENT'] or '')
# NWT showings 2024
for f in json.load(open(D+'nt_all.json')):
    a=f['attributes'];cs=[a[k+'COMMODITY'] or '' for k in 'ABCDE'];s=' '.join(cs)+' '+(a['MINERALIZA'] or '')
    if not re.search(r'\biron\b|magnet',s,re.I): continue
    add(prov='NT',src='NT-NTGS-Showings2024',id=a['SHOWING_ID'],name=a['SHOWING_NA'],status=(a['RANK'] or '')+'/'+(a['DEVELOPMEN'] or ''),prim=', '.join(x for x in cs if x.strip()),
        sec=a['MINERALIZA'] or '',lat=a['LATITUDE'],lon=a['LONGITUDE'],mag=M(s),url='https://app.nwtgeoscience.ca (showing '+a['SHOWING_ID']+')')
# Saskatchewan SMDI
for f in json.load(open(D+'sk_all.json')):
    a=f['attributes'];c=(a['PRIMARYCOMMODITIES'] or '')+'; '+(a['ASSOCIATEDCOMMODITIES'] or '');hm=a['HOSTMINERAL'] or ''
    if not (re.search(r'\biron\b',c,re.I) or M(hm) or M(c)): continue
    g=f.get('geometry') or {}
    add(prov='SK',src='SK-SMDI',id=a['SMDI'],name=a['NAME'],status=a['STATUS'],prim=c,sec=hm,lat=g.get('y'),lon=g.get('x'),mag=M(hm) or M(c),url=a['WEBLINK'])
# Manitoba GeoFile 5 (MDD) - aggregate sample rows per MDD number
import openpyxl
tr=Transformer.from_crs('EPSG:26914','EPSG:4326',always_xy=True)
ws=openpyxl.load_workbook(D+'mb/GeoFile5-2025/GeoFile_5-2025.xlsx',read_only=True)['GeoFile5-2025']
rows=ws.iter_rows(values_only=True);h=list(next(rows));ix={k:i for i,k in enumerate(h)}
mb={}
for r in rows:
    c=r[ix['Commodities or feature of interest']] or '';cm=r[ix['Comments / occurrence description']] or '';cg=r[ix['Commodities group']] or ''
    if not (re.search(r'\bFe\b',c) or M(cm) or M(c)): continue
    k=r[ix['MDD number']] or ('MB-noid-%s-%s'%(r[ix['Easting (NAD83 Z14)']],r[ix['Northing (NAD83 Z14)']]))
    if r[ix['Easting (NAD83 Z14)']] is None: continue
    lon,lat=tr.transform(r[ix['Easting (NAD83 Z14)']],r[ix['Northing (NAD83 Z14)']])
    if k not in mb:
        mb[k]=dict(prov='MB',src='MB-GeoFile5-MDD',id=k,name=r[ix['MDD name']] or '',status=r[ix['Occurrence classification']] or '',prim=c,sec=str(cm)[:200],lat=lat,lon=lon,mag=M(cm) or M(c),url='Manitoba GeoFile 5-2025 '+str(k))
    else: mb[k]['mag']=mb[k]['mag'] or M(cm)
occ+=list(mb.values())
# Alberta DIG 2025-0009
def tsv(f): return list(csv.DictReader(open(D+'ab/'+f,encoding='latin-1'),delimiter='\t'))
com=collections.defaultdict(list)
for r in tsv('DIG_2025-0009_tblCommodity.txt'): com[r['Occurr_ID']].append(r['Commodity'])
geo={r['Occurr_ID']:r for r in tsv('DIG_2025-0009_tblGeology.txt')}
for r in tsv('DIG2025-0009_tblOccurrence.txt'):
    i=r['Occurr_ID'];cs=com.get(i,[]);g=geo.get(i,{});mins=(g.get('Ore_min') or '')+' '+(g.get('Gangue_min') or '')
    if not ('Iron' in cs or M(mins)): continue
    add(prov='AB',src='AB-AGS-DIG2025-0009',id=i,name=r['Name'],status=r['Dev_stage'],prim=', '.join(cs),sec=g.get('Ore_min',''),lat=float(r['Lat_NAD83']),lon=float(r['Long_NAD83']),
        mag=M(mins),url='AGS DIG 2025-0009 '+i)
# New Brunswick
for f in json.load(open(D+'nb_all.json')):
    a=f['attributes'];c=a['COMMODITIES'] or ''
    if not re.search(r'\bFe\b',c): continue
    add(prov='NB',src='NB-MOD',id=str(a['URN']),name=a['NAME'],status='',prim=c,sec='',lat=a['LAT'],lon=a['LON'],mag=False,url=a['MIN_OCCR_URL'])
# Nova Scotia MODB
for f in json.load(open(D+'ns_all.json')):
    a=f['attributes'];c=(a['comm_prim'] or '').strip()+'; '+(a['comm_list'] or '');ml=a['min_list'] or ''
    if not (re.search(r'\bFe\b',c) or M(ml)): continue
    add(prov='NS',src='NS-MODB',id=str(a['occ_num'] or a['geo_num']),name=a['name'],status=a['status'] or '',prim=c,sec=ml[:200],lat=a['lat_wm84dd'],lon=a['lon_wm84dd'],mag=M(ml),url=a['hotlink'] or '')
# Newfoundland & Labrador MODS
for a in json.load(open(D+'nl_all.json')):
    c=a['COMMODS'] or '';om=a['OREMIN'] or ''
    if not (re.search(r'\b(Iron|Magnetite|Hematite)\b',c,re.I) or M(om)): continue
    add(prov='NL',src='NL-MODS',id=a['NMINO'],name=a['DEPNAME'] or a['COMNAME'],status=a['STATUS'],prim=c,sec=om[:200],lat=a['LATITUDE'],lon=-abs(float(a['LONGITUDE'])),mag=M(om) or M(c),
        url='https://geoatlas.gov.nl.ca/ MODS '+a['NMINO']+' ('+(a['REGION'] or '')+')')
occ=[o for o in occ if o['lat'] and o['lon']]
for o in occ: o['lat']=float(o['lat']);o['lon']=float(o['lon'])
json.dump(occ,open(OUT,'w'),ensure_ascii=False)
c=collections.Counter(o['prov'] for o in occ);m=collections.Counter(o['prov'] for o in occ if o['mag'])
for k in c: print(k,c[k],'mag',m[k],'south<55:',sum(1 for o in occ if o['prov']==k and o['lat']<55))
print(len(occ))
