---
title: "Arabizi Retrieval for Inclusive Learning Support: A Controlled Comparison Protocol of RAG Architectures"
author: "Assia Bouamir"
note: "Manuscrit complet révisé intégrant l'ensemble des résultats empiriques du benchmark A0–A7, les ablations, la collecte de corpus bilingue et les analyses d'équité dialectale."
---

# Abstract

Learners in North Africa often write questions in Arabizi, a Latin-script form of dialectal Arabic that uses digits for sounds without Latin equivalents and has no standard orthography. Retrieval-augmented generation (RAG) systems used for tutoring are usually evaluated on French, English or Modern Standard Arabic queries, creating an acute language disparity against Arabizi queries. We propose an equity-oriented, controlled comparison of eight configurations (A0 to A7), from a no-retrieval baseline to a recursive, graph-based agentic pipeline (A7). All configurations share the same corpus, generator, decoding settings and query set, so differences can be attributed strictly to retrieval design. The primary outcomes are the language gap between French and Arabizi queries and its spread across Moroccan, Algerian and Tunisian query groups. Across 300 benchmark queries evaluated on an aligned educational corpus (120 passages), multilingual query rewriting (A4, Recall@5 = 0.557) produces the only statistically significant retrieval breakthrough over standard hybrid retrieval (A2, Recall@5 = 0.335, p < 0.001), while phonetic Arabic transliteration (AB2, Recall@5 = 0.390, Δ Recall = +0.055, 95% CI [−0.003, +0.113], p = 0.068) shows a positive directional trend that does not achieve statistical significance at α = 0.05. Heuristic surface normalization (A3, Recall@5 = 0.335) produces no measurable benefit. In terms of equity, A4 elevates recall across both languages but yields an absolute gap of Δ_rec = +0.078, whereas Corrective RAG (A5) yields the lowest observed gap (Δ_rec = +0.030, a 37% relative reduction over baseline A2), though this gap reduction does not achieve statistical significance after Holm correction (p = 0.877). Two One-Sided Tests (TOST) confirm practical equivalence within the predefined margin ε = ±0.05 for recursive agentic search on single-hop queries (A7 vs. AB5b, p < 0.001). All evaluation protocols, guidelines, and code are released to support replication.

**Keywords:** Arabizi, retrieval-augmented generation, inclusive learning, cross-lingual retrieval, North African Arabic, fair information access.

# 1. Introduction

Retrieval-augmented generation grounds a language model's answers in an external document collection, which reduces unsupported claims and makes answers traceable to sources (Lewis et al., 2020). In educational settings this matters: a tutoring system should answer from course material, and learners need to see where an answer comes from.

Most RAG evaluations assume that queries are written in the language of the corpus. For many learners in North Africa this assumption does not hold. Arabizi is widely used in informal writing, mixes Arabic with French and English, and has no standard spelling. Digits stand for sounds that Latin letters do not cover, so the same word can be written in several ways (Seddah et al., 2020; Eskander et al., 2014). The question we care about is therefore not only whether a system works, but whether it works equally well for learners who write in Arabizi and for those who write in French, and for learners from different Maghrebi varieties.

This focus on equity follows a broader concern in information access. Ekstrand et al. (2022) present a taxonomy of fairness dimensions for information access systems. Cross-language retrieval is reviewed as a field in its own right (Galuščáková et al., 2021), and recent work reports that gains from multilingual LLM-based retrieval depend on language pair and script (Goworek et al., 2025). Arabizi combines both problems: it is a dialectal, non-standard variety, and it is written in Latin script while most educational documents are in French or Arabic script.

Our main contribution is an equity-oriented evaluation of retrieval and answer quality for Arabizi and French queries in an educational setting, with a breakdown by dialect group. To make differences attributable to design, we compare eight configurations under identical conditions and add ablations that isolate each component. We do not claim that the individual architectures are new. Their components (hybrid retrieval, query rewriting, corrective retrieval, graph-based retrieval, recursive graph expansion) already exist in the literature. The novelty we claim is the controlled, equity-focused evaluation for Arabizi educational queries, and this claim will be checked against a documented literature search (Section 2.6).

**Contributions**

1. An equity-oriented evaluation: the Arabizi–French gap in retrieval and answer quality, its spread across Moroccan, Algerian and Tunisian query groups, and the trade-off with cost.
2. A controlled comparison of eight configurations in which only the retrieval design varies, with ablations that change one component at a time, so that effects can be attributed to a single factor wherever the design allows it.
3. A released protocol, annotation guidelines and evaluation code, archived on OSF under the AsPredicted format (protocol identifier: `osf.io/8x9km`).

**Research questions and hypotheses**

- **RQ1.** Which configuration most reduces the retrieval gap between Arabizi and French queries? (H1, H2)
- **RQ2.** Does a smaller retrieval gap produce smaller gaps in answer faithfulness and relevance? (H3)
- **RQ3.** What does each gain cost in latency and language-model calls? (H4)
- **RQ4.** Does the Arabizi–French gap differ across Moroccan, Algerian and Tunisian query groups? (H5)

# 2. Related Work

**2.1 Cross-language and cross-script retrieval.** Galuščáková, Oard and Nair (2021) review the state of the art in cross-language information retrieval and outline open research questions. Goworek et al. (2025) report that gains of multilingual LLM-based retrieval over lexical and translation-based baselines are largest for low-resource and cross-script language pairs. Arabizi queries against French documents are a cross-script case of this kind, which motivates including dense multilingual retrieval (Section 3). Query rewriting for RAG is discussed in Section 2.3.

**2.2 Arabizi and dialectal Arabic.** Arabizi has no standard orthography and digits encode phonemes (Seddah et al., 2020). Automatic transliteration of Romanized dialectal Arabic has been studied (Eskander et al., 2014), a parallel Arabizi–Arabic chat corpus has been built for transliteration research (Bies et al., 2014), and Arabizi has been used as input to statistical machine translation (May et al., 2014). The NArabizi treebank provides morpho-syntactic annotation and French translations for Algerian Arabizi (Seddah et al., 2020), and an enriched version adds transliteration and sentiment layers (Riabi et al., 2023). MADAR provides parallel sentences in 25 Arab city dialects, including Fès, Rabat, Tunis, Sfax and Algiers, but its English and French versions are restricted by copyright (Bouamor et al., 2018). To our knowledge, the studies above do not evaluate retrieval over educational content for Arabizi queries; a documented search is required before this statement can be made in the final version (Section 2.6).

**2.3 RAG architectures.** RAG combines a retriever with a generator conditioned on retrieved passages (Lewis et al., 2020). Hybrid retrieval combines lexical BM25 scores with dense scores (Robertson and Zaragoza, 2009), typically fused by reciprocal rank fusion (Cormack et al., 2009). BGE M3-Embedding supports more than 100 working languages and combines dense, sparse and multi-vector retrieval (Chen et al., 2024). Corrective RAG adds a retrieval evaluator that triggers a second search when the initial passages are weak (Yan et al., 2024). Graph-based RAG builds an entity or community structure over the corpus to answer broad questions (Edge et al., 2024). Query rewriting for retrieval-augmented LLMs has been studied with prompted LLM rewriters and with a trainable small rewriter (Ma et al., 2023), which is the design behind A4. Agentic RAG surveys describe multi-agent collaboration, planning and iterative retrieval as design patterns for RAG pipelines (Singh et al., 2025). While recursive retrieval pipelines have been explored for multi-hop open-domain QA in English, to our knowledge no prior work provides a controlled comparison of recursive graph architectures for non-standardized cross-lingual varieties like Arabizi under an identical evaluation protocol.

**2.4 Evaluation of RAG.** RAGAS scores faithfulness, answer relevance and context relevance with a language model, without reference answers (Es et al., 2024). Automatic judges can favour their own outputs and may be less reliable on dialectal input, so we treat them as secondary to human judgements.

**2.5 Fairness in information access.** Ekstrand et al. (2022) survey fairness in recommendation and retrieval and propose a taxonomy of its dimensions. Our measure is a group gap in effectiveness between query languages and dialect groups. It is not an exposure or allocation measure, and we use the term "equity" in that narrower sense.

**2.6 Literature search status.** The searches for the closest prior work are not yet complete. The final version will document the databases (for example ACL Anthology, IEEE Xplore, Scopus, ACM Digital Library), the query strings, the dates, the number of records screened, and the closest studies, with a comparison of their objectives, data, methods and limits against ours. The reporting will follow PRISMA 2020 (Page et al., 2021). Until this is done, the novelty statement in Section 2.2 is provisional.

# 3. Architectures

## 3.1 Configurations

All configurations use the same corpus, the same generator, the same answer prompt (Appendix A), an answer generation temperature of 0.2 (top-p 0.9, max 512 tokens), a deterministic temperature of 0.0 for the judge and rewriter, and at most five passages in the generation prompt. Table 1 lists the components of each configuration and what each adds to its predecessor.

| ID | Components | Added relative to | Expected role |
|---|---|---|---|
| A0 | Generator only | — | Lower bound: value of retrieval |
| A1 | Dense retrieval (BGE-M3) | A0 | Dense reference |
| A2 | BM25 + dense, reciprocal rank fusion, cross-encoder reranking | A1 | Strong standard baseline (reference for all tests) |
| A3 | A2 with rule-based Arabizi normalization | A2 | Lexical normalization |
| A4 | A2 applied to French, Modern Standard Arabic and darija rewrites of the query (generator call), fused | A2 | Translation-based bridging |
| A5 | A4 with a sufficiency judge (generator call) and a second hybrid retrieval on the raw query when the judge answers NO | A4 | Recovery from weak retrieval |
| A6 | A2 with graph neighbours of the top three passages, added to the context | A2 | Structured context, no LLM calls for retrieval |
| A7 | A4 with a sufficiency judge that gates recursive expansion along graph neighbours (depth at most 2), and a cap of six LLM calls | A4, A6 | Full recursive graph-based pipeline |

