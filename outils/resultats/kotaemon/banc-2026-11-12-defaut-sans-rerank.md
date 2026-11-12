# Banc Kotaemon — defaut-sans-rerank — 2026-11-12T21:51:43

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 26 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 27 |
| citation_bonne_page | 20 |
| citations_avec_page | 20 |
| juge_llm_oui | 32 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 25.84 |
| latence_p95_s | 38.21 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '1/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '0/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-kotaemon': 1946, 'llm-central': 735, 'llm-swap': 5855, 'llm-speaches': 1331} |
| pic_ram_application_mo | 1946 |
| vram | 8583 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 0.3 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 25.84 | Selon les documents fournis, le chiffre d'affaires de Vélanor pour l'année 2025  |
| Q02 | fait simple | oui | True | True | 18.79 | D'après les documents fournis, Vélanor a été fondée en l'année **2014**.  Cette  |
| Q03 | fait simple | oui | True | True | 22.13 | Selon les documents fournis, la présidente de Vélanor est **Hélène Marchais**.   |
| Q04 | fait simple | oui | True | True | 26.49 | L'adresse du siège de Vélanor est **au 12 quai de la Fosse, à Nantes**.  Voici l |
| Q05 | tableau | oui | True | True | 20.25 | Selon les documents fournis, Vélanor compte **412 salariés** au 31 décembre 2025 |
| Q06 | tableau | oui | True | True | 31.18 | Selon les informations fournies dans le contexte, plus précisément dans la figur |
| Q07 | tableau | oui | True | True | 26.99 | Selon les informations fournies dans le document **rapport-annuel-2025.pdf**, pl |
| Q08 | tableau | oui | True | True | 24.17 | Selon les documents fournis, le prix public du modèle **Erdre Cargo** est de **4 |
| Q09 | tableau | oui | True | True | 22.33 | Selon les informations fournies dans le document « rapport-annuel-2025.pdf » (pl |
| Q10 | fait simple | oui | True | True | 21.2 | Selon les documents fournis dans le contexte, la part d'aluminium recyclé dans l |
| Q11 | fait simple | oui | True | True | 16.09 | D'après les informations fournies dans le contexte, le taux de recyclage des bat |
| Q12 | tableau | oui | True | True | 17.97 | Selon le contexte fourni, plus précisément dans la section intitulée **« Fournis |
| Q13 | tableau | oui | True | True | 24.16 | D'après les documents fournis, plus précisément la figure de la page 3 du rappor |
| Q14 | fait simple | oui | True | True | 22.8 | Selon les documents fournis, le taux de retour sous garantie est de **1,8 % des  |
| Q15 | scan | non | True | False | 32.71 | D'après les documents fournis, il n'est pas possible de connaître le prix unitai |
| Q16 | scan | non | True | False | 29.89 | D'après les documents fournis, il n'est pas possible de répondre à la question c |
| Q17 | scan | oui | False | False | 32.04 | D'après les documents fournis, il est impossible de répondre à cette question av |
| Q18 | scan | non | False | False | 70.27 | D'après les documents fournis, il n'est pas possible de déterminer le volume min |
| Q19 | fait simple | oui | True | True | 26.67 | D'après le contenu du document intitulé **"Procédure PR-SEC-04 — Charge et stock |
| Q20 | fait simple | oui | True | True | 22.44 | D'après les documents fournis, la personne responsable de la procédure de charge |
| Q21 | tableau | oui | True | True | 23.86 | D'après les documents fournis, plus précisément le contenu du fichier **`procedu |
| Q22 | fait simple | oui | True | True | 26.15 | Selon les documents fournis, le prix du modèle **Vilaine Compact** est de **2 49 |
| Q23 | fait simple | oui | True | True | 23.96 | Selon les documents fournis, la capacité prévue de l'usine de Saint-Nazaire est  |
| Q24 | tableau | non | True | True | 32.1 | D'après les documents fournis, voici la réponse détaillée :  **1. Quantité de st |
| Q25 | fait simple | oui | True | True | 19.08 | D'après le contenu fourni, spécifiquement dans le document **faq-sav.html (Page  |
| Q26 | fait simple | oui | True | True | 25.18 | D'après les documents fournis, le numéro de téléphone du service après-vente est |
| Q27 | fait simple | oui | True | True | 23.12 | D'après les documents fournis, le montant de la prime d'intéressement pour l'ann |
| Q28 | anglais | oui | True | True | 20.53 | D'après les informations fournies dans le contexte, Batterix GmbH a obtenu un sc |
| Q29 | anglais | oui | True | True | 30.17 | Selon les documents fournis dans le contexte, le taux de cellules défectueuses m |
| Q30 | multi-documents | non | False | False | 37.97 | Sur la base des documents fournis, il n'est pas possible de répondre à cette que |
| Q31 | multi-documents | non | False | True | 39.65 | D'après les documents fournis, voici les réponses détaillées :  **1. Score obten |
| Q32 | multi-documents | oui | True | True | 19.26 | D'après les documents fournis, voici les détails concernant les objectifs de Vél |
| Q33 | audio | non | False | False | 35.28 | Sur la base des documents fournis, je ne connais pas la réponse à cette question |
| Q34 | audio | non | False | False | 31.54 | D'après les documents fournis, je ne connais pas le nom du directeur de producti |
| Q35 | piège | oui | True | - | 38.21 | D'après les documents fournis dans le contexte, il n'est pas possible de connaît |
| Q36 | piège | oui | True | - | 27.98 | D'après les documents fournis, il est impossible de répondre à la question conce |
| Q37 | piège | oui | True | - | 37.85 | Sur la base des documents fournis, il n'est pas possible de connaître le nombre  |
| Q38 | piège | oui | True | - | 33.22 | D'après les documents fournis, il est impossible de déterminer le salaire exact  |
