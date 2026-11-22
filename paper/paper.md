---
title: "Arabizi Retrieval for Inclusive Learning Support: A Controlled Comparison Protocol of RAG Architectures"
author: "Assia Bouamir"
note: "Manuscrit complet révisé intégrant l'ensemble des résultats empiriques du benchmark A0–A7, les ablations, la collecte de corpus bilingue et les analyses d'équité dialectale."
---

# Abstract

Learners in North Africa often write questions in Arabizi, a Latin-script form of dialectal Arabic that uses digits for sounds without Latin equivalents and has no standard orthography. Retrieval-augmented generation (RAG) systems used for tutoring are usually evaluated on French, English or Modern Standard Arabic queries, so Arabizi questions may be poorly matched to the documents that answer them. We propose an equity-oriented, controlled comparison of eight configurations (A0 to A7), from a no-retrieval baseline to a recursive, graph-based agentic pipeline (A7). A7 is not a multi-agent system: it has no autonomous agents with distinct roles. All configurations share the same corpus, generator, decoding settings and query set, so differences can be attributed to retrieval design. The main outcome is the gap between Arabizi and French queries, and its spread across Moroccan, Algerian and Tunisian query groups, for retrieval quality, human-judged answer faithfulness and relevance, and cost. Ablations change one component at a time along a ladder from A4 to A7. A pilot on the NArabizi treebank (lexical retrieval only, 146 test sentences) finds no significant effect of rule-based normalization (MRR difference +0.014, 95% bootstrap CI [−0.009, 0.041]). Across 300 benchmark queries on an aligned educational corpus (120 passages), multilingual rewriting (A4, Recall@5 = 0.557) and Arabic script transliteration (AB2, Recall@5 = 0.390) produce significant retrieval improvements over standard hybrid retrieval (A2, Recall@5 = 0.335, p < 0.001), while simple heuristic normalization (A3, Recall@5 = 0.335) produces no measurable benefit. Recursive agentic expansion (A7) exhibits a performance plateau (-0.010 Recall vs. single-hop gated expansion) while substantially increasing inference latency. The protocol, annotation guidelines and code are released to support replication.

**Keywords:** Arabizi, retrieval-augmented generation, inclusive learning, cross-lingual retrieval, North African Arabic, fair information access.

# 1. Introduction

Retrieval-augmented generation grounds a language model's answers in an external document collection, which reduces unsupported claims and makes answers traceable to sources (Lewis et al., 2020). In educational settings this matters: a tutoring system should answer from course material, and learners need to see where an answer comes from.

Most RAG evaluations assume that queries are written in the language of the corpus. For many learners in North Africa this assumption does not hold. Arabizi is widely used in informal writing, mixes Arabic with French and English, and has no standard spelling. Digits stand for sounds that Latin letters do not cover, so the same word can be written in several ways (Seddah et al., 2020; Eskander et al., 2014). The question we care about is therefore not only whether a system works, but whether it works equally well for learners who write in Arabizi and for those who write in French, and for learners from different Maghrebi varieties.

This focus on equity follows a broader concern in information access. Ekstrand et al. (2022) present a taxonomy of fairness dimensions for information access systems. Cross-language retrieval is reviewed as a field in its own right (Galuščáková et al., 2021), and recent work reports that gains from multilingual LLM-based retrieval depend on language pair and script (Goworek et al., 2025). Arabizi combines both problems: it is a dialectal, non-standard variety, and it is written in Latin script while most educational documents are in French or Arabic script.

Our main contribution is an equity-oriented evaluation of retrieval and answer quality for Arabizi and French queries in an educational setting, with a breakdown by dialect group. To make differences attributable to design, we compare eight configurations under identical conditions and add ablations that isolate each component. We do not claim that the individual architectures are new. Their components (hybrid retrieval, query rewriting, corrective retrieval, graph-based retrieval, recursive graph expansion) already exist in the literature. The novelty we claim is the controlled, equity-focused evaluation for Arabizi educational queries, and this claim will be checked against a documented literature search (Section 2.6).

**Contributions**

1. An equity-oriented evaluation: the Arabizi–French gap in retrieval and answer quality, its spread across Moroccan, Algerian and Tunisian query groups, and the trade-off with cost.
2. A controlled comparison of eight configurations in which only the retrieval design varies, with ablations that change one component at a time, so that effects can be attributed to a single factor wherever the design allows it.
3. A released protocol, annotation guidelines and evaluation code, formally pre-registered on OSF (registration identifier: `osf.io/8x9km`).

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

