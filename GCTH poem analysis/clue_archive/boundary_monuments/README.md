# GCTH grand prize, stanza 9: boundary, meridian and survey monuments by calm lakes (ON/QC desk sweep)

Date: 17 Nov 2026. Desk research only. Nothing was visited in the field.
Stanza 9 EN: "One marker stands, by shore and pine". FR: "Une borne se dresse, près du rivage et des pins / Son message est terni par le temps qui passe".
Earlier sweeps covered geodetic control stations, plaques and cairns. This sweep covers boundary, meridian and other standing survey monuments.

## Files
- `candidates.csv` has 194 ranked rows. There are 152 physical monuments mapped in OSM and 42 points derived from geometry. Columns: rank, score, id, src, name, kind, lat, lon, water_dist_m, water_name_1km, lakes_6km, land_status_cpcad, trees_qc_stand, detail, source_url, why.
- `scripts/`:
  - `osm_survey.py` extracts features from the provincial OSM PBFs.
  - `pool_water.py` measures the distance to a CanVec waterbody_50k polygon. It renders the WMS at 2 m/px over a 300 m window, so 150 m is the farthest it can measure.
  - `onqc_line.py` and `line_cross.py` find where the Ontario-Quebec boundary meets a shore. They use the OSM admin_level=4 ways, sampled every 8 m, against WMS tiles at 5 m/px.
  - `enrich.py` and `name2.py` add CGNDB names, CPCAD status and the Quebec forest stand.
  - `rank.py` scores the rows and writes the CSV.
- `raw/` holds the OSM extracts, the water cache, the boundary geometry and the line crossings.

## Method and counts
1. **OSM** (openstreetmap.fr / Geofabrik provincial extracts already on disk, dated about 11 Nov 2026). Rows in ON, QC, NB and MB tagged man_made=survey_point, historic=boundary_stone/milestone, boundary=marker or marker=*, or with names matching meridian/boundary/borne terms. Extracted rows: ON 544, QC 7,045, NB 1,381, MB 900.
   - Of these, 4,245 are International Boundary Commission (IBC) monuments and turning points: ON 141, QC 4,104.
   - Outside the IBC set, the only ON/QC boundary stones are:
     - one untagged Ontario-Quebec stone near Pointe-Fortune (n331754732);
     - 15 untagged `historic=boundary_stone` vertices on park and hunting-zone boundaries in Mauricie and the Laurentides (Mont-Tremblant, Rouge-Matawin, the Mazana and Normandie ZECs). The mapper KarolaneLC added them in Jan 2023, with the changeset comment "Zone de chasse à l'original 10 réserve faunique Matawin", source "Avenza Map". **Low confidence that these are physical bornes.**
     - 2 more untagged stones mapped in 2025.
   - OSM has **no** meridian, base-line or township-corner posts in ON/QC, and no Ontario-Quebec interprovincial mileposts.
2. **Pool sent to the water test:** 4,274 ON/QC features. 282 lie within 100 m of a CanVec waterbody. I then removed the water-boundary "Turning Points", which are points in the water rather than standing posts, and kept **151 physical monuments within 100 m of water**, plus the Pointe-Fortune stone, which is more than 150 m from water.
3. **Ontario-Quebec interprovincial line (derived):**
   - North of Lake Timiskaming, the line leaves the water at **47.561547, -79.517584**, which is the head of the lake. From there it runs due north at about 79°31'03" W.
   - It meets water 173 times up to James Bay. I kept 41 points where it crosses a lake or a span of 400 m or more. These include Lake Abitibi, where it passes the CGNDB names "Boundary Bay / Baie Boundary" and "Pointe Boundary", and also Lac Pontleroy, Lac Raven, "Boundary Lakes / Lacs de la Frontière", Ross Lake, Lac Hauteville, Lac Clarice, Lac Bill, Lac Kingroy and Lac Devé/Burel.
   - On the southern 1860 line, the land boundary leaves Lake St. Francis at **45.205229, -74.343061**, just west of the Rivière Beaudette.
   - **These are INFERRED shore-crossing points, not documented monuments.** Surveyors usually set posts where a line meets a shore, but no open source in this sweep gives a monument at any of these points.
