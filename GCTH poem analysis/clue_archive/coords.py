"""Test digit fragments as latitude/longitude, against a random-digit baseline.

Rule set (kept small on purpose, so hits mean something):
  * latitude 41.67–66.56 (Canada, south of the Arctic Circle: "shall not see the midnight sun")
  * longitude west 52.6–141.0, written without a minus sign
  * point must fall on Canadian land (Natural Earth 1:50m)
  * decimal readings: DD.ddd… with the decimal after the 2 integer digits (lat) and after 2 or 3 (lon)
  * DMS readings: DD MM SS where MM, SS < 60
"""
import itertools, json, os, pickle, random, re, sys, math
from shapely.geometry import Point

D = os.path.dirname(os.path.abspath(__file__))
CAN = pickle.load(open(os.path.join(D, "..", "geo", "canada.pkl"), "rb"))
random.seed(217)

# nearest named place for reporting
PLACES = []
for row in open(os.path.join(D, "..", "ext", "CA.txt"), encoding="utf-8"):
    f = row.split("\t")
    if f[6] == "P":
        PLACES.append((float(f[4]), float(f[5]), f[1], f[10], int(f[14] or 0)))
ADM = {"01": "AB", "02": "BC", "03": "MB", "04": "NB", "05": "NL", "07": "NS", "08": "ON", "09": "PE", "10": "QC",
       "11": "SK", "12": "YT", "13": "NT", "14": "NU"}

def nearest(lat, lon):
    best = None
    for p in PLACES:
        d = (p[0] - lat) ** 2 + ((p[1] + lon) * math.cos(math.radians(lat))) ** 2
        if best is None or d < best[0]:
            best = (d, p)
    d, p = best
    return f"{p[2]}, {ADM.get(p[3], p[3])} ({math.sqrt(d) * 111:.1f} km)"

def ok(lat, lon):
    return 41.67 <= lat <= 66.56 and 52.6 <= lon <= 141.0 and CAN.contains(Point(-lon, lat))

def dec_readings(a, b):
    """a, b digit strings -> candidate (lat, lon) decimal readings."""
    out = []
    if len(a) >= 2:
        lat = float(a[:2] + "." + a[2:]) if len(a) > 2 else float(a)
        for k in (2, 3):
            if len(b) >= k:
                lon = float(b[:k] + "." + b[k:]) if len(b) > k else float(b)
                out.append((lat, lon, f"{a[:2]}.{a[2:]} / {b[:k]}.{b[k:]}"))
    return out

def dms_readings(a, b):
    out = []
    def parse(s, degw):
        if len(s) < degw + 2:
            return None
        dd, mm, ss = int(s[:degw]), int(s[degw:degw + 2]), s[degw + 2:degw + 4]
        ss = int(ss) if len(ss) == 2 else 0
        if mm >= 60 or ss >= 60:
            return None
        return dd + mm / 60 + ss / 3600
    lat = parse(a, 2)
    for w in (2, 3):
        lon = parse(b, w)
        if lat is not None and lon is not None:
            out.append((lat, lon, f"DMS {a} / {b}"))
    return out

def candidates_from_split(digits):
    """All ways to cut one digit string into two numbers (lat first)."""
    for i in range(2, len(digits) - 1):
        a, b = digits[:i], digits[i:]
        for r in dec_readings(a, b) + dms_readings(a, b):
            yield r

def candidates_from_groups(groups):
    """Ordered pairs of whole groups (each group one number)."""
    for a, b in itertools.permutations(groups, 2):
        for r in dec_readings(a, b) + dms_readings(a, b):
            yield r

def test(name, kind, data):
    gen = candidates_from_split if kind == "split" else candidates_from_groups
    cands = list(gen(data))
    hits = [(lat, lon, lab) for lat, lon, lab in cands if ok(lat, lon)]
    # null: same structure, random digits
    rates = []
    for _ in range(300):
        if kind == "split":
            rd = "".join(random.choice("0123456789") for _ in data)
        else:
            rd = ["".join(random.choice("0123456789") for _ in g) for g in data]
        c = list(gen(rd))
        rates.append(sum(1 for la, lo, _ in c if ok(la, lo)))
    mean = sum(rates) / len(rates)
    p = sum(1 for r in rates if r >= len(hits)) / len(rates)
    return {"name": name, "kind": kind, "n_cands": len(cands), "hits": len(hits), "null_mean": round(mean, 2), "p_ge": round(p, 3),
            "examples": [(round(la, 5), round(lo, 5), lab, nearest(la, lo)) for la, lo, lab in hits[:12]]}

# ---------------- fragments ----------------
nell_en = [(1, 13), (10, 4), (25, 1), (36, 3), (45, 1), (55, 13), (63, 1), (66, 21), (77, 32)]
nell_fr = [(4, 1), (9, 1), (22, 1), (28, 1), (36, 1), (37, 1), (47, 1), (65, 1), (70, 2), (81, 1), (82, 1)]
tor_txt = open(os.path.join(D, "..", "arts", "out", "text", "toronto_en.txt")).read().split("\n")[36]
tor = [(int(a), int(b)) for a, b in re.findall(r"(\d+)-\s*(\d+)", tor_txt)]
FR = {
    "Val-d'Or EN 810-419-227": ["810", "419", "227"],
    "Val-d'Or FR 1045-420-275": ["1045", "420", "275"],
    "One-year Quebec 20 · 60 · 5": ["20", "60", "5"],
    "Boyd video 217 · 14": ["217", "14"],
}
extra = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else {}
FR.update(extra.get("groups", {}))
SPLIT = {
    "Val-d'Or EN digits": "810419227",
    "Val-d'Or FR digits": "1045420275",
    "Val-d'Or EN+FR": "8104192271045420275",
    "Nelligan EN pair digits": "".join(f"{a}{b}" for a, b in nell_en),
    "Nelligan FR pair digits": "".join(f"{a}{b}" for a, b in nell_fr),
    "Toronto pair digits (first 40)": "".join(f"{a}{b}" for a, b in tor)[:40],
    "Quebec 20605": "20605",
    "Codes in chapter order (Toronto first-pair, Val-d'Or, Nelligan first-pair, Quebec)": "2835" + "810419227" + "113" + "20605",
}
SPLIT.update(extra.get("split", {}))
R = [test(k, "groups", v) for k, v in FR.items()] + [test(k, "split", v) for k, v in SPLIT.items()]
json.dump(R, open(os.path.join(D, "coords.json"), "w"), indent=1, ensure_ascii=False)
for r in R:
    print(f"{r['name'][:60]:60} cands={r['n_cands']:4} hits={r['hits']:3} null={r['null_mean']:6} p={r['p_ge']}")
    for e in r["examples"][:6]:
        print("      ", e)