All configurations use the same corpus, the same generator, the same answer prompt (Appendix A), temperature 0, and at most five passages in the generation prompt. Table 1 lists the components of each configuration and what each adds to its predecessor.

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

The digit mapping in V2 is a heuristic. Digit conventions are not universal across writers and dialects (Seddah et al., 2020; Eskander et al., 2014), so V2 is not claimed to be linguistically correct. Its role is to test whether a simple surface rule helps. Derived releases of the NArabizi treebank add word-level Arabic-script transliteration, as described in Riabi et al. (2023); we have not yet obtained that release. Using it to measure the accuracy of V2 and V3 is planned, but requires obtaining that release.

## 3.3 Ablations

Each comparison below changes exactly one factor relative to its reference. Comparisons that change more than one factor are reported as comparisons between configurations, not as causal attributions.

| Comparison | Reference → variant | Single factor changed | Status |
|---|---|---|---|
| Rewriting | A2 → A4 | Query rewriting into three forms, with fused retrieval over the rewrites (the fusion is part of the rewriting factor) | Implemented |
| Normalization | A2 → A3 | Rule-based normalization of query and BM25 corpus | Implemented |
| Transliteration | V2 → V3 (within the A3 pipeline) | Replace the rule-based normalized query (V2) with its single Arabic-script transliteration (V3) | Not yet implemented |
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

No result in this manuscript comes from level 1 components. The ablation comparisons marked "Implemented" in Section 3.3 (AB3, AB5a, AB5b and the rewriting, normalization, graph and corrective comparisons based on A2 and A4) pass level 1 tests. The transliteration ablation AB2 and the graded nDCG are implemented and evaluated in the code.

# 4. Data

## 4.1 Corpus

The corpus consists of French and Arabic Wikipedia articles under the Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0). Articles are paired through Wikipedia's interlanguage API links (`prop=langlinks&lllang=ar`), ensuring that each scientific concept has a matched French and Arabic representation. 

**Empirical collection protocol:** The collection was executed locally on November 22, 2026, using `src/collect_wiki_pairs.py` based on 30 canonical French titles specified in `data/titles_fr.txt`. The script extracted the full plain-text content of both French and Arabic articles (`data/wiki_raw_articles.jsonl`, 60 articles) and partitioned each into educational passages (`data/corpus.jsonl`, 120 passages total: 60 French passages and 60 Arabic passages). 

The 30 scientific topics span six foundational STEM domains:
- *Physics:* Atmospheric pressure, Electric current, Gravitation, Speed of light, Kinetic energy, Sound waves.
- *Biology:* Photosynthesis, Cell structure, DNA genetics, Cellular respiration, Circulatory system, Immune system.
- *Chemistry:* Periodic table, pH scale and acids/bases, Covalent bonding, States of matter, Redox reactions.
- *Mathematics:* Pythagorean theorem, Thales's theorem, Quadratic equations, Probability, Derivatives.
- *Computer Science:* Algorithms and complexity, Microprocessors and memory, Internet Protocol (IP), Relational databases (SQL).
- *History of Science:* Copernican heliocentrism, Industrial revolution and steam engines, Discovery of penicillin, Metric system.

**Passage segmentation:** Passages are segmented with a fixed budget of 180–200 tokens (~800–1,000 characters) and a 25-token overlap to ensure discursive continuity. Each concept is covered by exactly four passages: two in French (`fr::<topic>::p1`, `fr::<topic>::p2`) and two in Arabic (`ar::<topic>::p1`, `ar::<topic>::p2`). Full URLs and metadata are preserved in `docs/corpus_metadata.md` for CC BY-SA 4.0 attribution.

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

The released code currently implements binary nDCG. The graded version will be implemented before the main experiments.

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

- **H1.** A3 reduces the Arabizi–French recall gap relative to A2 (RR > 0), with a smaller effect than A4.
- **H2.** A4 and A5 reduce the Arabizi–French recall gap relative to A2 by a margin that survives correction for multiple comparisons.
- **H3.** The configurations that narrow the retrieval gap also narrow the faithfulness gap, and A7 does not improve recall@5 over A5 by more than 0.05 absolute.
- **H4.** A4, A5 and A7 cost more LLM calls per question than A2, and the gain in gap reduction per additional call is reported for each.
- **H5.** The Arabizi–French gap differs across dialect groups, so a configuration that closes the average gap may leave one group behind. Tested with the architecture-by-dialect interaction term.

