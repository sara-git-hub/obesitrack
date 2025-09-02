from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .config import settings
from .deps import get_db, Base, engine
from .routes import auth, predictions, admin


# Création de l'application FastAPI
app = FastAPI(
    title="ObesiTrack API",
    version="1.0",
    description="API de prédiction et gestion utilisateurs"
)

# Création de la base de données et des tables si elles n'existent pas
Base.metadata.create_all(bind=engine)  

# Inclusion des routeurs
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(predictions.router, prefix="/predict", tags=["predictions"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# Endpoint de 
@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "error"
    return {"status": "ok", "db": db_status}
