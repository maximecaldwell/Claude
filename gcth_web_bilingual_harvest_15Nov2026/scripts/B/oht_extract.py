# Extract Greater Sudbury Ontario Heritage Trust plaques (EN/FR) from the
# maps.heritagetrust.on.ca locations API (the data source of the plaque map pages).
import json, sys, os
B = sys.argv[1]
d = json.load(open(os.path.join(B, 'raw', 'oht_sudbury.json')))
slugs = {
 '8805AF44':'oht_mine_rescue_stations','48D04558':'oht_sudbury_structure','FE72C080':'oht_austin_airways',
 'FA8088A3':'oht_founding_of_sudbury','E527ED56':'oht_franco_ontarian_flag','B347931A':'oht_laurentian_university',
 '1BB60C70':'oht_sacred_heart_college','CD5F0E33':'oht_saint_louis_de_gonzague','7D2267E5':'oht_sainte_anne_des_pins',
 '750C7F6A':'oht_whitefish_lake_post'}
rows = []
def fix(t):
    # "Founding of Sudbury, The" -> "The Founding of Sudbury"
    for art in [', The', ', la', ', le', ", l'", ', les']:
        if t.endswith(art):
            a = art[2:]; a = a[0].upper()+a[1:]
            return (a + ('' if a.endswith("'") else ' ') + t[:-len(art)])
    return t
for x in d['data']['plaques']:
    k = x['uuid'][:8]
    if k not in slugs: continue
    s = slugs[k]
    json.dump(x, open(os.path.join(B,'raw',s+'.json'),'w'), ensure_ascii=False, indent=1)
    for lang in ('en','fr'):
        txt = fix(x['title_'+lang]) + '\n\n' + x['plaque_text_'+lang].strip() + '\n'
        open(os.path.join(B, f"{s}_{lang.upper()}.txt"),'w').write(txt)
    u = 'https://maps.heritagetrust.on.ca/search?view=plaques&details=true&id='+x['uuid']
    uf = 'https://maps.heritagetrust.on.ca/fr/search?view=plaques&details=true&id='+x['uuid']
    note = f"Physical provincial plaque (OHT, unveiled {x['unveiling_year']}); location: {x['location_en']}" + (f"; status: {x['plaque_status_en']}" if x['plaque_status_en'] else '') + "; text via site's /api/locations JSON"
    rows.append([s, fix(x['title_en']), u, uf, 'Ontario Heritage Trust', note])
json.dump(rows, open(os.path.join(B,'scripts','oht_rows.json'),'w'), ensure_ascii=False)
print(len(rows))