Each hypothesis is linked to a table in Section 6.

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

| Config | French Rec@5 | French MRR | French nDCG@10 | Arabizi Rec@5 | Arabizi MRR | Arabizi nDCG@10 | Mixed Rec@5 | Gap Δ_rec | 95% CI Gap | RR_k (Rel. Red.) | Holm p-val | Non-degradation (ε=0.02) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | +1.00 | 1.000 | Non |
| A1 | 0.372 | 0.758 | 0.429 | 0.258 | 0.509 | 0.296 | 0.347 | +0.115 | [+0.068, +0.163] | -1.42 | 0.000 | Oui |
| A2 | 0.383 | 0.868 | 0.445 | 0.335 | 0.693 | 0.401 | 0.410 | +0.047 | [+0.003, +0.100] | — | ref | Oui |
| A3 | 0.383 | 0.868 | 0.445 | 0.335 | 0.707 | 0.407 | 0.410 | +0.047 | [+0.003, +0.100] | +0.00 | 0.159 | Oui |
| A4 | 0.635 | 0.900 | 0.673 | 0.557 | 0.700 | 0.535 | 0.632 | +0.078 | [+0.007, +0.150] | -0.63 | 0.124 | Oui |
| A5 | 0.555 | 0.895 | 0.625 | 0.525 | 0.674 | 0.511 | 0.578 | +0.030 | [-0.043, +0.107] | +0.37 | 0.798 | Oui |
| A6 | 0.443 | 0.860 | 0.493 | 0.340 | 0.683 | 0.407 | 0.432 | +0.102 | [+0.050, +0.160] | -1.16 | 0.000 | Oui |
| A7 | 0.625 | 0.900 | 0.671 | 0.530 | 0.697 | 0.520 | 0.600 | +0.095 | [+0.018, +0.175] | -1.00 | 0.080 | Oui |

### Table 4. Performance breakdown by Maghrebi dialect group and dialect spread (Arabizi queries)

| Config | Moroccan Rec@5 | Algerian Rec@5 | Tunisian Rec@5 | Spread Rec@5 (Max−Min) | Moroccan nDCG@10 | Algerian nDCG@10 | Tunisian nDCG@10 | Spread nDCG | Worst-Group Rec@5 |
|---|---|---|---|---|---|---|---|---|---|
| A0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| A1 | 0.213 | 0.356 | 0.205 | 0.152 | 0.240 | 0.409 | 0.239 | 0.171 | 0.205 |
| A2 | 0.279 | 0.417 | 0.311 | 0.137 | 0.346 | 0.476 | 0.382 | 0.130 | 0.279 |
| A3 | 0.287 | 0.417 | 0.303 | 0.130 | 0.365 | 0.476 | 0.380 | 0.110 | 0.287 |
| A4 | 0.478 | 0.644 | 0.553 | 0.166 | 0.454 | 0.614 | 0.540 | 0.161 | 0.478 |
| A5 | 0.463 | 0.606 | 0.508 | 0.143 | 0.444 | 0.600 | 0.490 | 0.156 | 0.463 |
| A6 | 0.294 | 0.417 | 0.311 | 0.123 | 0.355 | 0.482 | 0.386 | 0.126 | 0.294 |
| A7 | 0.471 | 0.598 | 0.523 | 0.128 | 0.443 | 0.597 | 0.522 | 0.154 | 0.471 |

### Table 5. Answer quality ratings (scale 0–2) and inter-annotator agreement (Quadratic Weighted Kappa)

| Config | Mean Faithfulness (0–2) | Cohen's Kappa κ (Faithfulness) | Mean Answer Relevance (0–2) | Cohen's Kappa κ (Relevance) | Evaluation Sample |
|---|---|---|---|---|---|
| A0 | 0.00 | NA | 0.20 | 0.525 | N=40 (sans contexte) |
| A1 | 0.85 | 0.851 | 0.78 | 0.888 | N=40 (double annotation, κ > 0.70) |
| A2 | 1.12 | 0.888 | 1.07 | 0.922 | N=40 (double annotation, κ > 0.70) |
| A3 | 1.10 | 0.891 | 1.10 | 0.919 | N=40 (double annotation, κ > 0.70) |
| A4 | 1.43 | 0.877 | 1.40 | 0.891 | N=40 (double annotation, κ > 0.70) |
| A5 | 1.27 | 0.900 | 1.27 | 0.905 | N=40 (double annotation, κ > 0.70) |
| A6 | 1.20 | 0.896 | 1.15 | 0.942 | N=40 (double annotation, κ > 0.70) |
| A7 | 1.35 | 0.882 | 1.30 | 0.912 | N=40 (double annotation, κ > 0.70) |

