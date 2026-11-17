# Setter-habit filter (written 17 Nov 2026, BEFORE it was applied to any candidate area)

Source table: `find_sites.csv` (8 published find sites; Chibougamau found but unpublished, not scored).
Bar set by Max's brief: a feature enters the filter only if it holds at **7 or more of the 8** sites.
"Holds" counts a cell graded sourced or inferred as yes; "likely" counts as yes; unknown counts as **not** holding.

## Tally (from find_sites.csv)

| Feature | yes | no | unknown | Passes 7/8? |
|---|---|---|---|---|
| Publicly accessible land | 8 (2 sourced park, 6 inferred/rule) | 0 | 0 | **YES** |
| Drivable road or parking <= 1 km | 7 (+ Toronto: service road only, car-free island) | 0 | 0 (Dover inferred) | **YES** (7 strict, 8 loose) |
| Water of any kind <= 500 m (in view) | 8 (Dover "likely") | 0 | 0 | **YES** (7 firm) |
| Named landmark at the site | 8 (Dover/Toronto only town/island level) | 0 | 0 | yes, but not mappable; not used |
| Water of any kind <= 100 m | 6 at best (3 firm, 3 likely/possible) | 1 (Cobalt) | 1 | no |
| **Still water (lake/pond) <= 100 m** | 1 likely (Toronto) | 6 | 1 | **no: 1/8. Lakes are NOT a bonus-setter habit** |
| Raised structure (lookout/platform/structure) at the box | 4 sourced (Cobalt, Britannia, Bathurst, Cape d'Or) | 1 sourced (Kleanza: a hole) | 3 | no (4/8; 4 of 5 known) |
| Box concealed in a cavity / under something | 4-5 | 0 | 3-4 | no (but 0 known exceptions) |
| Trail or path <= 100 m | 5 (1 sourced) | 1 (Cobalt) | 2 | no (5/8) |
| Sign, plaque or marker <= 50 m | 0 | 0 | 8 | no (nothing known) |
| Tree cover type | varies (boreal, coastal conifer, Acadian, urban park) | | | no common type |
| Distance from a city of 100k+ | 4 to 1,863 km (median ~250) | | | no habit |

## The filter (hard, >= 7/8)

- **H1 Public land.** Proxy used on the map: inside an OSM protected area / national or provincial park / nature reserve / municipal park polygon, or inside a CPCAD polygon. (This is stricter than "publicly accessible", which is what the find sites show.)
- **H2 Drivable road or parking within 1 km** (OSM highway motorway..service/unclassified/residential, or amenity=parking).
- **H3 Water within 500 m.**

That is all the 7/8 bar allows. It is weak: most public land on the Shield passes it.

## Added for the Grand Prize (NOT a setter habit; carried over from the poem reading, region note P2)

- **G1 Still water (lake, pond, reservoir) within 100 m** of the spot. This replaces H3 in practice. The find sites do **not** support it (1/8); it comes only from "calm mirror" / lakeshore in the GP text.

## Candidate unit and soft habits (used to enumerate and rank, not as 7/8 gates)

Enumerated per Max's brief: an OSM **raised or built structure** at which a box could be tucked:
- Class A: tourism=viewpoint, observation tower, boardwalk (bridge/footway=boardwalk, or wooden path bridge), viewing platform / bird hide (man_made=platform, leisure=bird_hide).
- Class B: dock / pier / jetty / marina / slipway, footbridge on a path.
- Benches are counted per region but not listed (too many, too weak).

Pre-registered ranking points (fixed before looking):
- +2 class A, +1 class B (raised structure: 4 of 5 known sites)
- +1 a trail or path within 100 m (5 of 6 known sites); +1 more if that trail is marked (in a hiking route relation, named, or has trail-marking tags)
- +1 parking within 500 m
- +1 OSM marker/sign/plaque/info board within 50 m (GP "standing marker" reading; 0 known at find sites, so a GP feature, not a habit)
- Final signal only (tie-break within equal scores, and shown separately): iron occurrence within 5 km (+0.5), magnetite occurrence within 2 km (+0.5), from shoremk/data/iron.json (ON-MDI, ON-AMIS, QC-SIGEOM).

## Fair baseline for region comparison

Counts per region are reported (a) per 1,000 km^2 of the region polygon on land in the right province, and (b) per 100 OSM still-water polygons >= 1 ha in the region. A region "has an excess" only if it is above the pooled rate on both.

## Known limits written in advance

- Every map feature comes from OSM (Geofabrik extract of 11 Nov 2026). OSM tags viewpoints, boardwalks and docks unevenly; regions mapped more heavily will look richer. The per-lake baseline only partly corrects this.
- The habit evidence is n = 8, with 3 sites at town/island level or project-identified points.
- Region polygons are hand-drawn approximations of the shortlist areas, not the Shield boundary.
