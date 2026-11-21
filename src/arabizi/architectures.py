"""Architectures A0 à A7 pour la comparaison RAG sur requêtes arabizi.

Chaque architecture reçoit les mêmes composants (retriever lexical, embedder, reranker,
générateur) et renvoie les passages utilisés, la réponse et le coût (appels LLM, embeddings).

Les composants sont des interfaces : on branche de vrais modèles (BGE-M3, un LLM via API ou local)
ou des substituts pour les tests. Les résultats ne valent qu'avec de vrais modèles.

Budget de contexte commun : 5 passages dans le prompt de génération (A0 : aucun).
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Protocol

from .bm25 import BM25, tokenize
from .normalize import normalize_arabizi


# ---------- Interfaces des composants ----------

class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class Reranker(Protocol):
    def score(self, query: str, passages: list[str]) -> list[float]: ...


class Generator(Protocol):
    def complete(self, prompt: str) -> str: ...


# ---------- Coût et résultat ----------

@dataclass
class Cost:
    llm_calls: int = 0
    embed_calls: int = 0
    rerank_calls: int = 0


@dataclass
class Result:
    architecture: str
    passages: list[str] = field(default_factory=list)   # identifiants des passages dans le contexte
    answer: str = ""
    cost: Cost = field(default_factory=Cost)


# ---------- Corpus et index ----------

@dataclass
class Corpus:
    docs: dict[str, str]
    context_k: int = 5          # passages dans le prompt
    candidate_k: int = 20       # candidats avant reranking
    rrf_k: int = 60             # constante de la fusion par rangs

    def __post_init__(self):
        self.bm25_raw = BM25(self.docs)
        self.bm25_norm = BM25({d: normalize_arabizi(t) for d, t in self.docs.items()})
        self.doc_ids = list(self.docs)
        self._emb_cache: dict[str, list[float]] | None = None
        self.graph = build_doc_graph(self.docs)

    def dense_index(self, embedder: Embedder, cost: Cost) -> dict[str, list[float]]:
        if self._emb_cache is None:
            vecs = embedder.embed([self.docs[d] for d in self.doc_ids])
            cost.embed_calls += 1
            self._emb_cache = dict(zip(self.doc_ids, vecs))
        return self._emb_cache


def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal rank fusion (Cormack et al., 2009)."""
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += 1.0 / (k + rank)
    return [d for d, _ in sorted(scores.items(), key=lambda x: (-x[1], x[0]))]


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


def build_doc_graph(docs: dict[str, str], min_shared: int = 2, top_terms: int = 15) -> dict[str, list[str]]:
    """Graphe de documents : deux documents sont voisins s'ils partagent au moins `min_shared`
    de leurs `top_terms` termes les plus rares (idf). Construction déterministe, sans LLM.
    Pour pouvoir être partagés, les termes doivent avoir une fréquence de document df >= 2."""
    toks = {d: set(tokenize(t)) for d, t in docs.items()}
    df: Counter = Counter()
    for s in toks.values():
        df.update(s)
    graph: dict[str, list[str]] = {d: [] for d in docs}
    # On sélectionne en priorité les termes partagés par au moins deux documents (df >= 2)
    key_terms = {}
    for d, s in toks.items():
        shared = [w for w in s if df[w] >= 2]
        eligible = shared if len(shared) >= min_shared else list(s)
        key_terms[d] = set(sorted(eligible, key=lambda w: (df[w], w))[:top_terms])

    for a in docs:
        for b in docs:
            if a < b and len(key_terms[a] & key_terms[b]) >= min_shared:
                graph[a].append(b)
                graph[b].append(a)
    return graph


# ---------- Briques de récupération ----------

def _lexical(corpus: Corpus, query: str, normalized: bool) -> list[str]:
    index = corpus.bm25_norm if normalized else corpus.bm25_raw
    return index.rank(normalize_arabizi(query) if normalized else query, k=corpus.candidate_k)


def _dense(corpus: Corpus, query: str, embedder: Embedder, cost: Cost) -> list[str]:
    index = corpus.dense_index(embedder, cost)
    qv = embedder.embed([query])[0]
    cost.embed_calls += 1
    ranked = sorted(index, key=lambda d: -_cosine(qv, index[d]))
    return ranked[: corpus.candidate_k]


