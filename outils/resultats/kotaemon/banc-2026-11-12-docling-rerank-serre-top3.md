# Banc Kotaemon — docling-rerank-serre-top3 — 2026-11-12T22:53:03

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 31 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 32 |
| citation_bonne_page | 25 |
| citations_avec_page | 25 |
| juge_llm_oui | 34 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 21.95 |
| latence_p95_s | 38.67 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '4/4', 'anglais': '2/2', 'multi-documents': '2/3', 'audio': '0/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-kotaemon': 1710, 'llm-central': 735, 'llm-swap': 5633, 'llm-speaches': 1326} |
| pic_ram_application_mo | 1710 |
| vram | 9235 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 19.64 | Selon les documents fournis, le chiffre d'affaires de Vélanor pour l'année 2025  |
| Q02 | fait simple | oui | True | True | 13.55 | D'après les informations fournies dans le contexte, Vélanor a été fondée en l'an |
| Q03 | fait simple | oui | True | True | 21.12 | D'après les informations fournies dans le contexte, la présidente de Vélanor est |
| Q04 | fait simple | oui | True | True | 27.78 | L'adresse du siège de Vélanor est le **12 quai de la Fosse, à Nantes**.  Voici l |
| Q05 | tableau | oui | True | True | 22.91 | Selon les documents fournis, Vélanor compte **412 salariés** au 31 décembre 2025 |
| Q06 | tableau | oui | True | True | 24.99 | Selon les documents fournis, le chiffre d'affaires du troisième trimestre 2025 a |
| Q07 | tableau | oui | True | True | 23.72 | D'après les informations fournies dans le contexte, **15 400 unités** du modèle  |
| Q08 | tableau | oui | True | True | 20.46 | Selon les informations fournies dans le contexte, le prix public du modèle **Erd |
| Q09 | tableau | oui | True | True | 28.55 | D'après les informations fournies dans le contexte, il y a **97 salariés** au si |
| Q10 | fait simple | oui | True | True | 27.28 | D'après les éléments de contexte fournis, la part d'aluminium recyclé dans les c |
| Q11 | fait simple | oui | True | True | 11.52 | D'après le document fourni, spécifiquement dans la section « Environnement » du  |
| Q12 | tableau | oui | True | True | 25.73 | Selon les documents fournis, le fournisseur qui livre les moteurs est **Motodriv |
| Q13 | tableau | oui | True | True | 19.28 | D'après les informations fournies dans le contexte, Vélanor a dégagé un **résult |
| Q14 | fait simple | oui | True | True | 17.83 | D'après les documents fournis, le taux de retour sous garantie est de **1,8 % de |
| Q15 | scan | oui | True | True | 19.53 | Selon les documents fournis, le prix unitaire des batteries prévu par le contrat |
| Q16 | scan | oui | True | True | 14.67 | D'après le contenu du contrat fourni, spécifiquement l'**Article 5 Délais de liv |
| Q17 | scan | oui | True | True | 15.96 | D'après le contenu du contrat fourni, spécifiquement l'**Article 6** intitulé «  |
| Q18 | scan | oui | True | True | 15.83 | D'après les documents fournis, plus précisément le contenu du fichier **contrat- |
| Q19 | fait simple | oui | True | True | 22.43 | D'après les informations fournies dans le document **procedure-batteries.docx**  |
| Q20 | fait simple | oui | True | True | 16.74 | Selon le contexte fourni, la personne responsable de la procédure de charge et d |
| Q21 | tableau | oui | True | True | 17.28 | D'après le contenu du document "procedure-batteries.docx", spécifiquement dans l |
| Q22 | fait simple | oui | True | True | 22.42 | D'après les informations fournies dans le contexte, spécifiquement dans le docum |
| Q23 | fait simple | oui | True | True | 17.37 | D'après les documents fournis, la capacité prévue de l'usine de Saint-Nazaire es |
| Q24 | tableau | oui | False | True | 96.78 | D'après les documents fournis, voici l'analyse détaillée concernant le stock de  |
| Q25 | fait simple | oui | True | True | 26.84 | D'après le contenu du document **faq-sav.html** (Page 1), la durée de garantie d |
| Q26 | fait simple | oui | True | True | 18.99 | Selon le contenu fourni dans le document **faq-sav.html** (Page 1), le numéro de |
| Q27 | fait simple | oui | True | True | 21.95 | Selon le document « cse-2025-10-14.md », qui contient le compte rendu de la réun |
| Q28 | anglais | oui | True | True | 18.77 | D'après les informations fournies dans le contexte, Batterix GmbH a obtenu une * |
| Q29 | anglais | oui | True | True | 28.35 | Selon le document d'audit fournisseur fourni (intitulé **supplier-audit-batterix |
| Q30 | multi-documents | non | False | True | 23.81 | D'après les extraits de contrat fournis, voici la réponse détaillée :  **1. Déla |
| Q31 | multi-documents | oui | True | True | 21.26 | D'après les documents fournis, voici les réponses détaillées à votre question :  |
| Q32 | multi-documents | oui | True | True | 17.74 | D'après les documents fournis, voici les informations détaillées pour répondre à |
| Q33 | audio | non | False | False | 28.49 | Sur la base des documents fournis, je ne connais pas la réponse à cette question |
| Q34 | audio | non | False | False | 23.22 | D'après les documents fournis, il n'est pas possible de répondre à la question c |
| Q35 | piège | oui | True | - | 38.67 | D'après les extraits de contexte fournis, je ne connais pas le chiffre d'affaire |
| Q36 | piège | oui | True | - | 33.53 | D'après les documents fournis, il n'est pas possible d'identifier le directeur f |
| Q37 | piège | oui | True | - | 45.52 | D'après les extraits de contexte fournis dans le rapport annuel 2025 de Vélanor  |
| Q38 | piège | oui | True | - | 27.46 | D'après les documents fournis, il n'est pas possible de connaître le salaire de  |