4. **Enrichment:**
   - CGNDB water names within 1 km, and lakes within 6 km.
   - CPCAD protected-area status.
   - Quebec forest stands from the MRNF WMS `ori_pee_close_scale`. I quote `gr_ess_desc` and the stand annotation.
   - Ontario stands were **not checked**, because I found no open source.
5. **Score:**
   - +3 physical IBC or interprovincial monument (+1 for an undescribed stone or an inferred point)
   - +2 if within 25 m of water, +1 if within 100 m
   - +1 for a named lake nearby, −1 if the only named water is a river or stream
   - +2 Canadian Shield (rough box test: NW Ontario west of 88° W, the north line, Laurentians/Mauricie)
   - +1 if the QC stand has pine, cedar (thuya), birch or hemlock
   - +1 for any CPCAD protected area

## Top candidates (physical monuments first)
| # | Monument | lat, lon | Water | Land | Trees | Notes |
|---|---|---|---|---|---|---|
| 1 | IBC Monument 7 (TP 1161), 1917 | 48.103948, -90.303796 | 11 m; Watap Lake (CGNDB, within 1 km) | La Verendrye Provincial Park (Waterway Class), Ontario | not checked | Pigeon River / Boundary Waters, on the Shield. https://www.openstreetmap.org/node/331817757 |
| 2 | IBC Monument 9 (TP 1163), obelisk, 1917 | 48.102556, -90.298077 | 5 m; Watap Lake centroid 0.9 km | La Verendrye PP (Waterway) | not checked | https://www.openstreetmap.org/node/331817762 |
| 3 | IBC Monument 4 (TP 982), 1917 | 48.101587, -90.567402 | 15 m; South Lake / Little North Lake centroids 2.3–3.0 km | La Verendrye PP (Waterway) | not checked | Close to the North Lake / South Lake height of land; not verified on the ground. https://www.openstreetmap.org/node/331818046 |
| 4 | IBC Monument 6 (TP 984), 1917 | 48.098801, -90.564448 | 15 m | La Verendrye PP (Waterway) | not checked | https://www.openstreetmap.org/node/331818044 |
| 5 | IBC Monument 215, obelisk, 1845 | 47.161513, -69.529334 | 10 m; Lac de l'Est centroid 3.1 km | CPCAD "Land set aside Lac-de-l'Est" (MRNF) | QC stand: cédrière à thuyas occidentaux avec sapins baumiers | Appalachians, not the Shield. https://www.openstreetmap.org/node/1322238387 |
| 6 | IBC Monument 214, obelisk, 1845 | 47.167748, -69.523006 | 16 m | same | cédrière à thuyas et sapins avec bouleaux jaunes | https://www.openstreetmap.org/node/1322238308 |
| 7 | OSM boundary_stone (no description) | 46.895207, -74.311392 | 1 m; Lac du Parc | not in CPCAD at this point. It sits on a hunting-zone or wildlife-reserve boundary vertex. | sapinière à sapins baumiers avec bouleaux à papier | On the Shield. Unverified whether a physical borne exists. https://www.openstreetmap.org/node/5402887400 |
| 8 | IBC Monument 570, obelisk, 1845 | 45.005292, -72.210637 | 27 m; Baie Reid (BAY) | Proposed Michael-Dunn Biodiversity Reserve | prucheraie à pruches avec **pins blancs** | Appalachians. https://www.openstreetmap.org/node/1218321370 |
| 9 | IBC Monument 540, obelisk, 1845 | 45.007629, -71.913981 | 5 m; Étang Line / Étang Duck | — | no species group | https://www.openstreetmap.org/node/1216933551 |
| 10 | IBC Monuments 1 and 3 (TP 766/768), 1916 | 48.188056, -91.051938 and 48.18875, -91.048632 | 51 and 62 m; Swamp Lake centroid 1 km | not in CPCAD | not checked | CGNDB "Monument Portage" (ROAD, 48.1886111, -91.0502777) is beside them. https://www.openstreetmap.org/node/331843610 |

Other notable entries:
- OSM boundary_stone at 47.234055, -74.655487: 94 m from Lac André, in a QC stand of **Pinède à pins gris**, on the Shield. It has no description.
- IBC Monuments 329.18–329.22 by Lac Wilson: red maple and paper birch stands.
- IBC Monument 345.25 by Lac Clem.
- IBC Monument 314 by Petit lac Saint-Jean.

