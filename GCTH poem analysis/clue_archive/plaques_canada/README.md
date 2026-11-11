# Plaques, cairns, monuments and interpretive markers near iron/magnetite and water (Canada)

Run date: 2026-11-11. This follows the survey-marker searches in `shoremk/` and `shoremk_canada/`. Here the search covers non-survey markers: plaques, cairns, memorials and monuments, interpretive boards, mine shafts and adits, and heritage-register places.

## Outputs
- `candidates.csv`: 342 rows, 275 distinct sites. Each row is a marker that is within 60 m of CanVec water and either within 1.5 km of an iron/magnetite occurrence (101 rows) or has a keyword in its text. The file is sorted by `score`.
  - `why` lists the reasons for each score.
  - Rows from different sources that are within 60 m of each other share a `site_group`.
- `all_kept_unfiltered.csv`: 1,282 markers before the water filter (within 1.5 km of an occurrence, or with a keyword in the text), with the water distances.
- `data_keep.json`, `data_water_cache.json`, `data_enriched.json`, `counts_all.json`: intermediate files.
- `raw/`: source pulls (listed below).
- `scripts/`: `osm_extract2.py`, `hp_search.py`, `hp_detail.py`, `hp_retry.py`, `mhs_fetch.py`, `rtp_fetch.py`, `assemble.py`, `water.py`, `rank.py`, `geo.py`.
  - `water.py` reuses `shoremk_canada/scripts/wmsdist.py` (CanVec WMS) and `agq.py`.

## Iron/magnetite occurrences
There are 7,217 occurrences in total:
- `shoremk/data/iron.json`: QC + ON, 2,202 occurrences.
- `shoremk_canada/iron_canada.json`: the other provinces and territories, 5,015 occurrences.

`mag=True` marks an occurrence that names magnetite.

Many occurrences list iron only as a secondary commodity (for example, Ni-Cu or Au deposits). The `iron_prim` column shows the primary commodity.

## Marker sources
| Source | How it was accessed | Records loaded | Kept (within 1.5 km of an occurrence, or keyword) | Candidates (water ≤ 60 m) |
|---|---|---|---|---|
| OpenStreetMap | Provincial .osm.pbf extracts from download.openstreetmap.fr (dated 2026-11-11), filtered locally with pyosmium. Tags: historic=memorial/monument/marker/wayside_shrine/mine/mine_shaft/heritage/boundary_stone/plaque/cairn; memorial=plaque/cairn/stone; man_made=cairn/mineshaft/adit; tourism=information + information=board/plaque. Nodes and ways (way centroid) | 17,817 | 545 | 159 |
| Canadian Register of Historic Places (historicplaces.ca) | Public keyword search (mine, iron, ore, fer, compass, mining, forge, minerai, iron ore) with results per page set to "All". The search is a substring match, so the union of 12,745 places is close to the whole register. Detail pages (description and heritage value) were fetched for 224 places near occurrences, with keyword names, or matched to Parks Canada sites | 12,745 | 223 | 52 |
| Read the Plaque (readtheplaque.com) | Public `/api/plaques/geo` (25,196 plaques worldwide), restricted to those inside Canadian province polygons. `/api/plaques/{id}` was fetched for the text | 3,093 | 189 | 39 |
| Manitoba Historical Society, Historic Sites of Manitoba | mb1870.org map search for "Monument" (2,660 sites). Each site page gives its coordinates and description | 2,527 with coordinates | 47 | 12 |
| Quebec MCC Répertoire du patrimoine culturel (Données Québec) | Open-data CSVs: sites and immeubles that are classés, cités or déclarés, plus the national site | 1,573 | 162 | 46 |
| Ontario Heritage Trust provincial plaques | Public `maps.heritagetrust.on.ca/api/locations` (1,172 plaques, 1,161 with coordinates, full plaque text) | 1,161 | 72 | 17 |
| BC Stop of Interest signs | DataBC CSV (July 2022), with sign text | 174 | 44 | 17 |
| Parks Canada Directory of Federal Heritage Designations | open.canada.ca CSV as of 2026-03-31 (3,889 designations, with inscriptions). It has no coordinates, so it was used only to find the 87 designations whose inscriptions mention mining or iron, and the 31 matching National Historic Sites were linked through CRHP coordinates | 3,889 | (via CRHP) | (via CRHP) |

