# A6. Rapport d'essais

> **Objet** : décrire comment ce manuel a été produit et vérifié : méthode, machine, versions, preuves, incidents et limites.
> **Prérequis** : aucun ; renvoie aux autres annexes et aux résultats bruts de `outils/resultats/kotaemon/`.
> **Version décrite** : Kotaemon 0.12.0 (image `ghcr.io/cinnamon/kotaemon:main-full@sha256:cb4b7156…`, révision `9ad3e4e`), essais du 12 et 13 novembre 2026.
> **Statut des informations** : [Vérifié] observé sur la machine d'essai, avec son résultat brut ; [Source] lu dans le code ou la documentation ; [Estimation] calcul expliqué ; [À tester] non essayé.
> **Précautions** : les identifiants de démonstration sont dans `donnees/IDENTIFIANTS-LOCAUX.txt` (non versionné) ; la clé du service de modèles reste dans `.env`.

## Sommaire

1. [Méthode](#1-méthode)
2. [Machine et versions](#2-machine-et-versions)
3. [Preuves par chapitre](#3-preuves-par-chapitre)
4. [Incidents](#4-incidents)
5. [Ce qui n'a pas été vérifié](#5-ce-qui-na-pas-été-vérifié)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Méthode

- Lecture du code au tag `v0.12.0` par deux sous-agents (serveur et interface) : `cadrage-serveur.md`, `cadrage-interface.md`, relecture des composants avant lancement : `relecture.md`. [Vérifié]
- Chaque action de la partie 1 a été faite dans l'interface, à la souris, par Playwright (conteneur officiel `mcr.microsoft.com/playwright/python:v1.65.1-noble`), scénarios dans `outils/kotaemon/captures/c03_*.py` à `c13_*.py` et `carte.py`. Pour chaque capture : texte de la page dans `outils/resultats/kotaemon/captures/<chapitre>/<capture>.txt`, libellés des pastilles dans `scenario.json`, observations dans `notes.log`. [Vérifié]
- Clé du service de modèles masquée sur les captures (remplacée par des astérisques dans l'affichage seulement) et dans les textes enregistrés. [Vérifié] Exception corrigée : un préfixe de 6 caractères de la clé était resté dans `graphrag-2026-11-13.log`, masqué au commit `87ce88a` ; il reste dans l'historique git (réécriture interdite) : changer la clé est inscrit dans les décisions en attente.
- Banc de 38 questions par la bibliothèque dans le conteneur (annexe A1). [Vérifié]
- Exemples courts exécutés, sortie dans `exemples/kotaemon/sorties_verifiees.txt` (annexe A3). [Vérifié]

## 2. Machine et versions

| Élément | Valeur | Statut |
|---|---|---|
| Machine | Ryzen 5 9600X, 32 Go dans WSL2, RTX 4060 Ti 16 Go, 545 Go libres | [Vérifié] (`outils/resultats/machine/diagnostic-2026-11-12.json`) |
| Docker | 29.9.3, Compose 5.7.0 | [Vérifié] |
| Kotaemon | 0.12.0 (31 mai 2026), dernière version stable ; aucune image numérotée publiée, d'où `main-full` figée par empreinte | [Vérifié] (`versions-2026-11-12.json`) |
| Service de modèles | LiteLLM v1.109.0, llama-swap v272 (CUDA, llama.cpp b12282), speaches 0.8.3 ; noms fixes `chat` (Qwen3.5-4B), `embed` (bge-m3), `rerank` (bge-reranker-v2-m3) | [Vérifié] (`sante-2026-11-12-debut.txt`) |
| Projet | 25 906 étoiles, 39 contributeurs, aucune modification sur 90 jours au 12 novembre 2026 | [Vérifié] (`identite-github-2026-11-12.json`) |
| Paquets ajoutés dans le conteneur | `pipmaster` 1.2.2 (LightRAG), `nano-graphrag` 0.0.8.2 (option du chapitre 09), données NLTK `punkt_tab` et `averaged_perceptron_tagger_eng` | [Vérifié] |

## 3. Preuves par chapitre

| Chapitre | Preuves |
|---|---|
| 02 Installer | `installation-2026-11-12.log`, `installation-2026-11-12-essai-nltk-403.log`, `ports-publies-2026-11-12.txt`, `exploitation-2026-11-12.log` |
| 03 Premiers pas | `captures/03-premiers-pas/` (tests de connexion réussis des trois modèles dans `notes.log`) |
| 04 Première question | `captures/04-premiere-question/` (indexation 6,1 s, réponse en français) ; `incident-2026-11-12-visionneuse-pdf.txt` |
| 05 Documents | `captures/05-documents/` (8 fichiers déposés, 7 indexés, en 13,1 s, suppression sans confirmation, relecture Docling 47,1 s, groupe incomplet) ; `docling-2026-11-12.log` |
| 06 Questions et sources | `captures/06-questions/` (dont `05-citation-en-ligne-essai2-sorry.txt`) |
| 07 Réglages | `captures/07-reglages/` ; `essai-2026-11-12-alerte-pertinence.txt` ; `incident-2026-11-12-429-score-llm.log` |
| 08 Agents | `captures/08-agents/notes.log` (ReAct 26 s, ReWOO 74 s, étapes) |
| 09 GraphRAG | `lightrag-2026-11-12.log`, `lightrag-2026-11-13.log` (527 s), `lightrag-dependance-2026-11-13.log`, `nanographrag-2026-11-13.log`, `graphrag-2026-11-13.log` |
| 10 Collections et modèles | `captures/10-ressources/` ; erreur de chargement des réglages (« KeyError: 'index.options.4.reader_mode' ») relevée dans le journal du conteneur (`graphrag-2026-11-13.log`, `fin-de-mission-2026-11-13.log`) |
| 11 Comptes | `captures/11-comptes/` (session `camille`) |
| 12 Cas pratiques | `captures/12-cas-pratiques/` |
| 13 Problèmes | `captures/13-problemes/`, `contexte-2026-11-13.txt` |
| Carte | `captures/carte/` (24 pages) |

## 4. Incidents

| Incident | Effet | Suite | Statut |
|---|---|---|---|
| Données NLTK d'unstructured sur un stockage fermé (403) | DOCX et PPTX en échec | `installer.sh` fournit les données (`NLTK_DATA`) | [Vérifié] |
| Fichiers en échec inscrits sans passage | indexation sautée ensuite (« already indexed ») | réindexation forcée (pilote du banc, chapitre 05) | [Vérifié] |
| Notation par le modèle : 10 demandes simultanées | erreurs 429, réponse bloquée sur « Thinking ... » | option décochée | [Vérifié] |
| Notation par le modèle : note non reconnue (« AssertionError ») | notes à 0, alerte jamais affichée | documenté | [Vérifié] (trace dans `fin-de-mission-2026-11-13.log`, notes dans `essai-2026-11-12-alerte-pertinence.txt`) |
| Langue de session anglaise par défaut | réponses en anglais malgré « Settings » | « Chat settings » › « Language » | [Vérifié] |
| Visionneuse PDF vide (`cdn.skypack.dev` en erreur) | pas d'aperçu du PDF | vignette et texte surligné | [Vérifié] |
| « Delete » d'un fichier sans confirmation | une copie de test supprimée par erreur, un fichier du corpus supprimé puis remis | documenté | [Vérifié] |
| Relecture forcée : nouvel identifiant, groupe incomplet | contrat absent des recherches par groupe | groupe réparé | [Vérifié] |
| Création d'une collection : réglages non relus | interface revenue aux valeurs par défaut (anglais, 32 000, notation cochée) | réglages enregistrés de nouveau | [Vérifié] (KeyError et relevé de la sonde dans `fin-de-mission-2026-11-13.log`) |
| Question de suite trop tôt | réponse non affichée | attendre la fin de la réponse précédente | [Vérifié] pour la réponse affichée après attente (`fin-de-mission-2026-11-13.log`, `captures/12-cas-pratiques/02-client-suite.txt`) ; l'absence de réponse sans attente n'est consignée que dans `JOURNAL.md` |
| LightRAG sans `pipmaster` | graphe non construit, question bloquée 10 minutes | `completer_lightrag.sh` | [Vérifié] |
| nano-graphrag : hnswlib et pydantic | Chroma puis l'interface en panne | corrections dans `installer_nanographrag.sh` | [Vérifié] |
| NanoGraphRAG : « EmptyNetworkError » | aucun graphe | documenté | [Vérifié] |
| Microsoft GraphRAG : « No module named 'graphrag' » | aucun graphe, alors que l'interface annonce un succès | documenté | [Vérifié] |
| Question de 82 542 caractères | « LanceError(IO): sql parser error », aucune réponse | documenté | [Vérifié] |
| Un appel à `api.openai.com` | test de connexion d'un modèle « openai » préinstallé (clé vide), lors de la mise au point du scénario | aucune donnée envoyée hormis « Hi » | [Vérifié] |
| Plusieurs captures prises pendant les bancs | latences des bancs possiblement affectées | captures sans appel au modèle surtout | [Estimation] |

## 5. Ce qui n'a pas été vérifié

- Le profil sans carte graphique (annexe A2) : estimations. [Estimation]
- Le branchement d'un lecteur extérieur (serveur Docling ou PaddleOCR), l'image « lite », le second modèle `gemma-4-e4b`. [À tester]
- L'ajout effectif d'un serveur MCP, les liens web (service en ligne Jina Reader), `@WebSearch`. [À tester]
- `outils/communs/nettoyer.sh kotaemon` : relu, non rejoué pour garder le jeu de démonstration. [À tester]
- Les boutons « Download », « Download all files », « Report » et l'interrupteur « Suggest chat » ont été montrés sans être actionnés. [À tester]

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| un fichier de preuve cité manque | résultat brut regroupé dans un autre journal | chercher dans `outils/resultats/kotaemon/` par date |
| une capture ne correspond plus à l'interface | version différente de 0.12.0 | vérifier l'empreinte de l'image (`docker image inspect`) |

## Sources

- Résultats bruts : `outils/resultats/kotaemon/`.
- Scénarios : `outils/kotaemon/captures/`.
- Journal de la mission : `JOURNAL.md`.
