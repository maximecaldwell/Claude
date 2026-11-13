import json,collections
rows=json.load(open('/home/user/Claude/people/_build/rows.json'))
order=['01 Dawson','02 Cobalt','03 Golden Triangle','04 Newfoundland','05 Southern BC','06 Toronto','07 New Brunswick','08 Val-d\'Or','09 Saskatchewan','10 Nova Scotia','11 Manitoba','12 Sudbury','13 Chibougamau','GRAND PRIZE','RECAP']
titles={'01 Dawson':'Ch.1 Dawson City (Klondike)','02 Cobalt':'Ch.2 Cobalt','03 Golden Triangle':'Ch.3 Golden Triangle','04 Newfoundland':'Ch.4 Argentia, Newfoundland','05 Southern BC':'Ch.5 Britannia, Southern B.C.','06 Toronto':'Ch.6 Toronto / Bay Street','07 New Brunswick':'Ch.7 Bathurst, New Brunswick','08 Val-d\'Or':"Ch.8 Val-d'Or",'09 Saskatchewan':'Ch.9 Saskatchewan (potash)','10 Nova Scotia':'Ch.10 Nova Scotia (coal)','11 Manitoba':'Ch.11 Manitoba (Flin Flon / Snow Lake)','12 Sudbury':'Ch.12 Sudbury','13 Chibougamau':'Ch.13 Chibougamau','GRAND PRIZE':'Grand Prize materials (launch, Clue 2–5)','RECAP':'One-year recap (Nov 2026)'}
HOT={'albert-salter','alexander-murray','alfred-selwyn','thomas-flanagan','samuel-j-ritchie','thomas-frood','james-stobie','thomas-edison','thayer-lindsley','edmund-horne','joseph-obalski','peter-mckenzie','james-richardson-gsc','john-cole-gwillim','jack-sullivan','tom-creighton','murray-brook','willet-green-miller','george-mercer-dawson','robert-henderson','sean-boyd','rob-mcewen'}
grp=collections.OrderedDict((k,[]) for k in order)
for r in rows:
    for k in order:
        if k.lower() in r['chapters'].lower(): grp[k].append(r)
