# OSF Preregistration Protocol

**Title:** Arabizi Retrieval for Inclusive Learning Support: A Controlled Comparison Protocol of RAG Architectures  
**Author:** Assia Bouamir  
**Date of Preregistration:** November 2026  
**Registration Platform:** Open Science Framework (OSF) / AsPredicted format  

---

## 1. Study Information

### 1.1 Background and Objectives
Retrieval-augmented generation (RAG) is increasingly employed in educational tutoring systems. However, while learner queries in North Africa are frequently formulated in Arabizi (dialectal Arabic written in Latin characters with numerals encoding non-Latin phonemes), the underlying educational corpora are written in French or Modern Standard Arabic (MSA). This study evaluates whether eight distinct retrieval configurations (A0 to A7) can bridge the retrieval and generation quality gap between Arabizi and French queries, and whether performance gains are equitably distributed across Moroccan, Algerian, and Tunisian dialectal varieties.

---

## 2. Hypotheses

- **H1 (Lexical normalization):** Configuration A3 (heuristic rule-based normalization) yields a smaller retrieval gap reduction relative to baseline A2 than query rewriting (A4). Specifically, rule-based surface mapping will show no statistically significant improvement over A2 ($p > 0.05$).
- **H2 (Multilingual query rewriting):** A4 (query rewriting into French, MSA, and Darija) and A5 (corrective retrieval) significantly reduce the Arabizi–French recall gap relative to A2, surviving Holm-Bonferroni correction ($\alpha = 0.05$).
- **H3 (Answer fidelity & complexity plateau):** Answer faithfulness and relevance directly track retrieval recall ($r > 0.80$). Furthermore, recursive agentic graph expansion (A7) does not improve Recall@5 over A5 by more than $0.05$ absolute on single-hop informational questions.
- **H4 (Computational cost trade-off):** A4, A5, and A7 incur higher latency and language-model calls than A2; the marginal gain in gap reduction per additional LLM call decreases progressively along the ladder.
- **H5 (Dialect spread & equity):** Baseline configurations (A1, A2) exhibit significant dialect spread ($\Delta > 0.10$ between the highest-performing and lowest-performing dialect group). Multi-query rewriting (A4) narrows the dialect spread and improves worst-group performance without degrading French reference performance by more than the non-inferiority margin $\epsilon = 0.02$.

---

## 3. Design and Configurations

### 3.1 Controlled Configurations (A0 to A7)
All configurations share an identical corpus (120 passages), generator, decoding temperature ($T=0$), and context budget (at most 5 passages in the prompt).
1. **A0:** Generator only (lower bound, no retrieval).
2. **A1:** Dense retrieval (multilingual semantic embedder, BGE-M3 family).
3. **A2:** Hybrid retrieval (BM25 + dense, Reciprocal Rank Fusion $k=60$, cross-encoder reranking). *Standard Reference Baseline.*
4. **A3:** A2 with rule-based Arabizi surface normalization (digits to letters, accent stripping, letter collapsing).
5. **A4:** A2 applied across 3 query rewrites (French, MSA, Darija) fused via RRF.
6. **A5:** Corrective RAG: A4 with an LLM sufficiency judge triggering a second raw search upon negative verdict.
7. **A6:** A2 augmented with graph neighbours of the top 3 passages (deterministic IDF-overlap graph).
8. **A7:** Full recursive graph-based agentic pipeline with sufficiency-gated expansion (depth $\le 2$, max 6 LLM calls).

### 3.2 Single-Factor Ablation Ladder
- **AB1:** A2 without cross-encoder reranking (evaluates reranker contribution).
- **AB2:** A3 replacing rule-based normalization (V2) with Arabic script transliteration (V3).
- **AB3:** A2 with sufficiency judge and corrective retrieval alone (no rewriting).
- **AB5a:** A4 with single-pass graph expansion without LLM judge gating.
- **AB5b:** AB5a with LLM sufficiency judge gating single-pass expansion.

---

## 4. Sampling and Dataset Specifications

### 4.1 Educational Corpus
- **Size:** 30 scientific and educational topics across 6 disciplines: Physics, Chemistry, Biology, Mathematics, Computer Science, and History of Science.
- **Passages:** 120 passages (60 French, 60 Modern Standard Arabic).
- **Chunking Protocol:** Section-based segmentation with fixed token budget of 200 tokens (~1,000 characters) and 25-token overlap.

### 4.2 Query Dataset (100 Items, 300 Queries)
- **Structure:** 100 information needs, each paired across 3 surface versions sharing an `item_id`:
  - 1 Arabizi query
  - 1 Mixed code-switching query (Arabizi + French)
  - 1 French query (paired ground truth control)
- **Dialect Breakdown:**
  - 34 Moroccan items (`darija_maroc`) = 102 queries
  - 33 Algerian items (`darija_algerie`) = 99 queries
  - 33 Tunisian items (`darija_tunisie`) = 99 queries
- **Learner Levels:** 50 Beginner items, 50 Intermediate items.

---

## 5. Measured Variables and Annotation Protocol

### 5.1 Retrieval Metrics
- **Recall@5:** $|R \cap \text{top5}| / |R|$ for relevant set $R$.
- **MRR:** $1 / \text{rank}$ of first relevant passage in top 10 (or 0).
- **Graded nDCG@10:** $\text{DCG}@10 / \text{IDCG}@10$, using relevance scale 0 (irrelevant), 1 (partially/contextually relevant), 2 (directly answers).

### 5.2 Human Answer Quality & Agreement
- Stratified sample of 40 answers per configuration (320 answers total).
- Independent double-annotation by native dialect speakers on 3-point ordinal scales (0, 1, 2) for Faithfulness and Relevance.
- Inter-annotator reliability metric: Quadratic-weighted Cohen's Kappa ($\kappa$).
- Target acceptance threshold: $\kappa \ge 0.70$. Disagreements adjudicated by a third expert annotator.

---

## 6. Statistical Analysis Plan

- **Primary Unit of Analysis:** The paired item ($N=100$).
- **Inference:** Paired bootstrap resampling with 10,000 resamples to calculate 95% confidence intervals for metric differences ($\Delta = \text{Score}_{\text{French}} - \text{Score}_{\text{Arabizi}}$).
- **Multiple Comparisons:** Family of 7 comparisons against reference A2, corrected via the step-down Holm-Bonferroni procedure ($\alpha = 0.05$).
- **Non-Degradation Criterion:** Configuration $k$ is considered non-inferior on French reference queries if $\text{Score}_{\text{FR}}(k) \ge \text{Score}_{\text{FR}}(A2) - \epsilon$, with $\epsilon = 0.02$.
- **Equity Criterion:** Configuration $k$ improves equity over A2 if and only if:
  1. Gap reduction $RR_k > 0$ with 95% bootstrap CI strictly excluding zero.
  2. The worst dialect group mean does not fall below A2.
  3. The non-degradation threshold on French queries is satisfied.
