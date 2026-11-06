import json, re, unicodedata, collections, sys, os
import spacy, pronouncing

D = os.path.dirname(os.path.abspath(__file__))
TITLE = {"en": "The Great Canadian Treasure Hunt", "fr": "La grande chasse au trésor canadienne"}

def load(lang):
    raw = open(f"{D}/poem_{lang}.txt", encoding="utf-8").read().strip("\n")
    stanzas = [s.split("\n") for s in raw.split("\n\n")]
    return stanzas

def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def letters(s):
    return [c for c in s if c.isalpha()]

def a1z26(s):
    return sum(ord(c) - 96 for c in strip_acc(s).lower() if "a" <= c <= "z")

def ortho_words(line):
    # space-separated words, punctuation stripped; contractions/elisions/hyphens kept together
    out = []
    for w in line.split():
        w2 = w.strip(",.;:!?\"“”")
        if w2:
            out.append(w2)
    return out

def ling_words(line, lang):
    # split elisions (l’or -> l’ + or) and hyphens (zinc-toned -> zinc + toned) — EN contractions stay 1
    out = []
    for w in ortho_words(line):
        parts = re.split(r"-", w)
        for p in parts:
            if lang == "fr" and re.match(r"^(l|d|n|s|c|j|qu|m|t)’", p, re.I) and len(p) > 2:
                a, b = p.split("’", 1)
                out += [a + "’", b]
            elif p:
                out.append(p)
    return out

VOW = set("aeiouyàâäéèêëîïôöùûüÿœæ")

def syl_en(word):
    w = re.sub(r"[^a-z’']", "", word.lower()).replace("’", "'")
    special = {"chalco": 2, "verdigris": 3, "flinty's": 2, "bathurst": 2, "overgrown": 3, "zinc": 1, "toned": 1,
               "don’t": 1, "won’t": 1, "zinctoned": 2}
    if w in special:
        return special[w]
    ph = pronouncing.phones_for_word(w)
    if ph:
        return pronouncing.syllable_count(ph[0])
    w2 = w.rstrip("'s")
    ph = pronouncing.phones_for_word(w2)
    if ph:
        return pronouncing.syllable_count(ph[0])
    g = re.findall(r"[aeiouy]+", w)
    n = len(g) - (1 if w.endswith("e") and len(g) > 1 else 0)
    return max(1, n)

def syl_fr(word):
    # orthographic estimate (poetic count, mute final e not counted except before consonant)
    w = strip_acc(word.lower()).replace("’", "")
    w = re.sub(r"qu", "q", w)
    w = re.sub(r"gu(?=[ei])", "g", w)
    g = re.findall(r"[aeiouy]+", w)
    n = len(g)
    if re.search(r"[^aeiouy]e(s|nt)?$", w) and n > 1:
        n -= 1
    return max(1, n)

def vowels(s):
    return sum(1 for c in strip_acc(s).lower() if c in "aeiouy")

nlp = {"en": spacy.load("en_core_web_sm"), "fr": spacy.load("fr_core_news_sm")}

