# Manuel de Kotaemon

Ce manuel apprend à installer Kotaemon 0.12.0 sur un poste Windows 11 avec WSL2 et à s'en servir pour poser des questions à ses propres documents, en vérifiant chaque réponse à sa source. Il s'adresse à un utilisateur à l'aise avec un terminal, sans être forcément développeur. Tout ce qui est décrit a été fait sur un poste réel, à la souris, et chaque étape est illustrée par une capture d'écran annotée.

## Par où commencer

1. [01. Découvrir Kotaemon](manuel/01-decouvrir-kotaemon.md) : savoir si l'outil convient et quelle machine prévoir.
2. [02. Installer Kotaemon](manuel/02-installer-kotaemon.md) : l'installer, l'arrêter, le supprimer.
3. [03. Premiers pas](manuel/03-premiers-pas.md) : se connecter, sécuriser le compte, déclarer les modèles.
4. [04. Première question en dix minutes](manuel/04-premiere-question.md) : un document, une question, une réponse citée.

## Partie 1 — Manuel utilisateur

À lire dans l'ordre.

| Chapitre | Ce qu'on saura faire |
|---|---|
| [01. Découvrir Kotaemon](manuel/01-decouvrir-kotaemon.md) | dire à quoi sert Kotaemon, pour qui, ce qu'il sait faire et sur quelle machine il tourne |
| [02. Installer Kotaemon](manuel/02-installer-kotaemon.md) | installer, démarrer, arrêter et supprimer Kotaemon sous Windows 11 et WSL2 |
| [03. Premiers pas](manuel/03-premiers-pas.md) | se connecter, changer le mot de passe administrateur, se repérer dans l'écran, déclarer les modèles du service de modèles, régler la langue |
| [04. Première question en dix minutes](manuel/04-premiere-question.md) | ajouter un PDF, poser une question en français, lire la réponse et ses passages cités |
| [05. Ajouter et organiser ses documents](manuel/05-ajouter-et-organiser-ses-documents.md) | ajouter plusieurs fichiers, consulter les passages d'un fichier, créer des groupes, supprimer, ajouter depuis le chat, choisir le lecteur de fichiers, brancher un serveur Docling séparé |
| [06. Poser des questions et lire les sources](manuel/06-poser-des-questions-et-lire-les-sources.md) | gérer les conversations, limiter la recherche à des fichiers ou un groupe, choisir le style de citation, lire les scores, donner un avis |
| [07. Régler la recherche et le raisonnement](manuel/07-regler-la-recherche-et-le-raisonnement.md) | choisir le mode de recherche, le tri, la notation par le modèle et son alerte, la méthode de raisonnement et les consignes |
| [08. Agents ReAct et ReWOO](manuel/08-agents-react-et-rewoo.md) | faire répondre un agent qui enchaîne des recherches, comparer les deux agents, voir où se déclarent les serveurs MCP |
| [09. Graphes de connaissances (GraphRAG)](manuel/09-graphes-de-connaissances.md) | indexer un document en graphe avec LightRAG ou NanoGraphRAG, l'interroger, connaître le coût |
| [10. Collections et modèles](manuel/10-collections-et-modeles.md) | créer une collection, réparer les réglages après création, supprimer un modèle |
| [11. Comptes et partage](manuel/11-comptes-et-partage.md) | créer des comptes, partager une collection et une conversation, se déconnecter |
| [12. Cas pratiques](manuel/12-cas-pratiques.md) | dérouler trois usages complets de bout en bout |
| [13. En cas de problème](manuel/13-en-cas-de-probleme.md) | reconnaître les erreurs rencontrées et les corriger |
| [14. Glossaire](manuel/14-glossaire.md) | retrouver le sens des mots techniques |

## Partie 2 — Évaluation et compléments

Pour choisir, dimensionner, automatiser ou exploiter ; rien de cette partie n'est nécessaire pour suivre la partie 1.

| Annexe | Contenu |
|---|---|
| [A1. Évaluation : qualité et performances](annexes/A1-evaluation-qualite-et-performances.md) | résultats du banc de 38 questions, avec et sans tri des passages, réglages qui changent le résultat |
| [A2. Choisir son matériel et ses modèles](annexes/A2-choisir-son-materiel-et-ses-modeles.md) | configurations minimales sans et avec carte graphique, mémoire, temps d'attente |
| [A3. Automatiser par la bibliothèque Python](annexes/A3-automatiser-par-la-bibliotheque.md) | piloter Kotaemon sans l'interface, exemples exécutés |
| [A4. Exploitation](annexes/A4-exploitation.md) | sauvegarde, restauration, mise à jour, journaux, sécurité |
| [A5. Fonctionnement interne](annexes/A5-fonctionnement-interne.md) | architecture, stockage, chemin d'une question |
| [A6. Rapport d'essais](annexes/A6-rapport-d-essais.md) | méthode, preuves, incidents |
| [Carte de l'interface](annexes/carte-interface.md) | chaque onglet, menu et réglage, et le chapitre qui le couvre |

## Parcours conseillés

| Besoin | Chapitres |
|---|---|
| Essayer en une heure | 01, 02, 03, 04 |
| Interroger un fonds documentaire et vérifier les sources | 01 à 07, puis 12 (cas 1 et 2 ; le cas 3 demande aussi les chapitres 10 et 11) |
| Mettre l'outil à disposition d'une petite équipe | 01 à 04, 10, 11, puis annexe A4 |
| Comparer avec d'autres outils ou dimensionner un poste | 01, annexes A1 et A2 |

## Ce qui reste ouvert

| Sujet | État |
|---|---|
| Lecteur PaddleOCR installé hors de Kotaemon, serveur Docling sur une autre machine | même méthode que le serveur Docling séparé essayé sur le poste (chapitre 05, étapes 17 et 18) ; non essayés |
| Image « lite », plus légère | non essayée ; perd probablement la lecture des DOCX et PPTX |
| Poste sans carte graphique | temps estimés à partir des mesures du service de modèles (annexe A2), non mesurés avec Kotaemon |
| Serveurs MCP, liens web, `@WebSearch` | formulaires montrés ; services en ligne ou serveurs tiers non branchés |
| Visionneuse PDF, notation par le modèle, Microsoft GraphRAG, NanoGraphRAG | défauts constatés (chapitres 04, 07, 09, 13), sans correction possible depuis l'interface |
| Second modèle de réponse (`gemma-4-e4b`) | exposé par le service de modèles, non passé au banc |

## Décisions en attente

Choix qui restent à faire par la personne qui gère le poste ; aucun n'empêche de suivre le manuel.

1. Faire servir par le service de modèles une version de `chat` qui répond sans réfléchir d'abord, ou un modèle plus léger : réponses plus rapides ; c'est un réglage du service de modèles, pas de Kotaemon.
2. Garder ou supprimer la sauvegarde d'essai `donnees/sauvegardes/kotaemon-20261113-013435.tar.gz` (1 007 Mo) ; elle contient la clé du service de modèles.
3. Changer la clé du service de modèles : un fragment de 6 caractères en est resté dans l'historique du dépôt (annexe A6).
