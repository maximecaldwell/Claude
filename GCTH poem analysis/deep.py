import json, re, random, unicodedata, collections, os, statistics
import pronouncing, wordfreq

D = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(D, "..", "ext")
random.seed(1856)

def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def load(lang):
    raw = open(f"{D}/poem_{lang}.txt", encoding="utf-8").read().strip("\n")
    return [s.split("\n") for s in raw.split("\n\n")]

ST = {"en": load("en"), "fr": load("fr")}
LINES = {k: [l for s in v for l in s] for k, v in ST.items()}
def words_of(line):
    return [w.strip(",.;:!?") for w in line.split() if w.strip(",.;:!?")]
def lets(s):
    return re.sub(r"[^a-z]", "", strip_acc(s).lower())

OUT = {}

# ------------------------------------------------------------------ dictionaries
EN_WORDS = set()
for w in wordfreq.top_n_list("en", 40000):
    if w.isalpha() and w.isascii() and len(w) >= 5:
        EN_WORDS.add(w)
FR_WORDS = set()
for w in wordfreq.top_n_list("fr", 40000):
    w2 = lets(w)
    if w2 == strip_acc(w).lower() and len(w2) >= 5:
        FR_WORDS.add(w2)

PLACES = collections.defaultdict(set)   # key -> set of (name, admin1, featurecode)
ADM = {"01": "AB", "02": "BC", "03": "MB", "04": "NB", "05": "NL", "07": "NS", "08": "ON", "09": "PE", "10": "QC",
       "11": "SK", "12": "YT", "13": "NT", "14": "NU"}
for row in open(os.path.join(EXT, "CA.txt"), encoding="utf-8"):
    f = row.rstrip("\n").split("\t")
    name, fclass, fcode, adm, pop = f[1], f[6], f[7], f[10], f[14]
    if fclass not in ("P", "H", "T", "L", "S"):
        continue
    key = lets(name)
    if len(key) >= 6:
        PLACES[key].add((name, ADM.get(adm, adm), fcode, int(pop or 0)))
print("dict sizes", len(EN_WORDS), len(FR_WORDS), len(PLACES))

def stream_cross(lines):
    """letters with word-boundary index so we can require a hit to span >=2 words"""
    s, wid = [], []
    k = 0
    for line in lines:
        for w in words_of(line):
            for c in lets(w):
                s.append(c); wid.append(k)
            k += 1
    return "".join(s), wid

def find_spanning(stream, wid, vocab, minlen, maxlen=20):
    hits = []
    n = len(stream)
    for i in range(n):
        for L in range(minlen, maxlen + 1):
            j = i + L
            if j > n:
                break
            if wid[i] == wid[j - 1]:
                continue  # inside a single word: not hidden
            sub = stream[i:j]
            if sub in vocab:
                hits.append((i, sub, wid[i], wid[j - 1]))
    return hits

def word_shuffle_lines(lines):
    ws = [w for l in lines for w in words_of(l)]
    random.shuffle(ws)
    return [" ".join(ws)]

def hidden_test(lang, vocab, minlen, nnull=300):
    lines = LINES[lang]
    s, wid = stream_cross(lines)
    real = find_spanning(s, wid, vocab, minlen)
    rev = find_spanning(s[::-1], wid[::-1], vocab, minlen)
    nulls = []
    for _ in range(nnull):
        sl = word_shuffle_lines(lines)
        ss, ww = stream_cross(sl)
        nulls.append(len(find_spanning(ss, ww, vocab, minlen)) + len(find_spanning(ss[::-1], ww[::-1], vocab, minlen)))
    obs = len(real) + len(rev)
    pct = sum(1 for x in nulls if x >= obs) / len(nulls)
    allw = [w for l in lines for w in words_of(l)]
    def ctx(h):
        return " ".join(allw[h[2]:h[3] + 1])
    return {"observed": obs, "null_mean": round(statistics.mean(nulls), 1), "null_sd": round(statistics.pstdev(nulls), 1),
            "null_max": max(nulls), "p_ge": round(pct, 3),
            "forward": [[h[1], ctx(h)] for h in real], "reverse": [[h[1], " ".join(allw[h[3]:h[2] + 1])] for h in rev]}