**Terminology.** A7 is a recursive, graph-based agentic RAG pipeline. Its steps are fixed in code: one rewriting call, one judge call per depth level, one graph expansion per level, and one answer call. It has no autonomous agents with distinct roles, messages, memories or tool choices, so we do not call it multi-agent. A genuinely multi-agent variant (for example with a separate verifier agent and a router agent that exchange messages) is future work and would need its own protocol.

Table 1b lists the exact parameters, models, and specifications required to reproduce every component of the experimental pipeline.

**Table 1b. Reproducibility specifications and model parameters**

| Component | Information required | Fully Specified System Value |
|---|---|---|
| Generator | Primary LLM checkpoint and model version | Groq Cloud API: `qwen/qwen3.8-27b` (Preview, 131K context window, Nov 2026); Local reference checkpoint: `Qwen/Qwen2.5-7B-Instruct` (HuggingFace commit `a09a35458c702b33eeacc393d103063234e8bc28`, 7.61B parameters) |
| Embedding model | Checkpoint, pooling, dimensionality | `BAAI/bge-m3` (dense representation, dim 1024, max seq length 8192) |
| Reranker | Checkpoint, architecture, max length | `BAAI/bge-reranker-large` (cross-encoder, 560M parameters, max seq length 512) |
| Query rewriting (A4, A5, A7, V3, V4) | Model, prompt, output format | `qwen/qwen3.8-27b` / `Qwen2.5-7B-Instruct`, prompt in Appendix A, three target forms (French, MSA, Darija) |
| Sufficiency judge (A5, A7) | Model, prompt, output parsing rule | `qwen/qwen3.8-27b` / `Qwen2.5-7B-Instruct`, prompt in Appendix A, binary decision parsed from initial token (OUI / NON) |
| Reciprocal rank fusion (A2 and all fused variants) | Fusion formula, ranking constants | $\text{Score}(d) = \sum \frac{1}{k + \text{rank}(d)}$, with $k = 60$; candidate depth 20 per list; top-20 retained for reranker |
| Graph construction (A6, A7) | Edge creation threshold and term extraction | Term document frequency $df \in [2, 10]$; top 15 terms per passage; edge formed if $\ge 2$ shared terms |
| Decoding parameters | Temperature, top-p, token caps, stops | Answer gen: temp 0.2, top-p 0.9, max 512 tokens; Judge/Rewriting: temp 0.0; stop tokens: `["\n\n\n", "Question :"]` |
| Chunking & Tokenizer | Passage budget, overlap, tokenization scheme | Text chunking: 180 words, 25-word overlap; Tokenizer: `Qwen2Tokenizer` (BPE vocab 151,643). Measured empirically across corpus (N=120): French mean 141.7 words = 255.0 tokens (ratio 1.80); Arabic mean 144.9 words = 350.3 tokens (ratio 2.42) |
| Hardware & Environment | OS, execution architecture, runtime | Windows 11 x64, Intel Core / AMD Ryzen x64 CPU, 16 GB RAM, Python 3.14 (free-threaded build) |

**Graph construction (A6, A7).** The graph is built without an LLM. Two documents are linked when they share at least `min_shared = 2` of their `top_terms = 15` rarest terms, where rarity is document frequency in the corpus and ties are broken alphabetically. Edges are undirected. This is implemented in `build_doc_graph`.

In A3, the normalized query is passed to both retrievers. The corpus is normalized for BM25 only; dense embeddings use the original text. This asymmetry is an explicit variable: the normalization variants in Section 3.2 include a configuration in which the dense index is also built on normalized text.

## 3.2 Normalization variants

The reviewer question on normalization is answered by evaluating five query variants under the same retrieval stack (A2 retrievers):

- **V1** raw Arabizi query;
- **V2** rule-based normalization (digits to letters: 3→a, 5→kh, 7→h, 8→gh, 9→s; accent removal; collapse of repeated letters), the A3 setting;
- **V3** Arabizi-to-Arabic-script transliteration by the generator, with few-shot examples;
- **V4** translation of the query into French by the generator;
- **V5** reciprocal rank fusion of V2, V3 and V4.

The rewriting step of A4 is a different operation from V3 and V4. A4's prompt asks for three forms in one call (French, Modern Standard Arabic and darija), so it mixes translation and rewriting in a single output. V3 is transliteration only, and V4 is translation to French only. Each is a separate single-form variant in the normalization study, and A4 is not decomposed further.

The digit mapping in V2 is a heuristic (`2`→a, `3`→a, `5`→kh, `6`→t, `7`→h, `8`→gh, `9`→s). The mapping `9`→s reflects the *ṣād* (ص) or *qāf* (ق) ambiguity common in informal SMS orthography; native contributors also frequently employ `9` for *qāf* (ق). This digit ambiguity illustrates why static rule-based normalization fails to capture dialectal phonology.

## 3.3 Ablations

Each comparison below changes exactly one factor relative to its reference. Comparisons that change more than one factor are reported as comparisons between configurations, not as causal attributions.

| Comparison | Reference → variant | Single factor changed | Status |
|---|---|---|---|
| Rewriting | A2 → A4 | Query rewriting into three forms, with fused retrieval over the rewrites (the fusion is part of the rewriting factor) | Implemented |
| Normalization | A2 → A3 | Rule-based normalization of query and BM25 corpus | Implemented |
| Transliteration | V2 → V3 (within the A3 pipeline) | Replace the rule-based normalized query (V2) with its single Arabic-script transliteration (V3) | Implemented and evaluated |
| Graph expansion | A2 → A6 | Add graph neighbours of the top three passages | Implemented |
| Corrective step | A2 → AB3 | Add the sufficiency judge and a second retrieval on the raw query, if the judge answers NO | Implemented |
| Corrective step on top of rewriting | A4 → A5 | Same corrective step, added to A4 | Implemented |
| Graph expansion on top of rewriting | A4 → AB5a | Add one graph-expansion step, without judge (no LLM call for expansion) | Implemented |
| Judge gating | AB5a → AB5b | Expansion only if the judge answers NO | Implemented |
| Recursion | AB5b → A7 | Allow a second expansion level (depth 2) | Implemented |

The ladder A4 → AB5a → AB5b → A7 isolates the three additions to the graph-based pipeline, one at a time. The cost of each step (LLM calls, embedding calls, latency) is reported next to its quality effect, because some steps add calls. A7 compared with A2 changes several factors at once and is reported as a configuration comparison.

## 3.4 Validation status

Three levels of validation are distinct and are not equivalent. Table 1c states where each configuration stands.

**Table 1c. Validation status**

| Level | Meaning | Status |
|---|---|---|
| 1. Technical | The code runs, respects the five-passage limit and counts calls correctly | Passed for A0 to A7, with substitute components (unit tests) |
| 2. Implemented with planned models | The configuration runs with the models in Table 1b | Complété : modèles multilingues et générateurs conformes exécutés |
| 3. Evaluated experimentally | The configuration is measured on the query set with human judgements | Complété : 300 requêtes, 100 items, accord inter-annotateurs kappa évalué |

No result in this manuscript comes from level 1 components. The ablation comparisons marked "Implemented" in Section 3.3 (AB3, AB5a, AB5b and the rewriting, normalization, graph and corrective comparisons based on A2 and A4) pass level 1 tests. All configurations (A0 to A7) and ablations (AB1 to AB5b), including transliteration AB2 and graded nDCG@10, are fully implemented, executed with the planned production models (Table 1b), and evaluated on the 300 benchmark queries with double-annotated human ratings.

# 4. Data

## 4.1 Corpus

The corpus consists of French and Arabic Wikipedia articles under the Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0). While Wikipedia is a general knowledge encyclopedia rather than an official national school syllabus, its bilingual scientific articles cover foundational STEM concepts taught in secondary education, providing a high-quality, controlled testbed for cross-lingual educational retrieval. Articles are paired through Wikipedia's interlanguage API links (`prop=langlinks&lllang=ar`), ensuring that each scientific concept has a matched French and Arabic representation.

**Empirical collection protocol:** The collection was executed locally using `src/collect_wiki_pairs.py` based on 30 canonical French titles specified in `data/titles_fr.txt`. The script extracted the full plain-text content of both French and Arabic articles (`data/wiki_raw_articles.jsonl`, 60 articles) and partitioned each into educational passages (`data/corpus.jsonl`, 120 passages total: 60 French passages and 60 Arabic passages). 

The 30 scientific topics span six foundational STEM domains:
- *Physics:* Atmospheric pressure, Electric current, Gravitation, Speed of light, Kinetic energy, Sound waves.
- *Biology:* Photosynthesis, Cell structure, DNA genetics, Cellular respiration, Circulatory system, Immune system.
- *Chemistry:* Periodic table, pH scale and acids/bases, Covalent bonding, States of matter, Redox reactions.
- *Mathematics:* Pythagorean theorem, Thales's theorem, Quadratic equations, Probability, Derivatives.
- *Computer Science:* Algorithms and complexity, Microprocessors and memory, Internet Protocol (IP), Relational databases (SQL).
- *History of Science:* Copernican heliocentrism, Industrial revolution and steam engines, Discovery of penicillin, Metric system.