def _hybrid(corpus: Corpus, query: str, embedder: Embedder, reranker: Reranker | None,
            cost: Cost, normalized: bool = False) -> list[str]:
    lex = _lexical(corpus, query, normalized)
    dense = _dense(corpus, normalize_arabizi(query) if normalized else query, embedder, cost)
    fused = rrf([lex, dense], k=corpus.rrf_k)[: corpus.candidate_k]
    if reranker is None:
        return fused
    scores = reranker.score(query, [corpus.docs[d] for d in fused])
    cost.rerank_calls += 1
    return [d for _, d in sorted(zip(scores, fused), key=lambda x: -x[0])]


def _answer(corpus: Corpus, query: str, passages: list[str], generator: Generator, cost: Cost) -> str:
    context = "\n".join(f"[{i+1}] {corpus.docs[d]}" for i, d in enumerate(passages))
    prompt = (
        "Réponds à la question en utilisant uniquement les passages. "
        "Cite les numéros des passages. Si l'information manque, dis-le.\n\n"
        f"Passages :\n{context}\n\nQuestion : {query}\nRéponse :"
    )
    cost.llm_calls += 1
    return generator.complete(prompt)


def _rewrite_variants(query: str, generator: Generator, cost: Cost) -> list[str]:
    prompt = (
        "Réécris la question suivante (écrite en arabizi) en trois formes : "
        "français, arabe standard, darija. Une forme par ligne, sans commentaire.\n"
        f"Question : {query}"
    )
    cost.llm_calls += 1
    lines = [l.strip() for l in generator.complete(prompt).splitlines() if l.strip()]
    return [query] + lines[:3]


# ---------- Architectures ----------

