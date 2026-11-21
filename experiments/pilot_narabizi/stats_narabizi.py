"""Statistiques descriptives du NArabizi Treebank (format CoNLL-U).

Usage : python3 -I stats_narabizi.py <dossier_gold_annotation>
"""

import collections
import glob
import os
import re
import sys

DIGITS = set("23567 89".replace(" ", ""))  # chiffres utilisés en arabizi


def parse(path):
    sents = []
    cur = {"text": None, "trad": None, "tokens": []}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("# text ="):
                cur["text"] = line.split("=", 1)[1].strip()
            elif line.startswith("# trad_fr ="):
                cur["trad"] = line.split("=", 1)[1].strip()
            elif line == "":
                if cur["text"] is not None:
                    sents.append(cur)
                cur = {"text": None, "trad": None, "tokens": []}
            elif not line.startswith("#"):
                cols = line.split("\t")
                if len(cols) == 10 and "-" not in cols[0] and "." not in cols[0]:
                    cur["tokens"].append(cols)
    if cur["text"] is not None:
        sents.append(cur)
    return sents


def lang_of(misc):
    m = re.search(r"lang=([^|]+)", misc)
    return m.group(1) if m else "NA"


def main(folder):
    files = sorted(glob.glob(os.path.join(folder, "*.conllu")))
    all_texts = {}
    for path in files:
        name = os.path.basename(path).split(".")[0]
        sents = parse(path)
        n_tok = sum(len(s["tokens"]) for s in sents)
        lens = [len(s["tokens"]) for s in sents]
        with_trad = sum(1 for s in sents if s["trad"])
        with_digits = sum(1 for s in sents if any(c in DIGITS for c in s["text"]))
        langs = collections.Counter(lang_of(t[9]) for s in sents for t in s["tokens"])
        print(f"== {name} ==")
        print(f"phrases: {len(sents)}  tokens: {n_tok}  "
              f"longueur moyenne: {sum(lens)/max(len(lens),1):.1f}")
        print(f"avec traduction FR: {with_trad} ({100*with_trad/max(len(sents),1):.1f}%)")
        print(f"avec chiffres (arabizi): {with_digits} ({100*with_digits/max(len(sents),1):.1f}%)")
        total = sum(langs.values())
        print("langues (tokens): " + ", ".join(
            f"{k} {100*v/total:.1f}%" for k, v in langs.most_common(6)))
        for s in sents:
            all_texts.setdefault(s["text"], set()).add(name)
        print()

    dup = [t for t, splits in all_texts.items() if len(splits) > 1]
    print(f"Phrases identiques présentes dans plusieurs splits : {len(dup)}")


if __name__ == "__main__":
    main(sys.argv[1])