Candidates by province: BC 126, ON 83, QC 78, MB 13, NB 11, AB 9, NS 9, NL 6, NT 3, YT 2, PE 1, NU 1.

Candidates within 1.5 km of an occurrence: QC 31, ON 30, BC 21, NB 9, NL 4, NS 4, AB 1, MB 1.

19 candidates are within 1 km of a magnetite-flagged occurrence. 40 candidates fall inside a CPCAD protected area.

## Enrichment
- **Water**: CanVec 1:50k WMS distance to the nearest water pixel, using the same method as `shoremk_canada`. Three layers were measured: `waterbody_50k`, `watercourse_50k` and `shoreline_50k`.
  - **Caution**: `shoreline_50k` also draws inland lake shorelines, so the `marine` column is not reliable.
  - 1.4 m means the point plots on or inside the water polygon.
- **Road**: CanVec `road_segment_50k` within 300 m (`road_m`), else within 2 km (`road2k_m`). Forest and trail roads are often missing from CanVec.
- **Protected area**: CPCAD point-in-polygon (`land`). An empty value means the point is not in CPCAD. That does not mean it is private: municipal parks and Crown land are not in CPCAD.
- **Water name**: CGNDB, nearest named water feature within 2 km.
- **Keywords**: iron, magnetite, magnetic, lodestone, compass, ore, mine/mining/miner, furnace, forge, plus the French terms fer, minerai, aimant, boussole, magnétite, ferrifère and haut fourneau.
  - "chemin de fer", "fer à cheval" and "fer forgé" are excluded.
  - Matches on "ore" or "mine" are often incidental.

## Scoring (rank.py)
- **Water**: inland water ≤ 15 m +4, ≤ 30 m +3, ≤ 60 m +2. Marine coastline only: +1.
- **Iron**: occurrence ≤ 1 km +3, ≤ 1.5 km +2. Iron or magnetite as the primary commodity +1.
- **Magnetite**: magnetite-flagged occurrence ≤ 1 km +2, ≤ 1.5 km +1.
- **Marker type**: plaque, cairn, memorial or marker +2 (cairn +1 more). Interpretive board +1.
- **Text**: mentions iron, magnetite, compass or lodestone (strong term) +3. Any other keyword +1.
- **Land**: in a CPCAD protected area +2.
- **Road**: road ≤ 25 m (roadside) −1. Road 25–300 m (walk-in) +1. No road within 2 km −1. BC highway Stop of Interest sign −1.

## Gaps and unreachable sources
- **Overpass API**: overpass-api.de, z./lz4. mirrors, kumi.systems, private.coffee, osm.jp, openstreetmap.ru and maps.mail.ru all reset or timed out from the container. The user's Mac (LMCP `run_terminal_command`) was not reachable: the first call timed out, and the next said "LMCP app is not running on this device (no active tunnel)". The OSM data came from the openstreetmap.fr provincial extracts instead, so it covers the same tags.
- **ohsome API (HeiGIT)**: `elements/count` works, but `elements/centroid` and `elements/geometry` return HTTP 403. These were not used further.
- **HMDB (hmdb.org)**: Cloudflare "Just a moment" challenge (HTTP 403). Not accessed. HMDB Canada entries are therefore missing. Many of them duplicate OHT, RTP or Parks Canada plaques.
- **Parks Canada plaque locations**: the designation dataset has inscriptions but no coordinates. Locations are known only where a CRHP record exists. HSMBC plaques that stand away from the designated place are not located.
- **Quebec commemorative plaques ("commémorations")**: the Répertoire lists plaques and commemorations on its website, but they are not in the open data. Only designated properties and sites were used.
- **Not searched (no bulk open data with coordinates found in the time available)**: Ontario municipal plaque programs, Saskatchewan and Alberta provincial historic markers, NS, NB and NL provincial plaque programs, Yukon and NWT.
- **Manitoba Historical Society**: 133 of the 2,660 monument pages have no coordinates. Some page texts include page-script junk (for example, Muck Car Monument).
- **CanVec water**: small ponds can be missing. Distances are ±2 m pixel precision, plus the position error of the marker itself.
- **Read the Plaque**: for overseas or US border areas, Canada membership comes from Natural Earth 1:50m province polygons.
