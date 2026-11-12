# Banc Kotaemon — rerank — 2026-11-12T22:10:07

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 26 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 28 |
| citation_bonne_page | 20 |
| citations_avec_page | 20 |
| juge_llm_oui | 31 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 23.97 |
| latence_p95_s | 41.86 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '1/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '0/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-kotaemon': 1505, 'llm-central': 742, 'llm-swap': 5852, 'llm-speaches': 1326} |
| pic_ram_application_mo | 1505 |
| vram | 9118 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 32.45 | D'après les documents fournis, le chiffre d'affaires de Vélanor pour l'année 202 |
| Q02 | fait simple | oui | True | True | 20.41 | D'après les documents fournis, Vélanor a été fondée en **2014**.  Cette informat |
| Q03 | fait simple | oui | True | True | 23.38 | D'après les documents fournis dans le contexte, la présidente de Vélanor est **H |
| Q04 | fait simple | oui | True | True | 20.86 | L'adresse du siège de Vélanor est située au **12 quai de la Fosse, à Nantes**.   |
| Q05 | tableau | oui | True | True | 19.04 | Selon les documents fournis, Vélanor compte **412 salariés** au 31 décembre 2025 |
| Q06 | tableau | oui | True | True | 26.86 | Selon les documents fournis, le chiffre d'affaires du troisième trimestre 2025 a |
| Q07 | tableau | oui | True | True | 21.66 | D'après les documents fournis, plus précisément la figure de la page 5 du rappor |
| Q08 | tableau | oui | True | True | 22.09 | D'après les documents fournis, le prix public du modèle Erdre Cargo est de **4 2 |
| Q09 | tableau | oui | True | True | 17.11 | Selon les informations fournies dans le document **rapport-annuel-2025.pdf** (pl |
| Q10 | fait simple | oui | True | True | 20.64 | D'après les documents fournis, la part d'aluminium recyclé dans les cadres est d |
| Q11 | fait simple | oui | True | True | 21.69 | Selon les documents fournis, le taux de recyclage des batteries usagées collecté |
| Q12 | tableau | oui | True | True | 23.75 | D'après les documents fournis, le fournisseur qui livre les moteurs est **Motodr |
| Q13 | tableau | oui | True | True | 20.78 | Selon les informations fournies dans le rapport annuel 2025 de Vélanor SAS, spéc |
| Q14 | fait simple | oui | True | True | 22.84 | Selon les documents fournis, le taux de retour sous garantie s'établit à **1,8 % |
| Q15 | scan | non | True | False | 39.85 | D'après les documents et extraits de contexte fournis, il n'est pas possible de  |
| Q16 | scan | non | True | False | 35.86 | D'après les documents fournis, il n'est pas possible de déterminer le délai de l |
| Q17 | scan | oui | False | False | 34.71 | D'après les documents fournis, je ne connais pas la réponse à cette question. Il |
| Q18 | scan | non | False | False | 30.65 | Sur la base des documents fournis, je ne connais pas la réponse à cette question |
| Q19 | fait simple | oui | True | True | 23.97 | D'après le document **procedure-batteries.docx** (Procédure PR-SEC-04 — Charge e |
| Q20 | fait simple | oui | True | True | 23.32 | D'après les documents fournis, la personne responsable de la procédure de charge |
| Q21 | tableau | oui | True | True | 23.36 | D'après les documents fournis, plus précisément le contenu du fichier **`procedu |
| Q22 | fait simple | oui | True | True | 19.86 | Selon les documents fournis, le prix public du modèle **Vilaine Compact** est de |
| Q23 | fait simple | oui | True | True | 36.67 | D'après les documents fournis, la capacité prévue de l'usine de Saint-Nazaire es |
| Q24 | tableau | non | False | True | 109.45 | D'après les documents fournis, il est impossible de déterminer avec certitude le |
| Q25 | fait simple | oui | True | True | 14.77 | D'après les documents fournis, la durée de garantie du cadre est de **7 ans**.   |
| Q26 | fait simple | oui | True | True | 25.74 | D'après les informations fournies dans le contexte, le numéro de téléphone du se |
| Q27 | fait simple | oui | True | True | 22.67 | D'après le contenu du document intitulé **"Compte rendu de la réunion du CSE du  |
| Q28 | anglais | oui | True | True | 24.41 | D'après le document fourni, spécifiquement la figure extraite du fichier **suppl |
| Q29 | anglais | oui | True | True | 23.37 | Selon le document fourni, spécifiquement la figure extraite du fichier **supplie |
| Q30 | multi-documents | non | False | True | 37.4 | Sur la base des documents fournis, je ne connais pas la réponse à cette question |
| Q31 | multi-documents | non | False | True | 50.09 | D'après les documents fournis, voici les réponses détaillées à votre question :  |
| Q32 | multi-documents | oui | True | True | 26.49 | Selon les documents fournis, voici les détails concernant les objectifs de Vélan |
| Q33 | audio | non | False | False | 40.17 | Sur la base des documents fournis, je ne connais pas la réponse à cette question |
| Q34 | audio | non | False | False | 32.17 | D'après les documents contextuels fournis, il est impossible de nommer le **dire |
| Q35 | piège | oui | True | - | 34.52 | D'après les documents fournis, il est impossible de répondre à la question conce |
| Q36 | piège | oui | True | - | 36.35 | D'après les documents fournis, il n'est pas possible de déterminer qui est le di |
| Q37 | piège | oui | True | - | 41.86 | D'après les documents fournis, je ne connais pas le nombre de trottinettes élect |
| Q38 | piège | oui | True | - | 33.1 | Sur la base des documents et extraits de contexte fournis, **je ne connais pas l |
