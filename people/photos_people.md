# People in the archival photos: catalogue and identifications (13 Nov 2026, updated 17 Nov 2026)

Scope: archival photographs and stills in the published clue videos that show people. Modern footage of living private people (the Alamos corporate photo, organizers, winners) was not examined for identity. The full table, one row per photo or per person, is in `photos_people.csv` (44 rows). Crops are in `crops/`.

Evidence ranks used: (1) the source publication's own caption or key; (2) the source book's text naming who was present; (3) comparison with documented portraits. Rank 3 is weak evidence at these resolutions and was never treated as an identification.

## Update, 17 Nov 2026: what the local GCTH chat settled after 13 Nov

Taken from the master record (`record/GCTH_findings.csv`), rows R-2094 to R-2105, R-2165, R-2177 and R-2234. The sections below this one are the 13 Nov text, left unchanged; where they disagree, this update wins.

**Newly identified people**
- **Chibougamau ~19 s, the man at the rapid, is Peter McKenzie** (R-2096). The source is a captioned plate, "Peter McKenzie discoverer of 'gold' at Chibogamoo", in F.G. Pauli's 1907 book on his summer-1906 trip (archive.org `arecordatripthr00paulgoog`). The video shows him while the narration says "McKenzie discovered copper"; the original caption says "gold".
- **Toronto ~32 s, the speaker at the microphone, is most likely Lt-Gov. Herbert A. Bruce** (R-2165, medium confidence). The scene is the laying of the Toronto Stock Exchange cornerstone on 19 Aug 1936 (NFB stock shot 7349). The NFB record names Bruce as the man laying the stone but does not caption the speaker.
- **Grand Prize launch video ~20 s: Mine Superintendent Alfred Daviis** [sic in the record], second from right (R-2100). The photo is Galt Museum 19760210118, Lethbridge No. 10 City Drift Mine, 1909, and the archive's own caption names him.

**Photos traced, but the captions name nobody**
- **Cobalt 8.1 s:** Fig. 42a "Prospectors at Cobalt, May, 1904", in W.G. Miller's Bureau of Mines report (R-2094). The caption has been read and names no one, so the standing man stays unidentified.
- **Chibougamau ~17 s:** A.P. Low's GSC photo of 1892, "Canoe, Paint Mount, Lake Chibougamau" (R-2095; LAC MIKAN 3389528). It shows 9 men, none named, and is 11 years older than the "1903" spoken over it.
- **Saskatchewan title card:** "First Car of Potash", Colonsay, 3 Feb 1970 (R-2102). The six men are not named.
- **Val-d'Or ~30 s:** a Val-d'Or street with an M. Rabinovitch dry-goods sign, c.1935–37 (R-2103). The original photo has not been found.
- **Grand Prize launch ~18 s:** the Lethbridge City Mine, 1912 (R-2101).

**Correction**
- **Val-d'Or 4.75 s, the soup line, is not NARA 541927 itself** (R-2104). It is a companion photo of the same Capone soup kitchen in Chicago (Feb 1931) with the people standing differently, possibly Getty 615307766. Sections 4 and the CSV said NARA 541927; the CSV is now corrected.

**Still unidentified**
- **Val-d'Or camp, the animated seated man:** no change.
- **Gowganda King Edward Hotel group:**
  - Every route tried on 14 Nov came back negative or blocked (R-2120). The Archives of Ontario RG 13-30-1-10 images are not online.
  - Google Lens finds no exact match (R-2105).
  - The 15 Nov re-scan shows the second man from the left lifting his head once, at about 11.2–11.8 s (R-2177).
  - One route is still open: Peter Fancy's working files at Laurentian University Archives, fonds P230 (R-2083). It needs an in-person appointment.
- **Saskatchewan 35.4 s:** the ring-on-column monument is real, part of the photograph and not pasted in (R-2234, R-2260). It has no source yet.
- **Live-region stills:** none has an exact Google Lens match (R-2105).

## 1. Val-d'Or, 39.5–42.6 s: the Gwillim camp photograph (priority)

**Source, confirmed from the page itself:** the frontispiece of the Chibougamau Mining Commission's *Report on the geology and mineral resources of the Chibougamau region* (Quebec, 1911), Internet Archive `cu31924072684552`, leaf n13 (https://archive.org/details/cu31924072684552/page/n13/mode/1up). The printed caption reads: *"Prof. Gwillim and group of assistants and guides—Camp on Chamuchuan river."* The page carries **no key**: no left-to-right list and no numbers on the figures.

- `crops/frontispiece_full.jpg`: the plate from the book scan, which is sharper than the 698 px Commons copy and the video.
- `crops/frontispiece_seated_man_boxed.jpg`: the animated man, boxed.
- `crops/frontis_animated_seated_man_region.jpg` and `crops/frontispiece_seated_man_head_4x.jpg`: close-ups.
- `crops/valdor_39.5s_video_frame_boxed_lowres.jpg`: the project's own boxed video frame (`out4/VC_frame_boxed.png`), brought over at 256 px. I used it only to match the box to the plate.

**Locating the animated man.** I matched the video frame to the plate using fixed points: the tent pole at the left, the tree at the right edge, and the tallest man at the back right. The motion box (1008,549, 285×392 at 1920×1080) falls on the **front-row man seated on the ground just right of centre**. His knees are up and his forearms rest on them. He wears a light work shirt with a dark neckerchief. His dark hair is swept back and he is clean-shaven. The book scan shows him at about twice the video's resolution.

