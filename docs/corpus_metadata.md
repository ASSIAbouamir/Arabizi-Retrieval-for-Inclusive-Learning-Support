# Documentation du Corpus Éducatif Bilingue (FR-AR)

**Date de collecte :** 22 novembre 2026  
**Source :** Wikipédia (fr.wikipedia.org et ar.wikipedia.org via l'API MediaWiki)  
**Licence :** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)  
**Attribution :** Contributeurs de Wikipédia  
**Fichiers générés :**
* `data/corpus.jsonl` : 120 passages segmentés (60 FR, 60 AR)
* `data/wiki_raw_articles.jsonl` : 60 articles intégraux bruts (30 FR, 30 AR)
* `data/titles_fr.txt` : 30 titres canoniques en français

---

## 1. Paramètres de segmentation en passages

* **Budget par passage :** ~180 à 200 tokens (environ 800 à 1 000 caractères).
* **Recouvrement (overlap) :** 25 tokens entre passages successifs pour préserver la continuité discursive.
* **Volume par concept :** 4 passages au total par sujet scientifique :
  * 2 passages en français (`fr::<topic>::p1`, `fr::<topic>::p2`)
  * 2 passages en arabe (`ar::<topic>::p1`, `ar::<topic>::p2`)
* **Total corpus :** 30 concepts × 4 passages = **120 passages documentaires**.

---

## 2. Table des 30 paires d'articles Wikipédia collectées

