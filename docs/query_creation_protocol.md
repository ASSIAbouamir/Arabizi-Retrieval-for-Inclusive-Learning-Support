# Protocole de Création, Validation et Recouvrement Lexical des Requêtes

**Date :** Novembre 2026  
**Jeu de données :** `data/queries_benchmark.csv` (100 items d'information × 3 versions = 300 requêtes)  
**Distribution dialectale :** 34 items Maroc (102 requêtes), 33 items Algérie (99 requêtes), 33 items Tunisie (99 requêtes)

---

## 1. Profil et Recrutement des Rédacteurs Natifs

* **Recrutement :** Les rédacteurs ont été recrutés via les réseaux universitaires du Maghreb (facultés des sciences et d'ingénierie au Maroc, en Algérie et en Tunisie).
* **Critères d'éligibilité :**
  1. Locuteur natif de la variété maghrébine ciblée (Darija marocaine, algérienne ou tunisienne).
  2. Pratique quotidienne de l'arabizi sur les plateformes de messagerie (WhatsApp, Discord, réseaux sociaux).
  3. Bilinguisme actif français/arabe et familiarité avec le programme scolaire/universitaire scientifique.
* **Effectif :** 2 rédacteurs natifs par région (6 rédacteurs au total) travaillant sous la supervision d'un coordinateur de projet.

---

## 2. Consignes et Brief Donné aux Rédacteurs (*Writer Brief*)

Chaque rédacteur reçoit une liste de concepts scientifiques et de niveaux d'apprenant (débutant / intermédiaire). Pour chaque concept, le rédacteur doit formuler **trois versions authentiques** d'une question naturelle :

1. **Version A — Arabizi dialectal pur (`arabizi`) :**
   * *Consigne :* Écrire la question telle qu'elle serait posée spontanément à un pair ou un tuteur sur messagerie instantanée, en utilisant la graphie latine avec chiffres pour les phonèmes arabes spécifiques (3 = ع, 7 = ح, 5 = خ, 9 = ق, etc.).
   * *Règle :* Utiliser le vocabulaire, la syntaxe et les morphèmes grammaticaux authentiques du dialecte régional (ex. négation, marqueurs temporels, pronoms interrogatifs).
2. **Version B — Alternance codique / Mixte (`mixed` / `code-switching`) :**
   * *Consigne :* Formuler la question en mélangeant la structure dialectale arabizi avec les termes techniques ou scientifiques en français (pratique très courante chez les élèves maghrébins étudiant les matières scientifiques en français).
   * *Exemple :* `3lach l'air kaykhelli la pression tbeddel f le baromètre ?`
3. **Version C — Français standard scolaire (`fr`) :**
   * *Consigne :* Exprimer le même besoin d'information en français académique standard, tel que posé en milieu scolaire formel.
   * *Exemple :* `Comment l'air atmosphérique exerce-t-il une pression mesurable par le baromètre ?`

---

## 3. Protocole de Validation et Contrôle Qualité

Toutes les requêtes rédigées ont fait l'objet d'un contrôle en double aveugle par un coordinateur linguistique :
1. **Validation des marqueurs régionaux :**
   * *Maroc :* présence des marqueurs caractéristiques (*daba*, *kaydghet*, *chno*, *dyal*).
   * *Algérie :* présence des marqueurs caractéristiques (*derk*, *ydir*, *wech*, *ta3*).
   * *Tunisie :* présence des marqueurs caractéristiques (*tawwa*, *ya3mel*, *chnowa*, *mta3*).
2. **Cohérence thématique :** Vérification que les trois variantes ciblent exactement le même fait scientifique dans le corpus.
3. **Élimination des artefacts :** Suppression des abréviations SMS excessives ou ambiguës pouvant fausser l'évaluation.

---

## 4. Mesure Empirique du Recouvrement Lexical (Requêtes vs Passages Pertinents)

Le script `experiments/compute_lexical_overlap.py` a mesuré le taux de recouvrement des termes de la requête dans les passages cibles pertinents ($|Q \cap D| / |Q|$) ainsi que l'indice de Jaccard :

| Version de Requête | Taux de Recouvrement Lexical moyen (*Containment*) | Indice de Jaccard moyen | Interprétation RAG |
|---|---|---|---|
| **Arabizi pur** | **12,2 %** | **0,0114** | Échec majeur de la recherche lexicale pure (BM25 brut) en raison de l'incompatibilité graphico-lexicale. |
| **Alternance codique (Mixte)** | **22,3 %** | **0,0221** | Recouvrement intermédiaire grâce aux termes scientifiques français insérés. |
| **Français standard** | **28,4 %** | **0,0415** | Recouvrement direct optimal avec les documents éducatifs francophones. |

### Ventilation par groupe dialectal et version :

| Groupe Dialectal | Arabizi pur | Mixte / Code-Switching | Français standard |
|---|---|---|---|
| **Darija Marocaine** | 9,3 % | 24,0 % | 28,4 % |
| **Darija Tunisienne** | 10,2 % | 19,9 % | 28,0 % |
| **Darija Algérienne** | 17,0 % | 22,8 % | 28,7 % |

> [!IMPORTANT]
> L'écart abrupt de recouvrement lexical (12,2 % pour l'arabizi contre 28,4 % pour le français) démontre empiriquement la nécessité d'architectures RAG dotées d'embeddings denses multilingues (BGE-M3), de normalisation ou de réécriture/translittération, la recherche lexicale seule étant structurellement défavorisée.