# Manual POS overrides after review of the small models' mistakes on poetic syntax
OVR = {
    "en": {"crowned@1.1": "VERB", "whisper": "VERB", "hides": "VERB", "bore": "VERB", "reign": "VERB", "sighs": "VERB",
           "mislead": "VERB", "lies": "VERB", "grew": "VERB", "remembers": "VERB", "forgets": "VERB", "pulls": "VERB",
           "wets": "VERB", "stitched": "VERB", "sparked": "VERB", "ignites": "VERB", "flew": "VERB", "reflects": "VERB",
           "lead": "VERB", "begun": "VERB", "gripped": "VERB", "ceased": "VERB", "hums": "VERB", "marks": "VERB",
           "bends": "VERB", "told": "VERB", "speak": "VERB", "confess": "VERB", "hold": "VERB", "sings": "VERB",
           "lean": "VERB", "remains": "VERB", "stands": "VERB", "dulled": "VERB", "declared": "VERB",
           "disappears": "VERB", "fell": "VERB", "rang": "VERB", "fade": "VERB", "trails": "VERB", "pales": "VERB",
           "struck": "VERB", "crowned@11.2": "VERB", "point": "VERB", "stare": "VERB", "step": "VERB", "align": "VERB",
           "forgets": "VERB", "grows": "VERB", "speaks": "VERB", "knows": "VERB", "marked": "VERB", "rests": "VERB",
           "look": "VERB", "turns": "VERB", "is": "AUX", "won’t": "AUX", "don’t": "AUX", "may": "AUX", "have": "AUX",
           "will": "AUX", "be": "AUX",
           "cold": "ADJ", "vast": "ADJ", "old": "ADJ", "gilded": "ADJ", "brittle": "ADJ", "northern": "ADJ",
           "red": "ADJ", "fleeting": "ADJ", "giant": "ADJ", "ancient": "ADJ", "current@6.4": "ADJ", "sleeping": "ADJ",
           "sunken": "ADJ", "quiet": "ADJ", "loud": "ADJ", "forged": "VERB", "warm": "ADJ", "zinc-toned": "ADJ",
           "deepest": "ADJ", "numbered": "ADJ", "tall": "ADJ", "overgrown": "NOUN", "strong": "ADJ", "silent": "ADJ",
           "free": "ADJ", "passing": "ADJ", "growing": "ADJ", "salt": "ADJ", "copper": "ADJ", "birch": "NOUN",
           "chalco": "NOUN", "buried": "ADJ",
           "flinty’s": "PROPN", "bathurst": "PROPN", "bay": "PROPN", "street": "PROPN", "shield": "PROPN",
           "gold": "NOUN", "verdigris": "NOUN", "glaciers": "NOUN", "mountain’s": "NOUN", "siren’s": "NOUN",
           "miner’s": "NOUN", "current@3.4": "NOUN", "echo": "NOUN", "lore": "NOUN", "press": "NOUN", "core": "NOUN",
           "hush": "NOUN", "brush": "NOUN", "script": "NOUN", "share": "NOUN", "accord": "NOUN", "trees": "NOUN",
           "east": "NOUN", "ease": "NOUN", "haste": "NOUN", "design": "NOUN", "mark": "NOUN",
           "once": "ADV", "now": "ADV", "still": "ADV", "never": "ADV", "low": "ADV", "even": "ADV", "not": "PART",
           "where": "ADV", "yet": "CCONJ", "but@5.3": "ADV", "past": "ADP", "beyond": "ADP", "beneath": "ADP",
           "what": "PRON", "none": "PRON", "all": "PRON", "one@12.4": "PRON", "one@9.1": "NUM",
           "truth": "NOUN", "name": "NOUN", "flame": "NOUN", "veins": "NOUN", "peaks": "NOUN", "waters": "NOUN", "moss": "NOUN", "alone": "ADV", "long": "ADV", "back": "ADV", "to@11.4": "ADP", "lies": "VERB", "held": "VERB", "fever": "NOUN", "seams": "NOUN", "breaks": "NOUN", "faults": "NOUN", "suits": "NOUN", "stones": "NOUN", "sun": "NOUN", "call": "NOUN", "light": "NOUN", "hue": "NOUN", "strain": "NOUN"},
    "fr": {"couronnée": "VERB", "chuchotent": "VERB", "cache": "VERB", "porté": "VERB", "règnent": "VERB",
           "soupire": "VERB", "trompent": "VERB", "trouve": "VERB", "poussé": "VERB", "portait": "VERB",
           "guident": "VERB", "souvient": "VERB", "oublie": "VERB", "tire": "VERB", "mouille": "VERB",
           "cousu": "VERB", "fait": "VERB", "jaillir": "VERB", "enflamme": "VERB", "envolé": "VERB",
           "regardera": "VERB", "reflète": "VERB", "mènent": "VERB", "commencé": "VERB", "emparée": "VERB",
           "cessé": "VERB", "fredonne": "VERB", "marque@6.4": "VERB", "incline": "VERB", "parlaient": "VERB",
           "parlent": "VERB", "avouées": "VERB", "peuvent": "VERB", "retenir": "VERB", "chante": "VERB",
           "appuient": "VERB", "demeure": "VERB", "forgée": "VERB", "être": "AUX", "dresse": "VERB",
           "terni": "VERB", "passe": "VERB", "déclaré": "VERB", "disparaît": "VERB", "passent": "VERB",
           "tombaient": "VERB", "sonnait": "VERB", "estompent": "VERB", "traîne": "VERB", "pâlit": "VERB",
           "accordés": "VERB", "couronnait": "VERB", "indiquera": "VERB", "fixent": "VERB", "marchez": "VERB",
           "alignent": "VERB", "oublie@12.2": "VERB", "poussent": "VERB", "dit": "VERB", "sait": "VERB",
           "marqué": "VERB", "repose": "VERB", "regardez": "VERB", "tourne": "VERB",
           "ont": "AUX", "a": "AUX", "est": "AUX", "sont": "AUX", "été": "AUX", "n’est": "AUX", "n’a": "AUX",
           "s’est": "AUX",
           "froide": "ADJ", "vaste": "ADJ", "vieilles": "ADJ", "dorée": "ADJ", "salé": "ADJ", "fragiles": "ADJ",
           "nordique": "ADJ", "rouges": "ADJ", "éphémère": "ADJ", "géante": "ADJ", "ancien": "ADJ",
           "actuelle": "ADJ", "endormis": "ADJ", "noyés": "ADJ", "silencieuse": "ADJ", "invisible": "ADJ",
           "bruyante": "ADJ", "chaudes": "ADJ", "teintées": "ADJ", "profonde": "ADJ", "minier": "ADJ",
           "doré": "ADJ", "numérotée": "ADJ", "hautes": "ADJ", "enterré": "ADJ", "seul": "ADJ", "silencieux@13.4": "ADJ",
           "forts": "NOUN", "silencieux@8.4": "NOUN", "libres": "NOUN",
           "flinty": "PROPN", "bathurst": "PROPN", "bay": "PROPN", "street": "PROPN", "bouclier": "PROPN",
           "est@6.1": "PROPN", "nord": "PROPN", "vert-de-gris": "NOUN", "chalco": "NOUN", "zinc": "NOUN",
           "mineur": "NOUN", "or": "NOUN", "l’or": "NOUN", "marque@12.3": "NOUN", "pierres": "NOUN", "l’est": "PROPN", "dessin": "NOUN", "hâtivement": "ADV", "teinte": "NOUN", "braise": "NOUN", "borne": "NOUN", "pins": "NOUN", "herbes": "NOUN", "autrefois": "ADV", "au-delà": "ADP", "où": "ADV", "là": "ADV", "personne": "PRON", "rien": "PRON", "nuages": "NOUN", "l’écho": "NOUN", "l’écriture": "NOUN", "l’appel": "NOUN", "l’eau": "NOUN", "l’air": "NOUN", "ne": "PART", "n’": "PART", "pas": "PART", "jamais": "ADV", "plus@4.3": "ADV", "plus@10.2": "ADV", "aucune": "DET", "aucun": "DET", "ni": "CCONJ", "que@5.3": "ADV", "non": "PART", "passé": "NOUN", "travers": "ADP", "bas": "NOUN", "arrière": "NOUN", "vue": "NOUN", "trésor": "NOUN", "action": "NOUN", "facilité": "NOUN", "presse": "NOUN", "courant": "NOUN", "or": "NOUN", "fait": "VERB", "envolé": "VERB", "commencé": "VERB", "seul": "ADJ", "tout": "PRON", "il": "PRON", "les@11.2": "DET", "même": "ADV", "encore": "ADV", "longtemps": "ADV", "près": "ADP", "aujourd’hui": "ADV"},
}

