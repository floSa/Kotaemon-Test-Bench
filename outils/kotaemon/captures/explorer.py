"""Repérage : se connecte, ouvre chaque onglet indiqué (chemin « Onglet/Sous-onglet/... »), enregistre une capture brute
(donnees/repere/, ignoré par git) et le texte visible. Usage : explorer.py [--sans-connexion] "Chat" "Resources/LLMs" ..."""
import sys
from pathlib import Path
from ui import Scenario

args = [a for a in sys.argv[1:] if not a.startswith("--")]
s = Scenario("repere", connecter="--sans-connexion" not in sys.argv)
out = Path("donnees/repere"); out.mkdir(parents=True, exist_ok=True)
try:
    for chemin in args or [""]:
        for nom in [x for x in chemin.split("/") if x]:
            s.onglet(nom)
        f = out / (chemin.replace("/", "_") or "accueil")
        s.page.screenshot(path=str(f) + ".png")
        txt = s.page.locator("body").inner_text()
        Path(str(f) + ".txt").write_text(txt)
        print("=====", chemin, len(txt)); print(txt[:2500])
finally:
    s.fermer()
