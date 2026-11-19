# D100: leaf-number reads on all 10 tours of the Rainbow Routes "Trail Tours" booklet (EN + FR). See PREREG.
import json, os, random, sys, unicodedata, wordfreq
OUT = os.path.dirname(os.path.abspath(__file__))
def fold(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if c.isalpha() and ord(c) < 128)

def sets(items):
    return {'T': [fold(i['title']) for i in items], 'B': [i['body'] for i in items],
            'TB': [fold(i['title']) + i['body'] for i in items]}
UNITS = []   # (scheme, lang, tour, set, list)
for lang in ('EN', 'FR'):
    items = json.load(open(os.path.join(OUT, f'items100_{lang}.json')))
    for s, us in sets(items).items(): UNITS.append(('global', lang, 0, s, us))
    for t in range(1, 11):
        for s, us in sets([i for i in items if i['tour'] == t]).items(): UNITS.append(('tour', lang, t, s, us))

ENW = [1,1,2,2,1,2,2,1,2]; FRW = [1,1,2,2,1,2,2,2,1]
z = lambda d: 10 if d == 0 else d
def groups(ds, w):
    o = []; i = 0
    for k in w: o.append(int(ds[i:i+k])); i += k
    return o
def keys(en, fr):
    e, f = groups(en, ENW), groups(fr, FRW)
    ed, fd = [z(int(c)) for c in en], [z(int(c)) for c in fr]
    return {'Z1': list(zip(e, f)), 'Z2': list(zip(f, e)), 'D1': list(zip(ed, fd)), 'D2': list(zip(fd, ed))}
def read(us, pairs):
    o = []
    for it, le in pairs:
        if it < 1 or it > len(us) or le < 1 or le > len(us[it-1]): return None
        o.append(us[it-1][le-1])
    return ''.join(o)
def reads(K):
    out = []
    for scheme, lang, tour, s, us in UNITS:
        rds = ('Z1', 'Z2', 'D1', 'D2') if scheme == 'global' else ('D1', 'D2')
        for rd in rds:
            r = read(us, K[rd]); tag = rd
            if r is None and scheme == 'tour' and rd == 'D1':
                r = read(us, K[rd][:13]); tag = 'D1-prefix13'
            if r is not None: out.append((scheme, lang, tour, s, tag, r))
    return out

LONG = set()
for lg in ('en', 'fr'):
    for w in wordfreq.top_n_list(lg, 50000):
        f = fold(w)
        if len(f) >= 7: LONG.add(f)
for w in ('whitewater','falconbridge','coppercliff','creighton','wahnapitae','chelmsford','nickeldale','vermilion','belvedere','derriere','treasure','lookout'): LONG.add(w)
def s1(s):
    b = ''
    for i in range(len(s)):
        for j in range(i+7, len(s)+1):
            if s[i:j] in LONG and j-i > len(b): b = s[i:j]
    return b
def the(r):
    lang, s = r[1], r[5]
    return s.startswith('the') if lang == 'EN' else (s.startswith('les') or s[:2] in ('le', 'la'))
def score(rs): return sum(1 for r in rs if s1(r[5])), sum(1 for r in rs if the(r))

REAL = keys('62763732569420', '32581671424253')
rr = reads(REAL); rs1, rthe = score(rr)
print(f'REAL: {len(rr)} reads in range; S1 {rs1}; THE {rthe}')
for r in rr:
    b = s1(r[5])
    print(' ', r[0].ljust(6), r[1], f'T{r[2]}'.ljust(3), r[3].ljust(2), r[4].ljust(11), r[5], ('| S1=' + b) if b else '', '| THE' if the(r) else '')

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
R = random.Random(100); n1 = []; n2 = []
for _ in range(N):
    en = ''.join(str(R.randint(0, 9)) for _ in range(14)); fr = ''.join(str(R.randint(0, 9)) for _ in range(14))
    a, b = score(reads(keys(en, fr))); n1.append(a); n2.append(b)
P1 = sum(x >= rs1 for x in n1) / N; P2 = sum(x >= rthe for x in n2) / N
print(f'NULL (n={N}): S1 mean {sum(n1)/N:.3f} P={P1:.4f}; THE mean {sum(n2)/N:.3f} P={P2:.4f}')

def plant(us, pairs, word):
    us = list(us)
    for it, le in pairs:
        while len(us) < it: us.append('x' * 20)
        if len(us[it-1]) < le: us[it-1] += 'x' * (le - len(us[it-1]))
    for (it, le), ch in zip(pairs, word):
        u = us[it-1]; us[it-1] = u[:le-1] + ch + u[le:]
    return us
gEN = [u for u in UNITS if u[:4] == ('global', 'EN', 0, 'TB')][0][4]
t2FR = [u for u in UNITS if u[:4] == ('tour', 'FR', 2, 'TB')][0][4]
c1 = read(plant(gEN, REAL['Z1'], 'whitewater'), REAL['Z1'])
c2 = read(plant(t2FR, REAL['D2'], 'dessouspont'), REAL['D2'])
print('CONTROLS:', c1, '->', s1(c1), '|', c2, '->', s1(c2))
json.dump(dict(reads=rr, S1=rs1, THE=rthe, P_S1=P1, P_THE=P2, null_n=N, null_S1_mean=sum(n1)/N, null_THE_mean=sum(n2)/N,
               controls=[c1, s1(c1), c2, s1(c2)]), open(os.path.join(OUT, 'd100_result.json'), 'w'), indent=1)