UPOS_GROUP = {"NOUN": "Nouns", "PROPN": "Proper nouns", "VERB": "Verbs", "AUX": "Auxiliaries", "ADJ": "Adjectives",
              "ADV": "Adverbs", "ADP": "Prepositions", "DET": "Determiners/articles", "PRON": "Pronouns",
              "CCONJ": "Conjunctions", "SCONJ": "Conjunctions", "PART": "Particles/negation", "NUM": "Numerals",
              "INTJ": "Other", "X": "Other", "SYM": "Other"}

def tag_line(lang, line, s, l):
    doc = nlp[lang](line)
    res = []
    for m in re.finditer(r"\S+", line):
        w = m.group(0).strip(",.;:!?\"“”")
        if not w:
            continue
        a = m.start() + m.group(0).find(w); b = a + len(w)
        cand = [t for t in doc if t.idx < b and t.idx + len(t.text) > a and not t.is_punct]
        if not cand:
            cand = [t for t in doc if t.idx < b and t.idx + len(t.text) > a]
        if lang == "fr" and "’" in w and len(cand) > 1:
            main = cand[-1]
        elif "-" in w and len(cand) > 1:
            main = cand[-1]
        else:
            main = cand[0] if cand else None
        pos = main.pos_ if main else "X"
        lemma = main.lemma_ if main else w
        key = w.lower()
        o = OVR[lang]
        k2 = f"{key}@{s}.{l}"
        if k2 in o:
            pos = o[k2]
        elif key in o:
            pos = o[key]
        elif lang == "fr" and "’" in key and key.split("’", 1)[1] in o and key not in o:
            pos = o[key.split("’", 1)[1]]
        res.append({"w": w, "pos": pos, "lemma": lemma})
    return res