def a0_no_retrieval(q: str, corpus: Corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    cost.llm_calls += 1
    return Result("A0", [], generator.complete(f"Question : {q}\nRéponse :"), cost)


def a1_dense(q, corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    top = _dense(corpus, q, embedder, cost)[: corpus.context_k]
    return Result("A1", top, _answer(corpus, q, top, generator, cost), cost)


def a2_hybrid(q, corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    top = _hybrid(corpus, q, embedder, reranker, cost)[: corpus.context_k]
    return Result("A2", top, _answer(corpus, q, top, generator, cost), cost)


def a3_hybrid_normalized(q, corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    top = _hybrid(corpus, q, embedder, reranker, cost, normalized=True)[: corpus.context_k]
    return Result("A3", top, _answer(corpus, q, top, generator, cost), cost)


def _multi_query(q, corpus, embedder, reranker, generator, cost) -> list[str]:
    variants = _rewrite_variants(q, generator, cost)
    rankings = [_hybrid(corpus, v, embedder, reranker, cost) for v in variants]
    return rrf(rankings, k=corpus.rrf_k)


def a4_hybrid_rewrite(q, corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    top = _multi_query(q, corpus, embedder, reranker, generator, cost)[: corpus.context_k]
    return Result("A4", top, _answer(corpus, q, top, generator, cost), cost)


def _judge_sufficient(q, corpus, passages, generator, cost) -> bool:
    context = "\n".join(corpus.docs[d] for d in passages)
    prompt = ("Les passages suivants permettent-ils de répondre à la question ? "
              f"Réponds OUI ou NON.\nQuestion : {q}\nPassages :\n{context}")
    cost.llm_calls += 1
    return generator.complete(prompt).strip().upper().startswith("OUI")


def a5_corrective(q, corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    base_rankings = _multi_query(q, corpus, embedder, reranker, generator, cost)
    top = base_rankings[: corpus.context_k]
    if not _judge_sufficient(q, corpus, top, generator, cost):
        # Relance : même pipeline hybride que la première passe, sur la requête brute (pas normalisée),
        # fusionné avec le résultat complet de base.
        extra = _hybrid(corpus, q, embedder, reranker, cost, normalized=False)
        top = rrf([base_rankings, extra], k=corpus.rrf_k)[: corpus.context_k]
    return Result("A5", top, _answer(corpus, q, top, generator, cost), cost)


def a6_graph(q, corpus, embedder, reranker, generator) -> Result:
    cost = Cost()
    base = _hybrid(corpus, q, embedder, reranker, cost)
    seeds = base[:3]
    neighbours = []
    for s in seeds:
        for n in corpus.graph.get(s, []):
            if n not in seeds and n not in neighbours:
                neighbours.append(n)
    top = (seeds + neighbours)[: corpus.context_k]
    return Result("A6", top, _answer(corpus, q, top, generator, cost), cost)


def a7_recursive_graph(q, corpus, embedder, reranker, generator, max_llm_calls: int = 6,
                       max_depth: int = 2, use_judge: bool = True, name: str = "A7") -> Result:
    """Pipeline agentique récursif basé sur un graphe (pas de multi-agents autonomes).

    Étapes déterministes : réécriture (A4), puis, à chaque profondeur, expansion vers les voisins
    du graphe des passages de tête. Si use_judge est vrai, l'expansion n'a lieu que si un appel
    juge répond NON. Le budget d'appels LLM est borné par max_llm_calls.
    """
    cost = Cost()
    base_top = _multi_query(q, corpus, embedder, reranker, generator, cost)[: corpus.context_k]
    depth = 0
    seeds = base_top[:3]
    frontier = seeds
    current_top = list(base_top)
    while depth < max_depth and cost.llm_calls < max_llm_calls and frontier:
        if use_judge and _judge_sufficient(q, corpus, current_top, generator, cost):
            break
        nxt = []
        for d in frontier:
            for n in corpus.graph.get(d, []):
                if n not in current_top and n not in nxt:
                    nxt.append(n)
        if not nxt:
            break
        current_top = (seeds + nxt)[: corpus.context_k]
        frontier = nxt[:3]
        depth += 1
    return Result(name, current_top, _answer(corpus, q, current_top, generator, cost), cost)


def ab5a_graph_single_pass(q, corpus, embedder, reranker, generator) -> Result:
    return a7_recursive_graph(q, corpus, embedder, reranker, generator,
                              max_depth=1, use_judge=False, name="AB5a")


def ab5b_graph_judge_once(q, corpus, embedder, reranker, generator) -> Result:
    return a7_recursive_graph(q, corpus, embedder, reranker, generator,
                              max_depth=1, use_judge=True, name="AB5b")


def _transliterate_arabic(query: str, generator: Generator, cost: Cost) -> str:
    """Translittération Arabizi vers alphabet arabe (V3)."""
    prompt = (
        "Transcris la phrase suivante écrite en arabizi (arabe dialectal en caractères latins) "
        "en caractères arabes uniquement. Réponds uniquement par la translittération, sans explication.\n"
        f"Arabizi : {query}\nArabe :"
    )
    cost.llm_calls += 1
    out = [line.strip() for line in generator.complete(prompt).splitlines() if line.strip()]
    return out[0] if out else query


def ab1_no_rerank(q: str, corpus: Corpus, embedder: Embedder, reranker: Reranker | None, generator: Generator) -> Result:
    """AB1 : A2 sans reranker (BM25 + Dense avec fusion RRF directe)."""
    cost = Cost()
    top = _hybrid(corpus, q, embedder, reranker=None, cost=cost, normalized=False)[: corpus.context_k]
    return Result("AB1", top, _answer(corpus, q, top, generator, cost), cost)


def ab2_transliteration(q: str, corpus: Corpus, embedder: Embedder, reranker: Reranker | None, generator: Generator) -> Result:
    """AB2 : Ablation translittération (V2 -> V3 au sein du pipeline A3).
    Remplace la normalisation heuristique de surface par une translittération en alphabet arabe.
    """
    cost = Cost()
    q_ar = _transliterate_arabic(q, generator, cost)
    top = _hybrid(corpus, q_ar, embedder, reranker, cost, normalized=False)[: corpus.context_k]
    return Result("AB2", top, _answer(corpus, q, top, generator, cost), cost)


def ab3_corrective_no_rewrite(q, corpus, embedder, reranker, generator) -> Result:
    """AB3 : A2 + étape corrective seule (juge puis relance avec composant lexical normalisé)."""
    cost = Cost()
    base_rankings = _hybrid(corpus, q, embedder, reranker, cost)
    top = base_rankings[: corpus.context_k]
    if not _judge_sufficient(q, corpus, top, generator, cost):
        extra = _lexical(corpus, q, normalized=True)
        top = rrf([base_rankings, extra], k=corpus.rrf_k)[: corpus.context_k]
    return Result("AB3", top, _answer(corpus, q, top, generator, cost), cost)


ARCHITECTURES = {
    "A0": a0_no_retrieval,
    "A1": a1_dense,
    "A2": a2_hybrid,
    "A3": a3_hybrid_normalized,
    "A4": a4_hybrid_rewrite,
    "A5": a5_corrective,
    "A6": a6_graph,
    "A7": a7_recursive_graph,
    "AB1": ab1_no_rerank,
    "AB2": ab2_transliteration,
    "AB3": ab3_corrective_no_rewrite,
    "AB5a": ab5a_graph_single_pass,
    "AB5b": ab5b_graph_judge_once,
}

ABLATIONS = {
    "AB1": ab1_no_rerank,
    "AB2": ab2_transliteration,
    "AB3": ab3_corrective_no_rewrite,
    "AB5a": ab5a_graph_single_pass,
    "AB5b": ab5b_graph_judge_once,
}
