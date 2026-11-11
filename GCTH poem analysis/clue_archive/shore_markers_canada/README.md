# Near-shore survey markers near iron/magnetite occurrences: rest of Canada (excluding QC/ON)

Run date: 2026-11-11. This extends `shoremk/` (QC + ON) to BC, AB, SK, MB, NB, NS, NL, YT and NT. PE and NU are not covered; see the gaps below.

## Outputs
- `iron_canada.json`: 5,015 iron/magnetite occurrences in the same format as `shoremk/data/iron.json`, plus a `prov` field. `mag=True` means magnetite is named in the record.
- `nearshore_markers_canada.csv`: 880 markers that are within 3 km of an occurrence and within 40 m of CanVec water.
  - The first 20 columns are the same as in `shoremk/nearshore_markers.csv`.
  - Added columns: `prov`, `mag_occ_d_m`/`mag_occ` (nearest occurrence flagged as magnetite), `road_m` (CanVec road within 300 m), `road_cl_desc_m` (distance to road centre line, parsed from the report), `road2k_m`, `rail`, `marine`, `has_desc`, `rock`, `post`, `hwy_words`, `alt_id`, `score`, `why`, `report_url`.
  - The file is sorted by `score`. `why` gives the reasons for each score.
- `data_*.json`: intermediate files (raw marker pulls, the 3 km candidate list, shore distances, enriched records).
- `scripts/`: the scripts for this run. They adapt `shoremk_scripts/`.

## Sources used

### Iron/magnetite occurrences
| Prov | Source | Filter | Records (magnetite-flagged) |
|---|---|---|---|
| BC | BC MINFILE (openmaps.gov.bc.ca WFS `WHSE_MINERAL_TENURE.MINFIL_MINERAL_FILE`) | commodity FE or MA (MA = magnetite; MT is magnesite and was excluded) | 574 (319) |
| AB | AGS DIG 2025-0009, Mineral Occurrences of Alberta | commodity Iron, or magnetite in ore/gangue minerals | 181 (27) |
| SK | Saskatchewan Mineral Deposit Index (gis.saskatchewan.ca egis Mineral_Exploration/2) | iron in primary or associated commodities, or magnetite in host minerals | 1,421 (142) |
| MB | Manitoba GeoFile 5-2025 (Mineral Deposits Database, xlsx) | Fe in commodities, or magnetite in the description. Sample rows were grouped by MDD number; UTM14 converted to lat/lon | 1,556 (180) |
| NB | NBGS Mineral Occurrences (gis-erd-der.gnb.ca OpenData) | commodity Fe. The layer has no mineral list, so magnetite cannot be flagged | 47 (0) |
| NS | NS Mineral Occurrence Database DP ME 2 (dawson.novascotia.ca FeatureServer) | Fe in commodities, or magnetite in the mineral list | 524 (145) |
| NL | NL MODS (dnrmaps.gov.nl.ca GeoAtlas Map_Layers/3) | Iron/Magnetite/Hematite in commodities, or magnetite in ore minerals. The source stores west longitudes as positive numbers; they were made negative | 637 (521); 481 Labrador, 156 Newfoundland |
| YT | Yukon MINFILE (mapservices.gov.yk.ca GY_Geological/4) | iron or magnetite in MAIN_COMMODITY. Only the main commodity is published, so coverage is undercounted | 40 (6) |
| NT | NTGS Mineral Showings 2024 (services3.arcgis.com NWT_Mineral_Showings_2024) | Iron in commodities A to E, or magnetite in mineralization | 35 (0) |

### Survey markers
- **NRCan passive control**: `getStations.php`, networks cbn, pvc, hc and hp3d, queried over 0.25° cells around the occurrences. 1,574 cells for the first run, plus the NL cells after the longitude fix. 12,298 station rows were returned with no errors.
- **BC**: geodetic control monuments from openmaps WFS `WHSE_REFERENCE.SRV_GEODETIC_CONTROL_SP`, 64,003 points (the same data MASCOT/GeoNetBC uses). Coordinates and tablet marking only. The GeoNetBC detail page is an interactive Blazor app, so no monument descriptions could be retrieved.
- **NS**: NSCRS stations from `nsgiwa2.novascotia.ca LOC_NSCRS_Stations_WM84`, layers 0, 1 and 4, 24,869 rows. Includes DESCRIPT and MONTYPE, but DESCRIPT is blank for most NSCCS monuments.
- **AB**: ASCM from the public `services.arcgis.com/.../ASCM/FeatureServer`, queried within 3.2 km of each AB occurrence. Only 2 found.
- A provincial marker was dropped as a duplicate when it sat within 10 m of an NRCan marker. Its ID was kept in `alt_id`.

### Hydro, roads, names and land status
- **Hydro**: NRCan CanVec 1:50k WMS (`maps.geogratis.gc.ca/wms/canvec_en`), layers `waterbody_50k` (lakes and double-line rivers) and `watercourse_50k` (single-line streams).
  - Each layer was rendered as a 600 × 600 m PNG at 2 m per pixel around the marker. The distance is from the marker to the nearest water pixel.
  - A value of 1.4 m means the marker plots on or inside the water polygon.
  - Check against 12 QC/ON markers from the earlier run: most agree within about 0 to 10 m. A few small ponds that are in the provincial layers are missing from CanVec.