NEG = {"en": r"\b(no|not|nor|never|none|don’t|won’t|no one)\b",
       "fr": r"\b(ne|n’|pas|aucun|aucune|ni|jamais|rien|personne|non)\b"}
NEGWORDS = {"en": ["no", "not", "nor", "never", "none", "don’t", "won’t", "but", "yet", "mislead", "forgets",
                   "unseen", "disappears", "fade", "pales", "dulled", "silence", "hush"]}

def analyze(lang):
    st = load(lang)
    out = {"lang": lang, "title": TITLE[lang], "stanzas": []}
    gi = 0
    allwords = []
    for si, stz in enumerate(st, 1):
        S = {"n": si, "lines": []}
        for li, line in enumerate(stz, 1):
            gi += 1
            ow = ortho_words(line)
            lw = ling_words(line, lang)
            tags = tag_line(lang, line, si, li)
            syl = [syl_en(w) if lang == "en" else syl_fr(w) for w in ow]
            words = []
            for wi, w in enumerate(ow, 1):
                words.append({"w": w, "i": wi, "len": len(letters(w)), "chars": len(w), "a1z26": a1z26(w),
                              "pos": tags[wi - 1]["pos"] if wi - 1 < len(tags) else "X",
                              "lemma": tags[wi - 1]["lemma"] if wi - 1 < len(tags) else w, "syl": syl[wi - 1]})
                allwords.append((si, li, gi, w))
            L = {"n": li, "g": gi, "text": line, "words": words, "nw": len(ow), "nlw": len(lw),
                 "letters": len(letters(line)), "chars": len(line), "chars_nospace": len(line.replace(" ", "")),
                 "vowels": vowels(line), "a1z26": a1z26(line), "syl": sum(syl),
                 "first": strip_acc(letters(line)[0]).upper(), "last": strip_acc(letters(line)[-1]).upper(),
                 "firstword": ow[0], "lastword": ow[-1].lower(),
                 "neg": len(re.findall(NEG[lang], line.lower())),
                 "punct": "".join(c for c in line if c in ",.;:!?’-")}
            S["lines"].append(L)
        for k in ["nw", "nlw", "letters", "chars", "chars_nospace", "vowels", "a1z26", "syl", "neg"]:
            S[k] = sum(l[k] for l in S["lines"])
        S["initials_lines"] = "".join(l["first"] for l in S["lines"])
        S["initials_words"] = " ".join("".join(strip_acc(w["w"][0]).upper() for w in l["words"]) for l in S["lines"])
        S["finals_lines"] = "".join(l["last"] for l in S["lines"])
        out["stanzas"].append(S)
    lines = [l for s in out["stanzas"] for l in s["lines"]]
    words = [w for l in lines for w in l["words"]]
    text = "\n".join(l["text"] for l in lines)
    T = {}
    T["stanzas"] = len(out["stanzas"])
    T["lines"] = len(lines)
    T["words"] = len(words)
    T["ling_words"] = sum(l["nlw"] for l in lines)
    T["letters"] = sum(l["letters"] for l in lines)
    T["chars"] = sum(l["chars"] for l in lines)
    T["chars_nospace"] = sum(l["chars_nospace"] for l in lines)
    T["vowels"] = sum(l["vowels"] for l in lines)
    T["consonants"] = T["letters"] - T["vowels"]
    T["syl"] = sum(l["syl"] for l in lines)
    T["a1z26"] = sum(l["a1z26"] for l in lines)
    T["accented"] = sum(1 for c in text if c.isalpha() and strip_acc(c) != c)
    T["capitals"] = sum(1 for c in text if c.isupper())
    pc = collections.Counter(c for c in text if not c.isalnum() and c not in " \n")
    T["punct"] = dict(pc)
    T["title_words"] = len(TITLE[lang].split())
    T["title_letters"] = len(letters(TITLE[lang]))
    T["title_a1z26"] = a1z26(TITLE[lang])
    lf = collections.Counter(strip_acc(c).lower() for c in text if c.isalpha())
    T["letter_freq"] = {ch: lf.get(ch, 0) for ch in "abcdefghijklmnopqrstuvwxyz"}
    T["missing_letters"] = [ch for ch in "abcdefghijklmnopqrstuvwxyz" if lf.get(ch, 0) == 0]
    wf = collections.Counter(w["w"].lower() for w in words)
    T["word_freq"] = wf.most_common()
    T["unique_words"] = len(wf)
    T["hapax"] = sum(1 for v in wf.values() if v == 1)
    T["avg_word_len"] = round(T["letters"] / T["words"], 3)
    pos = collections.Counter(UPOS_GROUP.get(w["pos"], "Other") for w in words)
    T["pos"] = dict(pos)
    T["pos_lists"] = {}
    for g in ["Verbs", "Auxiliaries", "Adjectives", "Nouns", "Proper nouns", "Adverbs", "Numerals", "Pronouns",
              "Prepositions", "Conjunctions", "Determiners/articles", "Particles/negation"]:
        T["pos_lists"][g] = [w["w"] for w in words if UPOS_GROUP.get(w["pos"], "Other") == g]
    T["first_word_freq"] = collections.Counter(l["firstword"] for l in lines).most_common()
    T["line_initials"] = "".join(l["first"] for l in lines)
    T["line_finals"] = "".join(l["last"] for l in lines)
    T["stanza_initials"] = "".join(s["lines"][0]["first"] for s in out["stanzas"])
    T["stanza_finals"] = "".join(s["lines"][-1]["last"] for s in out["stanzas"])
    T["word_initials"] = "".join(strip_acc(w["w"][0]).upper() for w in words)
    T["word_finals"] = "".join(strip_acc(letters(w["w"])[-1]).upper() for w in words)
    # Nth word of Nth line within stanza, Nth letter of Nth line
    diag = []
    for s in out["stanzas"]:
        diag.append(" ".join(l["words"][l["n"] - 1]["w"] if len(l["words"]) >= l["n"] else "·" for l in s["lines"]))
    T["diag_words"] = diag
    T["word_k_of_stanza_k"] = [" ".join(l["words"][s["n"] - 1]["w"] if len(l["words"]) >= s["n"] else "·"
                                        for l in s["lines"]) for s in out["stanzas"]]
    nthl = []
    for l in lines:
        lt = letters(l["text"])
        nthl.append(strip_acc(lt[l["n"] - 1]).upper())
    T["nth_letter_nth_line"] = "".join(nthl)
    gl = []
    for l in lines:
        lt = letters(l["text"])
        gl.append(strip_acc(lt[(l["g"] - 1) % len(lt)]).upper())
    T["global_nth_letter"] = "".join(gl)
    # second letters / second words
    T["second_letters"] = "".join(strip_acc(letters(l["text"])[1]).upper() for l in lines)
    T["last_words"] = [l["lastword"] for l in lines]
    T["first_words"] = [l["firstword"] for l in lines]
    # number words
    numw = {"en": ["one", "none", "no one", "first", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                   "ten", "once", "numbered", "share", "code", "deepest", "coin", "circles", "compass"],
            "fr": ["un", "une", "aucun", "aucune", "rien", "personne", "jamais", "numérotée", "code", "pièce",
                   "cercles", "boussole", "autrefois"]}
    T["number_words"] = [(l["g"], w["w"]) for l in lines for w in l["words"] if w["w"].lower() in numw[lang]]
    # sequences
    T["seq_words_per_line"] = [l["nw"] for l in lines]
    T["seq_words_per_stanza"] = [s["nw"] for s in out["stanzas"]]
    T["seq_letters_per_line"] = [l["letters"] for l in lines]
    T["seq_letters_per_stanza"] = [s["letters"] for s in out["stanzas"]]
    T["seq_syl_per_line"] = [l["syl"] for l in lines]
    T["seq_a1z26_per_line"] = [l["a1z26"] for l in lines]
    T["seq_a1z26_per_stanza"] = [s["a1z26"] for s in out["stanzas"]]
    T["seq_word_lengths"] = [w["len"] for w in words]
    T["a1z26_line_mod26"] = "".join(chr(64 + (l["a1z26"] - 1) % 26 + 1) for l in lines)
    T["a1z26_stanza_mod26"] = "".join(chr(64 + (s["a1z26"] - 1) % 26 + 1) for s in out["stanzas"])
    T["wpl_as_letters"] = "".join(chr(64 + n) if 1 <= n <= 26 else "?" for n in T["seq_words_per_line"])
    T["neg_per_stanza"] = [s["neg"] for s in out["stanzas"]]
    # longest/shortest
    T["longest_words"] = sorted({w["w"] for w in words}, key=lambda x: -len(letters(x)))[:12]
    T["longest_line"] = max(lines, key=lambda l: l["letters"])["g"]
    T["shortest_line"] = min(lines, key=lambda l: l["letters"])["g"]
    # where/là où
    T["count_where"] = len(re.findall(r"\bwhere\b", text.lower())) if lang == "en" else len(re.findall(r"\bl[àa] o[ùu]\b|\bo[ùu]\b", text.lower()))
    out["totals"] = T
    return out

