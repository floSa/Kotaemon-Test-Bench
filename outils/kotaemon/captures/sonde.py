"""Sonde de repérage (développement des scénarios) : ouvre un chemin d'onglets et liste les champs visibles.
Usage : sonde.py "Resources/LLMs/Add" """
import sys
from ui import Scenario
s = Scenario("repere")
try:
    for chemin in sys.argv[1:]:
        for nom in chemin.split("/"):
            s.onglet(nom)
        print("=====", chemin)
        print(s.page.evaluate("""() => [...document.querySelectorAll('input, textarea, button, select, .cm-content, [role=listbox], label')]
          .filter(e => e.offsetParent && e.getBoundingClientRect().width > 0)
          .map(e => e.tagName + '|' + (e.type||'') + '|' + (e.getAttribute('aria-label')||'') + '|' + (e.innerText||e.value||e.placeholder||'').slice(0,80).replace(/\\n/g,' ') + '|' + (e.id||'') + '|' + Math.round(e.getBoundingClientRect().x)+','+Math.round(e.getBoundingClientRect().y))
          .join('\\n')"""))
        s.page.screenshot(path="donnees/repere/sonde.png")
finally:
    s.fermer()
