"""Write Python reference results for web/crosscheck.js.

    python3 web/make_reference.py ref.json && node web/crosscheck.js ref.json
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from indexkit.text import Text
from indexkit.digits import DigitString
from indexkit.conventions import Config
from indexkit.engine import Analysis, NullTest, random_orders
from indexkit.demo_article import EN_PARAGRAPHS, FR_PARAGRAPHS, TARGETS, as_file_text
from indexkit.wordlists import builtin_wordlist
en = as_file_text(EN_PARAGRAPHS); fr = as_file_text(FR_PARAGRAPHS)
big = '\n\n'.join(as_file_text(EN_PARAGRAPHS).split('\n'))  # every line its own paragraph
tricky = "« Titre » : l’Or\n\nIl dit : « Bonjour. » Puis… Val-d'Or – c’est 1887 !\nNouvelle ligne ; ok.\n\nCœur ÉTÉ ? Oui. aujourd’hui (non) don't stop.\n\nFin\n"
texts = {'en': en, 'fr': fr, 'big': big, 'tricky': tricky}
rng = np.random.default_rng(42)
cases = []
digit_strings = ["67-90-143", "2638", "810-419-227", "6 2 76 37 3 25 69 4 20", "1", "0 0 0", "12345678901234", "3.14.15"]
for _ in range(10):
    k = rng.integers(1, 6)
    digit_strings.append(" ".join("".join(str(x) for x in rng.integers(0,10,rng.integers(1,4))) for _ in range(k)))
for tname, raw in texts.items():
    for mode in ('targets', 'letters'):
        for ds_raw in digit_strings:
            markers = ["Son magasin|Her store", "Ottawa"] if tname != 'tricky' else ["Nouvelle"]
            cfg = Config(mode, markers=markers)
            t = Text.from_string(tname, raw)
            ds = DigitString(ds_raw)
            wl = builtin_wordlist('en') + ['ab', 'abcdefghijklmn']
            an = Analysis(t, ds, cfg, targets=TARGETS + ['Or', 'Titre', 'Lanternes'], wordlist=wl)
            s, h = an.observed()
            orders = random_orders(rng, 2, len(t.paragraphs)) if len(t.paragraphs) >= 3 else None
            sb = an.evaluate(ds.matrix(), orders)[0].tolist() if orders is not None else None
            cases.append(dict(text=tname, mode=mode, digits=ds_raw, markers=markers,
                              names=[c.name for c in an.convs], aliases=[c.aliases for c in an.convs],
                              scores=s.tolist(), hits=h.astype(int).tolist(),
                              orders=orders.tolist() if orders is not None else None, scoresB=sb,
                              merged=an.tv.n_merged, warnings=an.tv.warnings))
# Null test comparison: fixed matrices
t = Text.from_string('en', en); ds = DigitString("67-90-143")
an = Analysis(t, ds, Config('targets'), targets=TARGETS)
ref, _ = an.null('A', 10000, 5, 0); test, _ = an.null('A', 10000, 5, 1)
nt = NullTest(ref, test); obs, _ = an.observed()
nulltest = dict(ref=ref.tolist(), test=test.tolist(), obs=obs.tolist(), p=nt.p(obs),
                lr=nt.tail.log_rarity(obs[None, :])[0].tolist(), stat=nt.null_stat[:50].tolist())
json.dump(dict(texts=texts, cases=cases, nulltest=nulltest, wl=wl, targets=TARGETS + ['Or', 'Titre', 'Lanternes']),
          open(sys.argv[1] if len(sys.argv) > 1 else 'ref.json', 'w'))
print(len(cases), 'cases')
