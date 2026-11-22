"""Collecte et segmentation de paires d'articles Wikipédia FR-AR via les liens interlangues.

À lancer sur votre machine (accès à fr.wikipedia.org et ar.wikipedia.org requis).
Licence des textes : Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
Attribution : Wikipedia contributors.

Usage :
    python src/collect_wiki_pairs.py --titles data/titles_fr.txt --out data/corpus.jsonl --raw-out data/wiki_raw_articles.jsonl
"""

import argparse
import datetime
import json
import re
import sys
import time

import requests

HEADERS = {"User-Agent": "arabizi-rag-research/0.2 (academic research on Arabizi retrieval; contact: assialsm0@gmail.com)"}
API = "https://{lang}.wikipedia.org/w/api.php"

TOPIC_MAP = {
    'Pression atmosphérique': ('pression_atm', 'physique'),
    'Courant électrique': ('electricite_courant', 'physique'),
    'Loi universelle de la gravitation': ('gravite_universelle', 'physique'),
    'Vitesse de la lumière': ('vitesse_lumiere', 'physique'),
    'Énergie cinétique': ('energie_cinetique', 'physique'),
    'Onde sonore': ('ondes_sonores', 'physique'),
    'Photosynthèse': ('photosynthese', 'biologie'),
    'Cellule (biologie)': ('cellule_biologie', 'biologie'),
    'Acide désoxyribonucléique': ('adn_genetique', 'biologie'),
    'Respiration cellulaire': ('respiration_cellulaire', 'biologie'),
    'Système circulatoire': ('systeme_circulatoire', 'biologie'),
    'Système immunitaire': ('systeme_immunitaire', 'biologie'),
    'Tableau périodique des éléments': ('tableau_periodique', 'chimie'),
    'Potentiel hydrogène': ('acides_bases_ph', 'chimie'),
    'Liaison covalente': ('liaison_covalente', 'chimie'),
    'État de la matière': ('etats_matiere', 'chimie'),
    "Réaction d'oxydoréduction": ('oxydoreduction', 'chimie'),
    'Théorème de Pythagore': ('pythagore', 'mathematiques'),
    'Théorème de Thalès': ('thales', 'mathematiques'),
    'Équation du second degré': ('equations_second_degre', 'mathematiques'),
    'Probabilité': ('probabilites', 'mathematiques'),
    'Dérivée': ('derivee_fonctions', 'mathematiques'),
    'Algorithme': ('algorithme_complexite', 'informatique'),
    'Microprocesseur': ('processeur_memoire', 'informatique'),
    'Internet Protocol': ('reseau_ip', 'informatique'),
    'Base de données relationnelle': ('base_de_donnees', 'informatique'),
    'Héliocentrisme': ('revolution_copernic', 'histoire_sciences'),
    'Révolution industrielle': ('revolution_industrielle', 'histoire_sciences'),
    'Pénicilline': ('penicilline_fleming', 'histoire_sciences'),
    'Système métrique': ('revolution_francaise_sciences', 'histoire_sciences'),
}


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


