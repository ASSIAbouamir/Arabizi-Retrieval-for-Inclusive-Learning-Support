"""Test de récupération lexicale sur le NArabizi Treebank (split test).

Tâche : pour chaque phrase arabizi du split test, retrouver sa traduction française
parmi les traductions françaises du même split (146 documents).
Ce n'est PAS une tâche éducative : c'est un test du pont lexical arabizi -> français.

Usage : python3 -I run_treebank_retrieval.py <chemin_test.conllu> <chemin_src_projet>
"""

import json
import os
import sys
from statistics import mean

sys.path.insert(0, sys.argv[2])
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arabizi.bm25 import BM25  # noqa: E402
from arabizi.metrics import ndcg_at_k, recall_at_k, reciprocal_rank  # noqa: E402
from arabizi.normalize import normalize_arabizi  # noqa: E402
from stats_narabizi import parse  # noqa: E402


def main():
    sents = parse(sys.argv[1])
    docs = {}
    queries = []
    for i, s in enumerate(sents):
        if not s["trad"]:
            continue
        doc_id = f"s{i}"
        docs[doc_id] = s["trad"]
        queries.append((s["text"], doc_id))

    # Seuls les textes arabizi non vides sont évalués
    queries = [(q, d) for q, d in queries if q.strip()]

    variants = {
        "brut": (lambda t: t, lambda t: t),
        "normalise": (normalize_arabizi, normalize_arabizi),
    }
    results = {}
    for name, (f_doc, f_q) in variants.items():
        index = BM25({d: f_doc(t) for d, t in docs.items()})
        rec, mrr, ndcg = [], [], []
        for text, gold in queries:
            ranked = index.rank(f_q(text), k=10)
            rec.append(recall_at_k(ranked, {gold}, 5))
            mrr.append(reciprocal_rank(ranked, {gold}))
            ndcg.append(ndcg_at_k(ranked, {gold}, 10))
        results[name] = {
            "recall@5": round(mean(rec), 4),
            "mrr": round(mean(mrr), 4),
            "ndcg@10": round(mean(ndcg), 4),
            "n_queries": len(queries),
            "n_docs": len(docs),
        }
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