| Domaine | Identifiant Topic | Titre Wikipédia Français | Titre Wikipédia Arabe | URL Source (FR) | URL Source (AR) |
|---|---|---|---|---|---|
| Physique | `pression_atm` | Pression atmosphérique | ضغط جوي | https://fr.wikipedia.org/wiki/Pression_atmosphérique | https://ar.wikipedia.org/wiki/ضغط_جوي |
| Physique | `electricite_courant` | Courant électrique | تيار كهربائي | https://fr.wikipedia.org/wiki/Courant_électrique | https://ar.wikipedia.org/wiki/تيار_كهربائي |
| Physique | `gravite_universelle` | Loi universelle de la gravitation | قانون الجذب العام لنيوتن | https://fr.wikipedia.org/wiki/Loi_universelle_de_la_gravitation | https://ar.wikipedia.org/wiki/قانون_الجذب_العام_لنيوتن |
| Physique | `vitesse_lumiere` | Vitesse de la lumière | سرعة الضوء | https://fr.wikipedia.org/wiki/Vitesse_de_la_lumière | https://ar.wikipedia.org/wiki/سرعة_الضوء |
| Physique | `energie_cinetique` | Énergie cinétique | طاقة حركية | https://fr.wikipedia.org/wiki/Énergie_cinétique | https://ar.wikipedia.org/wiki/طاقة_حركية |
| Physique | `ondes_sonores` | Onde sonore | صوت | https://fr.wikipedia.org/wiki/Onde_sonore | https://ar.wikipedia.org/wiki/صوت |
| Biologie | `photosynthese` | Photosynthèse | تركيب ضوئي | https://fr.wikipedia.org/wiki/Photosynthèse | https://ar.wikipedia.org/wiki/تركيب_ضوئي |
| Biologie | `cellule_biologie` | Cellule (biologie) | خلية | https://fr.wikipedia.org/wiki/Cellule_(biologie) | https://ar.wikipedia.org/wiki/خلية |
| Biologie | `adn_genetique` | Acide désoxyribonucléique | حمض نووي ريبوزي منقوص الأكسجين | https://fr.wikipedia.org/wiki/Acide_désoxyribonucléique | https://ar.wikipedia.org/wiki/حمض_نووي_ريبوزي_منقوص_الأكسجين |
| Biologie | `respiration_cellulaire` | Respiration cellulaire | تنفس خلوي | https://fr.wikipedia.org/wiki/Respiration_cellulaire | https://ar.wikipedia.org/wiki/تنفس_خلوي |
| Biologie | `systeme_circulatoire` | Système circulatoire | جهاز الدوران | https://fr.wikipedia.org/wiki/Système_circulatoire | https://ar.wikipedia.org/wiki/جهاز_الدوران |
| Biologie | `systeme_immunitaire` | Système immunitaire | جهاز مناعي | https://fr.wikipedia.org/wiki/Système_immunitaire | https://ar.wikipedia.org/wiki/جهاز_مناعي |
| Chimie | `tableau_periodique` | Tableau périodique des éléments | الجدول الدوري | https://fr.wikipedia.org/wiki/Tableau_périodique_des_éléments | https://ar.wikipedia.org/wiki/الجدول_الدوري |
| Chimie | `acides_bases_ph` | Potentiel hydrogène | أس هيدروجيني | https://fr.wikipedia.org/wiki/Potentiel_hydrogène | https://ar.wikipedia.org/wiki/أس_هيدروجيني |
| Chimie | `liaison_covalente` | Liaison covalente | رابطة تساهمية | https://fr.wikipedia.org/wiki/Liaison_covalente | https://ar.wikipedia.org/wiki/رابطة_تساهمية |
| Chimie | `etats_matiere` | État de la matière | حالة المادة | https://fr.wikipedia.org/wiki/État_de_la_matière | https://ar.wikipedia.org/wiki/حالة_المادة |
| Chimie | `oxydoreduction` | Réaction d'oxydoréduction | أكسدة واختزال | https://fr.wikipedia.org/wiki/Réaction_d%27oxydoréduction | https://ar.wikipedia.org/wiki/أكسدة_واختزال |
| Mathématiques | `pythagore` | Théorème de Pythagore | مبرهنة فيثاغورس | https://fr.wikipedia.org/wiki/Théorème_de_Pythagore | https://ar.wikipedia.org/wiki/مبرهنة_فيثاغورس |
| Mathématiques | `thales` | Théorème de Thalès | مبرهنة طاليس | https://fr.wikipedia.org/wiki/Théorème_de_Thalès | https://ar.wikipedia.org/wiki/مبرهنة_طاليس |
| Mathématiques | `equations_second_degre` | Équation du second degré | معادلة تربيعية | https://fr.wikipedia.org/wiki/Équation_du_second_degré | https://ar.wikipedia.org/wiki/معادلة_تربيعية |
| Mathématiques | `probabilites` | Probabilité | احتمال | https://fr.wikipedia.org/wiki/Probabilité | https://ar.wikipedia.org/wiki/احتمال |
| Mathématiques | `derivee_fonctions` | Dérivée | مشتق (رياضيات) | https://fr.wikipedia.org/wiki/Dérivée | https://ar.wikipedia.org/wiki/مشتق_(رياضيات) |
| Informatique | `algorithme_complexite` | Algorithme | خوارزمية | https://fr.wikipedia.org/wiki/Algorithme | https://ar.wikipedia.org/wiki/خوارزمية |
| Informatique | `processeur_memoire` | Microprocesseur | معالج صغري | https://fr.wikipedia.org/wiki/Microprocesseur | https://ar.wikipedia.org/wiki/معالج_صغري |
| Informatique | `reseau_ip` | Internet Protocol | بروتوكول الإنترنت | https://fr.wikipedia.org/wiki/Internet_Protocol | https://ar.wikipedia.org/wiki/بروتوكول_الإنترنت |
| Informatique | `base_de_donnees` | Base de données relationnelle | قاعدة بيانات علائقية | https://fr.wikipedia.org/wiki/Base_de_données_relationnelle | https://ar.wikipedia.org/wiki/قاعدة_بيانات_علائقية |
| Histoire des sciences | `revolution_copernic` | Héliocentrisme | مركزية الشمس | https://fr.wikipedia.org/wiki/Héliocentrisme | https://ar.wikipedia.org/wiki/مركزية_الشمس |
| Histoire des sciences | `revolution_industrielle` | Révolution industrielle | الثورة الصناعية | https://fr.wikipedia.org/wiki/Révolution_industrielle | https://ar.wikipedia.org/wiki/الثورة_الصناعية |
| Histoire des sciences | `penicilline_fleming` | Pénicilline | بنسلين | https://fr.wikipedia.org/wiki/Pénicilline | https://ar.wikipedia.org/wiki/بنسلين |
| Histoire des sciences | `revolution_francaise_sciences` | Système métrique | نظام متري | https://fr.wikipedia.org/wiki/Système_métrique | https://ar.wikipedia.org/wiki/نظام_متري |
