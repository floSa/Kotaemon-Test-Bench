# Banc Kotaemon — docling-scan-rerank — 2026-11-12T22:31:44

| Mesure | Valeur |
|---|---|
| questions | 6 |
| exactes | 5 |
| sur | 6 |
| refus_corrects | 0 |
| pieges | 0 |
| citation_bon_document | 6 |
| citation_bonne_page | 6 |
| citations_avec_page | 6 |
| juge_llm_oui | 5 |
| juge_llm_sur | 6 |
| erreurs | 0 |
| latence_p50_s | 23.44 |
| latence_p95_s | 39.86 |
| par_type | {'scan': '4/4', 'multi-documents': '1/2'} |
| pic_ram_mo | {'rag-kotaemon': 1634, 'llm-central': 737, 'llm-swap': 5685, 'llm-speaches': 1323} |
| pic_ram_application_mo | 1634 |
| vram | 8906 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | None |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q15 | scan | oui | True | True | 22.96 | Selon les documents fournis, le prix unitaire des batteries prévu par le contrat |
| Q16 | scan | oui | True | True | 17.91 | Selon le contexte fourni, le délai de livraison prévu par le contrat Batterix es |
| Q17 | scan | oui | True | True | 25.19 | D'après les documents fournis, le plafond des pénalités de retard du contrat Bat |
| Q18 | scan | oui | True | True | 23.44 | Selon les documents fournis, le volume minimal annuel prévu par le contrat Batte |
| Q30 | multi-documents | non | False | True | 39.86 | D'après les documents fournis, voici la réponse détaillée concernant le délai de |
| Q31 | multi-documents | oui | True | True | 24.65 | Selon les documents fournis dans le contexte, voici les réponses détaillées :  * |
