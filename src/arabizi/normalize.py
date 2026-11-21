"""Normalisation heuristique de l'arabizi vers une forme latine canonique.

Objectif : rapprocher les graphies d'une même forme pour améliorer la correspondance lexicale.
Ce n'est PAS une translittération fidèle vers l'arabe ; c'est une baseline volontairement simple.
"""

import re
import unicodedata

# Correspondances chiffre -> lettres usuelles en arabizi (variantes fréquentes au Maghreb).
DIGIT_MAP = {
    "2": "a",   # ء / أ
    "3": "a",   # ع
    "5": "kh",  # خ
    "6": "t",   # ط
    "7": "h",   # ح
    "8": "gh",  # غ
    "9": "s",   # ص / ق (usage variable)
}

_DIGIT_RE = re.compile("[" + "".join(DIGIT_MAP) + "]")


def strip_accents(text: str) -> str:
    """Supprime les accents (é -> e, ç -> c)."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def normalize_arabizi(text: str) -> str:
    """Retourne une forme latine canonique d'un texte en arabizi ou mixte.

    Étapes : minuscules, accents supprimés, chiffres remplacés par des lettres,
    lettres répétées réduites à une seule occurrence, espaces normalisés.
    """
    text = strip_accents(text.lower())
    text = _DIGIT_RE.sub(lambda m: DIGIT_MAP[m.group(0)], text)
    text = re.sub(r"(.)\1+", r"\1", text)  # "aa" -> "a", "ss" -> "s"
    text = re.sub(r"\s+", " ", text).strip()
    return text
