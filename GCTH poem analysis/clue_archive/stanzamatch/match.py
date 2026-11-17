import re, math, random, json, unicodedata, itertools
import numpy as np
from scipy.optimize import linear_sum_assignment
from wordfreq import zipf_frequency
A='/tmp/claude-0/-home-user-Claude/e088f49c-24ac-59a0-bf76-b6e7517bba6d/scratchpad/'
P='/home/user/Claude/GCTH poem analysis/'
en=[l for l in open(P+'poem_en.txt',encoding='utf-8').read().split('\n') if l.strip()]
fr=[l for l in open(P+'poem_fr.txt',encoding='utf-8').read().split('\n') if l.strip()]
T=A+'arts/out/text/'
CH={ # chapter: (EN file or None, FR file)
 'Cobalt':('2025-10-20__1003883782__Treasure-Hunt_Cobalt_BTM_embedded_Final.txt','2025-10-20__1003883783__Treasure-Hunt_Cobalt_FR.txt'),
 'Golden Triangle':('2025-11-19__1003884744__Golden-Triangle-Dreams-From-Buck-to-Billions_Final-FINAL.txt','2025-11-19__1003884743__Golden-Triangle-FR-version-FINAL.txt'),
 'Argentia':('2025-12-17__1003885767__English.txt','2025-12-18__1003885833__Argentia-Terre-dargent-et-de-secondes-chances.txt'),
 'Southern BC':('2026-01-27__1003886917__Southern-BC-English.txt','2026-01-27__1003886916__Southern-BC-French.txt'),
 'Toronto':('2026-02-24__1003888069__TH_Toronto_BTM_Final.txt','2026-02-24__1003888068__Toronto-fr.txt'),
 'Bathurst':('2026-03-24__1003889269__TH_Bathurst_Eng_Final.txt','2026-03-24__1003889268__TH_Bathurst_FR_Final.txt'),
 "Val-d'Or":('2026-04-28__1003890424__Val-dor-English.txt','2026-04-28__1003890425__val-dor-FR.txt'),
 'Klondike':(None,'2026-05-15__1003891142__Klondike.v.2-fr_final.txt'),
 'Saskatchewan':('2026-05-26__1003891454__SK_EN_Final.txt','2026-05-26__1003891453__Saskatchewan-FR.txt'),
 'Nova Scotia':(None,'2026-06-24__1003892426__TH_Nova_Scotia_Final_FR.txt'),
 'Manitoba':('2026-07-29__1003893528__Manitoba-Eng.txt','2026-07-29__1003893529__manitoba-fr.txt'),
 'Sudbury':('2026-08-25__1003894294__Sudbury_final.txt','2026-08-25__1003894293__Sudbury_final_FR.txt'),
 'Chibougamau':('../../../2026-09-29__1003895272__Nelligan-EN-FINAL.raw.txt','../../../2026-09-29__1003895273__Nelligan-FR-FINAL.raw.txt'),
}
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
def toks(s):
    return [strip(w.lower()) for w in re.findall(r"[A-Za-zÀ-ÿ]+",s.replace('’',"'"))]
def stem(w): return w[:6]
def bag(s,lang):
    out={}
    for w in toks(s):
        if len(w)<4: continue
        z=zipf_frequency(w,lang)
        if z>5.0: continue  # drop very common words
        out[stem(w)]=max(out.get(stem(w),0), 7.0-z)  # rarity weight
    return out
def stanzas(lines): return [' '.join(lines[i:i+4]) for i in range(0,len(lines),4)]
art={}
for k,(e,f) in CH.items():
    art[k]=( bag(open(T+e,encoding='utf-8',errors='ignore').read(),'en') if e else None,
             bag(open(T+f,encoding='utf-8',errors='ignore').read(),'fr'))
def score_matrix(SE,SF):
    BE=[bag(s,'en') for s in SE]; BF=[bag(s,'fr') for s in SF]
    M=np.zeros((len(CH),len(SE)))
    for i,k in enumerate(CH):
        ae,af=art[k]
        for j in range(len(SE)):
            se=sum(BE[j][w] for w in BE[j] if ae and w in ae)
            sf=sum(BF[j][w] for w in BF[j] if w in af)
            M[i,j]=(se if ae else sf)+sf  # FR-only chapters: count FR twice to keep scale
    # normalise per chapter (article length differs): z-score across stanzas
    M=(M-M.mean(1,keepdims=True))/(M.std(1,keepdims=True)+1e-9)
    return M
SE,SF=stanzas(en),stanzas(fr)
M=score_matrix(SE,SF)
r,c=linear_sum_assignment(-M); obs=M[r,c].sum()
names=list(CH)
print('Best one-to-one assignment (chapter -> stanza, z):')
for i,j in zip(r,c): print(f'  {names[i]:14s} -> stanza {j+1:2d}  z={M[i,j]:.2f}   (best single: stanza {M[i].argmax()+1}, z={M[i].max():.2f})')
left=sorted(set(range(13))-set(c)); print('Stanza left over:',[x+1 for x in left])
# null: shuffle lines across stanzas (same line pairs EN/FR kept together)
random.seed(1); null=[]
idx=list(range(len(en)))
for _ in range(1000):
    random.shuffle(idx)
    E=[en[i] for i in idx]; F=[fr[i] for i in idx]
    N=score_matrix(stanzas(E),stanzas(F)); rr,cc=linear_sum_assignment(-N); null.append(N[rr,cc].sum())
null=np.array(null); print(f'Total assignment score {obs:.2f}; null mean {null.mean():.2f} sd {null.std():.2f}; p = {(null>=obs).mean():.3f}')
json.dump({'names':names,'M':M.tolist(),'assign':[[names[i],int(j)+1] for i,j in zip(r,c)],'obs':obs,'null_mean':float(null.mean()),'p':float((null>=obs).mean())},open(A+'stanzamatch/result.json','w'),indent=1)
