# Setter-habit calibration on the found bonus caches, applied to the GP region shortlist (desk, 17 Nov 2026)

Follows section 5 of `region/GCTH_GP_region_narrowing_DESK_17Nov2026.md`. Desk only; nothing visited. No record rows written; nothing merged.

## Files
- `find_sites.csv`: the 8 published find sites, each feature cell = value + grade (sourced / inferred / unknown) + note. Chibougamau listed as row S9, not scored (found, site unpublished).
- `filter.md`: the tally and the filter, written before any candidate area was looked at (file time 04:08 UTC; candidate run started after).
- `candidates.csv`: 209 candidate spots (after 150 m de-duplication), ranked; `site_group` = lake @ park.
- `work/`: OSM extracts (pickles), `site_osm_metrics.json`, `wms_sites.json` (CanVec 50k WMS + CPCAD), `summary.json`, `cpcad_cache.json`, `top15.md`.
- `scripts/`: `extract.py` (pyosmium over the Geofabrik .pbf of 11 Nov 2026), `sites.py`, `score_sites.py`, `wms_sites.py`, `write_sites.py`, `candidates.py`, `finalize.py`.

## Step 1: find sites (9 found, 8 published)
Record R-0024 lists nine found caches; TNM's 1-year recap (Nov 2026) confirms the live four are QC (Val-d'Or), SK, MB, Sudbury. Chibougamau was found but the winners withheld the site (R-1276); not scored.

| # | Bonus | Best-known site | Point used | Grade of the point |
|---|---|---|---|---|
| S1 | Dawson | Bonanza Creek discovery claim site | 63.9168, -139.317 (Wikipedia "Discovery Claim") | official name; point +-600 m. The record's 63.916, -139.262 is an area centroid 2.7 km east (R-0828) |
| S2 | Cobalt | Nipissing Hill Lookout (TNM: "near Nipissing Falls") | 47.3913, -79.6801 | finder: "at the lookout"; point is the project geocode |
| S3 | Golden Triangle | Kleanza Creek PP, a hole by the park's only trail | 54.59767, -128.3962 | official park; spot within park unknown (+-1.5 km) |
| S4 | Newfoundland (Argentia clue) | Dover, NL | 48.887, -53.954 | town level only; Dover Fault site is circular |
| S5 | Southern BC | "a lookout near the Britannia Mine Museum" | 49.63455, -123.21023 | lookout class sourced; which lookout is project-identified |
| S6 | Toronto | Toronto Island | 43.62, -79.378 | island level only |
| S7 | Bathurst NB | beneath an old hydro structure, Tetagouche Falls | 47.617286, -65.825141 | official |
| S8 | Nova Scotia | under a viewing platform by the Cape d'Or lighthouse | 45.2914, -64.7740 | official + finders |

## Step 2-3: what the 8 sites share (full table in find_sites.csv)
Holds at >= 7/8: public access (8), road or parking <= 1 km (7 strict; Toronto has only a service road), water of some kind <= 500 m (8, Dover "likely").
Fails: **still water (lake/pond) <= 100 m: 1/8 (Toronto, likely)**; raised structure at the box 4/8 (4 of 5 known; Kleanza was a hole); trail <= 100 m 5/8; sign/marker <= 50 m 0 known; no common tree cover; distance to a 100k city 4-1,863 km.

**Main finding:** the bonus setter's only firm habits are "public, drive-up, by water, at a named landmark". The lakeshore part of the GP picture does not come from the bonus finds (they are creeks, falls, sea cliffs, a canyon, a hill lookout). "Box under a raised structure" is a real but partial pattern (Cobalt, Britannia, Bathurst, Cape d'Or). So the filter below is weak and cannot by itself rank regions.

## Step 4: application
Candidate = OSM viewpoint / observation tower / boardwalk / viewing platform / bird hide (class A) or dock / pier / footbridge (class B), within 100 m of a lake or pond (GP add-on, not a habit), road or parking <= 1 km, inside public land (OSM park/protected polygon or CPCAD). After the first run I dropped CPCAD-only habitat designations (deer yards, waterfowl areas), privately protected areas, research stations, scout/private reserves, access=private, and docks whose only "public" evidence is a canal/waterway-class corridor polygon: the public-land proxy had let them in. That cleanup was post hoc; the first-run counts are in this file's table for comparison.

| Region | land km2 | lakes >= 1 ha (OSM) | candidates (first run) | candidates (clean) | distinct lake@park groups | class A | score >= 5 | per 1,000 km2 | per 100 lakes |
|---|---|---|---|---|---|---|---|---|---|
| R1 eastern ON Shield edge | 11,762 | 9,052 | 90 | 58 | 33 | 34 | 15 | 4.93 | 0.64 |
| R2 Outaouais-Laurentians QC | 19,552 | 7,984 | 132 | 109 | 82 | 40 | 24 | 5.57 | 1.37 |
| R3 Nipissing-Temagami-Timiskaming | 30,271 | 12,531 | 58 | 42 | 26 | 4 | 0 | 1.39 | 0.34 |
| pooled | | | | 209 | 141 | | | 3.39 | 0.71 |

Pre-registered rule: excess on both baselines = R2 only. R1 is above on area, below per lake. R3 is below on both. Read with care: R2 has 1,408 mapped structures and 386 benches against R1's 493 and 61, so OSM mapping density explains much of the gap. Of the R3 candidates, 36 of 42 are docks; only 4 class-A spots (Restoule PP, 3 viewpoints; Restoule sits at the south edge of the R3 box, below Lake Nipissing). On high-scoring (>= 5) spots per 1,000 km2, R1 (1.28) and R2 (1.23) are level.

Iron signal (final only): candidates with an Fe occurrence <= 5 km: R1 27 / R2 19 / R3 5; magnetite <= 2 km: R1 6 / R2 8 / R3 0.

Top 15 distinct lake@park sites: `top15.md` (also in `work/`, and in the summary note).

## Limits
1. n = 8 habit sites, 3 of them town/island-level or project-identified points; many cells inferred from OSM around a point that may be 0.6-3 km off.
2. The 7/8 filter is weak (public + road + water). The candidate list is driven mainly by the GP "lake" reading and by what OSM happens to tag.
3. OSM coverage is uneven (Gatineau Park and the Laurentians are heavily mapped). Missing big-lake polygons: Lake Timiskaming and Lake Ontario did not appear as still-water polygons in the extract, so shore spots on them are missed.
4. Region polygons are hand-drawn approximations, not the Shield boundary; R1's south edge brushes Rice Lake / lowlands, R3 reaches south to Restoule.
5. "Public land" is a proxy (OSM + CPCAD); municipal parks without polygons are missed; some CPCAD polygons are corridors.
6. Markers within 50 m depend on OSM information boards; standing survey or boundary markers are not in this layer.
7. The candidate rule would itself miss 7 of the 8 bonus sites (no lake). It describes the GP reading, not the setter's record.