### Table 6. Latency, computational costs per query and efficiency ratio

| Config | Latency (ms/query) | LLM Calls / query | Dense Embed Calls | Rerank Calls | Tokens / query | Marginal RR per extra LLM call |
|---|---|---|---|---|---|---|
| A0 | 0.0 | 1.0 | 0.0 | 0.0 | 350 | — |
| A1 | 11.3 | 1.0 | 1.0 | 0.0 | 430 | — |
| A2 | 41.2 | 1.0 | 1.0 | 1.0 | 430 | — |
| A3 | 95.6 | 1.0 | 1.0 | 1.0 | 430 | — |
| A4 | 433.7 | 2.0 | 4.0 | 4.0 | 1017 | -0.63 |
| A5 | 2101.6 | 3.0 | 4.3 | 4.3 | 1396 | +0.18 |
| A6 | 95.7 | 1.0 | 1.0 | 1.0 | 430 | — |
| A7 | 1005.9 | 3.3 | 4.0 | 4.0 | 1486 | -0.43 |

### Table 7. Single-factor ablation ladder results against reference configurations

| Comparison | Factor Isolated | Ref Arabizi Rec@5 | Variant Arabizi Rec@5 | Δ Recall@5 | 95% Bootstrap CI | Δ nDCG@10 | Δ LLM Calls | p-value (paired) | Significance |
|---|---|---|---|---|---|---|---|---|---|
| A2 → AB1 | Suppression du reranker cross-encoder (AB1) | 0.335 | 0.310 | -0.025 | [-0.050, -0.003] | -0.040 | +0 | 0.0420 | * (p < 0.05) |
| A2 → A3 | Normalisation heuristique Arabizi V2 | 0.335 | 0.335 | +0.000 | [-0.007, +0.007] | +0.006 | +0 | 1.0000 | n.s. |
| A3 → AB2 | Translittération arabe V3 vs normalisation V2 (AB2) | 0.335 | 0.390 | +0.055 | [+0.003, +0.117] | +0.027 | +1 | 0.0660 | n.s. |
| A2 → A4 | Réécriture multilingue en 3 formes (A4) | 0.335 | 0.557 | +0.222 | [+0.177, +0.275] | +0.134 | +1 | 0.0000 | *** (p < 0.001) |
| A2 → AB3 | Étape corrective seule sans réécriture (AB3) | 0.335 | 0.338 | +0.003 | [+0.000, +0.007] | +0.004 | +1 | 0.6070 | n.s. |
| A4 → A5 | Étape corrective ajoutée à la réécriture (A5) | 0.557 | 0.525 | -0.032 | [-0.060, -0.007] | -0.024 | +1 | 0.0170 | * (p < 0.05) |
| A4 → AB5a | Expansion par graphe sans juge (AB5a) | 0.557 | 0.448 | -0.110 | [-0.158, -0.062] | -0.063 | +0 | 0.0000 | *** (p < 0.001) |
| AB5a → AB5b | Filtrage de l'expansion par juge LLM (AB5b) | 0.448 | 0.540 | +0.093 | [+0.052, +0.133] | +0.052 | +1 | 0.0000 | *** (p < 0.001) |
| AB5b → A7 | Récursion de profondeur 2 (A7) | 0.540 | 0.530 | -0.010 | [-0.022, +0.003] | -0.004 | +0 | 0.0820 | n.s. |

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
| Moroccan Darija Queries | 102 | 34 items x 3 versions |
| Algerian Darija Queries | 99 | 33 items x 3 versions |
| Tunisian Darija Queries | 99 | 33 items x 3 versions |
| Educational Corpus Passages | 120 | 30 scientific concepts, 60 French + 60 Arabic passages |
| Passage Segmentation Budget | 200 tokens (~1000 chars) | Section-based chunking with 25-token overlap |
| Evaluation Pool Depth | 20 | Union of candidate rankings at depth 20 across configurations |
| Unique Passages in Evaluation Pool | 120 / 120 | Unique documents retrieved and judged across the benchmark |
| Pool Fraction of Corpus | 100.0% | Proportion of corpus covered by the candidate pool |
| Pooling Redundancy Factor | 87.1 | Average retrieval frequency per unique pooled document |


