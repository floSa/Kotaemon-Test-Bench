"""Chapitre 07, Régler la recherche et le raisonnement : réglages de recherche (mode, MMR, tableaux, tri, notation par
LLM et alerte de pertinence), méthodes de raisonnement (simple, complex), consignes (prompts), historique.
Usage : lancer.sh outils/kotaemon/captures/c07_reglages.py [recherche] [raisonnement] [consignes] [complexe] [alerte]"""
from ui import Scenario, etapes

CH = "07-reglages"


def recherche(s):
    p = s.page
    s.onglet("Settings"); s.onglet("Retrieval settings")
    mode = s.champ("Retrieval mode")
    mode.click(); p.wait_for_timeout(600)
    s.cap_souple("01-mode-recherche", [(mode, "Retrieval mode"), (p.get_by_role("option", name="hybrid").locator("visible=true").first, "hybrid"),
                                       (p.locator("label").filter(has_text="Prioritize table").locator("visible=true").first, "Prioritize table"),
                                       (p.locator("label").filter(has_text="Use MMR").locator("visible=true").first, "Use MMR")])
    p.keyboard.press("Escape")
    s.tab("GraphRAG Collection").click(); p.wait_for_timeout(1000)
    s.cap_souple("02-recherche-graphrag", [(s.tab("GraphRAG Collection"), "GraphRAG Collection"), (s.tab("LightRAG Collection"), "LightRAG Collection"),
                                           (s.champ("Search type"), "Search type")])


def raisonnement(s):
    p = s.page
    s.onglet("Settings"); s.onglet("Reasoning settings")
    opts = p.locator("fieldset").filter(has_text="Reasoning options").locator("visible=true").first
    s.cap_souple("03-methodes", [(opts, "Reasoning options"), (p.locator("label").filter(has_text="Create Mindmap").locator("visible=true").first, "Create Mindmap"),
                                 (p.locator("label").filter(has_text="Create Embeddings Visualization").locator("visible=true").first, "Create Embeddings Visualization"),
                                 (p.locator("label").filter(has_text="Use Multimodal Input").locator("visible=true").first, "Use Multimodal Input")])
    opts.get_by_text("complex", exact=True).click(); p.wait_for_timeout(1500)
    s.cap_souple("04-complex", [(opts.get_by_text("complex", exact=True), "complex"), (s.texte("Complex QA"), "Complex QA"),
                                (s.texte("Decompose Prompt", exact=True), "Decompose Prompt")])
    opts.get_by_text("simple", exact=True).click(); p.wait_for_timeout(1000)


def consignes(s):
    p = s.page
    s.onglet("Settings"); s.onglet("Reasoning settings")
    sysp = s.champ("System Prompt")
    sysp.scroll_into_view_if_needed(); p.wait_for_timeout(800)
    s.cap_souple("05-consignes", [(sysp, "System Prompt"), (s.champ("QA Prompt (contains {context}, {question}, {lang})"), "QA Prompt"),
                                  (s.champ("Number of interactions to include"), "Number of interactions to include"),
                                  (s.champ("Maximum message length for context rewriting"), "Maximum message length for context rewriting")])


def complexe(s):
    p = s.page
    p.locator("#new-conv-button").click(); p.wait_for_timeout(1500)
    s.reglage_session("Language", "French")
    meth = s.reglage_session("Reasoning method", "complex")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    s.cap_souple("06-methode-conversation", [(meth, "Reasoning method : complex"), (p.locator("#index-0").get_by_text("Search All", exact=True), "Search All")])
    s.poser("Quel est le délai de livraison contractuel de Batterix et quel délai moyen est réellement constaté lors de l'audit ?", stable=12)
    s.cap_souple("07-reponse-decomposee", [(p.locator("#main-chat-bot .message").last, "réponse"), (p.locator("#html-info-panel"), "Information panel")])
    s.note("réponse complex : " + p.locator("#main-chat-bot .message").last.inner_text()[:800].replace("\n", " "))


def alerte(s):
    """Notation par LLM avec 4 passages (le service central sert 4 requêtes à la fois) : alerte de faible pertinence."""
    p = s.page
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.champ("Number of document chunks to retrieve").fill("4")
    sc = p.get_by_label("Use LLM relevant scoring").locator("visible=true").first
    sc.check()
    s.cap_souple("08-notation-llm", [(s.champ("Number of document chunks to retrieve"), "Number of document chunks to retrieve : 4"),
                                     (p.locator("label").filter(has_text="Use LLM relevant scoring").locator("visible=true").first, "Use LLM relevant scoring"),
                                     (s.champ("LLM for relevant scoring"), "LLM for relevant scoring"), (p.locator("#save-setting-btn"), "Save & Close")])
    p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)
    s.onglet("Chat")
    p.locator("#new-conv-button").click(); p.wait_for_timeout(1500)
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    s.poser("Combien de trottinettes électriques Vélanor a-t-elle vendues en 2025 ?")
    warn = p.get_by_text("WARNING!").locator("visible=true").first
    s.cap_souple("09-alerte-pertinence", [(p.locator("#main-chat-bot .message").last, "réponse"), (warn, "alerte de faible pertinence")])
    s.note("alerte : " + p.locator("#html-info-panel").inner_text()[:600].replace("\n", " "))
    # retour aux réglages du chapitre 03
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.champ("Number of document chunks to retrieve").fill("10")
    sc = p.get_by_label("Use LLM relevant scoring").locator("visible=true").first
    sc.uncheck()
    p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([recherche, raisonnement, consignes, complexe, alerte], s)
    finally:
        s.fermer()
