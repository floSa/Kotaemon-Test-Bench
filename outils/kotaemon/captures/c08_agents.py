"""Chapitre 08, Agents ReAct et ReWOO : réglages des agents, question posée à chaque agent, serveurs MCP (formulaire).
Usage : lancer.sh outils/kotaemon/captures/c08_agents.py [reglages] [react] [rewoo] [mcp]"""
from ui import Scenario, etapes

CH = "08-agents"
QUESTION = "Quel est le délai de livraison contractuel de Batterix et quel délai moyen est réellement constaté lors de l'audit ?"


def reglages(s):
    p = s.page
    s.onglet("Settings"); s.onglet("Reasoning settings")
    opts = p.locator("div.block").filter(has=p.get_by_text("Reasoning options", exact=True)).locator("visible=true").last
    opts.get_by_text("ReAct", exact=True).click(); p.wait_for_timeout(1500)
    s.cap_souple("01-reglages-react", [(opts.get_by_text("ReAct", exact=True), "ReAct"), (s.champ("Language model"), "Language model"),
                                       (s.bloc("Tools for knowledge retrieval"), "Tools for knowledge retrieval"),
                                       (s.champ("Maximum number of iterations the LLM can go through"), "Maximum number of iterations the LLM can go through")])
    opts.get_by_text("ReWOO", exact=True).click(); p.wait_for_timeout(1500)
    s.cap_souple("02-reglages-rewoo", [(opts.get_by_text("ReWOO", exact=True), "ReWOO"), (s.champ("Language model for Planner"), "Language model for Planner"),
                                       (s.champ("Language model for Solver"), "Language model for Solver"),
                                       (p.locator("label").filter(has_text="Highlight Citation").locator("visible=true").first, "Highlight Citation"),
                                       (s.bloc("Tools for knowledge retrieval"), "Tools for knowledge retrieval")])
    s.note("réglages agents : " + p.locator("body").inner_text()[:1500].replace("\n", " | "))
    opts.get_by_text("simple", exact=True).click(); p.wait_for_timeout(800)


def agent(s, nom, cap):
    p = s.page
    p.locator("#new-conv-button").click(); p.wait_for_timeout(1500)
    s.reglage_session("Language", "French")
    s.reglage_session("Reasoning method", nom)
    p.locator("#index-0").get_by_text("Search All", exact=True).click()
    import time; t0 = time.time()
    s.poser(QUESTION)
    s.note(f"{nom} : {time.time() - t0:.0f} s ; réponse : " + p.locator("#main-chat-bot .message").last.inner_text()[:700].replace("\n", " "))
    s.note(f"{nom} panneau : " + p.locator("#html-info-panel").inner_text()[:1200].replace("\n", " | "))
    s.cap_souple(cap, [(p.locator("#main-chat-bot .message").last, "réponse de l'agent"), (p.locator("#html-info-panel"), "étapes et sources")])


def react(s):
    agent(s, "ReAct", "03-reponse-react")


def rewoo(s):
    agent(s, "ReWOO", "04-reponse-rewoo")


def mcp(s):
    p = s.page
    s.onglet("Resources"); s.onglet("MCP Servers"); s.onglet("Add")
    s.cap_souple("05-mcp-ajouter", [(s.tab("MCP Servers"), "MCP Servers"), (s.tab("Add"), "Add"),
                                    (p.locator(".cm-editor, textarea").locator("visible=true").first, "Configuration (JSON)"),
                                    (s.bouton("Add MCP Servers"), "Add MCP Servers")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([reglages, react, rewoo, mcp], s)
    finally:
        s.fermer()
