# D100 item builder: split the Trail Tours booklet text (EN, FR) into numbered items per tour.
# Fixed rule (see PREREG): an item starts at a line whose folded text contains the item's key within its
# first len(key)+3 letters, searched in order; its body is the rest of that line after the key plus every
# following line up to the next item's line, the next tour header ("N. "), or the end-of-booklet credits.
# Titles are the canonical titles below. No key is applied here.
import json, os, re, sys, unicodedata
OUT = os.path.dirname(os.path.abspath(__file__))
def fold(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if c.isalpha() and ord(c) < 128)

EN = [
 ["Balsam Fir","Flying Squirrels","Cedar Waxwing","Northern Water Snake","Eastern White Cedar","Cedar vs Birch","Insect Invasion","Busy Beaver","Junction Creek"],
 ["Kelly Lake Outlet (Lookout #1)","Land History (Lookout #2)","Birch Coppice","Wetland with a Purpose","Trumpeter Swans","Do Glaciers Move?","Sudbury's Meteorite","Recovering Barrens","Kelly Lake's History","The Fielding Family"],
 ["Gypsy Moth","Minnow Lake","Jack Pine Forest","Green Alder","Survivors","Birch for Food"],
 ["As Canadian as Blueberry Pie","Rocks Have Ribs","Moon Rock","Twin Stacks","Minnow Lake Restoration Group","Lichen Schmichen","Fern Gully","Pretty in Pink"],
 ["Two Million + Trees","Acid Needles","Stumps","Black Locust","Lookout #1","Little Birch","Glacial Meltwater Channel","Lookout #2","Two-Toned Rock"],
 ["Water Striders","Pin Cherries","Vermilion River","Mossies, Mozzies and Skeeters","Ducks in the Woods","Blue and Rasp","Painted Turtles","Red Squirrels","Frogs Galore","Scenic Picnic"],
 ["A.Y. Jackson Lookout","High Falls","Smooth Rocks","Cedar Ridge","Roots Act as Glue","Moss Points North","Bracken Fern","Popular or Poplar","Woodpeckers","Old Tall White Pines"],
 ["Raspberry Lane","Sheep Laurel","Tracks and Trains","North View","Junction Creek","Birch Bowl","Zaitz Speedway","Willows","Are they Sundials or Flowers?"],
 ["Lookout on the Water","Shatter Cones","Living on the Edge","Pine Alley","Lucky Duck","Ruffed Grouse","Lost Ramsey"],
 ["Garter Snakes","Black Spruce Seedlings","Terry Fox Memorial Sports Complex","Labrador Tea","Home for the Pine Cone Willow Gall Midge","Where Porcupines Roam"]]