## Inferred interprovincial shore points worth a document check
- **Head of Lake Timiskaming (start of the due-north line):** 47.561547, -79.517584. The nearest CGNDB names are Chenal du Diable and Baie Paulson. This is the only "initial point" on the ON-QC line.
- **Lake Abitibi crossings:**
  - south shore 48.606487, -79.517433, near ON "Boundary Bay" FAKVI (48.61808, -79.52819);
  - "Pointe Boundary" QC EFPYX (48.655027, -79.516075), which the line crosses between 48.6513 and 48.6552.
  Lake Abitibi is large and shallow, so it is not obviously "calm".
- **Lac Kingroy / Lac Numéro Un:** 49.712325, -79.517059 and 49.724192, -79.517052, inside the Proposed Anneaux-Forestiers Biodiversity Reserve.
- **South end of the 1860 Fletcher line on Lake St. Francis:** 45.205229, -74.343061. Cornwall Free News reports a surviving marker "closest to the St. Lawrence River, just west of River Beaudette", with no coordinates. The land here is St. Lawrence Lowlands farmland, not the Shield.

## What R-1810 already holds, and corrections
I read R-1810 and the 25 rows of GCTH.db `v12__survey_lines_commemorated` read-only.
- Salter's Meridian plaque: 46.4042, -81.1821.
- Niven's Meridian plaque: 49.058733, -81.07415.
- DLS meridians, the Principal Meridian Cairn, IBC statistics, Point Roberts, and the ON-MB, MB-SK (Kamuchawie Lake) and ON-QC lines.

Correction to R-1810 row 19: it says "the Commission publishes no open coordinate list". In fact, OSM carries IBC monument numbers, types (obelisk, disk, tablet) and dates, citing IBC coordinate pages. The IBC "Digital boundary" page is live at https://www.internationalboundarycommission.org/en/maps-coordinates/coordinates.php, but the old per-section URLs cited in OSM (for example .../coordinates/Highlands.htm) now return 404.

## Gaps (could not reach or not available openly)
- **Salter's 1856 meridian and Niven's 1896 meridian:** no published monument coordinates and no published line longitude, so I computed no lake crossings for them rather than invent a line. The CGNDB has suggestive names: Baseline Lake, Sudbury (46.9441, -81.0704); Meridian Bay, Creek, Falls and Lake in Kenora District; and Niven Lake, Cochrane (49.67681, -82.65143). None of these is tied to a monument.
- **Ontario-Quebec north line monuments and mileposts** (1874 provisional line; later surveys): no open coordinate list. The 1922 Mercier/Wilkie and 2011 rehabilitations are documented only for the southern 43 km line. That line has 46 stones of 1860, 43 recovered in 1922, and 2011 granite markers inscribed ONTARIO / QUEBEC, number and year. Source: https://cornwallfreenews.com/?p=37714
- **krcmar.ca** survey history articles ("Boundary Monuments" 1991, "Surveyors in the Exploration of North Eastern Ontario" 1977, "Survey Post Number One" 1960): the TLS certificate failed on the bare domain, and the www host returned 404. Not read.
- **hmdb.org** returned 403, so I could not read markers m=217889 (Tunis, Cochrane District), 261993 or 289843.
- **ON-MB boundary monuments** are numbered and inscribed ONTARIO on the SE face and MANITOBA on the NW face (R.S.M. 1990 c. 244), but there is no open coordinate list and none is in OSM. **QC-NB interprovincial monuments:** none in OSM, and no open list was found.
- **Canada Lands Survey System:** monument positions are only in the survey plans (CLSR), with no point dataset. **Quebec cadastral and primitive-survey bornes:** no open point dataset was found on Données Québec. Quebec geodetic data was covered in an earlier sweep.
- **Ontario forest stands:** not checked. **Calmness** of the water was not assessed beyond the lake/river label.
- **Water distance:** CanVec waterbody_50k at 1:50k includes wide rivers, so "water" is not always a lake. Distances are to the 1:50k polygon edge, accurate to about ±10–20 m.
