# Banc Kotaemon — docling-deporte-rerank-serre-top3 — 2026-11-13T21:53:05

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 29 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 32 |
| citation_bonne_page | 24 |
| citations_avec_page | 25 |
| juge_llm_oui | 33 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 18.38 |
| latence_p95_s | 27.34 |
| par_type | {'tableau': '8/10', 'fait simple': '13/13', 'scan': '4/4', 'anglais': '2/2', 'multi-documents': '2/3', 'audio': '0/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-kotaemon': 2409, 'rag-docling-serve': 2524, 'llm-central': 721, 'llm-swap': 7707, 'llm-speaches': 1371} |
| pic_ram_application_mo | 4933 |
| vram | 10620 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 28.2 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 17.11 | Le chiffre d'affaires de Vélanor en 2025 est de **48,6 M€**.  **Explication :**  |
| Q02 | fait simple | oui | True | True | 15.81 | Selon les documents fournis, Vélanor a été fondée en **2014**.  Cette informatio |
| Q03 | fait simple | oui | True | True | 17.73 | D'après les documents fournis, la présidente de Vélanor est **Hélène Marchais**. |
| Q04 | fait simple | oui | True | True | 19.01 | D'après les documents fournis, l'adresse du siège de Vélanor est la suivante :   |
| Q05 | tableau | oui | True | True | 16.83 | Vélanor compte **412 salariés** au 31 décembre 2025.  **Explication :** Cette in |
| Q06 | tableau | oui | True | True | 18.37 | Le chiffre d'affaires du troisième trimestre 2025 a été de **14,2 M€**.  **Expli |
| Q07 | tableau | oui | True | True | 19.07 | Selon le contexte fourni, **15 400 unités** du modèle Sèvre Trail ont été produi |
| Q08 | tableau | oui | True | True | 13.49 | Le prix public TTC du modèle Erdre Cargo est de **4 290 €**.  **Explication :**  |
| Q09 | tableau | oui | True | True | 14.25 | Selon le tableau fourni dans le document `rapport-annuel-2025.pdf` (Page 6), il  |
| Q10 | fait simple | oui | True | True | 14.35 | La part d'aluminium recyclé dans les cadres est de **82 %**.  **Explication :**  |
| Q11 | fait simple | oui | True | True | 15.3 | D'après les informations fournies dans le document « rapport-annuel-2025.pdf » ( |
| Q12 | tableau | oui | True | True | 12.78 | Selon le tableau fourni dans le contexte (page 8), le fournisseur des moteurs es |
| Q13 | tableau | non | False | True | 24.68 | D'après les extraits de contexte fournis, je ne connais pas le résultat net déga |
| Q14 | fait simple | oui | True | True | 20.66 | D'après les informations fournies dans le contexte, le taux de retour sous garan |
| Q15 | scan | oui | True | True | 14.3 | Selon le contenu du document « contrat-batterix-scan.pdf » (Page 1), plus précis |
| Q16 | scan | oui | True | True | 16.86 | Selon le contenu du contrat fourni, le délai de livraison prévu par le contrat B |
| Q17 | scan | oui | True | True | 14.61 | D'après les informations fournies dans le document `contrat-batterix-scan.pdf`,  |
| Q18 | scan | oui | True | True | 19.31 | Selon les documents fournis, le contrat Batterix prévoit un volume minimal annue |
| Q19 | fait simple | oui | True | True | 19.2 | Selon le document de procédure PR-SEC-04 (« Charge et stockage des batteries »), |
| Q20 | fait simple | oui | True | True | 14.58 | Selon le contenu du document intitulé **procedure-batteries.docx**, la personne  |
| Q21 | tableau | oui | True | True | 12.26 | Selon le document « procedure-batteries.docx », spécifiquement dans la section i |
| Q22 | fait simple | oui | True | True | 19.7 | Selon les informations fournies dans le contexte, le prix du modèle **Vilaine Co |
| Q23 | fait simple | oui | True | True | 18.38 | La capacité prévue de l'usine de Saint-Nazaire est de **25 000 vélos par an**.   |
| Q24 | tableau | non | False | True | 97.32 |  |
| Q25 | fait simple | oui | True | True | 23.84 | Selon le document fourni, plus précisément dans le fichier **faq-sav.html (Page  |
| Q26 | fait simple | oui | True | True | 17.79 | D'après le contenu fourni dans le fichier `faq-sav.html`, le numéro de téléphone |
| Q27 | fait simple | oui | True | True | 18.88 | Le montant de la prime d'intéressement 2025 est de **1 150 euros par salarié**.  |
| Q28 | anglais | oui | True | True | 19.47 | D'après les informations fournies dans le document "supplier-audit-batterix-en.p |
| Q29 | anglais | oui | True | True | 18.22 | D'après les informations fournies dans le document « supplier-audit-batterix-en. |
| Q30 | multi-documents | non | False | True | 23.61 | D'après les extraits de contrat fournis, voici la réponse détaillée :  **1. Déla |
| Q31 | multi-documents | oui | True | True | 18.38 | D'après les documents fournis, voici les réponses détaillées :  **1. Score obten |
| Q32 | multi-documents | oui | True | True | 21.05 | D'après les documents fournis, voici les détails concernant les objectifs de Vél |
| Q33 | audio | non | False | False | 26.02 | D'après les documents fournis, je ne connais pas la réponse à cette question.  V |
| Q34 | audio | non | False | False | 26.69 | D'après les documents fournis, je ne connais pas l'identité du directeur de prod |
| Q35 | piège | oui | True | - | 15.63 | Je ne peux pas répondre à cette question avec les informations fournies dans le  |
| Q36 | piège | oui | True | - | 29.48 | D'après les documents fournis, je ne connais pas le nom du directeur financier d |
| Q37 | piège | oui | True | - | 27.34 | D'après les informations fournies dans le rapport annuel 2025, il n'est pas poss |
| Q38 | piège | oui | True | - | 22.69 | Je ne connais pas le salaire de Karim Benali d'après les informations fournies.  |
