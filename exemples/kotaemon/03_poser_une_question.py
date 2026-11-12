"""Pose une question à « File Collection » avec les réglages enregistrés dans l'interface par le compte admin, et
affiche la réponse et les pages citées (même chemin que le bouton d'envoi du chat, sans l'interface)."""
import os, re, sys
os.chdir("/app"); sys.path.insert(0, "/app")
from sqlmodel import Session, select
from ktem.app import BaseApp
from ktem.components import reasonings
from ktem.db.models import User, Settings, engine

QUESTION = "Quel est le prix unitaire des batteries prévu par le contrat avec Batterix ?"
app = BaseApp()
with Session(engine) as s:
    uid = s.exec(select(User).where(User.username == "admin")).one().id
    reglages = app.default_settings.flatten()
    reglages.update(s.exec(select(Settings).where(Settings.user == uid)).first().setting)
idx = app.index_manager.indices[0]
pref = f"index.options.{idx.id}."
with Session(engine) as s:
    ids = [i for (i,) in s.execute(select(idx._resources["Source"].id).where(idx._resources["Source"].user == uid)).all()]
r = idx._retriever_pipeline_cls[0].get_pipeline({k[len(pref):]: v for k, v in reglages.items() if k.startswith(pref)}, idx.config, ids)
r.Source, r.Index, r.VS, r.DS, r.FSPath, r.user_id = idx._resources["Source"], idx._resources["Index"], idx._vs, idx._docstore, idx._fs_path, uid
qa = reasonings[reglages["reasoning.use"]].get_pipeline(reglages, {"app": {"regen": False}, "pipeline": {}}, [r])
reponse, info = "", ""
for d in qa.stream(QUESTION, conv_id="", history=[]):
    if d.channel == "chat":
        reponse = "" if d.content is None else reponse + d.content
    elif d.channel == "info" and d.content:
        info += str(d.content)
print("Question :", QUESTION)
print("Réponse :", reponse.strip()[:400])
print("Sources :", sorted(set(re.findall(r"\[Page \d+\] [\w.-]+\.pdf", re.sub(r"<[^>]+>", " ", info)))))
