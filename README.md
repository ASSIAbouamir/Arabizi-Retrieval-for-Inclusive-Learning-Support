# Arabizi et RAG pour l'apprentissage inclusif

Projet de départ pour une étude comparative d'architectures RAG sur des requêtes en arabizi
(arabe dialectal écrit en lettres latines), par rapport à des requêtes en français.

## Contenu

| Fichier | Rôle |
|---|---|
| `src/arabizi/normalize.py` | Normalisation heuristique de l'arabizi (chiffres vers lettres, accents, lettres répétées) |
| `src/arabizi/bm25.py` | BM25 minimal, sans dépendance externe |
| `src/arabizi/metrics.py` | Recall@k, MRR, nDCG@k |
| `src/collect_wiki_pairs.py` | Collecte de paires d'articles FR-AR via les liens interlangues de Wikipédia (à lancer en local) |
| `experiments/run_baseline.py` | Compare brut vs normalisé, par type de requête |
| `data/queries_template.csv` | Modèle de jeu de requêtes à annoter (les lignes EXEMPLE ne sont pas des données de test) |
| `src/arabizi/architectures.py` | Architectures A0 à A7 derrière des interfaces (embedder, reranker, générateur) ; testées avec des composants factices |
| `experiments/pilot_narabizi/` | Statistiques du treebank NArabizi et pilote de récupération lexicale (test split) |
| `paper/paper.md` | Manuscrit de travail (résultats principaux encore à produire) |
| `tests/` | Tests de la normalisation, des métriques et de la plomberie des architectures |

## Mise en route

```bash
pip install -r requirements.txt
python -m pytest tests -q

# 1. Collecte du corpus (en local, accès réseau requis)
python src/collect_wiki_pairs.py --titles data/titles_fr.txt --out data/corpus.jsonl

# 2. Baseline
python experiments/run_baseline.py --corpus data/corpus.jsonl --queries data/queries.csv --k 5
```

## Ce qui est automatisé et ce qui ne l'est pas

Automatisé dans ce projet : la normalisation de base, le BM25, les métriques, la collecte des paires
Wikipédia et le calcul des résultats.

**À faire par toi (étapes qui demandent un jugement humain) :**
1. Rédiger ou collecter les requêtes en arabizi, avec des locuteurs de chaque variante dialectale.
2. Annoter les passages pertinents pour chaque requête (deux annotateurs, accord kappa).
3. Évaluer la fidélité et la pertinence des réponses générées sur un échantillon.
4. Vérifier les licences des sources avant publication.

## Limites de la normalisation actuelle

La normalisation est volontairement simple : elle sert de baseline. Elle ne gère pas les
variantes dialectales ni l'ambiguïté des chiffres (par exemple « 3 » peut représenter ع ou un
autre son selon les usages). Les architectures plus avancées (translittération par LLM,
réécriture multilingue) doivent être comparées à cette baseline.


## Pilote NArabizi

```bash
python3 experiments/pilot_narabizi/stats_narabizi.py <dossier Gold_annotation>
python3 experiments/pilot_narabizi/run_treebank_retrieval.py <test.conllu> src
```

Les architectures A1 et A4 à A7 ont besoin d'un embedder et d'un générateur réels ; les tests utilisent des factices qui ne mesurent pas la qualité.
