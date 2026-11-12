# 01. Découvrir Kotaemon

> Ce chapitre explique à quoi sert Kotaemon, pour qui, ce qu'il sait faire, sur quelle machine il tourne et ce qu'il a donné aux essais.
> **Point de départ** : aucun ; ce chapitre se lit sans l'application.
> **Durée** : environ 10 minutes. **Avant** : aucun.

## Ce qu'il faut savoir

Kotaemon est une application web qui permet de **poser des questions à ses propres documents** et d'obtenir des réponses rédigées, accompagnées des **passages qui les justifient** : nom du document, numéro de page, vignette de la page et phrases surlignées. Sa force est la vérification : chaque réponse se contrôle d'un coup d'œil dans le panneau des sources.

Les documents se rangent dans des **collections** (une collection ordinaire et deux collections « en graphe » à l'installation). Chaque compte a ses propres fichiers dans une collection privée ; une collection peut aussi être partagée entre tous les comptes.

Pour répondre, Kotaemon propose plusieurs **méthodes de raisonnement** : la réponse simple (chercher puis répondre), la décomposition d'une question composée en sous-questions, et deux **agents** (ReAct et ReWOO) qui enchaînent plusieurs recherches avant de répondre.

Kotaemon ne contient pas de modèle d'IA dans cette installation : il s'appuie sur un **service de modèles** installé sur le même poste (le service LLM central), qui fournit le modèle de réponse, le modèle d'embedding (qui représente le sens des textes) et le modèle de tri des passages. Rien ne part vers un service en ligne pour répondre aux questions.

## Pour qui

| Adapté | Peu adapté |
|---|---|
| Une personne ou une petite équipe qui veut vérifier chaque réponse dans ses documents : page citée, vignette de la page, phrases surlignées, notes de pertinence | Un public qui ne lit pas l'anglais : l'interface n'existe qu'en anglais (les réponses, elles, sont en français) |
| Des documents PDF, Word, PowerPoint, Excel, HTML, Markdown, avec des tableaux | Des PDF scannés : le lecteur par défaut ne lit pas le texte des images ; il faut passer par le lecteur Docling, plus lent |
| Des questions composées ou à plusieurs étapes : décomposition et agents | Des fichiers audio ou vidéo : non lus |
| Essayer les graphes de connaissances (GraphRAG) sur quelques documents | Une installation sans surveillance pour une grande équipe : projet peu actif depuis plusieurs mois, plus de 250 demandes ouvertes |

## Le projet

| | |
|---|---|
| Dépôt | https://github.com/Cinnamon/kotaemon |
| Documentation | https://cinnamon.github.io/kotaemon/ |
| Licence | Apache 2.0 : libre, usage commercial autorisé |
| Éditeur | Cinnamon AI (Japon et Viêt Nam) |
| Popularité | 25 906 étoiles, 2 171 copies (forks) sur GitHub |
| Activité | ralentie : aucune modification sur les 90 derniers jours, dernière modification en juillet 2026, 262 demandes et propositions ouvertes, 39 contributeurs |
| Ancienneté | projet créé en mars 2024 ; version décrite 0.12.0 du 31 mai 2026 |
| Coût | gratuit ; aucun abonnement |

Chiffres relevés sur GitHub le 12 novembre 2026.

## Fonctions

Réponses : **Oui**, **Non**, ou **Partiel** avec la limite en une phrase.

### Modèles d'IA

| Fonction | Réponse |
|---|---|
| Service de modèles local compatible OpenAI (llama.cpp, vLLM, LiteLLM…) | Oui (type `ChatOpenAI`, déclaré dans « Resources ») |
| Ollama en direct | Oui |
| Fournisseurs en ligne (OpenAI, Azure, Anthropic, Google, Cohere, Mistral, Groq) | Oui |
| Tri des passages par un modèle de tri (reranker) | Oui, y compris celui du service de modèles (type `CohereReranking`) |
| Notation des passages par le modèle de réponse | Partiel : fonctionne, mais envoie dix demandes à la fois, que le service de modèles refuse au-delà de quatre |
| Couper la réflexion du modèle | Non : aucun réglage ne le permet |
| Transcription de l'audio | Non |

### Documents acceptés

| Fonction | Réponse |
|---|---|
| PDF, Word, PowerPoint, Excel, CSV, HTML, Markdown, texte, archives ZIP | Oui (Word et PowerPoint après une correction appliquée par le script d'installation) |
| PDF scannés et images (lecture optique) | Partiel : seulement avec le lecteur Docling |
| Pages web par leur adresse | Partiel : passe par un service en ligne (Jina Reader) |
| Audio et vidéo | Non |
| Groupes de fichiers | Oui |

### Recherche et réponses

| Fonction | Réponse |
|---|---|
| Recherche combinant mots exacts et sens (hybride) | Oui, par défaut |
| Numéro de page du passage cité | Oui, pour les PDF |
| Phrases de la source surlignées et notes de pertinence | Oui |
| Visionneuse PDF ouverte à la page citée | Non dans la version décrite : la visionneuse reste vide |
| Alerte quand les passages sont peu pertinents | Partiel : seulement avec la notation par le modèle de réponse |
| Décomposition des questions composées | Oui |
| Agents ReAct et ReWOO | Oui |
| Graphes de connaissances (GraphRAG) | Partiel : LightRAG fonctionne ; NanoGraphRAG demande une installation de plus ; Microsoft GraphRAG ne fonctionne pas avec le service de modèles |
| Carte mentale de la réponse | Oui |

### Installation et exploitation

| Fonction | Réponse |
|---|---|
| Installation | Docker, un seul conteneur (image de 12,7 Go) |
| Mémoire nécessaire, hors modèles d'IA | XX |
| Interface en français | Non : anglais seulement |
| Comptes et rôles | Oui : administrateur ou utilisateur ; collections privées ou partagées ; conversations partageables |
| API REST | Non : pilotage possible par la bibliothèque Python de Kotaemon |
| Sauvegarde | Oui, par copie du dossier de données |

## Matériel nécessaire

Le matériel se partage entre le service de modèles (le plus gros) et Kotaemon. Le détail des mesures est dans l'[annexe A2](../annexes/A2-choisir-son-materiel-et-ses-modeles.md).

### Sans carte graphique

| Élément | Minimum |
|---|---|
| Processeur | 8 cœurs récents |
| Mémoire vive | 16 Go : environ 4,3 Go pour le service de modèles, XX pour Kotaemon, le reste pour Windows et WSL |
| Disque libre | 25 Go : 12,7 Go pour l'image de Kotaemon, environ 5 Go pour les modèles du service, le reste pour les documents |
| Temps d'attente | le modèle produit environ 14 jetons par seconde, cinq fois moins qu'avec une carte graphique : XX |

### Avec une carte graphique NVIDIA

| Élément | Minimum |
|---|---|
| Carte graphique | 8 Go de mémoire (7 Go pris par les trois modèles permanents) ; 16 Go sur le poste d'essai |
| Mémoire vive | 16 Go : environ 5,4 Go pour le service de modèles, XX pour Kotaemon |
| Disque libre | 25 Go |
| Temps d'attente | XX |

Le volume de documents n'est pas limité par la mémoire : Kotaemon ne transmet au modèle que les passages utiles (10 au plus, environ 8 000 jetons avec les réglages du chapitre 03), quelle que soit la taille de la collection.

## Résultats mesurés

Test sur 38 questions dont la réponse est connue, posées à 9 documents d'une entreprise fictive (rapport annuel, contrat scanné, procédure, présentation, tableur, page web, note, audit en anglais, message vocal), avec le modèle de réponse `chat` sur une carte graphique de 16 Go.

| Mesure | Résultat |
|---|---|
| XX | XX |

Détail : [annexe A1](../annexes/A1-evaluation-qualite-et-performances.md).

## Pour aller plus loin

| Pour | Lire |
|---|---|
| Installer | [02. Installer Kotaemon](02-installer-kotaemon.md) |
| Première réponse citée | [04. Première question en dix minutes](04-premiere-question.md) |
| Trois usages complets | [12. Cas pratiques](12-cas-pratiques.md) |
| Choisir le matériel | [annexe A2](../annexes/A2-choisir-son-materiel-et-ses-modeles.md) |

## Résultat

Le lecteur sait ce que fait Kotaemon, s'il convient à son besoin et quelle machine prévoir.

---
*Version décrite : Kotaemon 0.12.0, essais du 12 novembre 2026. Détails et preuves : [rapport d'essais](../annexes/A6-rapport-d-essais.md).*
