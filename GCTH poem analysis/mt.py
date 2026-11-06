import json, os, re, sacrebleu
from transformers import MarianMTModel, MarianTokenizer
D=os.path.dirname(os.path.abspath(__file__))
en=[l for l in open(f"{D}/poem_en.txt",encoding="utf-8").read().split("\n") if l.strip()]
fr=[l for l in open(f"{D}/poem_fr.txt",encoding="utf-8").read().split("\n") if l.strip()]
m='Helsinki-NLP/opus-mt-en-fr'; tok=MarianTokenizer.from_pretrained(m); mod=MarianMTModel.from_pretrained(m)
def tr(lines):
    out=[]
    for i in range(0,len(lines),8):
        b=tok(lines[i:i+8],return_tensors="pt",padding=True)
        g=mod.generate(**b,num_beams=5,max_new_tokens=80)
        out+=tok.batch_decode(g,skip_special_tokens=True)
    return out
mt_line=tr(en)
# stanza-level (lines joined, then compare whole stanza)
stz=[" ".join(en[i:i+4]) for i in range(0,52,4)]
mt_stz=tr(stz)
norm=lambda s: re.sub(r"\s+"," ",s.replace("'", "’").strip().rstrip(".")).lower()
rows=[]
for i,(e,f,t) in enumerate(zip(en,fr,mt_line),1):
    c=sacrebleu.sentence_chrf(norm(t),[norm(f)]).score
    rows.append([i,e,f,t,round(c,1),norm(t)==norm(f)])
corpus_chrf=sacrebleu.corpus_chrf([norm(x) for x in mt_line],[[norm(x) for x in fr]]).score
corpus_bleu=sacrebleu.corpus_bleu([norm(x) for x in mt_line],[[norm(x) for x in fr]]).score
frs=[" ".join(fr[i:i+4]) for i in range(0,52,4)]
stz_chrf=sacrebleu.corpus_chrf([norm(x) for x in mt_stz],[[norm(x) for x in frs]]).score
exact=sum(r[5] for r in rows)
# word-level: fraction of official FR content words that also appear in MT line
import collections
ov=[]
for r in rows:
    a=set(re.findall(r"[a-zàâäéèêëîïôöùûüç]+",norm(r[2]))); b=set(re.findall(r"[a-zàâäéèêëîïôöùûüç]+",norm(r[3])))
    ov.append(len(a&b)/max(1,len(a)))
res={"rows":rows,"corpus_chrf":round(corpus_chrf,1),"corpus_bleu":round(corpus_bleu,1),"stanza_chrf":round(stz_chrf,1),"exact":exact,"word_overlap_mean":round(sum(ov)/len(ov),3),"mt_stanzas":mt_stz}
json.dump(res,open(f"{D}/mt.json","w"),ensure_ascii=False,indent=1)
print({k:v for k,v in res.items() if k not in("rows","mt_stanzas")})
for r in rows: print(r[0],r[4],"EXACT" if r[5] else "","|",r[2],"||",r[3])