R = {"en": analyze("en"), "fr": analyze("fr")}

# EN content-word threads (repeated lemmas across stanzas)
threads = collections.defaultdict(set)
stem = lambda w: re.sub(r"(’s|s|es|ed|ing)$", "", w.lower())
for s in R["en"]["stanzas"]:
    for l in s["lines"]:
        for w in l["words"]:
            if w["pos"] in ("NOUN", "VERB", "ADJ", "PROPN") and len(w["w"]) > 2:
                threads[stem(w["w"])].add(s["n"])
manual = {"mark": ["marks", "marker", "mark", "marked"], "crown": ["crowned"], "gild": ["gilded"],
          "birch": ["birch", "birches"], "whisper": ["whisper", "whispers"], "silen": ["silence", "silent"],
          "root": ["roots"], "current": ["current"], "gold": ["gold"], "bore": ["bore"], "northern": ["northern"],
          "once": ["once"], "now": ["now"], "where": ["where"], "forget": ["forgets"], "truth": ["truth"],
          "speak": ["speak", "speaks"], "grow": ["grew", "grows", "growing", "overgrown"],
          "hold": ["hold", "held"], "stand": ["stands"], "trail/track/path/road": ["trail", "track", "path", "paths", "road"],
          "tree words": ["birch", "birches", "pine", "cedars", "trees"],
          "metal words": ["gold", "copper", "iron", "zinc-toned", "verdigris", "chalco", "coin", "gilded"],
          "water words": ["salt", "brine", "current", "water", "waters", "moss", "shore", "glaciers", "sunken", "wets"],
          "sound words": ["whisper", "whispers", "song", "hums", "sings", "rang", "bell", "sounds", "echo", "speak", "speaks", "loud", "call", "silence", "silent", "quiet", "hush", "confess", "told", "declared", "message"],
          "light/fire words": ["fire", "sparked", "flame", "ember", "ignites", "phoenix", "sun", "gleam", "light", "gilded", "hue", "reflects", "mirror"],
          "sight words": ["mirror", "sight", "unseen", "look", "stare", "reflects", "point", "script", "mark"]}
