# Build manifest.tsv from scripts/pairs.jsonl + scripts/oht_rows.json; recount words from saved txt files.
import json, os, sys, re
B = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(B,'scripts','pairs.jsonl'))]
for s,t,u,uf,o,n in json.load(open(os.path.join(B,'scripts','oht_rows.json'))):
    rows.append(dict(slug=s,title_en=t,url_en=u,url_fr=uf,org=o,note=n))
fix_title = {'gsm_home': ('Greater Sudbury Museums', 'Musées du Grand Sudbury')}
for s,(te,tf) in fix_title.items():
    for L,t in (('EN',te),('FR',tf)):
        p=os.path.join(B,f'{s}_{L}.txt'); x=open(p).read()
        if not x.startswith(t): open(p,'w').write(t+'\n'+x)
extra = {
 'geotour_discovery_site': 'GeoTour of the 1883 nickel discovery site near the Murray Mine, Regional Road 35 ~5 km NW of downtown; describes the roadside commemorative plaque in a paved pull-off',
 'gs_cenotaphs': 'Describes cenotaphs and monuments (physical memorials) across Greater Sudbury in general terms',
 'gs_public_art': 'Describes the City public art collection/program (physical installations)',
 'gs_crosses_for_change': 'Describes a physical permanent memorial installation (Crosses for Change)',
 'gs_heritage_sites': 'Heritage Register overview (designated/listed physical heritage properties)',
 'sn_science_north': 'Science North building page incl. architecture section (100 Ramsey Lake Rd)',
 'pdx_a_propos': 'FR version substantially longer than EN (loose twin)',
 'pdx_realisations_depuis_2007': 'EN version longer than FR (loose twin)',
 'pdx_le_parcours': 'Place des Arts tour page (building at 27 Larch St, former King Edward Hotel site)',
 'oht_sudbury_structure': None,
}
out=[]
for r in rows:
    s=r['slug']
    w={}
    for L in ('EN','FR'):
        t=open(os.path.join(B,f'{s}_{L}.txt')).read()
        w[L]=len(t.split())
    if min(w.values())<40: print('SHORT',s,w); continue
    n = r.get('note','') or ''
    if extra.get(s): n = (n+'; ' if n else '') + extra[s]
    if s.startswith('vm_'): n = (n+'; ' if n else '') + 'Virtual-museum local-history page; EN and FR at same URL with lang=en/lang=fr'
    if s.startswith('geotour_'): n = (n+'; ' if n else '') + 'PDF documents; text via pdftotext, lines reflowed'
    out.append([s, r['title_en'], r['url_en'], r['url_fr'], r['org'], str(w['EN']), str(w['FR']), n])
order = lambda x: (['oht','geotour','on_','gs_','gsm','vm_','sn_','pda','pdx','cs_','lu_','gspl'].index(next(p for p in ['oht','geotour','on_','gs_','gsm','vm_','sn_','pda','pdx','cs_','lu_','gspl'] if x[0].startswith(p))), x[0])
out.sort(key=order)
with open(os.path.join(B,'manifest.tsv'),'w') as f:
    f.write('slug\ttitle_en\turl_en\turl_fr\tsource_org\twords_en\twords_fr\tnotes\n')
    for o in out: f.write('\t'.join(x.replace('\t',' ').replace('\n',' ') for x in o)+'\n')
print(len(out))
