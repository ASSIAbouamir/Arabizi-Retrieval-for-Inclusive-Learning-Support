import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from arabizi.normalize import normalize_arabizi, strip_accents  # noqa: E402


def test_digits_become_letters():
    assert normalize_arabizi("3lach") == "alach"
    assert normalize_arabizi("7ob") == "hob"
    assert normalize_arabizi("5ir") == "khir"


def test_accents_removed():
    assert strip_accents("Photosynthèse") == "Photosynthese"


def test_repeated_letters_collapsed():
    assert normalize_arabizi("saaaalam") == "salam"


def test_whitespace_collapsed_and_lowercased():
    assert normalize_arabizi("  Qu'est-ce   QUE  ") == "qu'est-ce que"
