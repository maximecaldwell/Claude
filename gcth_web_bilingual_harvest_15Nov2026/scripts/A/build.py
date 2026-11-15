#!/usr/bin/env python3
"""Build <slug>_EN.txt / <slug>_FR.txt from raw/ and write manifest.tsv.
Run from bi/A:  python3 -I scripts/build.py"""
import subprocess, os, re, sys

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(A)
EX = ['python3', '-I', 'scripts/extract.py']
TCE = 'https://thecanadianencyclopedia.ca/en/article/'
LAC = 'https://epe.lac-bac.gc.ca/100/205/301/ic/cdc/incocoin/'
DFHD = 'https://www.pc.gc.ca/apps/dfhd/'

def tce_fr(s):
    h = open('raw/tce_%s_EN.html' % s, encoding='utf-8', errors='replace').read()
    return re.search(r'hreflang="fr" href="([^"]+)"', h).group(1)

def title_of(path):
    return open(path, encoding='utf-8').readline().strip()

P = []  # (slug, mode, rawEN, rawFR, urlEN, urlFR, org, extra_args, notes)

# --- Parks Canada DFHD / HSMBC / FHBRO / HRS (physical places in Greater Sudbury first)
P.append(('hsmbc_mining_nhe', 'blocks:.centercontent', 'raw/dfhd_mining_nhe_EN.html', 'raw/dfhd_mining_nhe_FR.html',
          DFHD + 'page_nhs_eng.aspx?id=871', DFHD + 'page_nhs_fra.aspx?id=871', 'Parks Canada (DFHD) / HSMBC', ['--nn'],
          'Mining National Historic Event; all plaque texts incl. Nickel Mining plaque at Dynamic Earth, 122 Big Nickel Rd, Sudbury, and Copper Industry plaque at Noranda. FR page plaque order/labels differ from EN as published.'))
P.append(('dfhd_sudbury_cpr_station', 'blocks:.centercontent', 'raw/dfhd_sudbury_cpr_station_hrs_EN.html', 'raw/dfhd_sudbury_cpr_station_hrs_FR.html',
          DFHD + 'page_hrs_eng.aspx?id=2156', DFHD + 'page_hrs_fra.aspx?id=2156', 'Parks Canada (DFHD)', ['--nn'],
          'Heritage Railway Station, 1 Van Horne St, Sudbury (built 1907).'))
P.append(('dfhd_sudbury_gocb', 'blocks:.centercontent', 'raw/dfhd_sudbury_gocbldg_fhbro_EN.html', 'raw/dfhd_sudbury_gocbldg_fhbro_FR.html',
          DFHD + 'page_fhbro_eng.aspx?id=7588', DFHD + 'page_fhbro_fra.aspx?id=7588', 'Parks Canada (DFHD) / FHBRO', ['--nn'],
          'Government of Canada Building, 19 Lisgar St, Sudbury (1957 post office); includes FHBRO Heritage Character Statement.'))
P.append(('dfhd_sudbury_taxation_centre', 'blocks:body', 'raw/derived/adpf_taxation_centre_EN.html', 'raw/derived/adpf_taxation_centre_FR.html',
          'https://adpf-dfhd.pc.gc.ca/en/report/1e5b2b62-b224-4200-b5e9-f8141335a2b3', 'https://adpf-dfhd.pc.gc.ca/fr/report/1e5b2b62-b224-4200-b5e9-f8141335a2b3',
          'Parks Canada (new DFHD) / FHBRO', [],
          'Taxation Data Centre (Sudbury), 1050 Notre Dame Ave. Report pages are JS-rendered; text taken from the en/fr fields of the site search API JSON (raw/adpf_search_sudbury.json) via raw/derived/*.html.'))