OUT["hidden_en_words6"] = hidden_test("en", EN_WORDS, 6)
OUT["hidden_fr_words6"] = hidden_test("fr", FR_WORDS, 6, 150)
OUT["hidden_en_places7"] = hidden_test("en", PLACES, 7, 150)
OUT["hidden_fr_places7"] = hidden_test("fr", PLACES, 7, 100)
for k in ["hidden_en_places7", "hidden_fr_places7"]:
    det = []
    for w, c in OUT[k]["forward"] + OUT[k]["reverse"]:
        ex = sorted(PLACES[w], key=lambda x: -x[3])[:3]
        det.append([w, c, [f"{n} ({a}, {fc})" for n, a, fc, p in ex]])
    OUT[k]["detail"] = det
for k in ["hidden_en_words6", "hidden_fr_words6", "hidden_en_places7", "hidden_fr_places7"]:
    o = OUT[k]
    print(k, o["observed"], "null", o["null_mean"], "+-", o["null_sd"], "max", o["null_max"], "p", o["p_ge"])
    print("  ", (o["forward"] + o["reverse"])[:40])

# ------------------------------------------------------------------ patterned streams (acrostic family) vs dictionary
def streams_patterned(lang):
    lines = LINES[lang]
    W = [[lets(w) for w in words_of(l)] for l in lines]
    W = [[w for w in ws if w] for ws in W]
    S = {}
    S["line initials"] = "".join(ws[0][0] for ws in W)
    S["line finals"] = "".join(ws[-1][-1] for ws in W)
    S["word initials"] = "".join(w[0] for ws in W for w in ws)
    S["word finals"] = "".join(w[-1] for ws in W for w in ws)
    S["first word of each line, 2nd letters"] = "".join(ws[0][1] if len(ws[0]) > 1 else "" for ws in W)
    S["last word initials"] = "".join(ws[-1][0] for ws in W)
    S["second-word initials"] = "".join(ws[1][0] for ws in W)
    for k in range(1, 9):
        S[f"letter {k} of each line"] = "".join(lets(l)[k - 1] for l in lines)
    for k in range(1, 6):
        S[f"word {k} initials"] = "".join(ws[k - 1][0] if len(ws) >= k else "" for ws in W)
    S["stanza initials"] = "".join(W[i][0][0] for i in range(0, 52, 4))
    S["stanza last-line initials"] = "".join(W[i][0][0] for i in range(3, 52, 4))
    return S

def scan(stream, vocab, minlen=4):
    out = []
    for direction, st in (("→", stream), ("←", stream[::-1])):
        for i in range(len(st)):
            for L in range(minlen, min(15, len(st) - i) + 1):
                if st[i:i + L] in vocab:
                    out.append(direction + st[i:i + L])
    return out

EN4 = set(w for w in wordfreq.top_n_list("en", 20000) if w.isalpha() and w.isascii() and len(w) >= 4)
FR4 = set(lets(w) for w in wordfreq.top_n_list("fr", 20000) if len(lets(w)) >= 4 and lets(w) == strip_acc(w).lower())
pat = {}
for lang, voc in (("en", EN4), ("fr", FR4)):
    S = streams_patterned(lang)
    res = {}
    for name, st in S.items():
        hits = scan(st, voc)
        # null: same letters permuted
        nl = []
        for _ in range(200):
            p = list(st); random.shuffle(p)
            nl.append(len(scan("".join(p), voc)))
        res[name] = {"stream": st.upper(), "hits": hits, "n": len(hits), "null_mean": round(statistics.mean(nl), 2),
                     "p_ge": round(sum(1 for x in nl if x >= len(hits)) / len(nl), 3)}
    pat[lang] = res
OUT["patterned"] = pat
for lang in pat:
    for k, v in pat[lang].items():
        if v["n"]:
            print(lang, k, v["n"], v["null_mean"], v["p_ge"], v["hits"][:8])