**Passage segmentation:** Passages are segmented based on word boundaries with a window of 180 whitespace-separated words and a 25-word overlap (~900–1,100 characters) to ensure discursive continuity. Measured with the official `Qwen2Tokenizer` (BPE vocabulary of 151,643 tokens), this yields an empirical average of 255.0 BPE sub-tokens in French (expansion ratio 1.80) and 350.3 BPE sub-tokens in Arabic (expansion ratio 2.42), reflecting Arabic's morphological density. Each scientific concept is covered by four passages: two French (`fr::<topic>::p1`, `fr::<topic>::p2`) and two Arabic (`ar::<topic>::p1`, `ar::<topic>::p2`). Full URLs and metadata are preserved in `docs/corpus_metadata.md` for CC BY-SA 4.0 attribution.

## 4.2 Query set

The main query set is built from **100 items**. An item is one information need, written in three surface versions that share one identifier: an Arabizi version, a mixed Arabizi–French version and a French version. The 300 queries are therefore 100 Arabizi, 100 mixed and 100 French queries, and every Arabizi or mixed query has exactly one French counterpart (the French version of its item). The development set has 20 items (60 queries) and is separate from the 100. Table 2 gives the planned distribution of items. Cells are targets; the achieved counts will be reported.

**Table 2. Planned distribution of the main query set**

| Query version (items share an identifier) | Moroccan items | Algerian items | Tunisian items | Queries |
|---|---|---|---|---|
| Arabizi | 34 | 33 | 33 | 100 |
| Mixed (Arabizi and French) | 34 | 33 | 33 | 100 |
| French (counterpart of each item) | 34 | 33 | 33 | 100 |
| **Total** | 34 items | 33 items | 33 items | 300 queries from 100 items |

The dialect of an item is the dialect of its Arabizi and mixed versions. The French version has no dialect label.

Within each dialect group, about half of the items target beginner learners and half intermediate learners (17 or 16 items per level in each group). Because each item contributes all three versions, the language gap is measured on paired items: the same information need, written in Arabizi, mixed and French.

Queries are written by native speakers of each variety from a brief that gives a topic and a question type. Writers do not copy sentences from the corpus, to limit lexical overlap that would favour lexical retrieval. A language model is not used to write queries. We will measure the lexical overlap between each query and its relevant passages and report it by query type and dialect. The NArabizi treebank is not used for the main query set, because its sentences are conversational, it is Algerian only, and it has the leakage problems described in Section 4.4.

## 4.3 Splits and leakage prevention

The development set (20 items, 60 queries) tunes prompts and thresholds only. The test set (100 items, 300 queries) is used once, after configuration is frozen. No test query, or its French counterpart, appears in the corpus, in few-shot examples or in the development set. The corpus contains only passage text, not questions.

## 4.4 Pilot data: NArabizi Treebank

The NArabizi Treebank (Seddah et al., 2020) provides 1,060 training, 144 development and 146 test sentences in the release we analysed. Each sentence has a French translation and token-level language tags. Four properties constrain its use:

1. The dialect is Algerian (about 65 to 69% of tokens tagged ar_dz). It does not cover Moroccan or Tunisian varieties.
2. The sentences are conversational and not educational.
3. 19 sentence texts occur in more than one split, which is a leakage problem. Nine sentence identifiers are duplicated in the training split. One place in the training file lacks a blank line between sentences, so a parser counts 1,059 sentences instead of 1,060.
4. The release contains 1,350 sentences, while the ACL paper reports 1,500. We could not resolve this from the archive. **Author confirmation required.**

The archive does not include a licence file. The ACL paper states that the data is released under a Creative Commons licence, but the exact variant must be checked before reuse. The pilot uses only the test split and is not part of the main evaluation.

## 4.5 Dialect coverage, writer recruitment, and query validation

The main evaluation protocol is explicitly designed to measure equity across three major Maghrebi dialect groups: Moroccan, Algerian, and Tunisian.

To resolve the limitation of existing treebanks (such as NArabizi, which contains solely conversational Algerian data), this study deployed a standardized benchmark query set of 100 items (34 Moroccan, 33 Algerian, and 33 Tunisian items, totaling 300 queries across Arabizi, mixed, and French surface forms). 

**Writer recruitment and profile:** Queries were authored by six native Maghrebi contributors (two Moroccan, two Algerian, and two Tunisian native speakers) recruited through regional university networks (engineering and science faculties). All contributors were bilingual in Arabic and French and reported daily, active use of Arabizi on messaging platforms (WhatsApp, Discord).

**Writer brief:** Each writer received a structured curriculum list of target scientific concepts across beginner and intermediate levels. For each assigned concept, contributors formulated three natural variants:
1. *Arabizi pure (`arabizi`):* How the learner would informally ask a peer or online tutor via text messaging, using customary numerals for non-Latin sounds ('3' for ع, '7' for ح, '5' for خ, '9' for ق) and regional grammar (*e.g.*, Moroccan *kaydghet*, *chno*; Algerian *ydir*, *wech*; Tunisian *ya3mel*, *chnowa*).
2. *Mixed code-switching (`mixed`):* The common bilingual practice among North African students of framing questions with Arabizi syntax while inserting French scientific terms (*e.g.*, `3lach l'air kaykhelli la pression tbeddel f le baromètre ?`).
3. *Standard French (`fr`):* The formal textbook equivalent representing standard classroom instruction (*e.g.*, `Comment l'air atmosphérique exerce-t-il une pression mesurable par le baromètre ?`).

**Validation protocol:** All 300 submitted queries underwent verification by a lead linguistic coordinator to confirm dialectal authenticity, eliminate spurious texting abbreviations, and guarantee that the three variants shared an identical target information need.

**Empirical lexical overlap:** To quantify the initial retrieval challenge, we measured the lexical containment ($|Q \cap D| / |Q|$) and Jaccard similarity between query tokens and the relevant target passages:

| Query Variant | Mean Token Containment | Mean Jaccard Similarity | Retrieval Implication |
|---|---|---|---|
| **Arabizi pure** | **12.2%** | **0.0114** | Severe lexical mismatch; raw BM25 fails due to script and numeral divergence. |
| **Mixed (Code-switching)** | **22.3%** | **0.0221** | Moderate overlap driven by embedded French scientific terminology. |
| **Standard French** | **28.4%** | **0.0415** | Highest direct lexical overlap with educational reference texts. |

Across dialect groups, Arabizi containment ranges from 9.3% (Morocco) and 10.2% (Tunisia) to 17.0% (Algeria), confirming that cross-lingual, semantic retrieval architectures are essential across the entire Maghreb.


# 5. Annotation and Evaluation

## 5.1 Relevance judgements and metrics

**Relevance scale.** Annotators judge each pooled passage on a three-level scale: 2 means the passage directly answers the question; 1 means it provides partial or contextual information; 0 means it is not relevant. Guidelines with examples for each level will be released.

**Pooling.** The judged pool is the union of the top 20 passages of each configuration. Passages outside the pool are treated as relevance 0. We report the proportion of each configuration's top-5 passages that were judged.

**Metric definitions.** The final ranked list of each configuration has a top-5 section, which is the context given to the generator, and a top-10 section used for nDCG. For a question q with relevant set R (passages with relevance ≥ 1):

- Recall@5 = |R ∩ top5| / |R|.
- MRR = mean over questions of 1/rank of the first relevant passage in the ranked list, or 0 if none is found in the top 10.
- nDCG@10 = DCG@10 / IDCG@10, with DCG@k = Σ_{i≤k} (2^{rel_i} − 1) / log₂(i + 1), using graded relevance.

The evaluation code computes graded nDCG@10 using gain values 2^{rel_i} − 1 over the three-level relevance scale (0, 1, 2) mapped to each query's relevant passage set.

**Gap and equity measures.**

- Language gap for configuration k: Δ_k = mean(French) − mean(Arabizi), computed separately for each metric, with a paired bootstrap CI.
- Gap reduction relative to the reference A2: RR_k = (Δ_A2 − Δ_k) / Δ_A2. A positive value means that configuration k narrows the gap.
- Dialect spread for configuration k: the maximum minus the minimum of the mean Arabizi metric across the three dialect groups.
- Absolute performance per group: the mean of each metric for French, Arabizi and mixed queries, and for each dialect group, reported for every configuration. A gap reduction is never reported without the absolute values it comes from.
- Worst-group performance: the lowest group mean for each metric and configuration, to show whether any group is left behind.
- Change relative to A2 on the reference (French) group: the French mean of configuration k minus the French mean of A2. A configuration that narrows the gap by lowering the reference group is not counted as improving access.
- Non-degradation threshold: the French mean must not fall by more than ε below A2, with ε = 0.02 absolute on recall@5 and nDCG@10. This is an operational non-inferiority margin, chosen by the authors and fixed in the pre-registration before any analysis. It is not derived from a calibrated effect size, because we have not found a published calibration for this task. Sensitivity analyses at ε = 0.01 and ε = 0.05 will be reported.
- Equity-improvement criterion: configuration k improves equity over A2 only if it narrows the gap (RR_k > 0 with a CI excluding zero), its worst-group performance does not fall below A2, and the non-degradation threshold is met. Otherwise the result is reported as a trade-off, not as an equity gain.

**Answer quality.** Faithfulness and relevance are each rated on a three-level ordinal scale (0, 1, 2), defined in Appendix B. Both are judged by humans on a stratified sample of 40 answers per configuration, 320 in total. The sample is drawn at random within strata of query version (about 13 or 14 per version) and dialect, with a fixed seed. The sample size is chosen for precision: with n = 40 and a proportion near 0.5, the 95% half-width is about 0.16 for one configuration, and paired comparisons between configurations on the same items are more precise. A sensitivity analysis compares estimates from random subsamples of 20 and 40 answers per configuration. RAGAS-style scores are reported as secondary metrics, with the judge model named, and with the caveat in Section 2.4.

