"""Collecte de paires d'articles Wikipédia FR-AR via les liens interlangues.

À lancer sur ta machine (accès à fr.wikipedia.org et ar.wikipedia.org requis).
Licence des textes : CC BY-SA 4.0 ; conserve l'attribution dans tes publications.

Usage :
    python src/collect_wiki_pairs.py --titles data/titles_fr.txt --out data/corpus.jsonl

Le fichier de titres contient un titre d'article français par ligne.
Sortie : un JSON par ligne, avec id, lang, title, text, source_url.
"""

import argparse
import json
import sys
import time

import requests

HEADERS = {"User-Agent": "arabizi-rag-research/0.1 (contact: to-fill@example.org)"}
API = "https://{lang}.wikipedia.org/w/api.php"


def _get(lang: str, params: dict) -> dict:
    params = {"format": "json", "formatversion": 2, **params}
    r = requests.get(API.format(lang=lang), params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def arabic_title(fr_title: str) -> str | None:
    data = _get("fr", {"action": "query", "titles": fr_title, "prop": "langlinks",
                       "lllang": "ar", "lllimit": 1})
    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return None
    links = pages[0].get("langlinks", [])
    return links[0]["title"] if links else None


def extract(lang: str, title: str) -> str:
    data = _get(lang, {"action": "query", "titles": title, "prop": "extracts",
                       "explaintext": 1, "exlimit": 1})
    pages = data.get("query", {}).get("pages", [])
    return pages[0].get("extract", "") if pages else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--titles", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--sleep", type=float, default=0.5, help="pause entre requêtes (s)")
    args = parser.parse_args()

    with open(args.titles, encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]

    written = 0
    with open(args.out, "w", encoding="utf-8") as out:
        for fr_title in titles:
            ar_title = arabic_title(fr_title)
            fr_text = extract("fr", fr_title)
            if fr_text:
                out.write(json.dumps({
                    "id": f"fr::{fr_title}", "lang": "fr", "title": fr_title,
                    "text": fr_text,
                    "source_url": f"https://fr.wikipedia.org/wiki/{fr_title.replace(' ', '_')}",
                }, ensure_ascii=False) + "\n")
                written += 1
            if ar_title:
                ar_text = extract("ar", ar_title)
                if ar_text:
                    out.write(json.dumps({
                        "id": f"ar::{ar_title}", "lang": "ar", "title": ar_title,
                        "text": ar_text,
                        "source_url": f"https://ar.wikipedia.org/wiki/{ar_title.replace(' ', '_')}",
                    }, ensure_ascii=False) + "\n")
                    written += 1
            else:
                print(f"[info] pas de lien AR pour : {fr_title}", file=sys.stderr)
            time.sleep(args.sleep)

    print(f"{written} documents écrits dans {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
