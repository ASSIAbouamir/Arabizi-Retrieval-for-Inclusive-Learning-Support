"""Baseline : BM25 sur requêtes brutes contre requêtes normalisées, par type de requête.

Format attendu du corpus (JSONL) : {"id", "lang", "text", ...}
Format attendu des requêtes (CSV) : query_id, query_type, query_text, relevant_ids
    - query_type : arabizi, fr ou mixed
    - relevant_ids : identifiants séparés par ';'

Usage :
    python experiments/run_baseline.py --corpus data/corpus.jsonl --queries data/queries.csv --k 5
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from statistics import mean

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from arabizi.bm25 import BM25  # noqa: E402
from arabizi.metrics import ndcg_at_k, recall_at_k, reciprocal_rank  # noqa: E402
from arabizi.normalize import normalize_arabizi  # noqa: E402


def load_corpus(path: str) -> dict[str, str]:
    docs = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            docs[row["id"]] = row["text"]
    return docs


def load_queries(path: str) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if not r["query_id"].startswith("EXEMPLE")]
    for r in rows:
        relevant = set()
        for x in r["relevant_ids"].split(";"):
            x = x.strip()
            if not x:
                continue
            if ":" in x and x.rsplit(":", 1)[1].isdigit():
                relevant.add(x.rsplit(":", 1)[0])
            else:
                relevant.add(x)
        r["relevant"] = relevant
    return rows


def evaluate(index: BM25, queries: list[dict], k: int, normalize: bool) -> dict:
    """Évalue un index déjà construit. Si normalize=True, l'index doit avoir été
    construit sur le corpus normalisé (même transformation que les requêtes)."""
    per_type = defaultdict(lambda: {"recall": [], "mrr": [], "ndcg": []})
    for q in queries:
        text = normalize_arabizi(q["query_text"]) if normalize else q["query_text"]
        ranked = index.rank(text, k=max(k, 10))
        bucket = per_type[q["query_type"]]
        bucket["recall"].append(recall_at_k(ranked, q["relevant"], k))
        bucket["mrr"].append(reciprocal_rank(ranked, q["relevant"]))
        bucket["ndcg"].append(ndcg_at_k(ranked, q["relevant"], k))
    return {
        t: {m: round(mean(v), 4) for m, v in vals.items()} | {"n": len(vals["recall"])}
        for t, vals in per_type.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--queries", required=True)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    docs = load_corpus(args.corpus)
    queries = load_queries(args.queries)
    if not queries:
        print("Aucune requête annotée (les lignes EXEMPLE sont ignorées).", file=sys.stderr)
        return 1

    # Deux index : le corpus brut, et le corpus normalisé avec la même transformation que les requêtes.
    index_raw = BM25(docs)
    index_norm = BM25({doc_id: normalize_arabizi(text) for doc_id, text in docs.items()})
    results = {
        "brut": evaluate(index_raw, queries, args.k, normalize=False),
        "normalise": evaluate(index_norm, queries, args.k, normalize=True),
    }
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
