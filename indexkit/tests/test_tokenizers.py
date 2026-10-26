"""Every tokenizer on tricky French and English text."""
import unicodedata

import pytest

from indexkit.text import TOKENIZERS, fold, normalize, tokenize, tokens

FR = "« Bonjour », dit-il : l’Or de Val-d'Or – c’est tout."
EN = "“We don’t,” she said – it’s Val-d'Or: 1887 (not 1950)!"


# --- French -----------------------------------------------------------------

def test_ws_french_keeps_standalone_punctuation():
    assert tokens(FR, "ws") == ["«", "Bonjour", "»,", "dit-il", ":", "l’Or", "de", "Val-d'Or", "–",
                                "c’est", "tout."]


def test_ws_drop_french():
    assert tokens(FR, "ws-drop") == ["Bonjour", "dit-il", "l’Or", "de", "Val-d'Or", "c’est", "tout."]


def test_strip_french():
    assert tokens(FR, "strip") == ["Bonjour", "dit-il", "l’Or", "de", "Val-d'Or", "c’est", "tout"]


def test_split_french():
    assert tokens(FR, "split") == ["Bonjour", "dit", "il", "l", "Or", "de", "Val", "d", "Or", "c", "est", "tout"]


def test_both_apostrophes_behave_the_same():
    for name in TOKENIZERS:
        assert [fold(t) for t in tokens("l'Or Val-d'Or", name)] == \
               [fold(t) for t in tokens("l’Or Val-d’Or", name)]


def test_non_breaking_spaces_are_spaces():
    # French typography: narrow no-break space before ; and no-break space inside « »
    s = "« Bonjour » ; oui !"
    assert tokens(s, "ws") == ["«", "Bonjour", "»", ";", "oui", "!"]
    assert tokens(s, "ws-drop") == ["Bonjour", "oui"]
    assert tokens(s, "strip") == ["Bonjour", "oui"]
    assert tokens(s, "split") == ["Bonjour", "oui"]


def test_colon_and_dash_are_standalone_tokens_only_in_ws():
    s = "Il dit : non – jamais"
    assert tokens(s, "ws") == ["Il", "dit", ":", "non", "–", "jamais"]
    for name in ("ws-drop", "strip", "split"):
        assert tokens(s, name) == ["Il", "dit", "non", "jamais"]


def test_nfc_composed_and_decomposed_are_equal():
    composed = "Hérons à l’église"
    decomposed = unicodedata.normalize("NFD", composed)
    assert decomposed != composed
    for name in TOKENIZERS:
        assert tokens(decomposed, name) == tokens(composed, name)
    assert tokens(decomposed, "split")[0] == "Hérons"  # one token, not split at the accent


def test_ligatures_and_accents_fold():
    assert fold("Cœur") == "coeur"
    assert fold("Œuvre") == "oeuvre"
    assert fold("Pointe-aux-Hérons") == "pointeauxherons"
    assert fold("VAL-D’OR") == fold("Val-d'Or") == "valdor"
    assert fold("l’Or") == "lor"
    assert fold("1887") == ""


# --- English ----------------------------------------------------------------

def test_ws_english():
    assert tokens(EN, "ws") == ["“We", "don’t,”", "she", "said", "–", "it’s",
                                "Val-d'Or:", "1887", "(not", "1950)!"]


def test_ws_drop_english():
    assert tokens(EN, "ws-drop") == ["“We", "don’t,”", "she", "said", "it’s",
                                     "Val-d'Or:", "1887", "(not", "1950)!"]


def test_strip_english():
    assert tokens(EN, "strip") == ["We", "don’t", "she", "said", "it’s", "Val-d'Or", "1887", "not", "1950"]


def test_split_english():
    assert tokens(EN, "split") == ["We", "don", "t", "she", "said", "it", "s", "Val", "d", "Or", "1887", "not", "1950"]


def test_spans_point_at_the_token():
    s = normalize(FR)
    for name in TOKENIZERS:
        for tok, a, b in tokenize(s, name):
            assert s[a:b] == tok


def test_unknown_tokenizer():
    with pytest.raises(ValueError):
        tokens("x", "nope")
