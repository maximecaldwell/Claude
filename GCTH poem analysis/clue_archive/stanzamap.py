import os,re,json,numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.optimize import linear_sum_assignment
D=os.path.dirname(os.path.abspath(__file__)); T=os.path.join(D,"..","arts","out","text"); W=os.path.join(D,"..","arts","web")
poem=[l for l in open(f"{D}/poem_en.txt").read().split("\n\n")]
CH=[("1 Dawson City",f"{W}/1003882693.txt"),("2 Cobalt",f"{T}/cobalt_en.txt"),("3 Golden Triangle",f"{T}/golden_en.txt"),
("4 Argentia",f"{T}/argentia_en.txt"),("5 Britannia (S. BC)",f"{T}/southbc_en.txt"),("6 Toronto",f"{T}/toronto_en.txt"),
("7 Bathurst",f"{T}/bathurst_en.txt"),("8 Val-d'Or",f"{T}/valdor_en.txt"),("9 Saskatchewan",f"{T}/sask_en.txt"),
("10 Nova Scotia",f"{W}/1003892433.txt"),("11 Manitoba",f"{T}/manitoba_en.txt"),("12 Sudbury",f"{T}/sudbury_en.txt"),("13 Chibougamau",f"{T}/nelligan_en.txt")]
docs=[open(p).read() for _,p in CH]
# expand poem with domain glosses so metaphors meet article vocabulary
GL={"glaciers":"glacier ice mountain","gold":"gold","copper":"copper","salt":"salt sea ocean coast","brine":"brine sea salt","fire":"fire burned flames",
"phoenix":"rebuilt fire","seams":"veins seams","coin":"coin nickel","circles":"basin crater impact","chalco":"chalcopyrite copper","flinty":"flin flon flintabbatey",
"east":"quebec east","shield":"shield precambrian","iron":"iron ore","cedars":"cedar","marker":"plaque marker cairn","pine":"pine","shore":"shore lake",
"zinc":"zinc","bathurst":"bathurst brunswick","bell":"bell","suits":"bankers financiers","bay":"bay street exchange","share":"shares stock","mining":"mining",
"birch":"birch","verdigris":"copper green patina","mirror":"lake water","veins":"veins","code":"code","current":"river current"}
def gloss(s): return s+" "+" ".join(GL[w] for w in re.findall(r"[a-z]+",s.lower()) if w in GL)
vec=TfidfVectorizer(stop_words="english",sublinear_tf=True,token_pattern=r"[a-zA-Z]{3,}")
X=vec.fit_transform(docs+[gloss(p) for p in poem])
A=X[:13]; P=X[13:]
S=(P@A.T).toarray()   # 13 stanzas x 13 chapters
r,c=linear_sum_assignment(-S)
out={"chapters":[n for n,_ in CH],"S":S.round(3).tolist(),"assign":[[int(i),int(j)] for i,j in zip(r,c)]}
json.dump(out,open(f"{D}/stanzamap.json","w"),indent=1)
print("stanza -> top-3 chapters (score)")
for i in range(13):
    top=np.argsort(-S[i])[:3]
    print(f"S{i+1:2} {poem[i].split(chr(10))[0][:42]:42} | "+" ; ".join(f"{CH[j][0]} {S[i,j]:.3f}" for j in top)+f"  || assigned: {CH[c[i]][0]}")
# null: how often does random stanza shuffle give >= total assignment score? (permutation of stanza rows)
tot=S[r,c].sum()
rng=np.random.default_rng(1)
