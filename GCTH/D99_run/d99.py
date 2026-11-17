# D99: leaf-number reads on the Jane Goodall trail's 9 numbered booklet items (EN + FR). See PREREG.
import json, os, random, unicodedata, wordfreq
OUT = os.path.dirname(os.path.abspath(__file__))
def fold(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if c.isalpha() and ord(c) < 128)

def units(lang):
    d = json.load(open(os.path.join(OUT, f'items_{lang}.json')))
    T = [fold(t) for t, b in d['items']]; B = [fold(b) for t, b in d['items']]
    TB = [fold(t + b) for t, b in d['items']]
    Bt = list(B); Bt[6] = fold(d['items'][6][1] + d['tip'])
    TBt = list(TB); TBt[6] = fold(d['items'][6][0] + d['items'][6][1] + d['tip'])
    return {'T': T, 'B': B, 'TB': TB, 'B+tip': Bt, 'TB+tip': TBt}   # T has no tip variant; counted once
U = {lang: units(lang) for lang in ('EN', 'FR')}

z = lambda d: 10 if d == 0 else d
def keys(en, fr):
    e = [z(int(c)) for c in en]; f = [z(int(c)) for c in fr]
    return {'D1': list(zip(e, f)), 'D2': list(zip(f, e))}
def read(us, pairs):
    o = []
    for it, le in pairs:
        if it < 1 or it > len(us) or le < 1 or le > len(us[it-1]): return None
        o.append(us[it-1][le-1])
    return ''.join(o)
def reads(K, U):
    out = []
    for lang, uu in U.items():
        for ut, us in uu.items():
            for rd, pairs in K.items():
                s = read(us, pairs)
                if s is None and rd == 'D1': s = read(us, pairs[:13]); tag = 'D1-prefix13'
                else: tag = rd
                if s is not None: out.append((lang, ut, tag, s))
    return out

LONG = set()
for lang in ('en', 'fr'):
    for w in wordfreq.top_n_list(lang, 50000):
        f = fold(w)
        if len(f) >= 7: LONG.add(f)
for w in ('whitewater','falconbridge','coppercliff','creighton','wahnapitae','chelmsford','nickeldale','vermilion','belvedere','derriere','treasure','lookout'): LONG.add(w)
def s1(s):
    b = ''
    for i in range(len(s)):
        for j in range(i+7, len(s)+1):
            if s[i:j] in LONG and j-i > len(b): b = s[i:j]
    return b
def the(r): lang, s = r[0], r[3]; return s.startswith('the') if lang == 'EN' else (s.startswith('les') or s[:2] in ('le', 'la'))
def score(rs): return sum(1 for r in rs if s1(r[3])), sum(1 for r in rs if the(r))

EN, FR = '62763732569420', '32581671424253'
REAL = keys(EN, FR)
rr = reads(REAL, U)
rs1, rthe = score(rr)
print(f'REAL: {len(rr)} reads in range; S1 {rs1}; THE {rthe}')
for r in rr: print(' ', r[0], r[1].ljust(7), r[2].ljust(12), r[3], '| S1=' + s1(r[3]) if s1(r[3]) else '', '| THE' if the(r) else '')

R = random.Random(99)
N = 10000; ge1 = ge2 = 0; nul1 = []; nul2 = []
for _ in range(N):
    en = ''.join(str(R.randint(0, 9)) for _ in range(14)); fr = ''.join(str(R.randint(0, 9)) for _ in range(14))
    a, b = score(reads(keys(en, fr), U)); nul1.append(a); nul2.append(b)
    ge1 += a >= rs1; ge2 += b >= rthe
print(f'NULL (n={N}): S1 mean {sum(nul1)/N:.3f}, P(S1>=real) = {ge1/N:.4f}; THE mean {sum(nul2)/N:.3f}, P(THE>=real) = {ge2/N:.4f}')

# controls: plant via D2 into copies of TB, padding every pair
def plant(us, pairs, word):
    us = list(us)
    for it, le in pairs:
        while len(us) < it: us.append('x' * 20)
        if len(us[it-1]) < le: us[it-1] += 'x' * (le - len(us[it-1]))
    for (it, le), ch in zip(pairs, word):
        u = us[it-1]; us[it-1] = u[:le-1] + ch + u[le:]
    return us
c1 = read(plant(U['EN']['TB'], REAL['D2'], 'whitewater'), REAL['D2'])
c2 = read(plant(U['FR']['TB'], REAL['D2'], 'dessouspont'), REAL['D2'])
print('CONTROLS:', c1, '->', s1(c1), '|', c2, '->', s1(c2))
json.dump(dict(reads=rr, S1=rs1, THE=rthe, P_S1=ge1/N, P_THE=ge2/N, null_S1_mean=sum(nul1)/N, null_THE_mean=sum(nul2)/N,
               controls=[c1, s1(c1), c2, s1(c2)]), open(os.path.join(OUT, 'd99_result.json'), 'w'), indent=1, ensure_ascii=False)
