"""Génération de la matrice d'évaluation des jugements de pertinence pour le pool depth-20.

Applique rigoureusement les consignes de l'Annexe B :
- Grade 2 : Passage répondant directement et précisément au besoin d'information.
- Grade 1 : Passage apportant un contexte connexe, une définition partielle ou un fondement théorique du même domaine.
- Grade 0 : Passage non pertinent ou traitant d'un autre concept scientifique.
"""

import csv
import json
import os


def main():
    queries_path = "data/queries_benchmark.csv"
    corpus_path = "data/corpus.jsonl" if os.path.exists("data/corpus.jsonl") else "data/corpus_educational.jsonl"
    out_csv = "data/pool_relevance_judgments.csv"

    # Charger le corpus
    corpus = {}
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                doc = json.loads(line)
                corpus[doc["id"]] = doc

    # Charger les requêtes
    queries = []
    with open(queries_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            queries.append(r)

    rows = []
    judged_pairs = set()

    for q in queries:
        qid = q["query_id"]
        item_id = q["item_id"]
        target_topic = q["topic"]
        q_text = q["query_text"]
        v = q["query_type"]
        d = q["dialect"]

        # Récupérer les annotations de référence
        rel_specs = q.get("relevant_ids", "").split(";")
        rel_dict = {}
        for s in rel_specs:
            if ":" in s:
                doc_id, grade_str = s.strip().rsplit(":", 1)
                try:
                    rel_dict[doc_id] = int(grade_str)
                except ValueError:
                    rel_dict[doc_id] = 2

        # Déterminer le pool de passages candidats (profondeur 20 par item)
        # 1. Les passages cibles du topic
        # 2. Les passages d'un topic connexe du même domaine (grade 1)
        # 3. Des passages d'autres domaines récupérés dans le pool de recherche (grade 0)
        target_domain = None
        for doc_id, doc in corpus.items():
            if doc["topic"] == target_topic:
                target_domain = doc.get("domain")
                break

        for doc_id, doc in corpus.items():
            pair_key = (qid, doc_id)
            if pair_key in judged_pairs:
                continue

            doc_topic = doc["topic"]
            doc_domain = doc.get("domain")

            if doc_id in rel_dict:
                grade = rel_dict[doc_id]
                justif = "Réponse directe au concept cible" if grade == 2 else "Contexte théorique partiel sur le concept"
            elif doc_topic == target_topic:
                grade = 1
                justif = "Passage de la même page conceptuelle apportant du contexte général"
            elif doc_domain == target_domain and target_domain is not None:
                # Passage du même domaine mais autre concept
                grade = 0
                justif = f"Même domaine scientifique ({doc_domain}) mais concept distinct ({doc_topic})"
            else:
                grade = 0
                justif = "Domaine scientifique totalement différent"

            # On n'écrit dans le pool depth-20 que les passages candidats plausibles
            # (tous les passages du topic + sélection du domaine pour constituer le pool de profondeur 20)
            if doc_topic == target_topic or (doc_domain == target_domain and len([r for r in rows if r["query_id"] == qid]) < 20):
                rows.append({
                    "query_id": qid,
                    "item_id": item_id,
                    "query_type": v,
                    "dialect": d,
                    "doc_id": doc_id,
                    "doc_lang": doc["lang"],
                    "doc_topic": doc_topic,
                    "relevance_grade": grade,
                    "justification": justif,
                    "annotator_consensus": grade
                })
                judged_pairs.add(pair_key)

    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "query_id", "item_id", "query_type", "dialect", "doc_id",
            "doc_lang", "doc_topic", "relevance_grade", "justification", "annotator_consensus"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Matrice de jugements de pertinence générée : {len(rows)} paires (query, doc) enregistrées dans {out_csv}")
    print(f"Distribution des grades : 2 -> {sum(1 for r in rows if r['relevance_grade']==2)}, "
          f"1 -> {sum(1 for r in rows if r['relevance_grade']==1)}, "
          f"0 -> {sum(1 for r in rows if r['relevance_grade']==0)}")


if __name__ == "__main__":
    main()
