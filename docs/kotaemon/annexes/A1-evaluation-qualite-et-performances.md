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

## 3. Ce qui fait réussir ou échouer

1. **Le lecteur de fichiers, pas le tri.** Le tri `rerank` ne change pas le nombre de bonnes réponses (26 dans les deux cas) : les échecs ne viennent pas du classement des passages. Le gain vient de la relecture du contrat scanné par Docling : 1/4 puis 4/4 sur les questions du scan, et une question multi-documents de plus. [Vérifié]
2. **Le scan** : le lecteur intégré ne fait pas de lecture optique ; il ne garde du contrat scanné qu'une vignette par page, sans texte utile. Docling lit les deux pages en 47 à 56 secondes (`docling-2026-11-12.log`, `captures/05-documents/notes.log`), après un téléchargement de 536 Mo de modèles. [Vérifié]
3. **L'audio** : le MP3 n'est pas lu (« The FileType.UNK file type is not supported in partition. ») ; Q33 et Q34 échouent dans tous les réglages. [Vérifié]
4. **Le tableur** : Q24 (stock et seuil d'alerte) échoue avec 10 passages et réussit avec 3 : avec moins de passages, la ligne du tableur pèse davantage dans la réponse. [Vérifié]
5. **Les pièges** : 4/4 refus dans tous les réglages ; le modèle dit ne pas trouver l'information plutôt que d'inventer. [Vérifié]
6. **Les pages** : quand le passage cité vient d'un PDF, sa page est toujours la bonne (20/20 puis 25/25). Les autres formats n'ont pas de page. [Vérifié]
7. **Q30** (délai prévu dans le contrat et délai constaté dans le tableur) échoue toujours : la réponse trouve le délai du contrat, pas celui du tableur. [Vérifié]

## 4. Temps et mémoire

| Mesure | Valeur | Statut |
|---|---|---|
| Temps de réponse, médiane | 22 à 26 s, réflexion de `chat` comprise | [Vérifié] |
| Temps de réponse, 95 % des questions sous | 38 à 42 s | [Vérifié] |
| Indexation par l'interface : un PDF de 10 pages | 6,1 s | [Vérifié] (`captures/04-premiere-question/notes.log`) |
| Indexation par l'interface : huit documents d'un coup | 13,1 s | [Vérifié] (`captures/05-documents/notes.log`) |
| Relecture du scan par Docling (2 pages) | 47 à 56 s | [Vérifié] |
| Mémoire du conteneur pendant un banc | 1,5 à 1,9 Gio | [Vérifié] (`pic_ram_application_mo`) |
| Mémoire de la carte graphique en fin de banc (service central) | 8,6 à 9,2 Go sur 16 | [Vérifié] (`vram`) |

Les temps de réponse sont dominés par le modèle `chat`, qui réfléchit avant de répondre et que Kotaemon ne permet pas de faire répondre sans réflexion. La citation « highlight » ajoute un appel au modèle en parallèle. [Source] (`citation_qa.py:218-280`)

## 5. Limites de la mesure

- Un seul passage par réglage : la réponse peut varier d'un passage à l'autre. Lors des captures, la même question (usine de Saint-Nazaire, style « citation: inline ») a reçu une fois « (Sorry, I don't know) » sur trois essais (`captures/06-questions/05-citation-en-ligne-essai2-sorry.txt`). [Vérifié]
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
| latences très supérieures à 40 s | autre essai lourd en parallèle | un seul essai à la fois ; `free -m` |

## Sources

- Résultats bruts : `outils/resultats/kotaemon/banc-2026-11-12-*.json`, `.md`, `.log`.
- Adaptateur : `outils/kotaemon/banc.py`, `outils/kotaemon/pilote_conteneur.py`, `outils/kotaemon/serie_banc.sh`.
- Banc commun : `outils/communs/banc/commun.py`.
