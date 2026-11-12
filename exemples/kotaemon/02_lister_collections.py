"""Liste les collections de Kotaemon, leurs fichiers et le nombre de passages de chacun (lecture seule de la base)."""
import os, sys
os.chdir("/app"); sys.path.insert(0, "/app")
from sqlmodel import Session, select
from ktem.app import BaseApp
from ktem.db.models import engine

app = BaseApp()
for idx in app.index_manager.indices:
    Source, Index = idx._resources["Source"], idx._resources["Index"]
    with Session(engine) as s:
        fichiers = s.execute(select(Source.id, Source.name)).all()
        print(f"{idx.id}. {idx.name} ({type(idx).__name__}, privée : {idx.config.get('private', False)}) : {len(fichiers)} fichier(s)")
        for fid, nom in sorted(fichiers, key=lambda x: x[1]):
            n = len(s.execute(select(Index.id).where(Index.source_id == fid)).all())
            print(f"   - {nom} : {n} élément(s) indexé(s)")
