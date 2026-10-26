import numpy as np
import pytest

from indexkit.conventions import Config, TextViews, build_conventions
from indexkit.digits import DigitString, distinct_groupings, numbers
from indexkit.scoring import LetterScorer, TargetScorer
from indexkit.text import Text, line_spans, sentence_spans


# --- text structure -------------------------------------------------------

def test_paragraphs_title_and_blank_lines():
    t = Text.from_string("x", "\n\n  My Title  \nfirst line\nsecond line\n\n\n\nnext para\n")
    assert t.paragraphs == ["My Title", "first line\nsecond line", "next para"]


def test_crlf_and_bom():
    t = Text.from_string("x", "﻿Title\r\n\r\nBody one.\r\n")
    assert t.paragraphs == ["Title", "Body one."]


def test_lines():
    assert [s for s, _, _ in line_spans("a b\n  c  \n\nd")] == ["a b", "c", "d"]


def test_sentences_french_quotes():
    p = "Il dit : « Bonjour. » Puis il part ! Fin… Vraiment ?"
    assert [s for s, _, _ in sentence_spans(p)] == ["Il dit : « Bonjour. »", "Puis il part !", "Fin…", "Vraiment ?"]


def test_sentences_english_quotes():
    p = "“We do it.” She left. Done"
    assert [s for s, _, _ in sentence_spans(p)] == ["“We do it.”", "She left.", "Done"]


def test_marker_alternatives_and_case():
    t = Text.from_string("fr", "Titre\n\nUn.\n\nCHAPITRE 2 ici\nsuite")
    assert t.find_marker("Chapter 2|chapitre 2")[:2] == (2, 0)
    assert t.find_marker("absent") is None


# --- digits ---------------------------------------------------------------

def test_digit_parsing_and_shape():
    ds = DigitString("810-419-227")
    assert ds.lengths == [3, 3, 3] and ds.shape() == "3-3-3"
    assert ds.format_row(ds.matrix()[0]) == "810-419-227"
    ds = DigitString("6 2 76 37 3 25 69 4 20")
    assert ds.lengths == [1, 1, 2, 2, 1, 2, 2, 1, 2]


def test_groupings():
    ds = DigitString("810-419-227")
    d = ds.matrix()
    assert numbers("given", d, ds.lengths).tolist() == [[810, 419, 227]]
    assert numbers("single", d, ds.lengths).tolist() == [[8, 1, 0, 4, 1, 9, 2, 2, 7]]
    assert numbers("pairs", d, ds.lengths).tolist() == [[81, 4, 19, 22, 7]]
    assert numbers("cumulative", d, ds.lengths).tolist() == [[810, 1229, 1456]]
    assert numbers("reversed", d, ds.lengths).tolist() == [[722, 914, 18]]


def test_identical_groupings_are_merged_by_shape():
    groups = distinct_groupings(DigitString("2638"), ["given", "single", "pairs", "cumulative", "reversed"])
    assert ["given", "cumulative"] in groups          # one number: steps == the number
    groups = distinct_groupings(DigitString("6 2 7"), ["given", "single", "pairs", "cumulative", "reversed"])
    assert ["given", "single"] in groups


def test_bad_digits():
    with pytest.raises(ValueError):
        DigitString("no digits")


# --- scoring --------------------------------------------------------------

def test_letter_score_counts_short_words():
    sc = LetterScorer(["a", "is", "or", "gold"])
    codes = np.array([[ord(c) - 97 for c in "isaor"]])
    score, cov = sc.best(codes)
    assert cov[0] == 5 and score[0] == 4 + 1 + 4      # is + a + or


def test_letter_score_prefers_long_words_and_respects_gaps():
    sc = LetterScorer(["go", "old", "gold"])
    codes = np.array([[6, 14, 11, 3], [6, 14, -1, 3]])  # GOLD, GO.D
    score, cov = sc.best(codes)
    assert score.tolist() == [16, 4]
    assert cov.tolist() == [4, 2]


def test_target_score_counts_distinct_targets_and_multiword():
    vocab = ["", "val", "d", "or", "lac", "valdor"]
    sc = TargetScorer(["Val-d'Or", "Lac"], vocab)
    codes = np.array([[1, 2, 3, 4],      # Val d Or Lac  -> both targets
                      [5, 5, 5, -1],     # valdor x3     -> one distinct target
                      [1, 2, -1, 3]])    # gap breaks Val d . Or
    s, h = sc.score("item", codes)
    assert s.tolist() == [2, 1, 0]
    assert h.tolist() == [True, True, False]


def test_target_score_on_letters():
    sc = TargetScorer(["or"], [""])
    codes = np.array([[14, 17, 0], [17, 14, 0], [14, -1, 17]])
    s, _ = sc.score("letter", codes)
    assert s.tolist() == [1, 0, 0]


# --- conventions ----------------------------------------------------------

def test_search_space_is_counted_and_duplicates_merged():
    t = Text.from_string("en", "Title\n\nOne two three.\n\nFour five six.")
    ds = DigitString("12-34")
    tv = TextViews(t, Config("targets"))
    convs, groups = build_conventions(tv, ds, Config("targets"))
    # no hard line breaks: 'line' == 'paragraph' -> merged
    assert tv.n_merged > 0
    assert len(convs) == len(tv.views) * len(groups) * 2
    assert len({c.name for c in convs}) == len(convs)


def test_letters_mode_skips_whole_word_reads():
    t = Text.from_string("en", "Title\n\nOne two three.")
    tv = TextViews(t, Config("letters"))
    assert all(v.kind == "letter" for v in tv.views)
