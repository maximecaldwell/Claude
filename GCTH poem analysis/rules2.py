import re, json, collections, pronouncing, os
D=os.path.dirname(os.path.abspath(__file__))
L=[l for l in open(f"{D}/poem_en.txt",encoding="utf-8").read().split("\n") if l.strip()]
W=lambda l:[w.strip(",") for w in l.split()]
def rp(w):
    w=re.sub(r"[^a-z']","",w.lower().replace("’","'"))
    if w=="wets": w="bets"
    p=pronouncing.phones_for_word(w)
    return pronouncing.rhyming_part(p[0]) if p else None
def nsyl(w):
    w=re.sub(r"[^a-z']","",w.lower().replace("’","'"))
    p=pronouncing.phones_for_word(w) or pronouncing.phones_for_word(w.replace("'s",""))
    return pronouncing.syllable_count(p[0]) if p else 2
print("== rhyme sounds")
snd=collections.defaultdict(list)
for i in range(0,52,2):
    a=W(L[i])[-1]; snd[re.sub(r"\d","",rp(a) or a)].append((i//4+1,W(L[i])[-1],W(L[i+1])[-1]))
for k,v in snd.items(): print(k,v)
print("== vowel of rhyme per couplet");
print([re.sub(r"\d","",(rp(W(L[i])[-1]) or "?").split()[0]) for i in range(0,52,2)])
print("== all-monosyllable lines")
for g,l in enumerate(L,1):
    if all(nsyl(w)==1 for w in W(l)): print(g,l)
print("== polysyllable count per line", [sum(1 for w in W(l) if nsyl(w)>1) for l in L])
print("== commas/contractions")
for g,l in enumerate(L,1):
    if "," in l or "’t" in l: print(g,l)
print("== openers by stanza position")
op=collections.defaultdict(list)
for g,l in enumerate(L,1): op[W(l)[0]].append(f"{(g-1)//4+1}.{(g-1)%4+1}")
for k,v in sorted(op.items(),key=lambda x:-len(x[1])): print(k,v)
print("== turn words")
TURN=r"\b(but|yet|no|not|nor|never|none|don’t|won’t|unseen|disappears|fade|pales|dulled|mislead|forgets)\b"
for s in range(13):
    t=[(j+1,m.group(0)) for j in range(4) for m in re.finditer(TURN,L[s*4+j].lower())]
    print(s+1,t)
print("== alliteration (repeated initial consonant sounds among stressed words)")
for g,l in enumerate(L,1):
    ws=[w.lower() for w in W(l) if len(w)>3 or w.lower() in("gold","salt","red","fire")]
    ini=collections.Counter(w[0] for w in ws if w[0] not in "aeiou")
    rep={k:v for k,v in ini.items() if v>=2}
    if rep: print(g,rep,l)
print("== content words repeated across stanzas")
STOP=set("the a an and but in of to by for with where what its is no not nor once now still yet be will may have through past beyond beneath behind all one none".split())
pos=collections.defaultdict(list)
norm=lambda w:{"birches":"birch","whispers":"whisper","marks":"mark","marker":"mark","marked":"mark","trees":"tree","roots":"root","speaks":"speak","waters":"water","silent":"silence","grows":"grow","grew":"grow","growing":"grow","paths":"path","held":"hold","forgets":"forget"}.get(w,w)
for g,l in enumerate(L,1):
    for w in W(l):
        k=norm(re.sub(r"[^a-z’]","",w.lower()))
        if k not in STOP: pos[k].append(g)
for k,v in sorted(pos.items(),key=lambda x:x[1][0]):
    st=sorted(set((g-1)//4+1 for g in v))
    if len(st)>1: print(k,v,"stanzas",st)
