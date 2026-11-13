"""Chapitre 13, En cas de problème : erreurs provoquées exprès et capturées.
Usage : lancer.sh outils/kotaemon/captures/c13_problemes.py [connexion] [cle] [format] [sans_recherche] [blocage] [contexte]"""
import shutil
from ui import Scenario, etapes, RACINE

CH = "13-problemes"


def connexion(s):
    c = Scenario(CH, connecter=False)
    try:
        p = c.page
        p.get_by_label("Username").first.fill("admin")
        p.get_by_label("Password").first.fill("mauvais-mot-de-passe")
        p.get_by_role("button", name="Login").click(); p.wait_for_timeout(1500)
        c.cap_souple("01-mot-de-passe-refuse", [(p.locator(".toast-body").first, "message d'erreur"), (c.bouton("Login"), "Login")], auto=True)
    finally:
        c.fermer()


def cle(s):
    p = s.page
    s.onglet("Resources"); s.onglet("LLMs"); s.onglet("Add")
    s.champ("LLM name").fill("essai-cle-fausse")
    s.choisir("LLM vendors", "ChatOpenAI")
    zone = p.locator("textarea").locator("visible=true").nth(1)
    zone.fill("api_key: cle-fausse\nbase_url: http://llm-central:8080/v1\nmodel: chat\ntimeout: 60\n")
    s.bouton("Add LLM").click(); p.wait_for_timeout(2500); s.sans_toasts()
    s.onglet("View")
    s.ligne("essai-cle-fausse").click(); p.wait_for_timeout(2000)
    s.texte("Test connection", exact=True).click(); p.wait_for_timeout(600)
    s.bouton("Test").click(); p.wait_for_timeout(8000)
    res = p.get_by_text("Connection failed").locator("visible=true").first
    s.note("clé fausse : " + (res.inner_text()[:400] if res.count() else "?"))
    s.cap_souple("02-cle-refusee", [(res, "Connection failed (clé refusée)")])
    s.bouton("Delete").click(); p.wait_for_timeout(800)
    s.bouton("Confirm Delete").click(); p.wait_for_timeout(2000)


def format(s):
    p = s.page
    s.onglet("Files"); s.onglet("File Collection"); s.onglet("Upload Files")
    try:
        s.deposer([RACINE / "corpus/documents/message-vocal-production.mp3"])
    except Exception as e:
        s.note(f"dépôt mp3 : {e}")
    s.bouton("Upload and Index").click(); p.wait_for_timeout(3000); s.attendre_fin()
    p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    infos = p.locator("textarea").locator("visible=true")
    s.note("après dépôt mp3 : toasts " + repr(s.toasts()) + " ; " + " | ".join(t.input_value()[:400] for t in infos.all()).replace("\n", " / "))
    s.sans_toasts()
    s.cap_souple("03-format-refuse", [(infos.first, "Upload result"), (infos.nth(1), "Upload info")])
    s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)
    # le fichier en échec reste inscrit dans la liste, sans passage : on le retire
    s.onglet("Files")
    s.ligne("message-vocal-production.mp3").click(); p.wait_for_timeout(2000)
    s.cap_souple("04-fichier-en-echec", [(s.ligne("message-vocal-production.mp3"), "message-vocal-production.mp3"),
                                         (s.texte("0 chunks"), "aucun passage"), (s.bouton("Delete"), "Delete")])
    s.bouton("Delete").click(); p.wait_for_timeout(2000)
    s.note("retrait du MP3 : toasts " + repr(s.toasts())); s.sans_toasts()


def sans_recherche(s):
    p = s.page
    s.onglet("Chat")
    s.nouvelle_conversation()
    s.reglage_session("Language", "French")
    s.poser("Quel est le prix public du modèle Erdre Cargo ?")
    s.note("sans recherche : " + p.locator("#main-chat-bot .message").last.inner_text()[:500].replace("\n", " ")
           + " ; panneau : " + p.locator("#html-info-panel").inner_text()[:200])
    s.cap_souple("05-sans-recherche", [(p.locator("#index-0"), "aucun choix (ni Search All ni Search In File(s))"),
                                       (p.locator("#main-chat-bot .message").last, "réponse sans document"),
                                       (p.locator("#html-info-panel"), "Information panel")])


def blocage(s):
    """« Use LLM relevant scoring » coché avec 10 passages : la réponse reste sur « Thinking ... »."""
    p = s.page
    s.onglet("Settings"); s.onglet("Retrieval settings")
    sc = p.get_by_label("Use LLM relevant scoring").locator("visible=true").first
    sc.check(); p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)
    s.onglet("Chat")
    s.onglet("Chat")
    s.nouvelle_conversation()
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    s.poser("Quel est le taux de retour sous garantie ?", envoyer=False).press("Enter")
    p.wait_for_timeout(120000)
    s.note("blocage : " + p.locator("#main-chat-bot .message").last.inner_text()[:200])
    s.cap_souple("06-reponse-bloquee", [(p.locator("#main-chat-bot .message").last, "Thinking ..."), (p.locator("#html-info-panel"), "passages trouvés")])
    s.onglet("Settings"); s.onglet("Retrieval settings")
    sc = p.get_by_label("Use LLM relevant scoring").locator("visible=true").first
    sc.uncheck(); p.locator("#save-setting-btn").click(); p.wait_for_timeout(2500)


def contexte(s):
    """Dépassement volontaire : une question de plus de 80 000 caractères (environ 20 000 jetons), au-delà des
    16 384 jetons du modèle chat et des 8 192 jetons par requête d'embed."""
    p = s.page
    s.onglet("Chat")
    s.nouvelle_conversation()
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    bloc = (RACINE / "corpus/documents/cse-2025-10-14.md").read_text()
    texte = "Résume ce texte : " + (bloc + "\n") * (82000 // len(bloc) + 1)
    s.note(f"question de {len(texte)} caractères")
    zone = p.locator("#chat-input textarea")
    zone.evaluate("(e, t) => { e.value = t; e.dispatchEvent(new Event('input', {bubbles: true})); }", texte)
    p.wait_for_timeout(1500)
    zone.press("Enter")
    s.attendre_reponse(delai=300, stable=4)
    s.note("dépassement : " + p.locator("#main-chat-bot .message").last.inner_text()[:300].replace("\n", " ")
           + " ; toasts " + repr(s.toasts()))
    s.cap_souple("07-depassement-contexte", [(p.locator("#main-chat-bot .message").last, "réponse"), (p.locator(".toast-body").first, "message d'erreur")])


if __name__ == "__main__":
    import sys
    if "connexion" in sys.argv[1:]:
        connexion(None)  # écran de connexion : navigateur sans session
    else:
        s = Scenario(CH)
        try:
            etapes([cle, format, sans_recherche, blocage, contexte], s)
        finally:
            s.fermer()