thr = {}
for k, forms in manual.items():
    hits = []
    for s in R["en"]["stanzas"]:
        for l in s["lines"]:
            for w in l["words"]:
                if w["w"].lower() in forms:
                    hits.append([s["n"], l["g"], w["w"]])
    thr[k] = hits
R["threads"] = thr

# line-by-line comparison
cmp_ = []
for le, lf in zip([l for s in R["en"]["stanzas"] for l in s["lines"]], [l for s in R["fr"]["stanzas"] for l in s["lines"]]):
    cmp_.append({"g": le["g"], "en": le["text"], "fr": lf["text"], "en_w": le["nw"], "fr_w": lf["nw"],
                 "en_l": le["letters"], "fr_l": lf["letters"], "en_c": le["chars"], "fr_c": lf["chars"],
                 "en_s": le["syl"], "fr_s": lf["syl"], "en_v": sum(1 for w in le["words"] if w["pos"] == "VERB"),
                 "fr_v": sum(1 for w in lf["words"] if w["pos"] == "VERB"),
                 "en_a": sum(1 for w in le["words"] if w["pos"] == "ADJ"),
                 "fr_a": sum(1 for w in lf["words"] if w["pos"] == "ADJ"),
                 "en_n": sum(1 for w in le["words"] if w["pos"] in ("NOUN", "PROPN")),
                 "fr_n": sum(1 for w in lf["words"] if w["pos"] in ("NOUN", "PROPN")),
                 "en_g": le["a1z26"], "fr_g": lf["a1z26"], "en_f": le["first"], "fr_f": lf["first"]})
