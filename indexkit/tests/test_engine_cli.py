import json

import numpy as np
import pytest

from indexkit import cli, gate
from indexkit.conventions import Config
from indexkit.demo_article import EN_PARAGRAPHS, FR_PARAGRAPHS, TARGETS, as_file_text
from indexkit.digits import DigitString
from indexkit.engine import Analysis, NullTest, analyse, gather, random_orders
from indexkit.text import Text


@pytest.fixture
def fr():
    return Text.from_string("fr", as_file_text(FR_PARAGRAPHS))


def test_shuffled_extraction_matches_rebuilt_text(fr):
    """The fast paragraph-shuffle path must equal literally rebuilding the
    text in the shuffled order (including a marker start)."""
    ds = DigitString("7 45 3 120")
    cfg = Config("targets", markers=["Son magasin"])
    an = Analysis(fr, ds, cfg, targets=TARGETS)
    orders = random_orders(np.random.default_rng(5), 3, an.n_paragraphs)
    for order in orders:
        t2 = Text("fr", [fr.paragraphs[i] for i in order])
        an2 = Analysis(t2, ds, cfg, targets=TARGETS)
        s1, _ = an.evaluate(ds.matrix(), order[None, :])
        s2, _ = an2.evaluate(ds.matrix())
        m1 = dict(zip([c.name for c in an.convs], s1[0]))
        m2 = dict(zip([c.name for c in an2.convs], s2[0]))
        common = set(m1) & set(m2)
        assert len(common) > 100
        assert all(m1[k] == m2[k] for k in common)


def test_identity_order_equals_plain(fr):
    ds = DigitString("12 345 6")
    an = Analysis(fr, ds, Config("letters"), wordlist=["or", "a"])
    ident = np.tile(np.arange(an.n_paragraphs), (4, 1))
    d = ds.random_matrix(np.random.default_rng(0), 4)
    for v in an.tv.views:
        for g in range(len(an.groups)):
            pos = an.positions(d, g, 1)
            assert np.array_equal(gather(v, pos), gather(v, pos, ident))


def test_nulltest_p_is_exact_and_bounded():
    rng = np.random.default_rng(0)
    ref = rng.poisson(0.3, size=(2000, 20)).astype(np.int32)
    test = rng.poisson(0.3, size=(2000, 20)).astype(np.int32)
    nt = NullTest(ref, test)
    zero = np.zeros(20, dtype=np.int32)
    assert nt.p(zero) == 1.0
    huge = zero.copy()
    huge[3] = 50
    assert nt.p(huge) == pytest.approx(1 / 2001)
    # fresh null rows give roughly uniform p-values
    ps = [nt.p(row, u) for row, u in zip(rng.poisson(0.3, size=(500, 20)).astype(np.int32), rng.random(500))]
    assert np.mean(np.array(ps) <= 0.05) <= 0.08


def test_minimum_draws_enforced(fr):
    with pytest.raises(ValueError):
        analyse(fr, DigitString("12"), Config("targets"), 500, 1, targets=TARGETS)


def test_planted_signal_found_and_random_not():
    en = Text.from_string("en", as_file_text(EN_PARAGRAPHS))
    r = analyse(en, DigitString("67-90-143"), Config("targets"), 10000, 1856, targets=TARGETS)
    assert r["p"] <= 0.005
    assert any("word | strip | item | from=title | 1-based | digits=given" in a for a in r["winners"])
    r = analyse(en, DigitString("130-315-814"), Config("targets"), 10000, 1856, targets=TARGETS)
    assert r["p"] > 0.1


# --- command line -----------------------------------------------------------

def test_commands_locked_without_selftest(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(gate, "STAMP", str(tmp_path / "missing.json"))
    assert cli.main(["conventions", "--digits", "12", "--text", "x.txt"]) == 2
    assert "locked" in capsys.readouterr().out


def test_stamp_for_other_code_is_rejected(tmp_path, monkeypatch):
    stamp = tmp_path / "stamp.json"
    monkeypatch.setattr(gate, "STAMP", str(stamp))
    stamp.write_text(json.dumps(dict(gate.environment(), passed=True, code_hash="0" * 64)))
    assert gate.check()[0] is False
    stamp.write_text(json.dumps(dict(gate.environment(), passed=True)))
    assert gate.check()[0] is True


@pytest.fixture
def unlocked(monkeypatch):
    monkeypatch.setattr(gate, "check", lambda: (True, "ok"))


@pytest.fixture
def files(tmp_path):
    en = tmp_path / "en.txt"
    en.write_text(as_file_text(EN_PARAGRAPHS), encoding="utf-8")
    places = tmp_path / "places.txt"
    places.write_text("\n".join(TARGETS), encoding="utf-8")
    return en, places


def test_prereg_roundtrip_and_refusals(tmp_path, unlocked, files, capsys):
    en, places = files
    pr = str(tmp_path / "t.prereg.json")
    args = ["--digits", "67-90-143", "--text", "en=%s" % en, "--targets", str(places)]
    assert cli.main(["prereg", "--out", pr] + args) == 0
    # re-running the same command is safe
    assert cli.main(["prereg", "--out", pr] + args) == 0
    assert "nothing changed" in capsys.readouterr().out
    # a different prereg under the same name is refused
    with pytest.raises(SystemExit) as e:
        cli.main(["prereg", "--out", pr, "--digits", "1-2-3", "--text", "en=%s" % en, "--targets", str(places)])
    assert "REFUSED" in str(e.value)
    # overriding a registered option is refused
    with pytest.raises(SystemExit) as e:
        cli.main(["run", "--prereg", pr, "--digits", "1-2-3"])
    assert "REFUSED" in str(e.value)
    # the registered run works
    out = str(tmp_path / "r.md")
    assert cli.main(["run", "--prereg", pr, "--out", out]) == 0
    report = open(out, encoding="utf-8").read()
    assert "SIGNAL ONLY: this says nothing about what it means." in report
    assert report.index("Null hypothesis") < report.index("## Result")
    # editing the text afterwards is refused
    en.write_text(as_file_text(EN_PARAGRAPHS) + "extra\n", encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        cli.main(["run", "--prereg", pr, "--out", out])
    assert "changed" in str(e.value)


def test_edited_prereg_is_refused(tmp_path, unlocked, files):
    en, places = files
    pr = tmp_path / "t.prereg.json"
    cli.main(["prereg", "--out", str(pr), "--digits", "67-90-143", "--text", "en=%s" % en,
              "--targets", str(places)])
    pr.write_text(pr.read_text(encoding="utf-8").replace('"threshold": 0.01', '"threshold": 0.5'),
                  encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        cli.main(["run", "--prereg", str(pr)])
    assert "edited" in str(e.value)
