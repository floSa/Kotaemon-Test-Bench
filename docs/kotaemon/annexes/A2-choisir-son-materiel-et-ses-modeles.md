# A2. Choisir son matériel et ses modèles

> **Objet** : dire sur quelle machine faire tourner Kotaemon et son service de modèles, sans et avec carte graphique NVIDIA, quelle place prend chaque élément, combien de documents passent et combien de temps attendre.
> **Prérequis** : [chapitre 01](../manuel/01-decouvrir-kotaemon.md) ; annexe [A1](A1-evaluation-qualite-et-performances.md) pour les résultats du banc.
> **Version décrite** : Kotaemon 0.12.0 ; service LLM central (LiteLLM v1.109.0, llama-swap v272, llama.cpp build 12282, speaches 0.8.3) ; essais du 12 et 13 novembre 2026.
> **Statut des informations** : [Vérifié] mesuré sur la machine d'essai (profil B) ; [Source] repris des mesures de LLM-Service, fichier cité ; [Estimation] calcul expliqué ; [À tester] non mesuré.
> **Précautions** : le profil A (sans carte graphique) n'a pas été mesuré avec Kotaemon ; ses temps sont des estimations à partir des mesures du service central.

## Sommaire

1. [Ce qui consomme la mémoire et le disque](#1-ce-qui-consomme-la-mémoire-et-le-disque)
2. [Profil A : sans carte graphique](#2-profil-a--sans-carte-graphique)
3. [Profil B : avec carte graphique NVIDIA](#3-profil-b--avec-carte-graphique-nvidia)
4. [Budget de contexte et volume de documents](#4-budget-de-contexte-et-volume-de-documents)
5. [Modèles](#5-modèles)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Ce qui consomme la mémoire et le disque

| Élément | Mémoire ou disque | Statut |
|---|---|---|
| Kotaemon au repos | 0,5 à 0,9 Gio | [Vérifié] (`installation-2026-11-12.log`, `exploitation-2026-11-12.log`) |
| Kotaemon pendant un banc (10 passages, citations, tri) | 1,5 à 1,9 Gio | [Vérifié] (`banc-2026-11-12-*.json`, `pic_ram_application_mo`) |
| Docling (lecture optique d'un scan) | mémoire non mesurée séparément ; environ 1,1 Go de modèles et de cache sur disque | [Vérifié] pour le disque (`fin-de-mission-2026-11-13.log`) |
| Image de Kotaemon « full » | 12,7 Go sur disque | [Vérifié] (`installation-2026-11-12.log`) |
| Service central, profil `cpu` : LiteLLM, llama-swap, speaches | 0,59 + 3,6 + 0,13 Gio ≈ 4,3 Go | [Source] (`LLM-Service/mesures/cpu/memoire-vive-conteneurs.txt`) |
| Service central, profil `gpu` : mémoire vive | LiteLLM 0,8, llama-swap 4,4, speaches 0,2 à 1,5 Go | [Source] (`LLM-Service/README.md`, « Mesures ») |
| Service central, profil `gpu` : carte graphique | 7,0 Go pour `chat`, `embed` et `rerank` ; 8,6 à 9,2 Go relevés en fin de banc avec le bureau Windows | [Source] [Vérifié] |

Le volume de documents change peu la mémoire : vecteurs et textes sont sur disque (Chroma, LanceDB), et seuls quelques passages partent au modèle. [Source] (annexe A5)

## 2. Profil A : sans carte graphique

Machine type : PC portable Intel Core Ultra 7 255H, 15,3 Go dans WSL ; service en profil `cpu` (`demarrer.sh cpu`).

| Élément | Valeur | Statut |
|---|---|---|
| Processeur | 8 cœurs récents (AVX2) | [Estimation] (profil A du banc) |
| Mémoire vive | 16 Go : 4,3 Go service, 1 à 2 Gio Kotaemon, le reste pour Windows, WSL et Docker | [Estimation] (somme des lignes de la section 1) |
| Disque | 25 Go : image Kotaemon 12,7 Go, modèles du service environ 5 Go, Docling environ 1,1 Go, données | [Estimation] |
| Débit de `chat` | 14 jetons/s pour une requête, 31 jetons/s cumulés pour quatre (profil `cpu` mesuré sur le Ryzen 5 9600X) | [Source] (`LLM-Service/README.md`) ; sur le Core Ultra 7 255H : [Estimation] du même ordre |
| Temps de réponse attendu | environ 2 minutes en médiane, 3 à 4 minutes pour les plus longues | [Estimation] (rapport de débit 68 / 14 ≈ 4,9 appliqué à la médiane de 22 à 26 s et au p95 de 38 à 42 s du profil B) |
| Relecture d'un scan par Docling | plusieurs minutes par page | [Estimation] (Docling tourne déjà sur le processeur en profil B : 47 à 56 s pour 2 pages, sans charge du modèle ; un processeur portable est plus lent) |

| Profil A | Valeur |
|---|---|
| Profil du service | `cpu` (`llm-swap-cpu`) |
| Modèles | `chat` = Qwen3.5-4B Q4_K_M, `embed` = bge-m3 Q8_0, `rerank` = bge-reranker-v2-m3 ; `transcribe` non utilisé par Kotaemon |
| Contexte | 16 384 jetons |
| Mémoire service et application | 4,3 Go + 1 à 2 Gio [Estimation] |
| Réglages conseillés | 3 passages, tri `llm-service-rerank`, carte mentale décochée, « no citation » ou « citation: inline » pour éviter l'appel de plus |
| Résultats du banc | non mesurés sur ce profil ; la qualité ne dépend pas du matériel (mêmes modèles) [Estimation] |
| Temps d'attente | environ 2 minutes, jusqu'à 4 minutes [Estimation] |

## 3. Profil B : avec carte graphique NVIDIA

Machine d'essai : Ryzen 5 9600X, 32 Go dans WSL, RTX 4060 Ti 16 Go ; service en profil `gpu`. [Vérifié] (`outils/resultats/machine/diagnostic-2026-11-12.json`)

| Profil B | Valeur | Statut |
|---|---|---|
| Profil du service | `gpu` (`llm-swap`) | [Vérifié] |
| Modèles | mêmes noms que le profil A [Vérifié] (`/v1/models`) ; quantifications Q4_K_M et Q8_0 [Source] (README de LLM-Service) |
| Contexte | 16 384 jetons | [Source] (configuration et README de LLM-Service) |
| Carte graphique | 12 Go conseillés : 7,0 Go pour les trois modèles permanents [Source] plus le bureau Windows ; 8,6 à 9,2 Go mesurés sur la carte de 16 Go [Vérifié] ; une carte de 8 Go est trop juste [Estimation] |
| Mémoire vive | 16 Go : 5,4 Go pour le service au repos [Source] ; 7,7 Gio (7 920 Mo) mesurés pendant les bancs, transcription chargée [Vérifié] (`pic_ram_mo`) ; 1,5 à 1,9 Gio Kotaemon [Vérifié] |
| Débit de `chat` | 68 jetons/s pour une requête, 174 jetons/s cumulés pour quatre | [Source] |
| Réglages | modèles du service, Docling pour les scans, 3 ou 10 passages, tri `rerank` | [Vérifié] |
| Résultats du banc | 25 à 31 bonnes réponses sur 34, 4/4 refus | [Vérifié] (A1) |
| Temps d'attente | médiane 22 à 26 s, p95 38 à 42 s ; indexation de huit fichiers déposés (sept indexés) 13 s ; relecture Docling d'un scan de 2 pages 47 à 56 s | [Vérifié] |

## 4. Budget de contexte et volume de documents

Le modèle `chat` accepte 16 384 jetons par requête, question, passages, réflexion et réponse compris. Avec les réglages du chapitre 03 : [Estimation]

| Poste | Jetons |
|---|---|
| passages (« Max context length (LLM) ») | 8 000 au plus |
| consignes, question, historique (5 échanges) | environ 500 à 1 500 |
| réponse et réflexion (`max_tokens`) | 6 144 au plus |
| total | 14 644 à 15 644, sous la limite |

- 10 passages de 1 024 jetons (taille par défaut) peuvent dépasser 8 000 : Kotaemon coupe alors les derniers passages. [Source] (`format_context.py:107-112`)
- La valeur par défaut de Kotaemon, 32 000, dépasserait la fenêtre du modèle avec des documents longs : le service refuserait la requête. [Estimation] (essai de dépassement non mené à son terme dans l'interface)
- Le nombre de documents d'une collection n'est pas limité par le contexte : seuls les passages retrouvés partent au modèle. [Source]

## 5. Modèles

- Les modèles sont ceux du service central, noms fixes `chat`, `embed`, `rerank` [Vérifié] ; `transcribe` n'est pas utilisable (Kotaemon ne lit pas l'audio). [Vérifié]
- La réflexion de `chat` ne peut pas être coupée depuis Kotaemon (aucun paramètre `chat_template_kwargs`) ; le levier serait côté service. [Source]
- Un modèle plus léger, pour situer un plancher de qualité, relève de LLM-Service : proposition inscrite dans les décisions en attente du journal (`JOURNAL.md`).
- Un second modèle de réponse est exposé sans modification du service : `gemma-4-e4b` (environ 5,3 Go de carte graphique en plus). Il se déclare comme `chat` dans « Resources › LLMs », avec `model: gemma-4-e4b` ; non passé au banc. [À tester]

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| WSL ralentit fortement | moins de 2 Go de mémoire libre | arrêter les autres applications du banc ; `free -m` |
| réponses de plusieurs minutes | profil `cpu` et réflexion du modèle | normal sur processeur ; moins de passages, carte mentale décochée |
| réponse bloquée sur « Thinking ... » | notation par le modèle, plus de quatre demandes simultanées | décocher « Use LLM relevant scoring » |

## Sources

- LLM-Service, `README.md` section « Mesures » et dossiers `mesures/cpu`, `mesures/gpu` (commit `8568e75`, 12 novembre 2026).
- Bancs : `outils/resultats/kotaemon/banc-2026-11-12-*.json`.
- Diagnostic : `outils/resultats/machine/diagnostic-2026-11-12.json`.