- **Roads**: CanVec `road_segment_50k`, rendered the same way within 300 m and within 2 km.
- **Water names**: CGNDB geonames API, nearest named lake, river, bay or channel feature within 2 km. This is a hint only.
- **Protected areas**: CPCAD point-in-polygon at `maps-cartes.ec.gc.ca`.
- **Monument descriptions**: NRCan station report pages (`report-rapport.php`).

## Counts per province
| Prov | Occurrences | Markers within 3 km (by source) | Within 40 m of water | With a monument description |
|---|---|---|---|---|
| BC | 574 | 1,497 (NRCan 317, BC-GCM 1,180) | 343 | 79 |
| AB | 181 | 34 (NRCan 29, BC 3, ASCM 2) | 5 | 4 |
| SK | 1,421 | 76 | 6 | 6 |
| MB | 1,556 | 249 | 37 | 37 |
| NB | 47 | 140 | 30 | 30 |
| NS | 524 | 3,190 (NRCan 501, NSCRS 2,689) | 416 | 133 (NSCRS rows count only if DESCRIPT has text) |
| NL | 637 | 158 | 40 | 40 |
| YT | 40 | 21 | 3 | 3 |
| NT | 35 | 3 | 0 | 0 |
| PE | 0 (no source) | n/a | n/a | n/a |
| NU | 0 (no source) | n/a | n/a | n/a |

Markers are assigned to the province of their nearest occurrence. A few markers near a border are therefore counted under the neighbouring province.

### Territories
- **YT**: 40 occurrences. Only 21 markers are within 3 km, mostly around Whitehorse (Whitehorse Copper belt). 3 are near shore.
- **NT**: 35 iron showings, all north of 60°. Only 3 NRCan markers are within 3 km and none are near water. Almost no NT iron showings are near the road network.
- **NU**: not covered.

## Ranking
The score is additive. `why` lists every term that applied.

Points added:
- +2: within 40 m of a lake or river polygon. +1 instead if only within 40 m of a single-line stream.
- +3: rock, outcrop or boulder monument, from the report text (English or French).
- +1: post, pipe or rod type monument, when it is not on a structure.
- +1: off-road, meaning the report gives more than 30 m from a road centre line, or CanVec shows no road within 60 m but a road within 2 km.
- +1: access is "car + walk of 50 to 500 m".
- +3: a magnetite occurrence within 1 km. +1 instead if only an iron occurrence within 1 km.
- +1: inside a CPCAD protected area.

Points subtracted:
- −2: monument on a structure (bridge, abutment, culvert, wall, dam, church and similar).
- −1: highway or roadside wording in the report.
- −1: the report puts the marker within 30 m or less of a road centre line.
- −1: railway setting.
- −1: boat or air access only.
- −3: marine or tidal wording, in the report or the CGNDB name.
- −3: no monument description available.
- −3: status destroyed, bad or not found.

## Gaps and caveats
- **Nunavut (NUMIN)**: the only access is the legacy form app at nunavutgeoscience.ca/apps/showing. No bulk download or REST service was found. Not covered.
- **PEI**: no open mineral-occurrence database with iron records was found. PE is sedimentary bedrock with no Shield. Not covered.
- **BC GeoNetBC/MASCOT detail pages**: interactive app, and the old MASCOT URL is under `/protected/`. BC-GCM markers have coordinates and tablet IDs only, with no monument type and no description. 265 of the BC near-shore survivors are BC-GCM points without a description. They score −3 and have to be checked by hand at the `report_url`.
- **Alberta ASCM**: the public FeatureServer was used. The ARLO PDF descriptions were not fetched because ARLO is a registry application.
- **NB control (SNB "NB Control Network" web app)**: no open bulk service was found. Not used. NB therefore uses NRCan markers only.
- **NS NSCRS**: DESCRIPT is empty for most NSCCS monuments. The MONTYPE codes are not decoded.
- **NB and NT magnetite flags**: the source layers do not list minerals, so `mag=False` there means unknown, not absent.
- **Marine shore**: CanVec waterbody includes ocean and tidal inlets, and there is no marine/lake attribute in the WMS. The `marine` flag comes only from wording in the report or the CGNDB name, so many coastal BC and NS markers are probably marine and are not flagged.
- **NRCan PVC coordinates**: benchmark positions are often scaled from maps and can be off by tens to hundreds of metres. CanVec 1:50k also has positional error of tens of metres. Treat every distance under 40 m as approximate.
- **Road distances**: the report's centre-line distances were preferred over CanVec. CanVec road positions disagreed with the report text by up to about 100 m in some cases (for example 90C021).
- **Land tenure**: only CPCAD protected areas were checked. Provincial Crown versus private land was not checked outside the protected areas.
