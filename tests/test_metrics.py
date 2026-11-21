import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from arabizi.bm25 import BM25  # noqa: E402
from arabizi.metrics import ndcg_at_k, recall_at_k, reciprocal_rank  # noqa: E402


def test_recall_at_k():
    assert recall_at_k(["a", "b", "c"], {"a", "c"}, k=2) == 0.5
    assert recall_at_k(["a", "b", "c"], {"a", "c"}, k=3) == 1.0


def test_reciprocal_rank():
    assert reciprocal_rank(["x", "a", "b"], {"a"}) == 0.5
    assert reciprocal_rank(["x", "y"], {"a"}) == 0.0


def test_ndcg_perfect_ranking_is_one():
    assert ndcg_at_k(["a", "b"], {"a", "b"}, k=2) == 1.0


def test_ndcg_graded_relevance():
    # Graded relevance: doc 'a' has grade 2, 'b' has grade 1, 'c' has grade 0
    # Perfect order ['a', 'b']: nDCG should be 1.0
    rel_map = {"a": 2, "b": 1, "c": 0}
    assert math.isclose(ndcg_at_k(["a", "b"], rel_map, k=2), 1.0)

    # Inverted order ['b', 'a']: DCG = (2^1 - 1)/log2(2) + (2^2 - 1)/log2(3) = 1/1 + 3/1.58496 = 1 + 1.89279 = 2.89279
    # Ideal order ['a', 'b']: IDCG = (2^2 - 1)/log2(2) + (2^1 - 1)/log2(3) = 3/1 + 1/1.58496 = 3 + 0.63093 = 3.63093
    # nDCG = 2.89279 / 3.63093 ≈ 0.7967
    ndcg_inverted = ndcg_at_k(["b", "a"], rel_map, k=2)
    assert 0.79 < ndcg_inverted < 0.81

    # Completely irrelevant docs: nDCG is 0
    assert ndcg_at_k(["c", "d"], rel_map, k=2) == 0.0


def test_bm25_ranks_matching_document_first():
    docs = {
        "d1": "la photosynthese convertit la lumiere en energie",
        "d2": "la revolution francaise commence en 1789",
    }
    index = BM25(docs)
    assert index.rank("photosynthese lumiere", k=2)[0] == "d1"