# ------------------------------------------------------------------ ELS
TARGETS = ["sudbury", "nickel", "copper", "gold", "cache", "chest", "treasure", "buried", "north", "south", "east", "west",
           "lake", "mine", "shaft", "kelly", "code", "dig", "rock", "core", "creek", "falls", "cobalt", "timmins",
           "ontario", "quebec", "manitoba", "canada", "nipissing", "huron", "trail", "cairn", "plaque", "marker", "salter",
           "murray", "compass", "birch", "cedar", "pine", "one", "two", "three", "four", "five", "six", "seven", "eight",
           "nine", "ten", "zero"]
def els_count(stream, word, maxskip=200):
    n = 0
    L = len(word)
    for d in list(range(2, maxskip + 1)) + list(range(-maxskip, -1)):
        span = (L - 1) * abs(d)
        for i in range(len(stream)):
            j = i + (L - 1) * d
            if j < 0 or j >= len(stream):
                continue
            if all(stream[i + k * d] == word[k] for k in range(L)):
                n += 1
    return n
s_en = lets(" ".join(LINES["en"]))
els = []
nulls = [ "".join(random.sample(s_en, len(s_en))) for _ in range(40)]
for t in TARGETS:
    o = els_count(s_en, t)
    nn = [els_count(x, t) for x in nulls]
    m = statistics.mean(nn)
    sd = statistics.pstdev(nn) or 0.5
    els.append([t, o, round(m, 1), round((o - m) / sd, 2), round(sum(1 for x in nn if x >= o) / len(nn), 3)])
    print("ELS", els[-1])
OUT["els"] = els

# ------------------------------------------------------------------ rarity
def rarity(lang):
    rows = []
    for gi, line in enumerate(LINES[lang], 1):
        for w in words_of(line):
            base = w.lower().replace("’", "'")
            z = wordfreq.zipf_frequency(base, lang)
            if z == 0 and "-" in base:
                z = min(wordfreq.zipf_frequency(p, lang) for p in base.split("-"))
            rows.append([w, gi, z])
    return rows
R_en, R_fr = rarity("en"), rarity("fr")
def uniq_sorted(rows):
    seen = {}
    for w, g, z in rows:
        k = w.lower()
        if k not in seen:
            seen[k] = [w, g, z]
    return sorted(seen.values(), key=lambda r: r[2])
