from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from pathlib import Path
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from fastapi.templating import Jinja2Templates


from .config import settings
from .deps import get_db, engine
from .models import Base
from .routes import auth, predictions, admin,web,admin_web

# App FastAPI
app = FastAPI(
    title="ObesiTrack API",
    version="1.0",
    description="API de prédiction et gestion utilisateurs pour l'obésité"
)

# Création des tables
Base.metadata.create_all(bind=engine)

# Fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Routes
app.include_router(auth.router)
app.include_router(predictions.router)
app.include_router(admin.router)
app.include_router(admin_web.router)
app.include_router(web.router)

# Endpoints généraux
@app.get("/", tags=["general"])
def root():
    return {
        "message": "ObesiTrack API is running!",
        "version": "1.0",
        "docs_url": "/docs",
        "status": "operational"
    }

@app.get("/health", tags=["general"])
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "database": db_status, "version": "1.0"}

@app.get("/metrics", tags=["model"])
def get_model_metrics():
    try:
        metrics_path = Path("ml/data/metrics.json")
        if not metrics_path.exists():
            return {"status": "metrics_not_found", "message": "Fichier de métriques non trouvé."}
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        model_path = Path(settings.MODEL_PATH)
        return {
            "model_info": {
                "algorithm": metrics.get("algo", "Unknown"),
                "accuracy": metrics.get("accuracy", 0),
                "training_date": metrics.get("date", "Unknown"),
                "train_size": metrics.get("train_size", 0),
                "test_size": metrics.get("test_size", 0),
                "classes_count": metrics.get("classes", 0)
            },
            "model_status": {
                "model_file_exists": model_path.exists(),
                "model_path": str(model_path),
                "metrics_file_exists": True
            },
            "api_info": {"version": "1.0", "status": "operational"}
        }
    except Exception as e:
        return {"status": "error", "message": f"Erreur lors de la lecture des métriques: {str(e)}"}
    

# Lancer l'application
#uvicorn api.main:app --reload
#netstat -aon | findstr :8000
#tasklist | findstr uvicorn
#taskkill /PID <PID> /F
#python -m uvicorn api.main:app --reload --port 8082
