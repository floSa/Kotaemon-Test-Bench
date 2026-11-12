# Banc Kotaemon — docling-rerank — 2026-11-12T22:34:52

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 30 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 32 |
| citation_bonne_page | 25 |
| citations_avec_page | 25 |
| juge_llm_oui | 34 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 23.36 |
| latence_p95_s | 41.34 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '4/4', 'anglais': '2/2', 'multi-documents': '2/3', 'audio': '0/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-kotaemon': 1710, 'llm-central': 739, 'llm-swap': 5866, 'llm-speaches': 1323} |
| pic_ram_application_mo | 1710 |
| vram | 8774 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 29.9 | D'après les documents fournis, le chiffre d'affaires de Vélanor pour l'année 202 |
| Q02 | fait simple | oui | True | True | 15.93 | Selon les informations fournies dans le contexte, Vélanor a été fondée en **2014 |
| Q03 | fait simple | oui | True | True | 21.63 | D'après les documents fournis, la présidente de Vélanor est **Hélène Marchais**. |
| Q04 | fait simple | oui | True | True | 23.17 | L'adresse du siège social de Vélanor est située au **12 quai de la Fosse, à Nant |
| Q05 | tableau | oui | True | True | 19.02 | Selon les documents fournis, Vélanor compte **412 salariés** au 31 décembre 2025 |
| Q06 | tableau | oui | True | True | 24.5 | Selon les documents fournis, le chiffre d'affaires du troisième trimestre 2025 a |
| Q07 | tableau | oui | True | True | 28.3 | D'après les informations fournies dans le contexte, **15 400 unités** du modèle  |
| Q08 | tableau | oui | True | True | 23.78 | Selon les documents fournis, le prix public du modèle **Erdre Cargo** est de **4 |
| Q09 | tableau | oui | True | True | 22.83 | D'après les informations fournies dans le contexte, **97 salariés** travaillent  |
| Q10 | fait simple | oui | True | True | 26.09 | D'après les documents fournis, la part d'aluminium recyclé dans les cadres est d |
| Q11 | fait simple | oui | True | True | 17.81 | D'après les informations fournies dans le contexte, le taux de recyclage des bat |
| Q12 | tableau | oui | True | True | 29.93 | D'après les documents fournis, le fournisseur des moteurs est **Motodrive Co.**  |
| Q13 | tableau | oui | True | True | 20.63 | D'après les informations fournies dans le rapport annuel 2025 de Vélanor SAS, l' |
| Q14 | fait simple | oui | True | True | 18.11 | D'après les documents fournis, le taux de retour sous garantie est de **1,8 %**. |
| Q15 | scan | oui | True | True | 23.18 | Selon les documents fournis, le prix unitaire des batteries prévu par le contrat |
| Q16 | scan | oui | True | True | 20.22 | Selon les documents fournis, le délai de livraison prévu par le contrat Batterix |
| Q17 | scan | oui | True | True | 19.45 | Selon les documents fournis, le plafond des pénalités de retard du contrat Batte |
| Q18 | scan | oui | True | True | 19.58 | Selon les documents fournis, le volume minimal annuel de batteries prévu par le  |
| Q19 | fait simple | oui | True | True | 23.12 | D'après le contenu du document **procedure-batteries.docx** (Procédure PR-SEC-04 |
| Q20 | fait simple | oui | True | True | 23.36 | Selon les documents fournis dans le contexte, la personne responsable de la proc |
| Q21 | tableau | oui | True | True | 18.79 | Selon le document intitulé `procedure-batteries.docx` (Procédure PR-SEC-04 — Cha |
| Q22 | fait simple | oui | True | True | 21.8 | Selon les documents fournis, le prix public du modèle **Vilaine Compact** est de |
| Q23 | fait simple | oui | True | True | 28.28 | D'après les documents fournis, la capacité prévue de l'usine de Saint-Nazaire es |
| Q24 | tableau | non | False | True | 110.25 |  |
| Q25 | fait simple | oui | True | True | 25.17 | D'après les documents fournis, la durée de garantie du cadre est de **7 ans**.   |
| Q26 | fait simple | oui | True | True | 22.47 | D'après les documents fournis, le numéro de téléphone du service après-vente est |
| Q27 | fait simple | oui | True | True | 22.4 | Selon le contexte fourni, plus précisément dans le document intitulé **"Compte r |
| Q28 | anglais | oui | True | True | 27.0 | D'après les documents fournis, Batterix a obtenu un score global de **87 sur 100 |
| Q29 | anglais | oui | True | True | 24.06 | Selon les documents fournis, le taux de cellules défectueuses mesuré chez Batter |
| Q30 | multi-documents | non | False | True | 30.79 | D'après les documents fournis, voici la réponse détaillée à votre question :  ** |
| Q31 | multi-documents | oui | True | True | 17.74 | Selon les documents fournis, voici les informations demandées :  1.  **Score de  |
| Q32 | multi-documents | oui | True | True | 25.86 | Selon les documents fournis, voici les détails concernant les objectifs de Vélan |
| Q33 | audio | non | False | False | 40.14 | Sur la base des documents fournis, je ne peux pas répondre à cette question conc |
| Q34 | audio | non | False | False | 33.9 | D'après les documents fournis, je ne connais pas l'identité du directeur de prod |
| Q35 | piège | oui | True | - | 37.83 | D'après les documents fournis, il n'est pas possible de connaître le chiffre d'a |
| Q36 | piège | oui | True | - | 36.04 | D'après les documents fournis, il n'est pas possible de répondre à la question s |
| Q37 | piège | oui | True | - | 41.34 | D'après les documents fournis, je ne connais pas le nombre de trottinettes élect |
| Q38 | piège | oui | True | - | 42.09 | Sur la base des documents fournis, il n'est pas possible de déterminer le salair |
