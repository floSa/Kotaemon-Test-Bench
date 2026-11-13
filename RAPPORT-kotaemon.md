# Rapport de mission — Kotaemon

Mission `kit/PROMPT.md`, fiche `kit/fiches/03-kotaemon.md`, essais du 12 et 13 novembre 2026 sur la machine du profil B (Ryzen 5 9600X, 32 Go dans WSL2, RTX 4060 Ti 16 Go).

## Ce qui a été installé

| Élément | Version |
|---|---|
| Kotaemon | 0.12.0 (31 mai 2026, dernière stable) ; image `ghcr.io/cinnamon/kotaemon:main-full@sha256:cb4b71561e529398bacdf12f1289c32290f6c70f286b8efb7a1ed7e66d089b66` (12,7 Go, révision `9ad3e4e` = tag v0.12.0 ; aucune image numérotée 0.12.0 n'est publiée) |
| Conteneur | `rag-kotaemon`, projet compose `rag-kotaemon`, port `127.0.0.1:7860` |
| Ajouts dans le conteneur | données NLTK (`punkt_tab`, `averaged_perceptron_tagger_eng`), `pipmaster` 1.2.2 (LightRAG), `nano-graphrag` 0.0.8.2 avec `chroma-hnswlib` 0.7.6 et `pydantic` 2.10.6 remis |
| Captures | `mcr.microsoft.com/playwright/python:v1.65.1-noble` (éphémère) |
| Modèles (service LLM central, LLM-Service) | `chat` = Qwen3.5-4B, `embed` = bge-m3, `rerank` = bge-reranker-v2-m3, déclarés dans « Resources » comme `llm-service-chat` (ChatOpenAI), `llm-service-embed` (OpenAIEmbeddings), `llm-service-rerank` (CohereReranking) ; `transcribe` non utilisable (Kotaemon ne lit pas l'audio) |

## Où l'ouvrir

`http://127.0.0.1:7860` dans le navigateur de Windows. Comptes : `admin` (administrateur) et `camille` (utilisateur) ; mots de passe dans `donnees/IDENTIFIANTS-LOCAUX.txt`. Jeu de démonstration : « File Collection » avec les 8 documents lisibles du corpus (contrat scanné lu par Docling), groupe « Fournisseur Batterix », « LightRAG Collection » (rapport annuel en graphe), « Documents partagés » (compte rendu du CSE), trois conversations « Démo — … » avec leurs citations.

## Manuels écrits

- Page d'accueil : [docs/kotaemon/README.md](docs/kotaemon/README.md).
- Partie 1 (14 chapitres, 92 captures annotées) : [01](docs/kotaemon/manuel/01-decouvrir-kotaemon.md), [02](docs/kotaemon/manuel/02-installer-kotaemon.md), [03](docs/kotaemon/manuel/03-premiers-pas.md), [04](docs/kotaemon/manuel/04-premiere-question.md), [05](docs/kotaemon/manuel/05-ajouter-et-organiser-ses-documents.md), [06](docs/kotaemon/manuel/06-poser-des-questions-et-lire-les-sources.md), [07](docs/kotaemon/manuel/07-regler-la-recherche-et-le-raisonnement.md), [08](docs/kotaemon/manuel/08-agents-react-et-rewoo.md), [09](docs/kotaemon/manuel/09-graphes-de-connaissances.md), [10](docs/kotaemon/manuel/10-collections-et-modeles.md), [11](docs/kotaemon/manuel/11-comptes-et-partage.md), [12](docs/kotaemon/manuel/12-cas-pratiques.md), [13](docs/kotaemon/manuel/13-en-cas-de-probleme.md), [14](docs/kotaemon/manuel/14-glossaire.md).
- Partie 2 : [A1](docs/kotaemon/annexes/A1-evaluation-qualite-et-performances.md), [A2](docs/kotaemon/annexes/A2-choisir-son-materiel-et-ses-modeles.md), [A3](docs/kotaemon/annexes/A3-automatiser-par-la-bibliotheque.md), [A4](docs/kotaemon/annexes/A4-exploitation.md), [A5](docs/kotaemon/annexes/A5-fonctionnement-interne.md), [A6](docs/kotaemon/annexes/A6-rapport-d-essais.md), [carte de l'interface](docs/kotaemon/annexes/carte-interface.md) (24 captures de repérage).
- Index de la série et comparatif : [docs/README.md](docs/README.md).

## Résultats du banc en cinq lignes

1. Lecteur intégré, 10 passages, sans puis avec le tri `rerank` : 25/34 justes après relecture (26 au comptage automatique) dans les deux cas, 4/4 refus ; le tri ne change pas le score.
2. Contrat scanné relu par Docling : 30/34 (scan 4/4 au lieu de 1/4).
3. Même chose avec 3 passages au lieu de 10 : 31/34, réponses un peu plus rapides (médiane 22 s).
4. Échecs restants : audio non lu (2), une question qui croise contrat et tableur.
5. Temps de réponse médian 22 à 26 s (réflexion du modèle comprise, non réglable dans Kotaemon) ; Kotaemon prend 0,5 à 1,9 Go de mémoire.

## Vérifié, non vérifié

- **Vérifié** : installation, ports, chaque chapitre de la partie 1 fait à la souris et capturé, banc (4 réglages complets, 1 partiel), exemples (4, code 0), sauvegarde et restauration, LightRAG, échecs de NanoGraphRAG et de Microsoft GraphRAG, comptes et partage.
- **Non vérifié** : profil sans carte graphique (estimations, annexe A2) ; lecteur Docling ou PaddleOCR externe (méthode lue dans le code, annexe A3) ; image « lite » ; modèle `gemma-4-e4b` ; ajout effectif d'un serveur MCP ; liens web et `@WebSearch` (services en ligne) ; `nettoyer.sh kotaemon` (pour garder le jeu de démonstration) ; boutons « Download », « Report » et « Suggest chat » montrés sans être actionnés.

## Incidents

Détail dans l'annexe A6, section 4. Principaux : données NLTK d'unstructured en 403 (DOCX, PPTX) corrigées par `installer.sh` ; notation par le modèle en 429 puis note non reconnue ; langue de session anglaise ; visionneuse PDF vide (`cdn.skypack.dev`) ; « Delete » sans confirmation ; groupe qui perd un fichier relu ; réglages non relus après création d'une collection ; LightRAG sans `pipmaster` ; nano-graphrag qui casse Chroma puis Gradio ; Microsoft GraphRAG qui ne démarre pas ; question trop longue (« LanceError »).

## Décisions en attente

1. **Serveur Docling externe** : la demande de l'utilisateur (brancher un docling-serve ou un PaddleOCR hors de Kotaemon) est décrite comme méthode (annexe A3, section 5) mais non essayée : l'image docling-serve n'est pas dans l'enveloppe autorisée. À essayer sur accord.
2. **Modèle de réponse plus léger** pour situer un plancher de qualité : relève de LLM-Service, hors mission.
3. **Réflexion de `chat`** : Kotaemon ne peut pas la couper ; une option côté LLM-Service (alias sans réflexion) raccourcirait les réponses de moitié environ [Estimation]. Hors mission.
4. **Sauvegarde d'essai** `donnees/sauvegardes/kotaemon-20261113-013435.tar.gz` (1 007 Mo, contient la clé du service en clair dans la base) : à garder ou supprimer.
5. **Défauts à signaler au projet Kotaemon** (aucun compte en ligne créé) : visionneuse PDF, `pipmaster` manquant dans l'image, `python` hors environnement pour Microsoft GraphRAG, réglages non relus après création d'une collection, groupes non mis à jour après relecture.

## Disque, mémoire, carte graphique

| Mesure | Valeur |
|---|---|
| Image Kotaemon | 12,7 Go |
| Données `donnees/kotaemon/` | 1,1 Go (dont 536 Mo de modèles de Docling) |
| Sauvegarde d'essai | 1 007 Mo |
| Mémoire de Kotaemon au repos (fin de mission) | 747 Mio |
| Service central, mémoire vive | LiteLLM 735 Mio, llama-swap 5,4 Gio, speaches 1,3 Gio |
| Carte graphique (service central, bureau compris) | 7 799 Mio sur 16 380 |

## Tout arrêter ou tout supprimer

```bash
outils/kotaemon/arreter.sh             # arrêt, données conservées
outils/communs/nettoyer.sh kotaemon    # suppression du conteneur et de donnees/kotaemon/, sur confirmation
docker image rm ghcr.io/cinnamon/kotaemon:main-full   # retire aussi l'image (12,7 Go)
```

LLM-Service n'est jamais arrêté ni modifié par ces scripts.

## Proposition pour la solution suivante

Open WebUI (fiche 05) : interface généraliste et multi-utilisateur, dont le branchement à un serveur compatible OpenAI et au reranker externe est natif. Reprendre de ce banc : l'attente de fin de réponse des scénarios Playwright (`outils/kotaemon/captures/ui.py`, `attendre_reponse`), la vérification systématique des groupes et réglages après chaque changement de structure, et un passage du banc avec 3 à 5 passages en plus du réglage par défaut.