FR = [
 ["Le sapin baumier","L'écureuil volant","Le jaseur d'Amérique","La couleuvre d'eau","Le thuya occidental","Le cèdre contre le bouleau","Une invasion d'insectes","Un castor à l'œuvre","Le ruisseau Junction"],
 ["Décharge du lac Kelly (Belvédère no 1)","Un peu d'histoire sur la région (Belvédère no 2)","Taillis de bouleaux","Un marécage avec un objectif","Le cygne trompette","Les glaciers se déplacent-ils?","Météorite de Sudbury","Des terres stériles en voie de rétablissement","L'histoire du lac Kelly","La famille Fielding"],
 ["La spongieuse","Le lac Minnow","Une forêt de pins gris","L'aulne vert","Des survivants","Du bouleau pour dîner"],
 ["Il n'y a pas plus canadien qu'une tarte aux bleuets","Les rochers ont des nervures","Un rocher lunaire","Des cheminées jumelles","Groupe de restauration du lac Minnow","Du lichen, partout du lichen","Un ravin de fougères","La vie en rose"],
 ["Plus de deux millions d'arbres","Des aiguilles acides","Des souches ancrées dans le temps","Le robinier faux-acacia","Belvédère no 1","De petits bouleaux","Un chenal d'eau de fonte glaciaire","Belvédère no 2","Un rocher à deux couleurs"],
 ["L'araignée d'eau","Des merises","La rivière Vermilion","Des maringouins, des maringouins, et encore","Des canards dans le bois","Des bleuets et des framboises","La tortue peinte","L'écureuil roux","Des grenouilles à profusion","Un pique-nique avec une belle vue"],
 ["Belvédère A. Y. Jackson","Les chutes High Falls","Des roches bien lisses","Une crête de thuyas","Des racines qui tiennent","La mousse vous fera perdre le nord","La fougère grand aigle","Un peuplement de peupliers","Le pic","De vieux et grands pins blancs"],
 ["Une parcelle de framboises","Le kalmia à feuilles étroites","Des trains et des rails","Une vue du nord","Le ruisseau Junction","Un bol fait d'écorce de bouleau","Zaitz Speedway","Le saule","Cadran solaire ou fleur?"],
 ["Une belle vue du lac","Les fractures coniques","Le faucon pèlerin","Des pins de toutes les couleurs","Mouillé comme un canard","La gélinotte huppée","Le Lac des perdus"],
 ["Le thamnophis","Des semis d'épinette noire","Complexe sportif commémoratif Terry Fox","Thé du Labrador","Un logis pour la cécidomyie","Un lieu de prédilection pour les porcs-épics"]]
# match keys where the printed line differs from the canonical title (superscript "no" prints as a stray "o ... n")
KEYFIX = {"Décharge du lac Kelly (Belvédère no 1)": "dechargedulackellybelvederen",
          "Un peu d'histoire sur la région (Belvédère no 2)": "unpeudhistoiresurlaregionbelvederen",
          "Belvédère no 1": "belvederen", "Belvédère no 2": "belvederen"}
HEADER = re.compile(r'^\s*(10|[1-9])\.\s')
CREDITS = re.compile(r'^\s*(A|Produced by:|Création :)\s*$')

def build(path, titles):
    lines = open(path, encoding='utf-8').read().replace('\f', '\n').split('\n')
    tours = []; i = 0
    for t, tl in enumerate(titles):
        while not (HEADER.match(lines[i]) and HEADER.match(lines[i]).group(1) == str(t + 1)): i += 1
        start = i; items = []
        for title in tl:
            key = KEYFIX.get(title, fold(title))
            while True:
                i += 1
                f = fold(lines[i])
                p = f.find(key)
                if 0 <= p <= 3 and not HEADER.match(lines[i]): break
            items.append([title, i, f[p + len(key):]])
        tours.append(items)
    # bodies: from item line to next item line / next header / credits
    flat = [(t, k, it) for t, items in enumerate(tours) for k, it in enumerate(items)]
    out = []
    for n, (t, k, (title, ln, rest)) in enumerate(flat):
        nxt = flat[n + 1][2][1] if n + 1 < len(flat) else len(lines)
        body = [rest]
        for j in range(ln + 1, nxt):
            if HEADER.match(lines[j]) or (t == len(titles) - 1 and CREDITS.match(lines[j])): break
            body.append(fold(lines[j]))
        out.append(dict(tour=t + 1, n=k + 1, g=n + 1, title=title, line=ln + 1, body=''.join(body)))
    return out

for lang, titles in (('EN', EN), ('FR', FR)):
    items = build(os.path.join(OUT, lang.lower() + '.txt'), titles)
    json.dump(items, open(os.path.join(OUT, f'items100_{lang}.json'), 'w'), ensure_ascii=False, indent=0)
    print(lang, len(items), 'items')
    for it in items:   # titles, text line and body LENGTH only: no body letters are printed before the PREREG
        print(f"  {it['g']:>2} T{it['tour']}.{it['n']:<2} line {it['line']:>4}  len {len(it['body']):>4}  {it['title']}")
