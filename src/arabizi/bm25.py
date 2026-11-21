"""BM25 minimal, sans dépendance externe, pour servir de baseline de récupération lexicale."""

import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class BM25:
    def __init__(self, docs: dict[str, str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_ids = list(docs)
        self.doc_tokens = {doc_id: tokenize(text) for doc_id, text in docs.items()}
        self.doc_len = {doc_id: len(toks) for doc_id, toks in self.doc_tokens.items()}
        self.avgdl = sum(self.doc_len.values()) / max(len(self.doc_len), 1)
        self.tf = {doc_id: Counter(toks) for doc_id, toks in self.doc_tokens.items()}
        df: Counter = Counter()
        for toks in self.doc_tokens.values():
            df.update(set(toks))
        n = len(self.doc_ids)
        self.idf = {term: math.log(1 + (n - f + 0.5) / (f + 0.5)) for term, f in df.items()}

    def score(self, query: str, doc_id: str) -> float:
        s = 0.0
        tf = self.tf[doc_id]
        dl = self.doc_len[doc_id]
        for term in tokenize(query):
            if term not in tf:
                continue
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            s += self.idf.get(term, 0.0) * freq * (self.k1 + 1) / denom
        return s

    def rank(self, query: str, k: int = 10) -> list[str]:
        scored = [(self.score(query, d), d) for d in self.doc_ids]
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [d for s, d in scored[:k] if s > 0]
