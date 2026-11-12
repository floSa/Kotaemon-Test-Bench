"""Chapitre 11, Comptes et partage : créer un compte, le modifier, se connecter avec, collections privées et partagées,
conversation partagée, déconnexion.
Usage : lancer.sh outils/kotaemon/captures/c11_comptes.py [creer] [liste] [partager] [utilisateur]"""
from ui import Scenario, etapes, identifiants, IDENT

CH = "11-comptes"


def creer(s):
    p = s.page
    s.onglet("Resources"); s.onglet("Users"); s.onglet("Create user")
    mdp = identifiants()["kotaemon.camille.mot_de_passe"]
    s.champ("Username").fill("camille")
    s.champ("Password").fill(mdp)
    s.champ("Confirm password").fill(mdp)
    s.cap_souple("01-creer-compte", [(s.tab("Users"), "Users"), (s.tab("Create user"), "Create user"), (s.champ("Username"), "Username"),
                                     (s.champ("Password"), "Password"), (s.champ("Confirm password"), "Confirm password"),
                                     (s.bouton("Create user"), "Create user")])
    s.bouton("Create user").click(); p.wait_for_timeout(2500)
    s.note("création : toasts " + repr(s.toasts()))


def liste(s):
    p = s.page
    s.onglet("Resources"); s.onglet("Users"); s.onglet("User list")
    s.ligne("camille").click(); p.wait_for_timeout(2000)
    s.cap_souple("02-fiche-compte", [(s.ligne("camille"), "camille"), (s.champ("Change password"), "Change password"),
                                     (p.locator("label").filter(has_text="Admin").locator("visible=true").first, "Admin"),
                                     (s.bouton("Save"), "Save"), (s.bouton("Delete"), "Delete")])
    s.bouton("Close").click(); p.wait_for_timeout(800)


def partager(s):
    """Admin : ajoute la note CSE dans la collection partagée et partage une conversation."""
    p = s.page
    from ui import RACINE
    s.onglet("Files"); s.onglet("Documents partagés"); s.onglet("Upload Files")
    s.deposer([RACINE / "corpus/documents/cse-2025-10-14.md"])
    s.bouton("Upload and Index").click(); p.wait_for_timeout(3000); s.attendre_fin()
    p.get_by_text("Upload Progress").locator("visible=true").first.wait_for()
    s.sans_toasts()
    s.bouton("Clear Upload Info and Close").click(); p.wait_for_timeout(1500)
    s.cap_souple("03-collection-partagee", [(s.tab("Documents partagés"), "Documents partagés"), (s.ligne("cse-2025-10-14.md"), "cse-2025-10-14.md")])
    s.onglet("Chat")
    p.locator("#new-conv-button").click(); p.wait_for_timeout(1500)
    s.reglage_session("Language", "French")
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    s.poser("Qui est la présidente de Vélanor ?")
    acc = p.locator("#report-accordion")
    acc.get_by_text("Feedback").first.click(); p.wait_for_timeout(800)
    p.locator("#is-public-checkbox input").check(); p.wait_for_timeout(2000)
    s.note("partage : toasts " + repr(s.toasts())); s.sans_toasts()
    s.cap_souple("04-partager-conversation", [(p.locator("#is-public-checkbox"), "Share this conversation"),
                                              (p.locator("#conversation-dropdown"), "conversation partagée")])


def utilisateur(s):
    """Session de camille : onglets visibles, collection privée vide, collection partagée, conversation partagée."""
    s.page.locator("#settings-tab-button").click() if False else None
    c = Scenario(CH, utilisateur="camille", mot_de_passe=identifiants()["kotaemon.camille.mot_de_passe"])
    try:
        p = c.page
        c.cap_souple("05-ecran-utilisateur", [(p.locator(".tab-nav").first, "onglets (sans Resources)"),
                                              (p.locator("#index-0"), "File Collection (privée)"),
                                              (p.get_by_text("Documents partagés").locator("visible=true").first, "Documents partagés")])
        c.onglet("Files"); c.onglet("File Collection")
        c.cap_souple("06-collection-privee-vide", [(c.tab("File Collection"), "File Collection"), (p.locator("table.table").locator("visible=true").first, "liste vide")])
        c.onglet("Chat")
        dd = p.locator("#conversation-dropdown input"); dd.click(); p.wait_for_timeout(1000)
        c.cap_souple("07-conversation-partagee-vue", [(dd, "liste des conversations"), (p.get_by_role("option").locator("visible=true").first, "conversation partagée par admin")])
        p.keyboard.press("Escape")
        c.onglet("Settings")
        c.cap_souple("08-deconnexion", [(c.texte("Current user: camille"), "Current user"), (c.bouton("Logout"), "Logout")])
        c.bouton("Logout").click(); p.wait_for_timeout(2500)
        c.note("déconnexion : " + p.locator("body").inner_text()[:200].replace("\n", " "))
    finally:
        c.fermer()


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([creer, liste, partager, utilisateur], s)
    finally:
        s.fermer()