**Who he is: not determinable from any source.**
- Rank 1: the caption names only Gwillim and does not place him.
- Rank 2: the report names 27 people. The 19+ men in the plate are the June 1910 ascent party. That excludes Faribault, who joined on 27 July, and Levesque and Néron, who had gone ahead with the freight. It also leaves Sioui, Lavoie and Groslouis possible, since they left in July. Nothing in the text links a name to a position in the photograph.
- **Plate V cross-match, tried and failed.** Plate V (leaf n26, `crops/plateV_gwillim_bateman.jpg`) is captioned *"Professor Gwillim and Mr. Bateman at work in the sampling mill, Pointe aux Bouleaux."* The caption does not say which man is which. The left man stands under the tarp with his face in deep shadow. The right man's head is bowed over the bench (`crops/plateV_left_head.jpg`, `crops/plateV_right_head.jpg`). Neither face is clear enough to match against the frontispiece. So Plate V cannot show which figure in the frontispiece is Gwillim, and it does not identify the seated man.
- **Plate XX**, *"The Chibougamau expedition on Chamuchuan River"* (leaf n68, `crops/plateXX_expedition_canoes.jpg`), shows canoes at a distance against a wooded shore. The figures are too small to identify anyone.
- Rank 3: not run. No period portraits exist online for Gwillim or Barlow. Bateman's (a 1958 painting) and Dufresne's (late career) were taken 40+ years later. The only observation is that the seated man **looks young**. That fits the assistants (Bateman 21, Dufresne 20, Poitevin c.22) or a young canoeman, and fits Gwillim (42) and Barlow (49) less well. Apparent age is weak evidence and **does not identify him.**
- The community's candidates (Gabriel Commanda, Pierre Beauchemin) are not on the roster.

The other two moving figures are the moustached man in a striped shirt and tie (frame 560,423) and a face at frame 695,373. Both are party members and neither can be identified.

## 2. Sudbury, 9.6–14.25 s: the Gowganda King Edward Hotel group (priority)

About 12 men sit on a bench outside the log hotel, with 2–3 more in the doorway (`crops/sudbury_9.6s_gowganda_frame_lowres.jpg`, the project's still at 320 px). The animation moves the man in the wide-brim hat, second from left, and the man in the doorway. **No source photograph has been found, so there is no caption, and nobody in it can be identified.** New check today: the Deseronto Archives Flickr set from H. M. Rathbun's trip to "Gow Ganda", 19 May–28 June 1909 (23 photos), has the Bank of Commerce, Baxter's Hotel, camps and the party. It has **no King Edward Hotel**, so that is a clean negative (https://www.flickr.com/photos/deserontoarchives/4155659652/). These leads remain open: Archives of Ontario F 4594; *Views of Gowganda from the Inside* (1910); a Library and Archives Canada image search, which needs Max at the keyboard.

## 3. Cobalt, 8.1 s: the standing man, hands on hips

A plate from a scanned geological annual report showing a prospecting party among stumps. The page text mentions the Cobalt series and Lorrain arkose. **The report and plate number are not yet established, so the caption has not been read.** Alamy and Flickr text searches from this container returned nothing usable. Next step: find the Internet Archive scan (an Ontario Bureau of Mines annual report or GSC Summary Report, c.1904–1910) and read the plate caption, which is the only rank-1 route.

## 4. Live regions: everything else

Saskatchewan (30.5, 35.4, 46 s), Manitoba (7.9, 9.6, 50.5 s, two men on the cut line), Sudbury quarries (18.4, 20.9 s) and Val-d'Or's other stills: no source captions were found (negative on TinEye, Yandex and Lens per the 6 Sep sweep), and nobody is identifiable. The Depression photos at Val-d'Or 4.75 and 7.75 s are traced (NARA 541927, the Capone soup kitchen, Chicago 1931; and US stock), but their captions name no one. Manitoba 48 s (Alamos Gold, modern) was excluded by the scope rule.

## 5. Chibougamau video: new check

I made a contact sheet of the English video from 12 to 38 s (`crops/chibougamau_EN_12-38s_contact_lowres.jpg`). It shows a canoe with about 7 men (~17 s) and a man with a pole in a rapid (~19 s). The canoe photo is **not** the report's Plate XX. I did not see the report's other people plates (Mistassini groups, the Iserhoff family) in that range. These stills were not in the 6 Sep sweep and should go through TinEye or full-frame Lens.

## 6. Solved regions (brief)

Traced but anonymous: Nova Scotia (Chilkoot packers; a woman and three men panning in Alaska; Hegg's Circle City, 1896) and Britannia 23.6 s (Mount Sheer townsite, Britannia Mine Museum). Untraced: the Toronto podium speaker at 31.9 s, which is a named public event and the most promising open item outside the live regions; Toronto panners, crowd and trading floor; the Argentia dock and soldiers; the New Brunswick road group; Dawson's prospectors.

## Bottom line

| Photo | Identified | Confidence |
|---|---|---|
| Val-d'Or camp, the group | Chibougamau Commission party, June 1910 | high (caption + text) |
| Val-d'Or camp, Gwillim | present, position unknown | high that he is in it; position unknown |
| Val-d'Or camp, the animated seated man | **unidentified**; one of the June party; looks young (weak) | none for the individual |
| Gowganda hotel group | unidentified; no source photo | none |
| Cobalt standing man | unidentified; plate caption not yet read | none |
| All other people photos | anonymous or untraced | n/a |