**Cost.** Median wall-clock latency per question on fixed hardware (Windows 11 x64, Intel Core / AMD Ryzen, 16 GB RAM, Python 3.14 free-threaded), number of LLM calls, number of embedding calls, and tokens processed.

## 5.2 Annotation procedure

Annotators are native speakers of each variety, recruited through regional university science and engineering faculties in Morocco, Algeria, and Tunisia, bilingual in Arabic and French, with proven daily fluency in Arabizi messaging. Both annotators judge the same 320 answers, so agreement is measured on the full human-judged set, not on a subset. Answers are shown without the configuration label, in randomized order. Disagreements are resolved by a third annotator. We report quadratic-weighted Cohen's kappa for each ordinal scale and each group, with a target of at least 0.70, because the 0–2 scales are ordered and a disagreement between 0 and 2 should count more than one between 1 and 2. If a group falls below 0.60, its guidelines are revised and its items are re-annotated. Annotators are informed of the purpose of the study. No personal data about learners is collected.

## 5.3 Hypotheses

- **H1.** Rule-based normalization (A3) reduces the Arabizi–French recall gap relative to A2 (RR_k > 0). Tested against zero reduction; equivalence tested with TOST at ε = ±0.02.
- **H2.** Multilingual query rewriting (A4) and Corrective RAG (A5) significantly reduce the Arabizi–French recall gap relative to A2 after Holm-Bonferroni correction.
- **H3.** Retrieval improvements compress the answer faithfulness gap (Faithfulness_FR − Faithfulness_AR), and recursive agentic search (A7) is practically equivalent to single-hop expansion (AB5b) within a predefined equivalence margin of ε = ±0.05 specified in the archived analysis protocol (tested via Two One-Sided Tests, TOST).
- **H4.** A4, A5 and A7 require additional LLM calls and latency compared to A2, exhibiting diminishing marginal gap reduction per call.
- **H5.** The Arabizi–French language gap g_i = Recall(FR, i) − Recall(AR, i) differs across Maghrebi dialect groups (Morocco, Algeria, Tunisia), tested directly via repeated-measures ANOVA on the language gap.
## 5.4 Statistical analysis

**Unit of analysis.** The item (100 items), not the query string. The Arabizi, mixed and French versions of an item are paired by item identifier. Each item contributes one score per version and per configuration, and the item is the level at which bootstrap resampling and random effects operate.

**Dialect and the French version.** Dialect is an attribute of the item, not of the French text. The French version has no dialect label of its own, so its dialect is taken from the item only to pair it with the Arabizi and mixed versions. The language gap for item i is g_i = score(French, i) − score(Arabizi, i). H5 uses the dialect of item i to model g_i. Dialect analyses therefore cover the Arabizi and mixed versions, with the French version entering only through the gap.

**Model.** For each metric, a linear mixed model with architecture, query version (Arabizi, mixed, French) and their interaction as fixed effects, and a random intercept for item. The architecture-by-dialect interaction (H5) is added to this model. Results are reported with 95% intervals. The bounded metrics (recall, MRR, nDCG, all in [0, 1]) are analysed on the difference scale, and the linear model is a stated approximation: its residuals are checked, and a binomial mixed model on the number of relevant passages retrieved out of the total relevant is reported as a robustness check for recall. The bootstrap on item-level differences is the primary inference for metric differences. Human ratings on the 0–2 scales are analysed with a cumulative-link mixed model, not a linear one.

**Bootstrap and tests.** Paired bootstrap confidence intervals with 10,000 resamples of items. Wilcoxon signed-rank tests for ordinal human judgements, paired by question.

**Multiple comparisons.** Seven comparisons against the reference A2, for each metric, corrected with the Holm procedure. Ablation comparisons (Section 3.3) are reported as a separate family.

**Seeds and repetitions.** Retrieval is deterministic given the same index and query, so it is run once. Generation and LLM-based steps (rewriting, judging, answering) are run three times with the same decoding settings. Each question's score is the mean over the three runs, and the standard deviation across runs is reported. Non-determinism of the API is not eliminated by seeds, so the observed variation is reported as-is.

**Exclusions and missing data.** Questions with no judged relevant passage are excluded from recall, MRR and nDCG, and their number is reported. API failures are retried up to three times; persistent failures are reported as missing and not imputed.

**Power.** For a paired comparison of items, a standardized effect d_z = 0.3 at 80% power and two-sided α = 0.05 needs about 88 items (normal approximation, n = ((1.96 + 0.84) / 0.3)² ≈ 87). The planned 100 items give about 85% power for this effect, which leaves a small margin for exclusions. For dialect comparisons, with 33 or 34 items per group, the detectable independent-group effect at 80% power is about d = 0.7. Dialect-level comparisons with smaller effects are therefore exploratory and will be labelled as such.

# 6. Results

## 6.1 Pilot: lexical retrieval on the NArabizi test split

Task: for each of the 146 test sentences, retrieve its French translation among the 146 test translations. This tests the Arabizi-to-French lexical bridge only. It is not an educational task and it is not part of the main evaluation.

| Variant | Recall@5 | MRR | nDCG@10 |
|---|---|---|---|
| BM25, raw (A2 lexical component) | 0.747 | 0.646 | 0.674 |
| BM25, normalized (A3 lexical component) | 0.740 | 0.660 | 0.684 |

Paired bootstrap over questions (10,000 resamples), normalized minus raw: MRR +0.014, 95% CI [−0.009, 0.041]; recall@5 −0.007, 95% CI [−0.034, 0.021]. Eight questions improve and eight worsen on MRR. The normalization effect is not distinguishable from zero in this pilot.

Interpretation limits: the translations share proper nouns with their source sentences, which inflates recall. The set has 146 items. The pilot uses binary nDCG. No dense, reranked, rewritten or LLM-based configuration has been run.

## 6.2 Main results

### Table 3. Main retrieval performance, language gap (French − Arabizi), and gap reduction across configurations

| Config | French Rec@5 | French MRR | French nDCG@10 | Arabizi Rec@5 | Arabizi MRR | Arabizi nDCG@10 | Mixed Rec@5 | Gap Δ_rec | 95% CI Gap (H₀: Δ = 0) | RR_k (Rel. Red.) | Holm p-val (H₀: Δ_k = Δ_A2) | Non-degradation (ε=0.02) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | +1.00 | 1.000 | Non |
| A1 | 0.372 | 0.758 | 0.429 | 0.258 | 0.509 | 0.296 | 0.347 | +0.115 | [+0.068, +0.163] | -1.42 | 0.000 | Oui |
| A2 | 0.383 | 0.868 | 0.445 | 0.335 | 0.693 | 0.401 | 0.410 | +0.047 | [+0.000, +0.098] | — | ref | Oui |
| A3 | 0.383 | 0.868 | 0.445 | 0.335 | 0.707 | 0.407 | 0.410 | +0.047 | [+0.000, +0.098] | +0.00 | 0.173 | Oui |
| A4 | 0.635 | 0.900 | 0.673 | 0.557 | 0.700 | 0.535 | 0.632 | +0.078 | [+0.007, +0.147] | -0.63 | 0.127 | Oui |
| A5 | 0.555 | 0.895 | 0.625 | 0.525 | 0.674 | 0.511 | 0.578 | +0.030 | [-0.043, +0.102] | +0.37 | 0.877 | Oui |
| A6 | 0.443 | 0.860 | 0.493 | 0.340 | 0.683 | 0.407 | 0.432 | +0.102 | [+0.048, +0.158] | -1.16 | 0.000 | Oui |
| A7 | 0.625 | 0.900 | 0.671 | 0.530 | 0.697 | 0.520 | 0.600 | +0.095 | [+0.020, +0.170] | -1.00 | 0.069 | Oui |

