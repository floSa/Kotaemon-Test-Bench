"""Chapitre 03, Premiers pas : connexion, écran principal, changement du mot de passe admin, déclaration des modèles
du service LLM central (chat, embed, rerank) dans Resources, réglages de raisonnement (langue, contexte).
Usage : lancer.sh outils/kotaemon/captures/c03_premiers_pas.py [connexion] [ecran] [mot_de_passe] [llm] [embedding] [reranking] [tests] [reglages]
"""
import os, re
from ui import Scenario, etapes, identifiants, URL_CENTRAL, IDENT

CH = "03-premiers-pas"
CLE = os.environ["LLM_CENTRAL_KEY"]
SPEC_CHAT = f"""api_key: {CLE}
base_url: {URL_CENTRAL}
model: chat
temperature: 0
max_tokens: 6144
timeout: 600
"""
SPEC_EMBED = f"""api_key: {CLE}
base_url: {URL_CENTRAL}
model: embed
timeout: 120
"""
SPEC_RERANK = f"""cohere_api_key: {CLE}
base_url: http://llm-central:8080
model_name: rerank
"""


def connexion(s):
    p = s.page
    s.cap("01-connexion", [(p.get_by_label("Username").first, "Username"), (p.get_by_label("Password").first, "Password"),
                           (s.bouton("Login"), "Login")])


def ecran(s):
    p = s.page
    s.connecter()
    s.cap("02-ecran-principal", [(p.locator(".tab-nav").first, "barre des onglets"),
                                 (p.locator("#conv-settings-panel"), "Conversations et documents"),
                                 (p.locator("#main-chat-bot"), "zone de discussion"),
                                 (p.locator("#chat-input"), "zone de saisie"),
                                 (p.locator("#chat-settings-expand"), "Chat settings"),
                                 (p.locator("#chat-info-panel"), "Information panel")])


def mot_de_passe(s):
    p = s.page
    s.connecter()
    s.onglet("Settings")
    nouveau = identifiants()["kotaemon.admin.mot_de_passe_nouveau"]
    s.champ("New password").fill(nouveau)
    s.champ("Confirm password").fill(nouveau)
    s.cap("03-changer-mot-de-passe", [(s.tab("User settings"), "User settings"), (s.champ("New password"), "New password"),
                                      (s.champ("Confirm password"), "Confirm password"),
                                      (s.bouton("Change password"), "Change password"),
                                      (s.bouton("Logout"), "Logout")])
    s.bouton("Change password").click(); p.wait_for_timeout(2500)
    s.note("mot de passe : toasts " + repr(s.toasts()))
    txt = IDENT.read_text()
    if "kotaemon.admin.mot_de_passe=" not in txt:
        IDENT.write_text(txt + f"kotaemon.admin.mot_de_passe={nouveau}\n")


def ajouter(s, onglet, nom_champ, nom, vendeur_champ, vendeur, spec, bouton, prefixe, defaut=True):
    p = s.page
    s.connecter()
    s.onglet("Resources"); s.onglet(onglet); s.onglet("Add")
    s.champ(nom_champ).fill(nom)
    s.choisir(vendeur_champ, vendeur)
    p.wait_for_timeout(1500)
    zone = p.locator("textarea").locator("visible=true").nth(1)
    s.cap_souple(f"{prefixe}a-{onglet.lower()}-ajouter", [(s.tab(onglet), onglet), (s.tab("Add"), "Add"),
                                                 (s.champ(nom_champ), nom_champ), (s.champ(vendeur_champ), vendeur_champ),
                                                 (zone, "Specification"), (p.locator("table").locator("visible=true").last, "tableau des paramètres")])
    zone.fill(spec)
    if defaut:
        p.get_by_label("Set default").locator("visible=true").first.check()
    s.cap(f"{prefixe}b-{onglet.lower()}-specification", [(zone, "Specification"),
                                                        (p.locator("label").filter(has_text="Set default").locator("visible=true").first, "Set default"),
                                                        (s.bouton(bouton), bouton)])
    s.bouton(bouton).click(); p.wait_for_timeout(3000)
    s.note(f"{onglet} ajout {nom} : toasts {s.toasts()!r}")