P.append(('crhp_sudbury_cpr_station', 'blocks:#maincontent', 'raw/hp_sudbury_cpr_station_crhp_EN.html', 'raw/hp_sudbury_cpr_station_crhp_FR.html',
          'https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=4596', 'https://www.lieuxpatrimoniaux.ca/fr/rep-reg/place-lieu.aspx?id=4596',
          'Canadian Register of Historic Places', ['SEARCH THE', 'RECHERCHE DANS', '--nn', '--drop=.redtextbox2'],
          'NEAR-DUPLICATE of dfhd_sudbury_cpr_station (same Statement of Significance, CRHP layout).'))
P.append(('crhp_sudbury_gocb', 'blocks:#maincontent', 'raw/hp_sudbury_gocbldg_crhp_EN.html', 'raw/hp_sudbury_gocbldg_crhp_FR.html',
          'https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=11081', 'https://www.lieuxpatrimoniaux.ca/fr/rep-reg/place-lieu.aspx?id=11081',
          'Canadian Register of Historic Places', ['SEARCH THE', 'RECHERCHE DANS', '--nn', '--drop=.redtextbox2'],
          'NEAR-DUPLICATE of dfhd_sudbury_gocb SoS part (CRHP layout).'))

# --- LAC-archived Canada's Digital Collections site "Minerals and Coins" (Science North, Sudbury; Inco coin collection)
lac = [('bnhist', 'The History of the Big Nickel'), ('cannickel', "Canada's Nickel Coinage"), ('nickel', 'Development of nickel for coinage'),
       ('advnickel', 'Advantages of nickel for coinage'), ('timeline', 'World timeline of nickel in coins'), ('histcoin', 'History of the Inco Coin Collection'),
       ('histmine', 'History of the Vickery Mineral Collection (Science North)'), ('coinage', 'Brief history of coinage'), ('minting', 'Minting of a coin'),
       ('makedie', 'Making of a die')]
for p, _ in lac:
    note = 'Archived Canada\'s Digital Collections (Industry Canada) site by Science North, Sudbury; hosted by Library and Archives Canada web archive (needs disclaimer cookie).'
    if p in ('coinage', 'minting', 'makedie'):
        note += ' Generic coin topic (not Sudbury-specific).'
    P.append(('lac_scn_' + p, 'blocks:body', 'raw/lacic_%s_EN.html' % p, 'raw/lacic_%s_FR.html' % p, LAC + p + '.html', LAC + 'f' + p + '.html',
              'LAC web archive / Science North / Industry Canada CDC', [], note))

# --- Bank of Canada Museum, Royal Canadian Mint, NRCan
P.append(('bocm_first_canadian_nickel', 'blocks:.post', 'raw/bocm_first_nickel_EN.html', 'raw/bocm_first_nickel_FR.html',
          'https://www.bankofcanadamuseum.ca/2019/01/the-first-canadian-nickel/', 'https://www.museedelabanqueducanada.ca/2019/01/petite-histoire-piece-canadienne-5-cents/',
          'Bank of Canada Museum', ['--skip=^(Share this page|Partag)'], 'Blog article on the 1922 nickel 5-cent coin (Mond Nickel blanks).'))
P.append(('rcm_blog_5cent_history', 'blocks:article', 'raw/rcm_blog_5cent_EN.html', 'raw/rcm_blog_5cent_FR.html',
          'https://www.mint.ca/en/blog/2022-03-5-stories-every-canadian-should-know-5-cent', 'https://www.mint.ca/fr/blogue/2022_03_5-stories-every-canadian-should-know-5-cent',
          'Royal Canadian Mint', ['More Than a Decade Later', "Plus d'un décennie", '--skip=^(Back to Articles$|Retour aux Articles$|via GIPHY$|Image credit|Source des images)'],
          'Mint blog on the 5-cent coin incl. 1951 nickel bicentennial design; related-article teasers cut. EN repeats intro paragraph as published.'))
P.append(('nrcan_nickel_facts', 'blocks:main', 'raw/nrcan_nickel_facts_EN.html', 'raw/nrcan_nickel_facts_FR.html',
          'https://natural-resources.canada.ca/minerals-mining/mining-data-statistics-analysis/minerals-metals-facts/nickel-facts',
          'https://ressources-naturelles.canada.ca/mineraux-exploitation-miniere/donnees-statistiques-analyses-exploitation-miniere/faits-mineraux-metaux/faits-nickel',
          'Natural Resources Canada', ['Date modified', 'Date de modification'], 'Statistics-heavy fact page (2024 data); mentions Sudbury refinery.'))

