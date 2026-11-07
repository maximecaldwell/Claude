/* ---------- SITE SCORECARD ---------- */
const CHECKS = [
 ['marker','Standing, weathered, inscribed survey-type marker (borne)','L33 · L4 · L51',3],
 ['shorepine','By a shore, among pines','L33',3],
 ['water','Still clear water with an edge you shouldn’t step to','Mirror quatrain · L3',3],
 ['junction','Leave a maintained trail at a junction onto a fading path','L45–46',2],
 ['grass','Tall grass, brush, overgrowth beyond the marker','L47 · L50–51',2],
 ['birch','Birch at the site','L8 · L44',2],
 ['compass','Compass deflects (magnetite)','L52',2],
 ['orebody','Old orebody now under water','L3–4',2],
 ['core','Drill-core connection','L49',1],
 ['cedar','Shade; inside eastern white cedar’s range','L29 · tercet',1],
 ['notdecoy','Not one of the poem’s decoy camps','stanzas 2–11',1],
 ['forgotten','Winner-style “forgotten path”','GT winners',1],
 ['shield','ON/QC at the Shield edge (soft prior)','project prior',1],
];
// Y = verified (full), P = partial (half), ? = unknown, N = no
const SITES = [
 {name:'Forsyth Mine (Hull iron mine), Gatineau Park, QC', gate:'pass?', gnote:'Public NCC parkland with a promoted walking circuit (“Chemins de la Mine”). Caveat: the NCC had a geocache there archived, so hidden objects may be unwelcome. Listed hazards: deep open holes, broken fence.',
  s:{marker:'P',shorepine:'?',water:'Y',junction:'Y',grass:'?',birch:'?',compass:'Y',orebody:'Y',core:'?',cedar:'Y',notdecoy:'Y',forgotten:'Y',shield:'Y'},
  notes:'Magnetite that “disturbed a compass in 1801” is the closest match yet to “The compass turns”. A bike path plus a side trail off it about 40 m in fits “where paths align / where the trail forgets design”. Interpretive panels, not a survey marker. Flooded workings.', coords:'45.4746, −75.7884', src:'tourismeoutaouais.com · capitalgems.ca/forsyth-mine · divermag.com'},
 {name:'Marmoraton pit lookout, Marmora, ON', gate:'pass?', gnote:'Public fenced viewing cage. The rest of the site is closed, with an active gravel operation and trucks on the access road. Your notes already flag the pit itself as lookout-only.',
  s:{marker:'?',shorepine:'P',water:'Y',junction:'?',grass:'?',birch:'Y',compass:'Y',orebody:'Y',core:'?',cedar:'Y',notdecoy:'Y',forgotten:'?',shield:'Y'},
  notes:'Crystal-clear flooded magnetite pit, found by a 1948 aeromagnetic survey. Young birch and pine on the waste rock. “Historical plaques at the lookout” come from a review aggregator only and are unverified. The lookout sits high above the water, not at a shore.', coords:'44.4813, −77.6588', src:'AMIS 04220 · thenarwhal.ca · johncharlton.substack · wanderlog'},
 {name:'Griffith Mine trails, Bruce Lake / Ear Falls, ON', gate:'unclear', gnote:'A listed public trail (about 20 km, interpretive signs), but the land is owned by Northern Iron Corp and the trails’ current status is unknown. Pits are barricaded.',
  s:{marker:'P',shorepine:'?',water:'Y',junction:'P',grass:'?',birch:'?',compass:'Y',orebody:'Y',core:'?',cedar:'?',notdecoy:'Y',forgotten:'?',shield:'Y'},
  notes:'Magnetite ore. South pit flooded to Bruce Lake level, and the trails pass the lakeshore. Interpretive signs, text unknown. Far northwest; eastern white cedar may be at its range edge there.', coords:'≈50.80, −93.38', src:'ontariotrails.on.ca · AMIS 03873 · MDI52K14SW00002'},
 {name:'Star Lake Gold Mine site, Whiteshell PP, MB', gate:'unclear', gnote:'Provincial park, but a mineral claim was staked over it (1992). The route to the capped shaft is undocumented.',
  s:{marker:'P',shorepine:'?',water:'N',junction:'P',grass:'?',birch:'?',compass:'N',orebody:'N',core:'?',cedar:'Y',notdecoy:'Y',forgotten:'?',shield:'N'},
  notes:'Four steel markers at the corners of the capped shaft (survey-like). Gold, not iron; no flooded pit. This is the Manitoba BONUS area (FIRST GOLD BAR, Star Lake), so it more likely holds the open Manitoba bonus box than the grand prize.', coords:'49.7327, −95.2519', src:'gov.mb.ca mininv/103 · mhs.mb.ca'},
 {name:'Steep Rock / Caland pits, Atikokan, ON', gate:'fail', gnote:'Pit lakes closed to the public under the Public Lands Act (rockfall). Caland gated. Unstable walls.', s:{marker:'?',shorepine:'?',water:'Y',junction:'P',grass:'?',birch:'?',compass:'N',orebody:'Y',core:'?',cedar:'?',notdecoy:'Y',forgotten:'?',shield:'Y'}, notes:'Hematite, not magnetite. Spectacular, but closed.', coords:'48.82, −91.60', src:'CGS · AMIS 08521 · CBC snippet'},
 {name:'Hilton Mines, Bristol, QC', gate:'fail', gnote:'Private active aggregate quarry (Lamarche McGuinty), gated.', s:{}, notes:'Flooded pit, no public point.', coords:'45.498, −76.345', src:'lamarchemcguinty.ca · capitalgems'},
 {name:'Moose Mountain, Capreol (Sudbury), ON', gate:'fail', gnote:'Gated private access; no lookout. Also in Sudbury, a decoy area for the grand prize.', s:{}, notes:'Flooded magnetite pits behind gates.', coords:'46.851, −81.035', src:'AMIS 05301'},
 {name:'Sherman Mine, Temagami, ON', gate:'fail', gnote:'Gated mine ground under rehabilitation; acid drainage; quarrying.', s:{}, notes:'No public point.', coords:'47.067, −79.840', src:'AMIS 03781'},
 {name:'Port Hope · Peterborough · Lindsay benchmarks (your 24 Sep field check)', gate:'pass', gnote:'Public, standing, low benchmarks with green patina (verdigris).', s:{marker:'Y',shorepine:'N',water:'N',junction:'?',grass:'?',birch:'?',compass:'N',orebody:'N',core:'N',cedar:'Y',notdecoy:'Y',forgotten:'?',shield:'N'}, notes:'The best marker match, but none is by water among pines.', coords:'—', src:'project field check 24 Sep 2026'},
];
function scoreSite(s){ let v=0,max=0,unk=0; CHECKS.forEach(([k,,,w])=>{const x=s.s[k]; if(x==='Y')v+=w; else if(x==='P'){v+=w/2;unk+=w/2;} else if(x==='?'||x===undefined)unk+=w;}); return {v, ceil:v+unk}; }
RENDER.sites = () => {
  const total = CHECKS.reduce((a,c)=>a+c[3],0);
  const rows = SITES.map(s=>({...s, ...scoreSite(s)})).sort((a,b)=> (a.gate==='fail')-(b.gate==='fail') || b.v-a.v);
  const cell = x => x==='Y'?'<span class="sev s">✓</span>':x==='P'?'<span class="sev m">½</span>':x==='N'?'<span class="sev c">✗</span>':'<span class="note">?</span>';
  return `<div><h2>Grand prize site scorecard</h2><p class="note">Every test comes from a poem line or an official clue. Vaccaro (Dig Deep, 19 Oct 2025): “That poem actually has everything you need to find the million.” Scores count only <b>verified</b> facts with a source: ✓ full points, ½ partial, ? unknown, ✗ no. The ceiling is what a site would score if every unknown came out yes. The site research ran 7 Nov 2026, desk only.</p></div>
  <div class="panel"><h3>Verdict</h3><ul class="callouts">
   <li><b>No site passes the strongest tests yet.</b> None has a <b>verified survey-type marker standing by water among pines</b>, the poem’s central image (stanza 9, the only middle stanza with no “but/no” turn).</li>
   <li><b>Best desk fit: Forsyth Mine, Gatineau Park (QC).</b> Public parkland, flooded magnetite workings, a recorded <b>compass deflection</b> (1801), and an informal side trail leaving a bike path, which fits “where paths align / where the trail forgets design”. Its marker is an interpretive panel, so line 33’s “borne” is not met yet. Shore, pines and birch are unverified. The NCC may object to hidden items.</li>
   <li><b>Second: Marmoraton lookout (ON).</b> Your existing pick. Clear flooded magnetite pit, birch and pine nearby. But the lookout is high above the water (no shore), active gravel operations surround it, and its “plaques” are unverified.</li>
   <li><b>Star Lake (Whiteshell)</b> fits the <b>Manitoba bonus</b> (FIRST GOLD BAR), not the grand prize: gold, no flooded pit, no iron.</li>
   <li>Hilton Mines, Moose Mountain, Sherman and Steep Rock fail the access rules: gated, private or closed.</li>
  </ul></div>
  <div class="panel scroll"><h3>Scores (out of ${total})</h3><table><thead><tr><th>Site</th><th>Access rules</th>${CHECKS.map(c=>`<th class="num" title="${esc(c[1])} · ${c[2]}">${c[0]}<br><span class="note" style="font-weight:400">${c[3]}</span></th>`).join('')}<th class="num">Verified</th><th class="num">Ceiling</th></tr></thead><tbody>
   ${rows.map(r=>`<tr${r.gate==='fail'?' style="opacity:.55"':''}><td><b>${esc(r.name)}</b><br><span class="note mono" style="font-size:11px">${r.coords}</span></td><td>${r.gate==='fail'?'<span class="sev c">fails</span>':r.gate==='pass'?'<span class="sev s">passes</span>':'<span class="sev m">'+(r.gate==='unclear'?'unclear':'probably')+'</span>'}</td>${CHECKS.map(c=>`<td class="num">${r.gate==='fail'&&!Object.keys(r.s).length?'':cell(r.s[c[0]])}</td>`).join('')}<td class="num"><b>${r.gate==='fail'?'—':r.v}</b></td><td class="num">${r.gate==='fail'?'—':r.ceil}</td></tr>`).join('')}
  </tbody></table>
  <p class="note" style="margin-top:8px">Column key: hover a column header for its test. marker 3 · shorepine 3 · water 3 · junction 2 · grass 2 · birch 2 · compass 2 · orebody 2 · core 1 · cedar 1 · notdecoy 1 · forgotten 1 · shield 1.</p></div>
  <div class="panel scroll"><h3>The checklist</h3><table><thead><tr><th>Test</th><th>From</th><th class="num">Points</th></tr></thead><tbody>
   <tr><td colspan="3" class="note"><b>Must pass (any failure rules a site out):</b> public, legal and on foot (no boat, rope or ATV; not private, mine or industrial ground) · not in or on a structure, not underwater, not in a cave or mine · not near a memorial, grave or cemetery · not buried (“Above the earth yet tucked away”) · south of the treeline and the Arctic Circle.</td></tr>
   ${CHECKS.map(c=>`<tr><td>${esc(c[1])}</td><td class="mono" style="font-size:12px">${c[2]}</td><td class="num">${c[3]}</td></tr>`).join('')}
  </tbody></table></div>
  <div class="panel scroll"><h3>Site notes and sources</h3><table><thead><tr><th>Site</th><th>Access</th><th>What fits / what doesn’t</th><th>Sources</th></tr></thead><tbody>
   ${rows.map(r=>`<tr><td><b>${esc(r.name)}</b></td><td style="font-size:13.5px">${esc(r.gnote)}</td><td style="font-size:13.5px">${esc(r.notes)}</td><td class="note mono" style="font-size:11px">${esc(r.src)}</td></tr>`).join('')}
  </tbody></table></div>
  <div class="panel"><h3>What would settle it on the ground</h3><ul class="callouts">
   <li><b>Forsyth Mine:</b> walk the Chemins de la Mine circuit and the side trail off the bike path. Look for any standing benchmark or survey post near the flooded workings. Check for pine and birch at the water and a compass swing near the old pits. Read the NCC rules on leaving or retrieving objects.</li>
   <li><b>Marmoraton:</b> confirm what the “plaques” at the viewing cage are. Look for any survey marker on public ground by water and pines near Miners’ Loop, outside the active operation.</li>
   <li><b>New candidates should be:</b> flooded magnetite workings on public parkland in ON/QC, with a trail junction and a standing survey marker at the shore. Forsyth shows this kind of site exists. A desk search for more like it (Ontario and Quebec iron occurrences inside parks or conservation areas) is the next desk step.</li>
  </ul></div>`;
};
