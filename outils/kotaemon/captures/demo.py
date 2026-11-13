"""Jeu de démonstration (kit/PROMPT.md, phase H) : par l'interface, retire les conversations d'essai du compte admin et
les fichiers d'essai des collections en graphe en échec (GraphRAG, NanoGraphRAG), puis crée trois conversations citées
« Démo — … » sur « File Collection ». Usage : lancer.sh outils/kotaemon/captures/demo.py [menage] [conversations]"""
from ui import Scenario, etapes

CH = "demo"
DEMOS = [("Démo — Chiffre d'affaires 2025", "Quel est le chiffre d'affaires 2025 de Vélanor et comment se répartit-il par trimestre ?"),
         ("Démo — Contrat Batterix", "Quel est le prix unitaire des batteries prévu par le contrat avec Batterix ?"),
         ("Démo — Garantie et SAV", "Quelle est la durée de garantie du cadre et quel numéro appeler pour le service après-vente ?")]


GARDER = ("Démo",)


def menage(s):
    """Supprime les conversations du compte admin, sauf celles dont le nom commence par « Démo » et la dernière
    conversation partagée (chapitre 11), passée en argument --garder « nom »."""
    import sys
    p = s.page
    garder = list(GARDER) + [a for a in sys.argv[1:] if a.startswith("Untitled")]
    n = 0
    for _ in range(60):
        dd = p.locator("#conversation-dropdown input")
        dd.click(); p.wait_for_timeout(800)
        opts = [o for o in p.get_by_role("option").locator("visible=true").all()
                if not any(g in o.inner_text().strip() for g in garder)]
        if not opts:
            p.keyboard.press("Escape"); break
        opts[0].click(); p.wait_for_timeout(1500)
        p.locator("#conv-settings-panel img[src*='delete']").locator("..").locator("visible=true").first.click()
        p.wait_for_timeout(600)
        s.bouton("Delete").click(); p.wait_for_timeout(1500)
        n += 1
    s.note(f"conversations d'essai supprimées : {n}")
    if "conversations" not in sys.argv[1:] and len(sys.argv) > 1:
        return
    for coll in ("GraphRAG Collection", "NanoGraphRAG Collection"):
        s.onglet("Files"); s.onglet(coll); s.onglet("Files")
        for _ in range(5):
            l = p.locator("table.table td").filter(has_text="procedure-batteries.docx").locator("visible=true")
            if not l.count():
                break
            l.first.click(); p.wait_for_timeout(1500)
            s.bouton("Delete").click(); p.wait_for_timeout(2000)
        s.note(f"{coll} : fichiers d'essai retirés ; toasts {s.toasts()!r}")
    s.onglet("Chat")


def conversations(s):
    p = s.page
    for nom, q in DEMOS:
        s.nouvelle_conversation()
        s.reglage_session("Language", "French")
        p.locator("#index-0").get_by_text("Search All", exact=True).click()
        s.poser(q, stable=6)
        p.wait_for_timeout(30000)
        p.locator("#conv-settings-panel img[src*='rename']").locator("..").locator("visible=true").first.click()
        p.wait_for_timeout(600)
        champ = p.get_by_placeholder("Conversation name").locator("visible=true").first
        champ.fill(nom); champ.press("Enter"); p.wait_for_timeout(2000)
        s.note(f"{nom} : " + p.locator("#main-chat-bot .message").last.inner_text()[:300].replace("\n", " "))
    s.cap("01-demo", [(p.locator("#conversation-dropdown"), "conversation de démonstration"),
                      (p.locator("#main-chat-bot .message").last, "réponse"), (p.locator("#html-info-panel"), "sources")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([menage, conversations], s)
    finally:
        s.fermer()