# --- The Canadian Encyclopedia (Historica Canada; federally funded, EN/FR)
tce = ['sudbury', 'valley-east', 'rayside-balfour', 'nickel', 'inco-limited', 'thayer-lindsley', 'noranda-inc', 'alfred-richard-cecil-selwyn',
       'impact-crater-meteor-meteorite', 'copper', 'platinum', 'mining', 'mineral-resources', 'geological-survey-of-canada', 'coins-and-tokens',
       'royal-canadian-mint', 'snolab', 'laurentian-university', 'acid-rain']
for s in tce:
    P.append(('tce_' + s.replace('-', '_'), 'tce', 'raw/tce_%s_EN.html' % s, 'raw/tce_%s_FR.html' % s, TCE + s, tce_fr(s),
              'The Canadian Encyclopedia (Historica Canada)', [], ''))

rows = []
for slug, mode, ren, rfr, uen, ufr, org, extra, notes in P:
    out = {}
    for L, raw in (('EN', ren), ('FR', rfr)):
        dst = '%s_%s.txt' % (slug, L)
        r = subprocess.run(EX + [mode, raw, dst] + extra, capture_output=True, text=True)
        if r.returncode:
            sys.exit('FAIL %s %s %s' % (slug, L, r.stderr))
        out[L] = len(open(dst, encoding='utf-8').read().split())
    rows.append([slug, title_of(slug + '_EN.txt'), uen, ufr, org, out['EN'], out['FR'], notes])

# --- subset pair: the bilingual HSMBC Nickel Mining plaque (Dynamic Earth, Big Nickel Road) cut from the NHE record
en = open('hsmbc_mining_nhe_EN.txt', encoding='utf-8').read().split('\n\n')
fr = open('hsmbc_mining_nhe_FR.txt', encoding='utf-8').read().split('\n\n')
def grab(parts, start, title):
    i = next(k for k, p in enumerate(parts) if p.startswith(start) and 'Big Nickel' in p)
    j = next(k for k, p in enumerate(parts) if k > i and p.startswith(title))
    return [parts[i]] + parts[j:j + 2]
pe = grab(en, 'Existing plaque:', 'Nickel Mining')
pf = grab(fr, 'Plaque existante', 'Production de Nickel')
pe = ['Nickel Mining in Canada (HSMBC plaque)'] + pe
pf = ['Production de nickel du Canada (plaque de la CLMHC)'] + pf
for L, parts in (('EN', pe), ('FR', pf)):
    open('hsmbc_nickel_plaque_%s.txt' % L, 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
rows.insert(1, ['hsmbc_nickel_plaque', pe[0], DFHD + 'page_nhs_eng.aspx?id=871', DFHD + 'page_nhs_fra.aspx?id=871',
                'Parks Canada (DFHD) / HSMBC', len('\n'.join(pe).split()), len('\n'.join(pf).split()),
                'SUBSET of hsmbc_mining_nhe: the Nickel Mining plaque at Dynamic Earth, 122 Big Nickel Road, Sudbury (physical bilingual plaque; new-DFHD record d4865285 holds both texts). First line is an added heading (not page text). Plaque FR text has missing accents as published.'])

with open('manifest.tsv', 'w', encoding='utf-8') as f:
    f.write('\t'.join(['slug', 'title_en', 'url_en', 'url_fr', 'source_org', 'words_en', 'words_fr', 'notes']) + '\n')
    for r in rows:
        f.write('\t'.join(str(x).replace('\t', ' ') for x in r) + '\n')
for r in rows:
    flag = ' <40!' if min(r[5], r[6]) < 40 else ''
    print('%-36s %5d %5d  %s%s' % (r[0], r[5], r[6], r[1][:60], flag))
print(len(rows), 'pairs')