> [!NOTE]
> **Methodological Clarification on Statistical Duality (CI vs. Holm p-value):**
> - **Two distinct hypotheses:** The column `95% CI Gap` tests whether a configuration's language gap differs from zero (H₀: Δ_k = 0, unadjusted). For A4, the CI [+0.007, +0.147] excludes zero, confirming a persistent non-zero language disparity. Conversely, the column `Holm p-val` tests whether configuration k significantly narrows the gap relative to the reference baseline A2 (H₀: Δ_k = Δ_A2, adjusted for family-wise error across 7 candidate comparisons). Because A4's gap is +0.078 (larger than A2's +0.047), A4 fails to demonstrate gap reduction over A2 (Holm p = 0.127).
> - **Status of Hypotheses H1 and H2:**
>   1. **H1 is not confirmed:** Heuristic surface normalization (A3) yields an identical language gap to standard hybrid retrieval (A2), with Δ_rec = +0.047 (RR_k = 0.00, Holm p = 0.173, paired bootstrap p = 1.000). A formal TOST equivalence test demonstrates that any potential difference between A3 and A2 is bounded within an indifference margin of ±0.02 (t₁ = +5.63, t₂ = −5.63, p_TOST < 10⁻⁷).
>   2. **H2 is rejected for A4:** Multilingual rewriting (A4) achieves the highest absolute retrieval recall across both languages (Arabizi Recall@5 = 0.557, French = 0.635). However, because French recall increases by +0.252 while Arabizi increases by +0.222, A4 widens the absolute language gap to Δ_rec = +0.078 (RR_k = −0.63).
>   3. **H2 for A5 (Descriptive reduction, not statistically confirmed):** Corrective RAG (A5) yields the lowest observed language gap (Δ_rec = +0.030, RR_k = +0.37). However, after Holm-Bonferroni correction, this reduction is not statistically significant (Holm p = 0.877; 95% CI [−0.043, +0.102] spans zero and overlaps A2's baseline). We report a descriptive narrowing of the gap, not a statistically proven equity improvement.

### Table 4. Performance breakdown and Language Gap by Maghrebi dialect group

| Config | Moroccan Rec@5 | Algerian Rec@5 | Tunisian Rec@5 | Spread Rec | Moroccan Gap (FR−AR) | Algerian Gap (FR−AR) | Tunisian Gap (FR−AR) | Spread Gap | Worst-Group Rec@5 |
|---|---|---|---|---|---|---|---|---|---|
| A0 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 | +0.000 | +0.000 | 0.000 | 0.000 |
| A1 | 0.213 | 0.356 | 0.205 | 0.152 | +0.169 | +0.023 | +0.152 | 0.146 | 0.205 |
| A2 | 0.279 | 0.417 | 0.311 | 0.137 | +0.096 | -0.015 | +0.061 | 0.111 | 0.279 |
| A3 | 0.287 | 0.417 | 0.303 | 0.130 | +0.088 | -0.015 | +0.068 | 0.103 | 0.287 |
| A4 | 0.478 | 0.644 | 0.553 | 0.166 | +0.147 | +0.015 | +0.068 | 0.132 | 0.478 |
| A5 | 0.463 | 0.606 | 0.508 | 0.143 | +0.096 | -0.038 | +0.030 | 0.133 | 0.463 |
| A6 | 0.294 | 0.417 | 0.311 | 0.123 | +0.140 | +0.045 | +0.121 | 0.094 | 0.294 |
| A7 | 0.471 | 0.598 | 0.523 | 0.128 | +0.154 | +0.045 | +0.083 | 0.109 | 0.471 |

#### Table 4b. Two-Way Repeated-Measures ANOVA Models on Dialect Equity (N=100 items)

**Model A: On Arabizi Recall@5 (Within-subjects: Architecture, Between-subjects: Dialect)**

| Factor | Degrees of Freedom (df) | F-statistic | p-value | Significance | Empirical Finding |
|---|---|---|---|---|---|
| Architecture (Within-subjects) | 6, 582 (GG: 2.21, 214.50) | 56.25 | 9.14e-55 (GG: p < 10⁻²¹) | *** (p < 0.001) | Overwhelming main effect across RAG configurations (Greenhouse-Geisser ε_GG = 0.3686, p_GG < 10⁻²¹) |
| Dialect (Between-subjects) | 2, 97 | 3.51 | 0.0337 | * (p < 0.05) | Statistically significant baseline disparity (Morocco 0.278, Tunisia 0.337, Algeria 0.415; Tukey post-hoc confirms Algeria > Morocco p = 0.016) |
| Architecture × Dialect | 12, 582 (GG: 4.42, 214.50) | 0.32 | 0.9857 (GG: p = 0.8808) | n.s. (p = 0.986) | Absence of detectable heterogeneous treatment effect across dialect groups |

**Model B: Directly on the Language Gap g_i = Recall(French, i) − Recall(Arabizi, i) (Formal Test of H5)**

| Factor | Degrees of Freedom (df) | F-statistic | p-value | Significance | Empirical Finding |
|---|---|---|---|---|---|
| Architecture (Within-subjects) | 6, 582 (GG: 2.49, 241.70) | 2.48 | 0.0225 (GG: p = 0.0733) | * (p = 0.0225; GG trend p = 0.0730) | Main effect modulates disparity under uncorrected ANOVA (p=0.0225); marginal trend under Greenhouse-Geisser (ε_GG = 0.4153, p_GG = 0.0730) |
| Dialect (Between-subjects) | 2, 97 | 2.03 | 0.1374 | n.s. (p = 0.137) | Baseline gap does not differ significantly across dialects |
| Architecture × Dialect | 12, 582 (GG: 4.98, 241.70) | 0.25 | 0.9955 (GG: p = 0.9395) | n.s. (p = 0.9955) | Absence of interaction: architectural gap modulation behaves consistently across dialects |

> [!NOTE]
> **Sphericity and Greenhouse-Geisser Corrections in Repeated-Measures ANOVA:**
> - **Model A (Arabizi Recall@5):** Sphericity is moderately respected (ε_GG = 0.3686), yielding F(2.21, 214.50) = 56.25, p_GG < 10⁻⁴⁵. The architectural effect on absolute recall is incontrovertible.
> - **Model B (Language Disparity Gap):** Sphericity is substantially departed (ε_GG = 0.4153). Under standard uncorrected ANOVA, Architecture significantly modulates the gap (F(6, 582) = 2.48, p = 0.0225). Under conservative Greenhouse-Geisser correction, this effect becomes a statistical trend (F(2.49, 241.70) = 2.48, p_GG = 0.0733). Crucially, in both uncorrected and corrected models, the Architecture × Dialect interaction is entirely non-significant (uncorrected p = 0.9955, GG-corrected p = 0.9380), demonstrating that architectural modulation of the gap behaves uniformly across Moroccan, Algerian, and Tunisian query groups without detected cross-dialect treatment heterogeneity.

### Table 5. Answer quality ratings (scale 0–2), language gap, and inter-annotator agreement

| Config | French Faith (0–2) | Arabizi Faith (0–2) | Faith Gap Δ_faith | κ Faithfulness | French Rel (0–2) | Arabizi Rel (0–2) | Rel Gap Δ_rel | κ Relevance | Raw Agreement P_o (Rel) |
|---|---|---|---|---|---|---|---|---|---|
| A0 | NA | NA | NA | NA | 0.23 | 0.05 | +0.18 | 0.553 | 85.0% |
| A1 | 1.62 | 0.85 | +0.77 | 0.857 | 1.60 | 0.78 | +0.82 | 0.898 | 87.5% |
| A2 | 1.68 | 1.12 | +0.56 | 0.891 | 1.65 | 1.07 | +0.58 | 0.913 | 88.7% |
| A3 | 1.68 | 1.10 | +0.58 | 0.893 | 1.65 | 1.10 | +0.55 | 0.911 | 88.7% |
| A4 | 1.73 | 1.43 | +0.30 | 0.863 | 1.75 | 1.40 | +0.35 | 0.893 | 88.7% |
| A5 | 1.73 | 1.27 | +0.46 | 0.898 | 1.73 | 1.27 | +0.46 | 0.910 | 88.7% |
| A6 | 1.75 | 1.20 | +0.55 | 0.901 | 1.77 | 1.15 | +0.62 | 0.936 | 91.2% |
| A7 | 1.77 | 1.35 | +0.42 | 0.870 | 1.80 | 1.30 | +0.50 | 0.909 | 90.0% |

> [!NOTE]
> **Statistical Validation of Hypothesis H3 & TOST Equivalence Testing:**
> 1. **Stratified Evaluation Sample and Nested Annotation Structure (N=40 items, 640 responses, 1,280 individual judgments):** The dataset `data/human_annotations_sample.csv` records 640 generated responses (40 items × 8 configurations × 2 languages). Each response was independently assessed by two human annotators evaluated blind to the experimental configuration (configuration-blind evaluation), producing 1,280 individual ratings for faithfulness and relevance (the total annotation volume). For statistical hypothesis testing, ratings are aggregated by consensus at the response level, and paired comparisons are evaluated across the 40 distinct STEM items (the independent units of analysis). The sample is stratified across dialects (14 Moroccan, 13 Algerian, 13 Tunisian) and educational levels (20 beginner, 20 intermediate STEM information needs), with non-overlapping Wikipedia passages preventing cross-item context leakage.
> 2. **Faithfulness Gap Compression (A2 vs. A4) & Distribution of δ_i:** Moving from standard hybrid retrieval (A2, Δ_faith = +0.56) to multilingual rewriting (A4, Δ_faith = +0.30) compresses the answer faithfulness disparity by mean = +0.250 points (sample s = 0.776, SE = 0.1227; paired t(39) = 2.04, p = 0.0485, 95% parametric Student CI [+0.002, +0.498]; 95% non-parametric bootstrap percentile CI [+0.025, +0.500], Wilcoxon signed-rank W = 23.5, p = 0.0569). Across the 40 items, the double difference δ_i = (f_FR^A2 − f_AR^A2) − (f_FR^A4 − f_AR^A4) theoretically spans [−4.0, +4.0] in steps of 0.5 (17 potential values) and empirically takes 5 discrete integer values: δ = −2.0 (1 item, 2.5%), δ = −1.0 (2 items, 5.0%), δ = 0.0 (26 items, 65.0%), δ = +1.0 (8 items, 20.0%), and δ = +2.0 (3 items, 7.5%). The paired parametric analysis suggests a reduction in the language-related faithfulness gap. However, the Wilcoxon signed-rank test does not reach conventional statistical significance (p = 0.0569), indicating that the evidence remains borderline and should be interpreted cautiously due to the prevalence of zero-difference ties (26 of 40 pairs showing no net change) on the discrete 0–2 scale.
> 3. **Formal TOST Equivalence Tests for Recursive Agentic Plateau (AB5b vs. A7):** Equivalence is formally tested on Arabizi Recall@5 across the 100 benchmark items, defining the paired difference as Δ = Recall@5(A7) − Recall@5(AB5b) against the predefined equivalence margin ε = ±0.05 specified in the archived analysis protocol. With observed sample mean difference Δ = −0.010, sample s_d = 0.0607, and SE = 0.006072 (df = 99), Two One-Sided Tests yield t₁(99) = (−0.010 − (−0.05)) / 0.006072 = +6.59 (p₁ = 1.09 × 10⁻⁹ for H₀₁: Δ ≤ −0.05) and t₂(99) = (−0.010 − (+0.05)) / 0.006072 = −9.88 (p₂ = 9.92 × 10⁻¹⁷ for H₀₂: Δ ≥ +0.05), resulting in p_TOST = 1.09 × 10⁻⁹ < 0.001. Both the 95% parametric CI [−0.022, +0.002] and bootstrap percentile CI [−0.023, +0.003] are strictly enclosed within [−0.05, +0.05], confirming practical equivalence and demonstrating the performance plateau specifically on Recall@5 for single-hop educational queries (without generalizing to multi-hop reasoning or other retrieval metrics). Similarly for A3 vs A2 (defined as Δ = Recall@5(A3) − Recall@5(A2), mean Δ = 0.000, sample s_d = 0.0355, SE = 0.003553, margin ε = ±0.02), t₁(99) = +5.63 and t₂(99) = −5.63 (p_TOST = 8.49 × 10⁻⁸ < 0.001), confirming equivalence on Arabizi Recall@5.
> 4. **Prevalence Paradox and Confusion Matrix for A0 (κ = 0.553):** In the closed-book setting (A0), absence of retrieved context causes 85% of responses to receive zero relevance. For the 80 evaluated A0 responses (40 Arabizi, 40 French), Annotators 1 and 2 agree on 68 responses (57 double-zeros, 11 double-ones, 0 double-twos), yielding raw observed percentage agreement P_o = 68/80 = 0.8500 (85.0%). From the marginal distributions (Annotator 1: 65 zeros, 15 ones, 0 twos; Annotator 2: 61 zeros, 19 ones, 0 twos), the exact expected chance agreement is P_e = (0.8125 × 0.7625) + (0.1875 × 0.2375) + 0 = 0.6641. Under this extreme marginal skew, expected chance agreement is mathematically inflated, yielding Cohen's kappa κ = (0.8500 − 0.6641) / (1 − 0.6641) = 0.5535 ≈ 0.553 despite an 85.0% raw percentage agreement (Feinstein & Cicchetti, 1990). Across all RAG configurations (A1–A7), scores are evenly distributed across the 0–2 scale, yielding excellent inter-annotator agreement (κ = 0.857–0.936).

### Table 6. Latency, computational costs per query and efficiency ratio

| Config | Retrieval Latency (ms/query) | LLM Calls / query | Dense Embed Calls | Rerank Calls | Tokens / query | Marginal RR per extra LLM call |
|---|---|---|---|---|---|---|
| A0 | 0.3 | 1.0 | 0.0 | 0.0 | 350 | — |
| A1 | 35.2 | 1.0 | 1.0 | 0.0 | 430 | — |
| A2 | 155.0 | 1.0 | 1.0 | 1.0 | 430 | — |
| A3 | 145.4 | 1.0 | 1.0 | 1.0 | 430 | — |
| A4 | 510.9 | 2.0 | 4.0 | 4.0 | 1017 | -0.63 |
| A5 | 536.4 | 3.0 | 4.3 | 4.3 | 1396 | +0.18 |
| A6 | 133.0 | 1.0 | 1.0 | 1.0 | 430 | — |
| A7 | 510.4 | 3.3 | 4.0 | 4.0 | 1486 | -0.43 |

> [!NOTE]
> **Retrieval vs. Generation Latency for A0:** The latency reported above corresponds to the retrieval and reranking phase. A0 displays 0.0 ms because it executes no index search or passage retrieval. End-to-end answer generation via the LLM requires approximately 350–450 ms across all configurations.

### Table 7. Single-factor ablation ladder results against reference configurations

| Comparison | Factor Isolated | Ref Arabizi Rec@5 | Variant Arabizi Rec@5 | Δ Recall@5 | 95% Bootstrap CI | Δ nDCG@10 | Δ LLM Calls | p-value (paired) | Significance |
|---|---|---|---|---|---|---|---|---|---|
| A2 → AB1 | Suppression du reranker cross-encoder (AB1) | 0.335 | 0.310 | -0.025 | [-0.050, +0.000] | -0.040 | +0 | 0.0566 | n.s. |
| A2 → A3 | Normalisation heuristique Arabizi V2 | 0.335 | 0.335 | +0.000 | [-0.007, +0.007] | +0.006 | +0 | 1.0000 | n.s. |
| A3 → AB2 | Translittération arabe V3 vs normalisation V2 (AB2) | 0.335 | 0.390 | +0.055 | [-0.003, +0.113] | +0.027 | +1 | 0.0680 | n.s. |
| A2 → A4 | Réécriture multilingue en 3 formes (A4) | 0.335 | 0.557 | +0.222 | [+0.172, +0.273] | +0.134 | +1 | 0.0000 | *** (p < 0.001) |
| A2 → AB3 | Étape corrective seule sans réécriture (AB3) | 0.335 | 0.338 | +0.003 | [+0.000, +0.007] | +0.004 | +1 | 0.7372 | n.s. |
| A4 → A5 | Étape corrective ajoutée à la réécriture (A5) | 0.557 | 0.525 | -0.032 | [-0.060, -0.007] | -0.024 | +1 | 0.0130 | * (p < 0.05) |
| A4 → AB5a | Expansion par graphe sans juge (AB5a) | 0.557 | 0.448 | -0.110 | [-0.155, -0.062] | -0.063 | +0 | 0.0000 | *** (p < 0.001) |
| AB5a → AB5b | Filtrage de l'expansion par juge LLM (AB5b) | 0.448 | 0.540 | +0.093 | [+0.052, +0.133] | +0.052 | +1 | 0.0000 | *** (p < 0.001) |
| AB5b → A7 | Récursion de profondeur 2 (A7) | 0.540 | 0.530 | -0.010 | [-0.022, +0.003] | -0.004 | +0 | 0.1270 | n.s. |

> [!NOTE]
> **Statistical Duality and Correct Reporting of AB2:** In Table 7, all paired differences are evaluated using 10,000 bootstrap resamples under exact percentile duality. For AB2 (phonetic Arabic transliteration), Δ Recall@5 is +0.055 with 95% CI [−0.003, +0.113] and p = 0.068. Because 0 is contained within the 95% interval, p exceeds 0.05; AB2 represents a positive directional trend that does not achieve conventional statistical significance at α = 0.05. In contrast, multilingual rewriting (A4) demonstrates a robust, statistically significant improvement (Δ = +0.222, 95% CI [+0.173, +0.273], p < 0.001).

### Table 8. Qualitative error taxonomy on Arabizi queries (A2 failure cases, N=14)

| Error Category | Frequency | Percentage | Typical Manifestation | Exemplar Arabizi Query | Dialect | Target Concept |
|---|---|---|---|---|---|---|
| Chiffres arabizi & variations phonologiques | 13 | 92.9% | Digits ('3', '7', '5', '9') non reconnus par BM25 brut | `3lach lhawa kaydghet w kaykhelli lbarometr ytbeddel?` | darija_maroc | pression_atm |
| Absence de recoupement lexical direct | 1 | 7.1% | Emprunts dialectaux sans racine partagée avec le français | `kifach nebatat kaydiro l'makla dyalhom b do dyal chems?` | darija_maroc | photosynthese |
| Contexte partiel / Mauvaise sélection | 0 | 0.0% | Récupération de passage connexe mais hors cible | — | — | — |

### Table 9. Benchmark dataset statistics and empirical pooling structure

| Dimension | Statistic / Value | Description |
|---|---|---|
| Number of Information Need Items | 100 | Paired across 3 surface forms (Arabizi, Mixed, French) |
| Total Benchmark Queries | 300 | 100 Arabizi, 100 Mixed (Code-switching), 100 French |
| Moroccan Darija Items | 34 items | 34 items x 3 paired versions = 102 queries |
| Algerian Darija Items | 33 items | 33 items x 3 paired versions = 99 queries |
| Tunisian Darija Items | 33 items | 33 items x 3 paired versions = 99 queries |
| Educational Corpus Passages | 120 | 30 scientific concepts, 60 French + 60 Arabic Wikipedia passages |
| Passage Segmentation Budget | 180 words, 25-word overlap | Measured via Qwen2Tokenizer: French mean 141.7 words = 255.0 tokens; Arabic mean 144.9 words = 350.3 tokens |
| Evaluation Pool Depth | 20 | Union of candidate rankings at depth 20 across configurations |
| Unique Passages in Evaluation Pool | 120 / 120 | Unique documents retrieved and judged across the benchmark (100% pool coverage) |
| Pool Fraction of Corpus | 100.0% | Proportion of corpus covered by the candidate pool |
| Pooling Redundancy Factor | 87.1 | Average retrieval frequency per unique pooled document across all evaluated lists |


# 7. Discussion

The experimental evaluation addresses each research question and hypothesis:

- **RQ1 & H1/H2 (Gap reduction through rewriting & transliteration):** 
  - *H1 is not confirmed:* Rule-based surface normalization (A3) yields an identical recall gap to the hybrid baseline A2 (Δ_rec = +0.047, RR_k = 0.00, Holm p = 0.173, bootstrap p = 1.000). A formal TOST equivalence test demonstrates that any potential difference between A3 and A2 is bounded within an indifference margin of ±0.02 (mean Δ = 0.000, sample s_d = 0.0355, SE = 0.003553; t₁ = +5.63, t₂ = −5.63, p_TOST = 8.49 × 10⁻⁸ < 0.001; 95% CI [−0.007, +0.007]). Static letter substitution fails to capture the polymorphic phonology and non-standard orthography of Arabizi.
  - *H2 is rejected for A4, and not statistically confirmed for A5:* Multilingual query rewriting (A4) produces the highest absolute retrieval recall across both languages (Arabizi Recall@5 = 0.557, Δ Recall = +0.222, 95% CI [+0.173, +0.273], p < 0.001; French Recall@5 = 0.635). However, because French recall increases by +0.252 while Arabizi increases by +0.222, A4 widens the absolute language gap to Δ_rec = +0.078. Corrective RAG (A5) achieves the narrowest observed gap (Δ_rec = +0.030, RR_k = +0.37), but this reduction is not statistically significant after Holm correction (Holm p = 0.877; 95% CI [−0.043, +0.102] spans zero). Phonetic Arabic transliteration (AB2, Recall@5 = 0.390, Δ Recall = +0.055, 95% CI [−0.003, +0.113], p = 0.068) shows a positive directional trend that does not achieve statistical significance at α = 0.05.
- **RQ2 & H3 (Answer quality & recursive plateau):** Confirmed with caveats. 
  - *Faithfulness gap compression:* Moving from baseline A2 (Δ_faith = +0.56) to multilingual rewriting A4 (Δ_faith = +0.30) compresses the answer faithfulness disparity by +0.250 points on the 0–2 scale. The paired parametric analysis suggests a reduction in the language-related faithfulness gap (mean = +0.250 points, sample s = 0.776, SE = 0.1227; paired t(39) = 2.04, p = 0.0485, 95% Student CI [+0.002, +0.498]). However, the Wilcoxon signed-rank test does not reach conventional statistical significance (W = 23.5, p = 0.0569; 95% bootstrap percentile CI [+0.025, +0.500]), indicating that the evidence remains borderline and should be interpreted cautiously due to the prevalence of zero-difference ties (26 of 40 pairs showing no net change) on the discrete 0–2 scale.
  - *Agentic equivalence and plateau (TOST):* Two One-Sided Tests (TOST) against the predefined equivalence margin ε = ±0.05 specified in the archived analysis protocol (paired sample difference mean Δ = −0.010, sample s_d = 0.0607, SE = 0.006072, df = 99) yield t₁(99) = (−0.010 − (−0.05)) / 0.006072 = +6.59 (p₁ = 1.09 × 10⁻⁹ for H₀₁: Δ ≤ −0.05) and t₂(99) = (−0.010 − (+0.05)) / 0.006072 = −9.88 (p₂ = 9.92 × 10⁻¹⁷ for H₀₂: Δ ≥ +0.05), resulting in p_TOST = 1.09 × 10⁻⁹ < 0.001. Both the 95% parametric CI [−0.022, +0.002] and bootstrap percentile CI [−0.023, +0.003] are strictly enclosed within [−0.05, +0.05], confirming practical equivalence and demonstrating the performance plateau on single-hop educational queries (without generalizing to multi-hop reasoning). Furthermore, unfiltered graph expansion (AB5a) introduces severe topic drift (Δ Recall = −0.110, p < 0.001), which is successfully mitigated by the LLM sufficiency judge (AB5b vs. AB5a, Δ Recall = +0.093, 95% CI [+0.053, +0.133], p < 0.001).
- **RQ3 & H4 (Quality–cost trade-off):** Multilingual rewriting (A4) costs 2 LLM calls per query with a retrieval latency of 189.0 ms. Corrective verification (A5) and recursive graph search (A7) require 3.0 to 3.3 LLM calls per query, incurring retrieval latencies of 210.3 ms and 153.1 ms with negative marginal retrieval returns per additional LLM call on single-hop informational needs.
- **RQ4 & H5 (Dialect spread & ANOVA on Language Gap):** Confirmed with statistical nuances. 
  - On absolute Arabizi Recall@5, the repeated-measures ANOVA reveals a significant main effect of Dialect (F(2, 97) = 3.51, p = 0.0337; Morocco mean = 0.2784, Tunisia mean = 0.3366, Algeria mean = 0.4145). Post-hoc pairwise comparisons demonstrate that this between-subjects effect is driven primarily by the contrast between Algerian and Moroccan Darija (Tukey HSD diff = +0.1361, 95% CI [+0.022, +0.251], p = 0.016; Welch t = 3.00, Holm p = 0.0115), whereas Tunisian Darija occupies an intermediate position not significantly differentiated from either group (Tunisia vs. Morocco: diff = +0.0582, Tukey p = 0.450; Algeria vs. Tunisia: diff = +0.0779, Tukey p = 0.247). Multilingual rewriting (A4) substantially improves all three groups (Moroccan = 0.478, Algerian = 0.644, Tunisian = 0.553), elevating worst-group recall from 0.279 to 0.478 (+71.3% relative improvement).
  - Directly on the Language Gap g_i = Recall(FR, i) − Recall(AR, i), the uncorrected repeated-measures ANOVA reveals a statistically significant main effect of Architecture (F(6, 582) = 2.48, p = 0.0225). When adjusting for departure from sphericity (Greenhouse-Geisser ε_GG = 0.4153), this effect becomes a statistical trend (F(2.49, 241.70) = 2.48, p_GG = 0.0730). Sphericity is moderately violated across repeated configurations on the gap metric; thus, while the uncorrected model supports H5 at α = 0.05, the conservative GG correction highlights that architectural modulation of the gap is a directional trend requiring larger paired item sets to establish unconditional significance. Crucially, the interaction Architecture × Dialect is strictly non-significant under both models (uncorrected F(12, 582) = 0.25, p = 0.9955; GG-corrected F(4.98, 241.70) = 0.25, p_GG = 0.9380), demonstrating that architectural gap modulation behaves uniformly across Moroccan, Algerian, and Tunisian Darija without detectable treatment heterogeneity.


# 8. Limitations and Threats to Validity

- **Internal validity.** The configurations differ in the number of LLM calls. Cost is reported, but a configuration with more calls may gain for reasons unrelated to its design. The ablations and the cost table are the main safeguards.
- **Construct validity.** Recall and MRR measure retrieval against human judgements, not learning outcomes. The study does not measure whether learners learn more from any configuration.
- **Linguistic validity.** Digit mappings are heuristics, and the dialect labels are assigned by the writers' own variety. Mixed-language queries may be ambiguous.
- **Dataset representativeness.** Wikipedia and Wikiversity are not curricula. Results may not transfer to a specific national syllabus. The pilot data is Algerian and conversational.
- **Query construction.** Writers are briefed rather than given sentences, which limits lexical overlap, but it does not remove it. Overlap will be measured and reported.
- **Annotator effects.** Relevance and faithfulness judgements depend on annotator background. We report agreement and annotator profiles.
- **Model dependency.** Results depend on the chosen generator and embedder, which may be updated or retired by their providers. Versions will be recorded.
- **Automatic judges.** Secondary metrics may favour the judge model's own outputs and are reported with that caveat.
- **Pooling.** Relevance judgements are on a pool built from the configurations. Passages that no configuration retrieved are not judged. We report judged coverage.
- **Generalization.** The study does not establish that the results hold in a live classroom, with learners who are not represented in the query set.

# 9. Conclusion

This study provides a controlled, equity-focused experimental evaluation of Retrieval-Augmented Generation architectures for educational queries formulated in Arabizi. Across 300 queries evaluated on an aligned bilingual Wikipedia corpus (120 passages), our findings establish that heuristic surface normalization (A3) yields no measurable advantage over standard hybrid retrieval, whereas multilingual query rewriting (A4) maximizes absolute retrieval coverage across both languages (Arabizi Recall@5 = 0.557, French = 0.635). Corrective RAG (A5) achieves the narrowest observed language disparity (Δ_rec = +0.030, representing a 37% relative reduction over baseline A2), though this gap reduction remains descriptive and does not achieve statistical significance after multiple-comparison correction. In answer generation, higher retrieval recall statistically compresses the French–Arabizi faithfulness gap (p = 0.0485). Formal equivalence testing (TOST) demonstrates that recursive graph pipelines (A7) achieve practical equivalence with single-hop expansion (AB5b) on single-hop queries (p_TOST < 0.001 within the predefined margin ε = ±0.05), confirming that query-side reformulation is the primary driver of cross-lingual retrieval equity on this benchmark. These empirical findings and open-source assets offer concrete guidance for designing inclusive tutoring systems in linguistically diverse regions.


# Ethics statement

This study complies with all applicable academic research ethics standards. All benchmark queries and evaluation annotations were contributed voluntarily by adult native speakers who provided informed consent regarding the public academic release of their anonymized contributions. No personally identifiable student information or private user communications were collected. All background texts were retrieved from Wikipedia under the Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0), and source attributions are maintained in `docs/corpus_metadata.md`. All automated LLM prompts comply with the terms of service of the underlying open-weights model provider.

# Preregistration and Protocol Archival

The study follows a formal evaluation protocol structured under the AsPredicted template, archived in `docs/preregistration_osf.md` (and deposited under registration identifier `osf.io/8x9km`). In the interest of full scientific transparency, we clarify that this document represents a formalized public protocol documenting our hypotheses (H1–H5), analysis plan, and predefined decision rules (including equivalence margins of ±0.05 for TOST), rather than an independently time-stamped prospective preregistration established prior to initial exploratory data collection.


# Data and code availability

The full experimental codebase, benchmark query dataset (300 items), segmented bilingual corpus (120 passages), double-blind human annotation sample (320 items), and evaluation pool judgments (5,856 pairs) are made publicly available under the MIT License (code) and CC BY-SA 4.0 (data) at the following GitHub repository: [https://github.com/ASSIAbouamir/Arabizi-Retrieval-for-Inclusive-Learning-Support](https://github.com/ASSIAbouamir/Arabizi-Retrieval-for-Inclusive-Learning-Support). The NArabizi Treebank is used under its original ACL research terms.

# Acknowledgements

We thank the peer reviewers for their rigorous methodological critiques and detailed feedback on the pre-registration and pooling framework. We express our sincere gratitude to the six native speaker contributors and annotators from Morocco, Algeria, and Tunisia whose dedicated work made this cross-dialectal evaluation possible.

# Appendix A. Prompt templates

The templates below are those used in the released code. Placeholders in braces are filled per query. The answer template is used by A1 to A7; A0 uses the no-retrieval template.

**No-retrieval template (A0).** `Question : {query}\nRéponse :`

**Answer template (A1 to A7).** "Réponds à la question en utilisant uniquement les passages. Cite les numéros des passages. Si l'information manque, dis-le." followed by the numbered passages `[i] {passage}`, then `Question : {query}` and `Réponse :`.

**Rewriting template (A4, A5, A7; V3 and V4 in Section 3.2).** "Réécris la question suivante (écrite en arabizi) en trois formes : français, arabe standard, darija. Une forme par ligne, sans commentaire." followed by `Question : {query}`. The output is split into lines, and the first three non-empty lines are kept, together with the original query.

**Sufficiency template (A5, A7).** "Les passages suivants permettent-ils de répondre à la question ? Réponds OUI ou NON." followed by `Question : {query}` and the concatenated passages. The answer is read as sufficient if it starts with OUI, after trimming and upper-casing.

Model, decoding and version fields are listed in Table 1b. Prompts for any further variant (V3, V4, graded relevance judges) are to be added before the main experiments.

# Appendix B. Annotation scales and rules

**Faithfulness (answer against cited passages).**
- **2**: every factual claim in the answer is supported by the passages it cites.
- **1**: the main claim is supported, but at least one secondary claim is unsupported, or a citation points to the wrong passage.
- **0**: the main claim is unsupported, contradicted by the passages, or the answer cites no passage for a factual claim.

**Relevance (answer against the learner's question and level).**
- **2**: answers the question directly, at the stated level of the learner (beginner or intermediate).
- **1**: answers part of the question, or answers it at the wrong level (for example, too technical for a beginner), or gives correct but off-target context.
- **0**: does not answer the question, answers a different question, or is unusable.

**Rules for special cases.**
- *Correct but incomplete answer*: relevance 1 if the missing part is the main point of the question; relevance 2 if the missing part is a secondary detail.
- *Refusal when the passages lack the answer*: faithfulness 2 if the passages indeed lack the information and the refusal says so; relevance 1, because the learner still gets no answer.
- *Refusal when the passages contain the answer*: faithfulness 0 and relevance 0.
- *Mixed language answers*: judged on content, not on the language of the answer. The answer language is recorded separately.

**Disagreement.** Both annotators rate every answer. If their ratings differ by one level, the item is kept with the mean, and disagreements of two levels are sent to a third annotator, whose rating replaces the discrepant one. Agreement is reported as quadratic-weighted kappa before resolution.

**Worked Annotation Examples across Scales (Annex B Guidelines):**

*Example 1: Faithfulness Scale (Answer vs. Cited Passages)*
* **Query (Arabizi):** `3lach lhawa kaydghet w kaykhelli lbarometr ytbeddel?` [Topic: `pression_atm`]
* **Passage [1]:** *"La pression atmosphérique est la force exercée par l'air... Au niveau de la mer, elle vaut environ 1013 hPa. Elle se mesure avec un baromètre..."*
  * *Grade 2 (Fully Faithful):* "L'air possède un poids qui exerce une force sur la Terre appelée pression atmosphérique, valant environ 1013 hPa au niveau de la mer et mesurée par le baromètre [1]." $\to$ All claims are strictly backed by passage [1].
  * *Grade 1 (Partially Faithful):* "L'air exerce une pression mesurée par un baromètre [1], inventé par Evangelista Torricelli en 1643." $\to$ The main claim is supported by [1], but the historical claim regarding Torricelli is absent from the cited passage.
  * *Grade 0 (Unfaithful / Hallucinated):* "Le baromètre monte car la gravité terrestre s'inverse avec la chaleur du soleil." $\to$ Factually unsupported and contradicted by the scientific evidence in the retrieved text.

*Example 2: Relevance Scale (Answer vs. Learner Question & Target Need)*
* **Query (Mixed):** `kifach nebatat kaydiro la photosynthèse b do dyal chems?` [Topic: `photosynthese`, Level: Débutant]
  * *Grade 2 (Direct & Appropriate):* "La photosynthèse permet aux plantes vertes de fabriquer leur matière organique et de l'oxygène en captant la lumière du soleil grâce à la chlorophylle, en combinant l'eau et le dioxyde de carbone." $\to$ Direct, complete, matches beginner educational level.
  * *Grade 1 (Partial / Off-target context):* "Les plantes ont des feuilles vertes qui contiennent des cellules végétales et des vacuoles assurant la turgescence." $\to$ Scientifically accurate biology context, but fails to directly explain the mechanism of photosynthesis requested.
  * *Grade 0 (Irrelevant / Unusable):* "Le système métrique a été adopté durant la Révolution française pour standardiser les mesures de masse et de longueur." $\to$ Completely unrelated domain; does not answer the question.

*Example 3: Graded Relevance Scale for Retrieval Pooling (0–2)*
* **Topic:** `pythagore` (*Théorème de Pythagore*)
  * *Grade 2 (Target Answer):* Passage `fr::pythagore::p1` detailing $a^2 + b^2 = c^2$ in right-angled triangles.
  * *Grade 1 (Foundational / Related Context):* Passage `fr::thales::p1` (*Théorème de Thalès*) from the same geometry domain covering proportional ratios in intersecting lines.
  * *Grade 0 (Irrelevant Distractor):* Passage `fr::penicilline_fleming::p1` discussing Alexander Fleming and antibiotic mold cultures.

# References

Bies, A., Song, Z., Maamouri, M., Grimes, S., Lee, H., Wright, J., Strassel, S., Habash, N., Eskander, R., and Rambow, O. (2014). Transliteration of Arabizi into Arabic Orthography: Developing a Parallel Annotated Arabizi-Arabic Script SMS/Chat Corpus. *Proceedings of the EMNLP 2014 Workshop on Arabic Natural Language Processing (ANLP)*, pp. 93–103.

Bouamor, H., Habash, N., Salameh, M., Zaghouani, W., Rambow, O., Abdulrahim, D., Obeid, O., Khalifa, S., Eryani, F., Erdmann, A., and Oflazer, K. (2018). The MADAR Arabic Dialect Corpus and Lexicon. *Proceedings of LREC 2018*, pp. 3387–3396.

Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D., and Liu, Z. (2024). BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation. arXiv:2402.03216.

Cormack, G. V., Clarke, C. L. A., and Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet and individual rank learning methods. *Proceedings of SIGIR 2009*, pp. 758–759. doi:10.1145/1571941.1572114.

Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., Metropolitansky, D., Ness, R. O., and Larson, J. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. arXiv:2404.16130.

Ekstrand, M. D., Das, A., Burke, R., and Diaz, F. (2022). Fairness in Information Access Systems. *Foundations and Trends in Information Retrieval*, 16(1–2), 1–177. doi:10.1561/1500000079.

Es, S., James, J., Espinosa-Anke, L., and Schockaert, S. (2024). RAGAs: Automated Evaluation of Retrieval Augmented Generation. *Proceedings of EACL 2024: System Demonstrations*. arXiv:2309.15217.

Eskander, R., Al-Badrashiny, M., Habash, N., and Rambow, O. (2014). Foreign Words and the Automatic Processing of Arabic Social Media Text Written in Roman Script. *Proceedings of the EMNLP 2014 Workshop on Arabic Natural Language Processing (ANLP)*, pp. 1–12.

Galuščáková, P., Oard, D. W., and Nair, S. (2021). Cross-language Information Retrieval. arXiv:2111.05988.

Goworek, R., Macmillan-Scott, O., and Özyiğit, E. B. (2025). What Drives Cross-Lingual Ranking? Retrieval Approaches with Multilingual Language Models. arXiv:2511.19324.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., and Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. arXiv:2005.11401; *Advances in Neural Information Processing Systems 33* (NeurIPS 2020).

Ma, X., Gong, Y., He, P., Zhao, H., and Duan, N. (2023). Query Rewriting in Retrieval-Augmented Large Language Models. *Proceedings of EMNLP 2023*. arXiv:2305.14283.

May, J., Benjira, Y., and Echihabi, A. (2014). An Arabizi-English Social Media Statistical Machine Translation System. *Proceedings of AMTA 2014*.

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., et al. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*, 372:n71.

Riabi, A., Mahamdi, M., and Seddah, D. (2023). Enriching the NArabizi Treebank: A Multifaceted Approach to Supporting an Under-Resourced Language. arXiv:2306.14866.

Robertson, S., and Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. *Foundations and Trends in Information Retrieval*, 3(4), 333–389. doi:10.1561/1500000019.

Seddah, D., Essaidi, F., Fethi, A., Futeral, M., Muller, B., Ortiz Suárez, P. J., Sagot, B., and Srivastava, A. (2020). Building a User-Generated Content North-African Arabizi Treebank: Tackling Hell. *Proceedings of ACL 2020*, pp. 1139–1150.

Singh, A., Ehtesham, A., Kumar, S., Talaei Khoei, T., and Vasilakos, A. V. (2025). Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. arXiv:2501.09136.

Yan, S.-Q., Gu, J.-C., Zhu, Y., and Ling, Z.-H. (2024). Corrective Retrieval Augmented Generation. arXiv:2401.15884.

<!-- Notes de vérification : vérifiés en ligne : Seddah 2020, Riabi 2023, Bouamor 2018, Chen 2024, Es 2024, Page 2021, Ekstrand 2022, Galuščáková 2021, Goworek 2025, May 2014, Eskander 2014 (titre et pages), Bies 2014 (titre). Non vérifiés en ligne mais cités de mémoire : Lewis 2020, Cormack 2009, Robertson & Zaragoza 2009, Edge 2024, Yan 2024. Les auteurs de Bies 2014 et Eskander 2014 sont à confirmer. -->
