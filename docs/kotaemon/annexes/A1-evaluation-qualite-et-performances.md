# A1. Évaluation : qualité et performances

> **Objet** : mesurer la justesse, les citations et les temps de Kotaemon 0.12.0 sur un jeu de 38 questions, sans puis avec le modèle de tri `rerank`, avec le lecteur Docling et avec un réglage serré, et en tirer des préconisations.
> **Prérequis** : [chapitre 01](../manuel/01-decouvrir-kotaemon.md) ; corpus et questions de `corpus/` ; installation des chapitres 02 et 03.
> **Version décrite** : Kotaemon 0.12.0 (image `main-full`, révision `9ad3e4e`) ; service LLM central en profil `gpu` (`chat` Qwen3.5-4B, `embed` bge-m3, `rerank` bge-reranker-v2-m3) ; essais du 12 novembre 2026.
> **Statut des informations** : [Vérifié] résultat brut cité ; [Source] lu dans le code ; [Estimation] calcul expliqué ; [À tester] non mesuré.
> **Précautions** : un seul passage par réglage ; les réponses du modèle varient un peu d'un passage à l'autre (section 5).

## Sommaire

1. [Méthode](#1-méthode)
2. [Résultats](#2-résultats)
3. [Ce qui fait réussir ou échouer](#3-ce-qui-fait-réussir-ou-échouer)
4. [Temps et mémoire](#4-temps-et-mémoire)
5. [Limites de la mesure](#5-limites-de-la-mesure)
6. [Préconisations](#6-préconisations)
7. [Dépannage](#dépannage)
8. [Sources](#sources)

## 1. Méthode

- **Corpus** : 9 documents d'une entreprise fictive (`corpus/MANIFEST.json`) : rapport annuel PDF de 10 pages, contrat PDF scanné, procédure DOCX, présentation PPTX, classeur XLSX, page HTML, note Markdown, audit PDF en anglais, message vocal MP3. [Vérifié]
- **Questions** : 38 (`corpus/questions.json`), dont 34 avec réponse (faits simples, tableaux, scan, anglais, multi-documents, audio) et 4 pièges sans réponse dans le corpus. [Vérifié]
- **Adaptateur** : Kotaemon n'a pas d'API REST. Le banc lance un pilote dans le conteneur (`outils/kotaemon/pilote_conteneur.py`, appelé par `outils/kotaemon/banc.py`) qui charge les pipelines de Kotaemon sans interface, lit les réglages enregistrés dans l'interface par le compte `admin` et pose chaque question à « File Collection » avec « Search All », sans historique. C'est le même chemin que le bouton d'envoi du chat, sans le navigateur. [Vérifié] Limite : les réglages de « Chat settings » (session du navigateur) ne s'appliquent pas ; le banc utilise ceux de « Settings » (langue French, méthode `simple`, citations « highlight », carte mentale désactivée).
- **Notation** : exactitude par mots-clés attendus (`outils/communs/banc/commun.py`) ; refus correct sur les pièges ; jugement complémentaire par le modèle `chat`, réflexion coupée (« juge LLM ») ; document et page cités relevés dans le panneau d'information. [Vérifié]
- **Mesures** : latence de bout en bout, mémoire du conteneur `rag-kotaemon` (`docker stats`), mémoire de la carte graphique en fin de banc. `free -m` et `outils/communs/llm_central_sante.sh --essai` relevés en tête de chaque journal `banc-*.log`. [Vérifié]

## 2. Résultats

| Réglage | Exactes (34) | Refus pièges (4) | Juge LLM (38) | Bon document cité | Bonne page (pages exposées) | p50 (s) | p95 (s) | Fichier |
|---|---|---|---|---|---|---|---|---|
| lecteur intégré, 10 passages, sans tri | 26 | 4 | 32 | 27 | 20/20 | 25,8 | 38,2 | `banc-2026-11-12-defaut-sans-rerank.json` |
| lecteur intégré, 10 passages, tri `rerank` | 26 | 4 | 31 | 28 | 20/20 | 24,0 | 41,9 | `banc-2026-11-12-rerank.json` |
| scan relu par Docling, 10 passages, tri `rerank` | 30 | 4 | 34 | 32 | 25/25 | 23,4 | 41,3 | `banc-2026-11-12-docling-rerank.json` |
| scan relu par Docling, 3 passages, tri `rerank` | 31 | 4 | 34 | 32 | 25/25 | 22,0 | 38,7 | `banc-2026-11-12-docling-rerank-serre-top3.json` |

[Vérifié] Les fichiers sont dans `outils/resultats/kotaemon/` (avec leur version `.md` et le journal `.log`). Un essai partiel (6 questions sur le scan et le multi-documents, juste après la relecture Docling) donne 5/6 : `banc-2026-11-12-docling-scan-rerank.json`.

Par type de question (meilleur réglage, 3 passages) : faits simples 13/13, tableaux 10/10, scan 4/4, anglais 2/2, multi-documents 2/3, audio 0/2, pièges 4/4. [Vérifié]

**Correction manuelle** : dans les deux premiers bancs, Q17 (plafond des pénalités, attendu « 8 ») est comptée juste alors que la réponse refuse ; le chiffre « 8 » vient de « Page 8 » dans le texte. Score réel : 25/34 pour ces deux bancs. [Vérifié] (réponse de Q17 dans `banc-2026-11-12-defaut-sans-rerank.json`)

### 2.1 Docling déporté (13 novembre 2026)

Même réglage que le meilleur banc (3 passages, tri `rerank`), mais les PDF sont lus par un serveur Docling séparé (`docling-serve` 1.38.2, version processeur, conteneur partagé `rag-docling-serve` sur le réseau `llm-net`), branché par le lecteur ajouté décrit en annexe [A3](A3-automatiser-par-la-bibliotheque.md). Tous les fichiers ont été réindexés. Commande [Testée] :

```bash
outils/kotaemon/serie_banc.sh docling-deporte-rerank-serre-top3 --top-k 3 --reindexer --docling-deporte
```

| Lecture des PDF | Exactes | Refus pièges | Bon document cité | Bonne page | p50 (s) | p95 (s) | Indexation | Pic RAM application |
|---|---|---|---|---|---|---|---|---|
| Docling intégré, scan seul relu (meilleur banc ci-dessus) | 31 | 4 | 32 | 25/25 | 22,0 | 38,7 | non mesurée | 1 710 Mo |
| Docling déporté, les trois PDF relus | 29 | 4 | 32 | 24/25 | 18,4 | 27,3 | 28 s | 4 933 Mo, dont 2 524 Mo pour Docling |

[Vérifié] (`outils/resultats/kotaemon/banc-2026-11-13-docling-deporte-rerank-serre-top3.json` et `.log`)

Lecture :

1. Le scan est lu (4/4) : le Docling déporté remplace le Docling intégré pour la lecture optique. Le contrat scanné est relu en 7,5 s contre 47 à 56 s avec le Docling intégré.
2. Les deux bancs ne diffèrent pas seulement par l'endroit où tourne Docling : le lecteur ajouté s'applique à tous les PDF, alors que le meilleur banc n'avait relu que le scan. Le rapport annuel est donc découpé autrement, et deux questions sur ses tableaux échouent : Q13 (résultat net, « je ne connais pas ») et Q24 (réponse vide après 97 s). L'écart de 31 à 29 vient de là, pas du déport.
3. Réponses plus rapides (médiane 18,4 s contre 22,0 s), mémoire de l'ensemble plus lourde si Docling ne sert qu'à Kotaemon (2,5 Gio de plus), plus légère s'il est déjà partagé avec une autre application.
4. L'audio reste non lu (0/2), comme dans tous les bancs Kotaemon.

Après le banc, Kotaemon a été remis dans sa configuration d'origine (`outils/kotaemon/compose.sh up -d --force-recreate kotaemon`), puis arrêté ; la collection garde les PDF lus par le Docling déporté.

## 3. Ce qui fait réussir ou échouer

1. **Le lecteur de fichiers, pas le tri.** Le tri `rerank` ne change pas le nombre de bonnes réponses (26 dans les deux cas) : les échecs ne viennent pas du classement des passages. Le gain vient de la relecture du contrat scanné par Docling : 0/4 réellement (1/4 au comptage automatique, avec le faux positif Q17) puis 4/4 sur les questions du scan, et une question multi-documents de plus. [Vérifié]
2. **Le scan** : le lecteur intégré ne fait pas de lecture optique ; il ne garde du contrat scanné qu'une vignette par page, sans texte utile. Docling lit les deux pages en 47 à 56 secondes (`docling-2026-11-12.log`, `captures/05-documents/notes.log`), après le téléchargement de ses modèles (environ 1,1 Go sur disque avec leur cache, `fin-de-mission-2026-11-13.log`). [Vérifié]
3. **L'audio** : le MP3 n'est pas lu (« The FileType.UNK file type is not supported in partition. ») ; Q33 et Q34 échouent dans tous les réglages. [Vérifié]
4. **Le tableur** : Q24 (stock et seuil d'alerte) échoue avec 10 passages (« impossible de déterminer » sans Docling ; réponse vide après 110 s dans `banc-2026-11-12-docling-rerank.json`) et réussit avec 3 passages. [Vérifié] Explication possible : avec moins de passages, la ligne du tableur pèse davantage. [Estimation]
5. **Les pièges** : 4/4 refus dans tous les réglages ; le modèle dit ne pas trouver l'information plutôt que d'inventer. [Vérifié]
6. **Les pages** : quand le passage cité vient d'un PDF, sa page est toujours la bonne (20/20 puis 25/25). Les autres formats n'ont pas de page. [Vérifié]
7. **Q30** (délai prévu dans le contrat et délai constaté dans le tableur) échoue toujours : avec Docling, la réponse trouve le délai du contrat mais pas celui du tableur ; sans Docling, elle ne trouve aucun délai. [Vérifié]

## 4. Temps et mémoire

| Mesure | Valeur | Statut |
|---|---|---|
| Temps de réponse, médiane | 22 à 26 s, réflexion de `chat` comprise | [Vérifié] |
| Temps de réponse, 95 % des questions sous | 38 à 42 s ; pointes isolées de 70 à 110 s | [Vérifié] |
| Indexation par l'interface : un PDF de 10 pages | 6,1 s | [Vérifié] (`captures/04-premiere-question/notes.log`) |
| Indexation par l'interface : huit fichiers déposés d'un coup (sept indexés, le huitième déjà présent) | 13,1 s | [Vérifié] (`captures/05-documents/notes.log`) |
| Relecture du scan par Docling (2 pages) | 47 à 56 s | [Vérifié] |
| Mémoire du conteneur pendant un banc | 1,5 à 1,9 Gio | [Vérifié] (`pic_ram_application_mo`) |
| Mémoire de la carte graphique en fin de banc (service central) | 8,6 à 9,2 Go sur 16 | [Vérifié] (`vram`) |

Les temps de réponse sont dominés par le modèle `chat`, qui réfléchit avant de répondre et que Kotaemon ne permet pas de faire répondre sans réflexion. La citation « highlight » ajoute un appel au modèle en parallèle. [Source] (`citation_qa.py:218-280`)

## 5. Limites de la mesure

- Un seul passage par réglage : la réponse peut varier d'un passage à l'autre. Lors des captures, la même question (usine de Saint-Nazaire, style « citation: inline ») a reçu « (Sorry, I don't know) » 5 fois sur 7 essais (`captures/06-questions/notes.log`, lignes « réponse inline ») ; le style « citation: highlight », celui du banc, a répondu juste à chaque essai de capture. [Vérifié]
- Le banc ne passe pas par le navigateur : la langue de session (anglais par défaut dans le chat) n'intervient pas ; dans l'interface, il faut choisir « French » à chaque visite (chapitre 04). [Vérifié]
- Le juge LLM est indulgent : il a validé Q15 et Q16 (« le document ne donne pas le prix ») dans le premier banc. Les chiffres « Exactes » font foi. [Vérifié]
- La notation par le modèle (« Use LLM relevant scoring ») n'a pas été passée au banc : avec 10 passages, elle bloque les réponses (erreur 429 du service central, `incident-2026-11-12-429-score-llm.log`) ; avec 4 passages, ses notes restent à 0 et l'alerte de pertinence ne s'affiche pas (`essai-2026-11-12-alerte-pertinence.txt`). [Vérifié]
- Un second modèle de réponse (`gemma-4-e4b`, exposé par le service central) n'a pas été passé au banc. [À tester]

## 6. Préconisations

1. Déclarer les trois modèles du service central, dont `llm-service-rerank` comme tri par défaut (chapitre 03) : sans lui, le tri prévu (« cohere ») est ignoré sans message. Le tri ne change pas le score sur ce corpus, mais c'est le seul tri utilisable. [Vérifié]
2. Utiliser Docling pour les PDF scannés, le lecteur intégré pour les PDF de texte (vignettes et rapidité). [Vérifié]
3. Passer à 3 à 5 passages (« Number of document chunks to retrieve ») : même qualité ou mieux, réponses un peu plus rapides. [Vérifié] (3 passages : 31/34)
4. Laisser « Use LLM relevant scoring » décoché avec ce service de modèles. [Vérifié]
5. Convertir l'audio en texte avant de l'ajouter (Kotaemon ne transcrit pas). [Vérifié] pour le refus ; transcription non essayée par Kotaemon.

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `banc.py` : « pilote arrêté » | le conteneur ne tourne pas | `outils/kotaemon/demarrer.sh`, puis relancer |
| un fichier du corpus « déjà indexé » sans passage | lecture précédente en échec | le pilote réindexe d'office les fichiers sans passage |
| latences de 70 à 110 s sur certaines questions | longue réflexion du modèle (pointes observées dans les bancs eux-mêmes) ; un autre essai en parallèle les aggrave [Estimation] | un seul essai à la fois ; `free -m` |

## Sources

- Résultats bruts : `outils/resultats/kotaemon/banc-2026-11-12-*.json`, `.md`, `.log`.
- Adaptateur : `outils/kotaemon/banc.py`, `outils/kotaemon/pilote_conteneur.py`, `outils/kotaemon/serie_banc.sh`.
- Banc commun : `outils/communs/banc/commun.py`.
