"""Tests de plomberie des architectures A0-A7 avec des composants factices.

Les composants factices ne mesurent PAS la qualité : ils vérifient que chaque pipeline
tourne, respecte le budget de contexte (5 passages) et compte correctement son coût.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from arabizi.architectures import ARCHITECTURES, Corpus, build_doc_graph, rrf  # noqa: E402

DOCS = {
    "pression": "la pression atmospherique est la force de l air sur une surface",
    "photo": "la photosynthese convertit la lumiere du soleil en energie",
    "cellule": "la cellule contient un noyau et du cytoplasme",
    "revolution": "la revolution francaise commence en 1789 avec la bastille",
    "pythagore": "le theoreme de pythagore relie les cotes d un triangle rectangle",
    "respiration": "la respiration apporte l oxygene aux cellules",
    "courant": "le courant electrique est un deplacement de charges",
}


class HashEmbedder:
    dim = 128

    def embed(self, texts):
        out = []
        for t in texts:
            v = [0.0] * self.dim
            s = f"  {t.lower()}  "
            for i in range(len(s) - 2):
                v[hash(s[i:i + 3]) % self.dim] += 1.0
            out.append(v)
        return out


class OverlapReranker:
    def score(self, query, passages):
        q = set(query.lower().split())
        return [len(q & set(p.split())) for p in passages]


class StubGenerator:
    def __init__(self):
        self.calls = 0

    def complete(self, prompt):
        self.calls += 1
        if "OUI ou NON" in prompt:
            return "OUI"
        if "Réécris" in prompt:
            return "la pression de l air\nاللحظة الضغط\nla pression daria"
        return "réponse factice"


def _run(name, query="3lach lhawa katdghet"):
    corpus = Corpus(DOCS, context_k=5, candidate_k=10)
    gen = StubGenerator()
    res = ARCHITECTURES[name](query, corpus, HashEmbedder(), OverlapReranker(), gen)
    return res, gen


def test_all_architectures_run_and_respect_context_budget():
    for name in ARCHITECTURES:
        res, _ = _run(name)
        assert res.architecture == name
        assert len(res.passages) <= 5
        assert len(set(res.passages)) == len(res.passages), "passages dupliqués"
        assert all(p in DOCS for p in res.passages)


def test_a0_uses_no_retrieval():
    res, _ = _run("A0")
    assert res.passages == []
    assert res.cost.embed_calls == 0


def test_retrieval_architectures_return_context():
    for name in ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]:
        res, _ = _run(name)
        assert len(res.passages) > 0, name


def test_a4_makes_exactly_one_rewrite_call_plus_answer():
    res, gen = _run("A4")
    # 1 réécriture + 1 réponse finale ; le juge n'existe pas dans A4
    assert res.cost.llm_calls == 2
    assert gen.calls == 2


def test_a5_judge_and_answer_cost_counted():
    res, gen = _run("A5")
    # réécriture + juge (OUI, donc pas de relance) + réponse
    assert res.cost.llm_calls == 3
    assert gen.calls == 3


def test_a7_respects_llm_call_budget():
    corpus = Corpus(DOCS, context_k=5, candidate_k=10)
    gen = StubGenerator()
    from arabizi.architectures import a7_recursive_graph
    res = a7_recursive_graph("3lach lhawa", corpus, HashEmbedder(), OverlapReranker(), gen,
                             max_llm_calls=2)
    assert res.cost.llm_calls <= 3  # réécriture + juge + réponse, au plus


def test_rrf_prefers_documents_ranked_high_in_several_lists():
    fused = rrf([["a", "b", "c"], ["b", "a", "d"]], k=60)
    assert fused[0] in {"a", "b"}
    assert fused.index("c") > fused.index("a")


def test_doc_graph_is_symmetric():
    g = build_doc_graph(DOCS, min_shared=1, top_terms=10)
    for a, nbrs in g.items():
        for b in nbrs:
            assert a in g[b]


def test_ablation_ladder_changes_one_factor_at_a_time():
    from arabizi.architectures import ABLATIONS, ARCHITECTURES
    corpus = Corpus(DOCS, context_k=5, candidate_k=10)
    # AB5a ne doit pas appeler le juge ; AB5b l'appelle une fois ; A7 peut l'appeler davantage.
    g = StubGenerator()
    ABLATIONS["AB5a"]("3lach lhawa", corpus, HashEmbedder(), OverlapReranker(), g)
    n_a = g.calls
    g2 = StubGenerator()
    ABLATIONS["AB5b"]("3lach lhawa", corpus, HashEmbedder(), OverlapReranker(), g2)
    assert g2.calls >= n_a  # le juge ajoute au moins un appel
    assert "A7" in ARCHITECTURES and "AB3" in ABLATIONS


def test_ab3_relaunch_uses_raw_query_like_a5():
    corpus = Corpus(DOCS, context_k=5, candidate_k=10)
    res = ABLATIONS_AB3(corpus)
    assert res.architecture == "AB3"
    assert len(res.passages) <= 5


def test_ab1_and_ab2_ablations_run():
    from arabizi.architectures import ABLATIONS
    corpus = Corpus(DOCS, context_k=5, candidate_k=10)
    gen = StubGenerator()
    res_ab1 = ABLATIONS["AB1"]("3lach lhawa", corpus, HashEmbedder(), OverlapReranker(), gen)
    assert res_ab1.architecture == "AB1"
    assert len(res_ab1.passages) <= 5
    assert res_ab1.cost.rerank_calls == 0  # AB1 removes reranker

    res_ab2 = ABLATIONS["AB2"]("3lach lhawa", corpus, HashEmbedder(), OverlapReranker(), gen)
    assert res_ab2.architecture == "AB2"
    assert len(res_ab2.passages) <= 5
    assert res_ab2.cost.llm_calls >= 2  # 1 transliteration + 1 answer


def ABLATIONS_AB3(corpus):
    from arabizi.architectures import ABLATIONS
    return ABLATIONS["AB3"]("3lach lhawa", corpus, HashEmbedder(), OverlapReranker(), StubGenerator())