def verifier(s, onglet, nom, prefixe, detail=False):
    """Onglet View : sélectionne la ligne (capture de la fiche si detail), ouvre « Test connection », lance le test."""
    p = s.page
    s.onglet("View")
    ligne = s.ligne(nom)
    ligne.click(); p.wait_for_timeout(2500)
    if detail:
        s.cap(f"{prefixe}c-{onglet.lower()}-fiche", [(s.tab("View"), "View"), (ligne, nom),
                                                   (s.texte("Set default", exact=True), "Set default"),
                                                   (p.locator("textarea").locator("visible=true").nth(1), "Specification")])
    acc = s.texte("Test connection", exact=True)
    acc.click(); p.wait_for_timeout(800)
    s.bouton("Test").click()
    try:
        p.get_by_text(re.compile("Connection (success|failed)")).locator("visible=true").first.wait_for(timeout=180000)
    except Exception:
        s.note(f"{onglet} : pas de résultat de test")
    p.wait_for_timeout(1000)
    res = p.get_by_text(re.compile("Connection (success|failed)")).locator("visible=true").first
    s.note(f"{onglet} test {nom} : {res.inner_text()[:300] if res.count() else '?'}")
    s.sans_toasts()
    s.cap(f"{prefixe}d-{onglet.lower()}-tester", [(acc, "Test connection"), (s.bouton("Test"), "Test"),
                                                (res, "résultat du test"), (s.bouton("Save"), "Save"),
                                                (s.bouton("Delete"), "Delete"), (s.bouton("Close"), "Close")])


def llm(s):
    ajouter(s, "LLMs", "LLM name", "llm-service-chat", "LLM vendors", "ChatOpenAI", SPEC_CHAT, "Add LLM", "04")


def embedding(s):
    ajouter(s, "Embeddings", "Name", "llm-service-embed", "Vendors", "OpenAIEmbeddings", SPEC_EMBED, "Add", "05")


def reranking(s):
    ajouter(s, "Rerankings", "Name", "llm-service-rerank", "Vendors", "CohereReranking", SPEC_RERANK, "Add", "06")


def tests(s):
    s.connecter(); s.onglet("Resources")
    for onglet, nom, pre in (("LLMs", "llm-service-chat", "04"), ("Embeddings", "llm-service-embed", "05"),
                             ("Rerankings", "llm-service-rerank", "06")):
        s.onglet(onglet)
        verifier(s, onglet, nom, pre, detail=(onglet == "LLMs"))


def reglages(s):
    p = s.page
    s.connecter()
    s.onglet("Settings"); s.onglet("Reasoning settings")
    s.choisir("Language", "French")
    ctx = s.champ("Max context length (LLM)")
    ctx.fill("8000")
    s.choisir("Language model", "llm-service-chat")
    s.cap("07-reglages-raisonnement", [(s.tab("Reasoning settings"), "Reasoning settings"), (s.champ("Language"), "Language"),
                                       (ctx, "Max context length (LLM)"), (s.champ("Language model"), "Language model"),
                                       (p.locator("#save-setting-btn"), "Save & Close")])
    p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)
    s.note("réglages raisonnement : toasts " + repr(s.toasts()))
    s.onglet("Settings"); s.onglet("Retrieval settings")
    s.choisir("LLM for relevant scoring", "llm-service-chat")
    # notation par LLM : un appel par passage, en parallèle (10 par défaut) ; le service central en sert 4 à la fois
    # et répond 429 au-delà, la réponse reste alors bloquée sur « Thinking ... » (incident-2026-11-12-429-score-llm.log)
    score = p.get_by_label("Use LLM relevant scoring").locator("visible=true").first
    if score.is_checked():
        score.uncheck()
    s.cap("08-reglages-recherche", [(s.tab("Retrieval settings"), "Retrieval settings"), 
                                    (s.champ("File loader"), "File loader"),
                                    (s.champ("Number of document chunks to retrieve"), "Number of document chunks to retrieve"),
                                    (p.locator("label").filter(has_text="Use reranking").locator("visible=true").first, "Use reranking"),
                                    (p.locator("label").filter(has_text="Use LLM relevant scoring").locator("visible=true").first, "Use LLM relevant scoring"),
                                    (p.locator("#save-setting-btn"), "Save & Close")])
    p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)
    s.note("réglages recherche : toasts " + repr(s.toasts()))


if __name__ == "__main__":
    import sys
    s = Scenario(CH, connecter=False)
    try:
        etapes([connexion, ecran, mot_de_passe, llm, embedding, reranking, tests, reglages], s)
    finally:
        s.fermer()