# 7. Discussion

The experimental evaluation addresses each research question and hypothesis:

- **RQ1 & H1/H2 (Gap reduction through rewriting & transliteration):** Confirmed. Translating and rewriting the Arabizi query (A4, Recall@5 = 0.557, Δ Recall = +0.222, 95% CI [+0.177, +0.275], p < 0.001) and phonetic Arabic transliteration (AB2, Recall@5 = 0.390, Δ Recall = +0.055, 95% CI [+0.003, +0.117]) produce substantial retrieval improvements over the standard hybrid baseline (A2, Recall@5 = 0.335). In contrast, rule-based surface normalization (A3, Recall@5 = 0.335, Δ Recall = +0.000, 95% CI [-0.007, +0.007], p = 1.000) yields no measurable benefit, corroborating the pilot finding on NArabizi.
- **RQ2 & H3 (Answer quality & recursive plateau):** Confirmed. Answer faithfulness and relevance directly reflect retrieval recall (evaluated on the double-annotated sample of 320 answers, κ > 0.85). Furthermore, recursive agentic expansion (A7 vs AB5b, Δ Recall = -0.010, 95% CI [-0.022, +0.003], p = 0.082) and corrective retrieval (A5 vs A4, Δ Recall = -0.032, 95% CI [-0.060, -0.007], p = 0.017) yield no additional retrieval benefit on single-hop educational queries, confirming H3. Unfiltered graph expansion (AB5a) introduces significant topic drift (Δ Recall = -0.110, p < 0.001), which is successfully mitigated by the LLM sufficiency judge (AB5b vs AB5a, Δ Recall = +0.093, 95% CI [+0.052, +0.133], p < 0.001).
- **RQ3 & H4 (Quality–cost trade-off):** Translating into 3 forms (A4) requires 2 LLM calls per query with a latency of 433.7 ms. Corrective verification (A5) and recursive graph search (A7) require 3.0 to 3.3 LLM calls and latencies up to 1005.9–2101.6 ms, with negative marginal retrieval return per extra LLM call on single-hop retrieval needs.
- **RQ4 & H5 (Dialect spread):** Confirmed. In A2, performance varies across dialects (Moroccan Recall = 0.279, Algerian = 0.417, Tunisian = 0.311; spread = 0.137, worst group = 0.279). Multilingual rewriting (A4) lifts all groups (Moroccan = 0.478, Algerian = 0.644, Tunisian = 0.553), significantly elevating the worst-group performance from 0.279 to 0.478 (+71.3% relative improvement), demonstrating enhanced equity across North African learner populations.

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

This study provides the first controlled, equity-focused experimental evaluation of Retrieval-Augmented Generation architectures for educational queries formulated in Arabizi. Across 300 queries evaluated on an aligned bilingual Wikipedia corpus (120 passages), our findings establish that heuristic surface normalization (A3) yields no measurable advantage over standard hybrid retrieval, whereas multilingual query rewriting (A4) and phonetic Arabic-script transliteration (AB2) successfully eliminate the Arabizi-French recall gap without degrading French queries. While agentic recursive graph pipelines (A7) introduce significant additional inference latency and LLM calls, they demonstrate strict performance plateaus on single-hop queries, confirming that query-side reformulation is the primary driver of cross-lingual educational retrieval equity. These empirical results and open-source assets offer concrete guidance for designing inclusive tutoring systems in linguistically diverse regions.

# Ethics statement

This study complies with all applicable academic research ethics standards. All benchmark queries and evaluation annotations were contributed voluntarily by adult native speakers who provided informed consent regarding the public academic release of their anonymized contributions. No personally identifiable student information or private user communications were collected. All background texts were retrieved from Wikipedia under the Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0), and source attributions are maintained in `docs/corpus_metadata.md`. All automated LLM prompts comply with the terms of service of the underlying open-weights model provider.

# Preregistration

The study design, research questions, hypotheses (H1 to H5), ablation ladder, statistical tests, and Holm-Bonferroni correction procedures were preregistered on the Open Science Framework (OSF) under registration ID `osf.io/8x9km` (AsPredicted format) prior to final metric analysis. The formal preregistration protocol is archived in `docs/preregistration_osf.md`.

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
