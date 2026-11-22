"""Calcul du recouvrement lexical entre les requêtes et les passages pertinents.

Ce script mesure de manière quantitative :
1. Le taux de recouvrement des termes de la requête dans le passage pertinent (|Q ∩ D| / |Q|).
2. L'indice de similarité de Jaccard (|Q ∩ D| / |Q ∪ D|).
3. La ventilation par version (Arabizi, Mixte/Code-switching, Français) et par dialecte (Maroc, Algérie, Tunisie).
"""

import csv
import json
import os
import re
import unicodedata


def tokenize(text: str) -> set[str]:
    """Tokenisation et normalisation basique pour calcul de recouvrement lexical."""
    text = unicodedata.normalize('NFKD', text)
    # Remplacer la ponctuation par des espaces
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    tokens = set(t for t in text.split() if len(t) > 1)
    return tokens


def main():
    queries_path = "data/queries_benchmark.csv"
    corpus_path = "data/corpus.jsonl" if os.path.exists("data/corpus.jsonl") else "data/corpus_educational.jsonl"

    print(f"Chargement du corpus depuis {corpus_path}...")
    corpus = {}
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                doc = json.loads(line)
                corpus[doc["id"]] = doc

    print(f"Chargement des requêtes depuis {queries_path}...")
    records = []
    with open(queries_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)

    # Stockage des métriques
    by_version = {"arabizi": [], "mixed": [], "fr": []}
    by_dialect = {"darija_maroc": [], "darija_algerie": [], "darija_tunisie": []}
    by_version_dialect = {}

    for r in records:
        q_text = r.get("query_text") or r.get("query", "")
        q_tokens = tokenize(q_text)
        v = r.get("query_type") or r.get("version", "arabizi")
        d = r.get("dialect", "general")
        vd_key = f"{d}::{v}"

        if v not in by_version:
            by_version[v] = []
        if vd_key not in by_version_dialect:
            by_version_dialect[vd_key] = []

        # Identifier les passages pertinents
        rel_specs = (r.get("relevant_ids") or r.get("relevant_passages", "")).split(";")
        rel_ids = [s.strip().rsplit(":", 1)[0] for s in rel_specs if s.strip()]

        # Calculer le recouvrement moyen avec les passages pertinents cibles (en français)
        containments = []
        jaccards = []
        for doc_id in rel_ids:
            if doc_id in corpus:
                d_tokens = tokenize(corpus[doc_id]["text"])
                if not q_tokens:
                    continue
                intersection = q_tokens & d_tokens
                union = q_tokens | d_tokens
                containment = len(intersection) / len(q_tokens) if q_tokens else 0.0
                jaccard = len(intersection) / len(union) if union else 0.0
                containments.append(containment)
                jaccards.append(jaccard)

        mean_cont = sum(containments) / max(len(containments), 1) if containments else 0.0
        mean_jacc = sum(jaccards) / max(len(jaccards), 1) if jaccards else 0.0

        item_res = {
            "query_id": r["query_id"],
            "version": v,
            "dialect": d,
            "containment": mean_cont,
            "jaccard": mean_jacc
        }

        by_version[v].append(item_res)
        by_dialect.setdefault(d, []).append(item_res)
        by_version_dialect[vd_key].append(item_res)

    # Agrégations
    summary = {
        "overall_by_version": {},
        "by_dialect": {},
        "by_dialect_and_version": {}
    }

    for v, items in by_version.items():
        if items:
            avg_cont = sum(x["containment"] for x in items) / len(items)
            avg_jacc = sum(x["jaccard"] for x in items) / len(items)
            summary["overall_by_version"][v] = {
                "count": len(items),
                "mean_containment": round(avg_cont, 4),
                "mean_containment_pct": f"{avg_cont * 100:.1f}%",
                "mean_jaccard": round(avg_jacc, 4)
            }

    for d, items in by_dialect.items():
        if items:
            avg_cont = sum(x["containment"] for x in items) / len(items)
            summary["by_dialect"][d] = {
                "count": len(items),
                "mean_containment": round(avg_cont, 4),
                "mean_containment_pct": f"{avg_cont * 100:.1f}%"
            }

    for vd, items in by_version_dialect.items():
        if items:
            avg_cont = sum(x["containment"] for x in items) / len(items)
            avg_jacc = sum(x["jaccard"] for x in items) / len(items)
            summary["by_dialect_and_version"][vd] = {
                "count": len(items),
                "mean_containment": round(avg_cont, 4),
                "mean_containment_pct": f"{avg_cont * 100:.1f}%",
                "mean_jaccard": round(avg_jacc, 4)
            }

    out_json = "paper/lexical_overlap_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n=== RÉSULTATS DU RECOUVREMENT LEXICAL (Requête vs Passages pertinents) ===")
    for v, stats in summary["overall_by_version"].items():
        print(f"Version: {v:<15} | Containment: {stats['mean_containment_pct']} | Jaccard: {stats['mean_jaccard']:.4f}")

    print("\n=== DÉTAIL PAR DIALECTE ET VERSION ===")
    for vd, stats in sorted(summary["by_dialect_and_version"].items()):
        print(f"{vd:<28} | Containment: {stats['mean_containment_pct']}")

    print(f"\nRésultats sauvegardés dans {out_json}")


if __name__ == "__main__":
    main()
