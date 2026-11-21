"""Métriques de récupération : recall@k, MRR et nDCG@k (binaire et gradué)."""

import math
from collections.abc import Mapping, Sequence, Set


def recall_at_k(ranked: Sequence[str], relevant: Set[str] | Mapping[str, int | float], k: int) -> float:
    """Recall@k. Si relevant est un dictionnaire, les documents avec un score > 0 sont considérés pertinents."""
    if not relevant:
        return 0.0
    rel_set = set(relevant.keys()) if isinstance(relevant, Mapping) else set(relevant)
    if isinstance(relevant, Mapping):
        rel_set = {d for d, r in relevant.items() if r > 0}
    if not rel_set:
        return 0.0
    hits = len(set(ranked[:k]) & rel_set)
    return hits / len(rel_set)


def reciprocal_rank(ranked: Sequence[str], relevant: Set[str] | Mapping[str, int | float]) -> float:
    """Mean Reciprocal Rank (MRR). Premier document pertinent (rel > 0)."""
    rel_set = {d for d, r in relevant.items() if r > 0} if isinstance(relevant, Mapping) else set(relevant)
    for i, doc_id in enumerate(ranked, start=1):
        if doc_id in rel_set:
            return 1.0 / i
    return 0.0


def ndcg_at_k(
    ranked: Sequence[str],
    relevant: Set[str] | Mapping[str, int | float],
    k: int = 10,
    graded: bool = True,
) -> float:
    """nDCG@k avec support des gains gradués (ex. échelle 0, 1, 2) ou binaires.
    Formule : DCG@k = sum_{i=1}^k (2^{rel_i} - 1) / log2(i + 1)
    """
    if not relevant:
        return 0.0

    if isinstance(relevant, Mapping):
        # Cas gradué : Mapping doc_id -> gain (ex: 2 pour direct, 1 pour partiel)
        rels = [float(relevant.get(doc_id, 0)) for doc_id in ranked[:k]]
        dcg = sum((2.0**rel - 1.0) / math.log2(i + 1) for i, rel in enumerate(rels, start=1))

        # Idéal : trier toutes les pertinence positives de relevant par ordre décroissant
        all_rels = sorted([float(r) for r in relevant.values() if r > 0], reverse=True)
        if not all_rels:
            return 0.0
        idcg = sum((2.0**rel - 1.0) / math.log2(i + 1) for i, rel in enumerate(all_rels[:k], start=1))
        return dcg / idcg if idcg > 0 else 0.0
    else:
        # Cas binaire (Set[str] ou Sequence[str])
        rel_set = set(relevant)
        if not rel_set:
            return 0.0
        dcg = sum(
            1.0 / math.log2(i + 1)
            for i, doc_id in enumerate(ranked[:k], start=1)
            if doc_id in rel_set
        )
        ideal_hits = min(len(rel_set), k)
        idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
        return dcg / idcg if idcg > 0 else 0.0