OUT["rarity_en"] = uniq_sorted(R_en)[:40]
OUT["rarity_fr"] = uniq_sorted(R_fr)[:40]
OUT["rarity_stanza_en"] = [round(statistics.mean(r[2] for r in R_en if (r[1] - 1) // 4 == s and r[2] > 0), 2) for s in range(13)]
OUT["rare_count_stanza_en"] = [sum(1 for r in R_en if (r[1] - 1) // 4 == s and r[2] < 3.5) for s in range(13)]
print("rarest EN", OUT["rarity_en"][:25])
print("rarest FR", OUT["rarity_fr"][:20])
print("stanza mean zipf", OUT["rarity_stanza_en"], OUT["rare_count_stanza_en"])

# ------------------------------------------------------------------ metre
def stresses(word):
    w = re.sub(r"[^a-z']", "", word.lower().replace("’", "'"))
    special = {"chalco": "10", "verdigris": "102", "flinty's": "10", "bathurst": "10", "overgrown": "201",
               "zinc-toned": "11", "zinctoned": "11"}
    if w in special:
        return special[w]
    ph = pronouncing.phones_for_word(w)
    if not ph and w.endswith("'s"):
        ph = pronouncing.phones_for_word(w[:-2])
    if ph:
        return pronouncing.stresses(ph[0])
    return None
metre = []
for gi, line in enumerate(LINES["en"], 1):
    pats = []
    for w in words_of(line):
        parts = w.split("-") if "-" in w and stresses(w) is None else [w]
        for p in parts:
            st = stresses(p) or "1"
            pats.append((w, st))
    seq = "".join(st for w, st in pats)
    nsyl = len(seq)
    offset = 1 if nsyl == 8 else (0 if nsyl == 7 else 1)
    # iambic: position (index+offset) odd => stressed
    dev = []
    pos = 0
    for w, st in pats:
        if len(st) > 1:
            for k, c in enumerate(st):
                expected_strong = ((pos + k + (1 if nsyl == 7 else 0)) % 2 == 1)
                if c == "1" and not expected_strong:
                    dev.append(f"{w} (primary stress on weak syllable {pos + k + 1})")
                if c == "0" and expected_strong and len(st) >= 2:
                    dev.append(f"{w} (unstressed syllable on beat {pos + k + 1})")
        pos += len(st)
    metre.append({"g": gi, "line": line, "syl": nsyl, "pattern": seq, "deviations": dev})
OUT["metre"] = metre
for m in metre:
    if m["deviations"] or m["syl"] != 8:
        print("METRE", m["g"], m["syl"], m["pattern"], m["deviations"], m["line"])

# ------------------------------------------------------------------ rhyme
def rhyme_part(w):
    w = re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))
    ph = pronouncing.phones_for_word(w)
    return pronouncing.rhyming_part(ph[0]) if ph else None
rh = []
for i in range(0, 52, 2):
    a, b = words_of(LINES["en"][i])[-1], words_of(LINES["en"][i + 1])[-1]
    ra, rb = rhyme_part(a), rhyme_part(b)
    kind = "perfect" if ra and ra == rb else "slant"
    if ra and rb and kind == "slant":
        va = re.sub(r"\d", "", ra.split()[0]); vb = re.sub(r"\d", "", rb.split()[0])
        kind = "slant (same vowel, consonant differs)" if va == vb else "slant"
    rh.append([i + 1, a, b, ra, rb, kind])
OUT["rhyme"] = rh
print("RHYME non-perfect", [r for r in rh if r[5] != "perfect"])

# ------------------------------------------------------------------ between the lines
jun = []
for i in range(51):
    a, b = words_of(LINES["en"][i])[-1], words_of(LINES["en"][i + 1])[0]
    jun.append([i + 1, a, b, lets(a)[-1].upper() + lets(b)[0].upper()])
OUT["junctions"] = jun
OUT["junction_letters"] = "".join(j[3] for j in jun)
print("JUNCTIONS", OUT["junction_letters"])

# ------------------------------------------------------------------ Murray 1856 comparison
mur = open(os.path.join(D, "..", "..", "..", "..", "..", "..", "home", "user", "Claude", "Murray_1856_report.txt"), encoding="utf-8").read() if False else open("/home/user/Claude/Murray_1856_report.txt", encoding="utf-8").read()
mur_clean = re.sub(r"¬\s*\n", "", mur)
mur_tokens = re.findall(r"[a-z]+", mur_clean.lower())
mur_set = collections.Counter(mur_tokens)
STOP = set(wordfreq.top_n_list("en", 300))
poem_content = collections.Counter(lets(w) for l in LINES["en"] for w in words_of(l) if lets(w) not in STOP and len(lets(w)) > 2)
shared = sorted([(w, poem_content[w], mur_set[w]) for w in poem_content if mur_set.get(w)], key=lambda x: -x[2])
OUT["murray_shared"] = shared
OUT["murray_poem_only"] = sorted([w for w in poem_content if not mur_set.get(w)])
# rarest shared words weighted
OUT["murray_shared_rare"] = sorted([(w, a, b, wordfreq.zipf_frequency(w, "en")) for w, a, b in shared if wordfreq.zipf_frequency(w, "en") < 4.2], key=lambda x: x[3])
# key contexts
ctxs = {}
for key in ["compass", "attraction", "deviation", "magnetic", "fault", "trap", "copper", "nickel", "salter", "birch", "cedar", "pine", "iron", "zinc", "gold", "shield"]:
    ms = [m.start() for m in re.finditer(r"\b" + key, mur_clean, re.I)]
    ctxs[key] = [len(ms)] + [re.sub(r"\s+", " ", mur_clean[max(0, m - 160):m + 200]) for m in ms[:2]]
OUT["murray_ctx"] = ctxs
print("MURRAY shared (top)", shared[:40])
print("MURRAY rare shared", OUT["murray_shared_rare"][:30])
print("compass ctx", ctxs["compass"][:2])

json.dump(OUT, open(f"{D}/deep.json", "w"), ensure_ascii=False, indent=1)
print("saved")
