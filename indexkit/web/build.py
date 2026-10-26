"""Build web/indexkit.html: one self-contained page (engine + data + UI).

    python3 web/build.py

The demo article, target list and word lists come from the Python package,
so both versions use exactly the same data.  The example result shown when
the page first opens is computed here with the browser engine (needs node).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from indexkit.demo import COINCIDENCE, PLANTED  # noqa: E402
from indexkit.demo_article import EN_PARAGRAPHS, FR_PARAGRAPHS, TARGETS, as_file_text  # noqa: E402
from indexkit.wordlists import ENGLISH, FRENCH  # noqa: E402

EXAMPLE_JS = r"""
const IK = require(process.argv[1]);
const D = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const ds = new IK.DigitString(D.demo.planted);
const cfg = new IK.Config({ mode: 'targets' });
const results = ['en', 'fr'].map(l => IK.analyse(IK.Text.fromString(l, D.demo[l], '(example ' + l + ' text)'), ds, cfg,
  10000, 1856, { targets: D.demo.targets }));
const info = { digits: ds.raw, shape: ds.shape(), n_digits: ds.nDigits, score: 'targets', targets: D.demo.targets,
  draws: 10000, seed: 1856, threshold: 0.01, prereg: null, restricted: null, markers: [] };
process.stdout.write(JSON.stringify({ info: info, results: results }));
"""


def main():
    data = {
        "demo": {"en": as_file_text(EN_PARAGRAPHS), "fr": as_file_text(FR_PARAGRAPHS), "targets": TARGETS,
                 "planted": PLANTED, "coincidence": COINCIDENCE},
        "wordlists": {"en": ENGLISH.split(), "fr": FRENCH.split()},
    }
    engine_path = os.path.join(HERE, "engine.js")
    out = subprocess.run(["node", "-e", EXAMPLE_JS, engine_path], input=json.dumps(data),
                         capture_output=True, text=True, check=True).stdout
    data["example"] = json.loads(out)
    with open(engine_path, encoding="utf-8") as fh:
        engine = fh.read()
    with open(os.path.join(HERE, "page.html"), encoding="utf-8") as fh:
        page = fh.read()
    blob = json.dumps(data, ensure_ascii=True).replace("</", "<\\/")
    page = page.replace("/*@ENGINE@*/", engine).replace("/*@DATA@*/", "window.IK_DATA = " + blob + ";")
    target = os.path.join(HERE, "indexkit.html")
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("wrote %s (%d KB)" % (target, len(page.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