def segment_passages(text: str, max_tokens: int = 180, overlap: int = 25, target_passages: int = 2) -> list[str]:
    """Segmente un texte en target_passages d'environ max_tokens avec overlap."""
    clean_text = re.sub(r'={2,}[^=]+={2,}', '', text)  # Retire les titres de section
    clean_text = re.sub(r'\n+', '\n', clean_text).strip()
    paragraphs = [p.strip() for p in clean_text.split('\n') if len(p.strip()) > 40]
    
    if not paragraphs:
        words = clean_text.split()
        if len(words) <= max_tokens:
            return [clean_text] if clean_text else []
        step = max_tokens - overlap
        return [" ".join(words[i:i + max_tokens]) for i in range(0, min(len(words), target_passages * step), step)][:target_passages]

    # Regrouper les paragraphes en passages cibles
    passages = []
    current_words = []
    for p in paragraphs:
        p_words = p.split()
        if len(current_words) + len(p_words) <= max_tokens:
            current_words.extend(p_words)
        else:
            if current_words:
                passages.append(" ".join(current_words))
            current_words = p_words
        if len(passages) >= target_passages:
            break

    if current_words and len(passages) < target_passages:
        passages.append(" ".join(current_words))

    # Si on a moins que target_passages, scinder par découpage de mots
    if len(passages) < target_passages:
        all_words = clean_text.split()
        passages = []
        step = max(50, (len(all_words) // target_passages))
        for i in range(target_passages):
            start = i * step
            end = start + min(max_tokens, len(all_words) - start)
            if start < len(all_words):
                passages.append(" ".join(all_words[start:end]))

    return passages[:target_passages]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--titles", required=True, help="Chemin vers le fichier data/titles_fr.txt")
    parser.add_argument("--out", required=True, help="Sortie corpus.jsonl segmenté")
    parser.add_argument("--raw-out", default="data/wiki_raw_articles.jsonl", help="Sortie articles bruts")
    parser.add_argument("--sleep", type=float, default=0.3, help="Pause entre requêtes (s)")
    args = parser.parse_args()

    collection_date = datetime.date.today().isoformat()

    with open(args.titles, encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]

    raw_articles = []
    passages_corpus = []

    print(f"Lancement de la collecte de {len(titles)} articles bilingues...")

    for i, fr_title in enumerate(titles, 1):
        topic_info = TOPIC_MAP.get(fr_title, (fr_title.lower().replace(" ", "_"), "general"))
        topic_id, domain = topic_info
        
        ar_title = arabic_title(fr_title)
        fr_text = extract("fr", fr_title)
        time.sleep(args.sleep)
        
        ar_text = extract("ar", ar_title) if ar_title else ""
        time.sleep(args.sleep)

        # Enregistrement brut
        fr_url = f"https://fr.wikipedia.org/wiki/{fr_title.replace(' ', '_')}"
        ar_url = f"https://ar.wikipedia.org/wiki/{ar_title.replace(' ', '_')}" if ar_title else ""
        
        raw_articles.append({
            "topic": topic_id, "domain": domain, "lang": "fr", "title": fr_title,
            "text": fr_text, "source_url": fr_url, "license": "CC BY-SA 4.0",
            "collection_date": collection_date
        })
        if ar_title:
            raw_articles.append({
                "topic": topic_id, "domain": domain, "lang": "ar", "title": ar_title,
                "text": ar_text, "source_url": ar_url, "license": "CC BY-SA 4.0",
                "collection_date": collection_date
            })

        # Segmentation en 2 passages par langue (4 passages par topic)
        fr_chunks = segment_passages(fr_text, max_tokens=180, overlap=25, target_passages=2)
        for idx, chunk in enumerate(fr_chunks, 1):
            passages_corpus.append({
                "id": f"fr::{topic_id}::p{idx}",
                "lang": "fr",
                "domain": domain,
                "topic": topic_id,
                "title": fr_title,
                "text": chunk,
                "source": "wikipedia",
                "source_url": fr_url,
                "license": "CC BY-SA 4.0",
                "collection_date": collection_date
            })

        if ar_text:
            ar_chunks = segment_passages(ar_text, max_tokens=180, overlap=25, target_passages=2)
            for idx, chunk in enumerate(ar_chunks, 1):
                passages_corpus.append({
                    "id": f"ar::{topic_id}::p{idx}",
                    "lang": "ar",
                    "domain": domain,
                    "topic": topic_id,
                    "title": ar_title,
                    "text": chunk,
                    "source": "wikipedia",
                    "source_url": ar_url,
                    "license": "CC BY-SA 4.0",
                    "collection_date": collection_date
                })

        print(f"[{i}/{len(titles)}] {fr_title} -> {ar_title or 'PAS DE LIEN'} ({len(fr_chunks)} FR p., {len(ar_chunks) if ar_text else 0} AR p.)")

    # Écriture du fichier brut
    if args.raw_out:
        with open(args.raw_out, "w", encoding="utf-8") as f_raw:
            for item in raw_articles:
                f_raw.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"Articles bruts écrits dans {args.raw_out} ({len(raw_articles)} articles)")

    # Écriture du corpus segmenté
    with open(args.out, "w", encoding="utf-8") as f_out:
        for p in passages_corpus:
            f_out.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"Corpus segmenté écrit dans {args.out} ({len(passages_corpus)} passages)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