R["compare"] = cmp_

# Anthem overlaps (public-domain lyrics)
ANTHEM_EN = """O Canada! Our home and native land! True patriot love in all of us command. With glowing hearts we see thee rise,
The True North strong and free! From far and wide, O Canada, we stand on guard for thee. God keep our land glorious and free!
O Canada, we stand on guard for thee. O Canada, we stand on guard for thee."""
ANTHEM_FR = """Ô Canada! Terre de nos aïeux, Ton front est ceint de fleurons glorieux! Car ton bras sait porter l'épée,
Il sait porter la croix! Ton histoire est une épopée Des plus brillants exploits. Et ta valeur, de foi trempée,
Protégera nos foyers et nos droits. Protégera nos foyers et nos droits."""
def wset(t):
    return set(re.findall(r"[a-zàâäéèêëîïôöùûüç]+", t.lower().replace("'", " ").replace("’", " ")))
STOP_EN = set("the a an and of in on to for with by but where what is its it we our thee no not now once nor".split())
STOP_FR = set("le la les de des du un une et à au aux en est ses sa son ce que qui ne pas l d n s par pour dans où là".split())
pe = wset("\n".join(l["text"] for s in R["en"]["stanzas"] for l in s["lines"]))
pf = wset("\n".join(l["text"] for s in R["fr"]["stanzas"] for l in s["lines"]))
R["anthem"] = {"en_shared": sorted(pe & wset(ANTHEM_EN)), "en_shared_content": sorted((pe & wset(ANTHEM_EN)) - STOP_EN),
               "fr_shared": sorted(pf & wset(ANTHEM_FR)), "fr_shared_content": sorted((pf & wset(ANTHEM_FR)) - STOP_FR),
               "en_anthem_words": len(re.findall(r"[A-Za-z]+", ANTHEM_EN)), "fr_anthem_words": len(re.findall(r"[^\W\d_]+", ANTHEM_FR))}

json.dump(R, open(f"{D}/data.json", "w"), ensure_ascii=False, indent=1)

# Console summary
for lang in ("en", "fr"):
    T = R[lang]["totals"]
    print("==", lang)
    for k in ["stanzas", "lines", "words", "ling_words", "letters", "chars", "chars_nospace", "vowels", "consonants", "syl",
              "a1z26", "accented", "capitals", "punct", "unique_words", "hapax", "avg_word_len", "pos", "missing_letters",
              "line_initials", "stanza_initials", "line_finals", "nth_letter_nth_line", "a1z26_line_mod26",
              "seq_words_per_line", "seq_words_per_stanza", "seq_letters_per_stanza", "seq_a1z26_per_stanza", "neg_per_stanza",
              "count_where", "first_word_freq", "number_words", "title_a1z26", "word_k_of_stanza_k", "diag_words"]:
        print(k, T[k])
    print("word_freq", T["word_freq"][:25])
    for g, ws in T["pos_lists"].items():
        print(g, len(ws), ws)
print(R["anthem"])