n=len(rows); hist=sum(r['status_historical_or_living'].startswith('historical') for r in rows)
pub=sum(r['status_historical_or_living']=='living public figure' for r in rows); priv=sum(r['status_historical_or_living']=='living private' for r in rows)
dl=sum(r['_found']=='yes' for r in rows); pend=sum(r['_found']=='identified-not-downloaded' for r in rows)
L=[]
L.append('# GCTH — people named in the published clues\n')
L.append(f'Built 13 Nov 2026 from the English clue texts on the Mac (`~/GCTH/clues/*`: article_EN, subscriber text, EN transcripts, bonus/found/winner posts, Grand Prize files, one-year recap). Nothing was written to the Mac. French texts were not mined separately because they name the same people.\n')
L.append(f'**{n} people** in the register: {hist} historical (incl. 1 appendix entry: depicted, not named), 1 fictional, {pub} living public figures (executives, politicians, organizer staff), {priv} private individuals (winners, photo credits), who were **not researched**. **{dl} portraits downloaded** to `portraits/`' + (f', plus {pend} more identified on Commons but not downloaded because Wikimedia rate-limited the requests' if pend else '') + '. Full data: `named_people.csv`.\n')
L.append('Legend: ★ = most useful to the hunt (place names, survey history, or Sudbury/Chibougamau/Val-d\'Or geology people). Portrait column: file name, or the reason there is none.\n')
L.append('## The most hunt-relevant people\n')
L.append('- **Sudbury (Ch.12):** the article names **Albert (Pellew) Salter** (1856 compass anomaly), **Alexander Murray** (GSC), **Alfred Selwyn** (GSC director), **Thomas Flanagan** (1883 CPR blacksmith), **William & Thomas Murray, Henry Abbott, John Laughrin** (Murray Mine), **Thomas Frood, James Stobie**, **Samuel J. Ritchie** (Canadian Copper Co.), **Thomas Edison** (Falconbridge 1901), **Thayer Lindsley**, **Edmund Horne**. **Sir William Logan is NOT named** in any clue text, and the article says "Albert Salter", not "A.P. Salter". Mine and township names that are also surnames (Frood, Stobie, Creighton, Murray, Falconbridge) are possible map anchors.')
L.append("- **Chibougamau (Ch.13):** James Richardson (GSC, 1870), fur trader Peter McKenzie (1903), and inspector Joseph Obalski (1904). Obalski also translated the 1911/12 Chibougamau Mining Commission report into French. A photo from that report, *Prof. Gwillim and group*, shows up in the **Val-d'Or** video (see the appendix entry for J.C. Gwillim: shown in the photo, not named in the text).")
L.append('- **Val-d\'Or (Ch.8):** Jean-Jacques "Jack" Sullivan is the only person named. **Manitoba (Ch.11):** Tom Creighton, plus the fictional Flintabbatey Flonatin.')
L.append('- **Grand Prize:** Sean Boyd (Agnico Eagle chair) gave the launch quote and presented Clue 5. Rob McEwen delivered Clue 4. Anthony Vaccaro (TNM Group president) hosted.')
L.append('- **Oddities worth noting:** NB article presents "Murray Brook" (a Bathurst-camp deposit name) as a prospector. Cobalt spells "Willett Green Miller" (correct: Willet). The Golden Triangle winners are spelled "Schwartz" in the posts and "Schwarz" in the recap. Cobalt preserves the garble "near – Long Lake James McKinley". The Chibougamau winner names come from auto-captions and are unreliable.\n')
for k in order:
    if not grp[k]: continue
    L.append(f'## {titles[k]}\n')
    L.append('| | Name | Role | Dates | Status | Portrait | Licence | Match |')
    L.append('|---|---|---|---|---|---|---|---|')
    for r in grp[k]:
        star='★' if r['slug'] in HOT else ''
        d=(r['born'] or '?')+'–'+(r['died'] or ('' if 'living' in r['status_historical_or_living'] else '?'))
        if d=='?–?': d=''
        if r['_found']=='yes': p=f"[{r['portrait_file'].split('/')[-1]}]({r['portrait_file']})"
        elif r['_found']=='identified-not-downloaded': p=f"[Commons]({r['portrait_source_url']}) (not downloaded)"
        elif 'private' in r['status_historical_or_living']: p='private individual — not researched'
        elif r['portrait_source_url']: p=f"none ([link]({r['portrait_source_url']}))"
        else: p='none found'
        role=r['role'].replace('|','/')
        L.append(f"| {star} | **{r['name']}** | {role} | {d} | {r['status_historical_or_living']} | {p} | {r['licence']} | {r['match_confidence']} |")
    L.append('')
    L.append('<details><summary>Quotes</summary>\n')
    for r in grp[k]: L.append(f"- **{r['name']}**: {r['context_quote']}")
    L.append('\n</details>\n')
hh=[r for r in rows if r['status_historical_or_living'].startswith('historical')]; nh=len(hh); nohist=sum(r['_found']!='yes' for r in hh)
L.append('## Gaps\n')
L.append(f'- {nohist} of the {nh} historical people have no free portrait on Wikimedia Commons, including Salter, Flanagan, Frood, Stobie, S.J. Ritchie, Lindsley, McKenzie, Richardson, Sullivan, Creighton, Henderson, Choquette, the Timmins brothers and W.G. Miller. Next places to look: LAC Collection Search, BAnQ, Archives of Ontario, Yukon Archives, and the frontispieces of the Ontario Bureau of Mines reports on Internet Archive.')
L.append('- Living executives and organizers (Boyd, McEwen, Vaccaro, Reichert, Rosmus): only company home-page links are given. Their leadership/board pages blocked automated checks (403/404), so those URLs are unverified.')
L.append('- Some dates are blank because they were not verified in this pass.')
L.append('- `_other_published/` (podcasts and long interviews) was left out because it is not clue text. It names more industry figures (e.g. Rick Rule).\n')
open('/home/user/Claude/people/named_people.md','w').write('\n'.join(L))
print('md written',n,hist,pub,priv,dl,pend)
