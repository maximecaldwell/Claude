#!/usr/bin/env python3
"""pdftotext (raw, non-layout) output -> paragraphs.
usage: pdf2txt.py in.txt out.txt [drop_regex]
Heuristic: a line that is clearly shorter than the column width ends a paragraph."""
import sys, re, statistics

LIG = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', '­': ''}

src = open(sys.argv[1], encoding='utf-8').read()
for k, v in LIG.items():
    src = src.replace(k, v)
src = src.replace('\f', '\n\n')
drop = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
lines = [l.rstrip() for l in src.split('\n')]
lens = [len(l) for l in lines if len(l) > 40]
width = statistics.quantiles(lens, n=10)[8] if len(lens) > 10 else 90
paras, cur = [], []
bullet = False
for l in lines:
    s = l.strip()
    if drop and s and drop.search(s):
        continue
    if not s:
        if cur:
            paras.append(cur); cur = []
        continue
    if s in ('•', '●', '▪', '-'):
        if cur:
            paras.append(cur); cur = []
        bullet = True
        continue
    if 'bullet' in globals() and bullet:
        s = '- ' + s; bullet = False
    cur.append(s)
    if len(l) < 0.8 * width:
        paras.append(cur); cur = []
if cur:
    paras.append(cur)
out = []
for p in paras:
    t = ''
    for s in p:
        if t.endswith('-') and not t.endswith(' -') and s[:1].islower():
            t = t[:-1] + s
        else:
            t = (t + ' ' + s) if t else s
    t = re.sub(r'\s+', ' ', t).strip()
    if t and not re.fullmatch(r'\d{1,3}', t):
        out.append(t)
open(sys.argv[2], 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
print(sys.argv[2], sum(len(x.split()) for x in out))
