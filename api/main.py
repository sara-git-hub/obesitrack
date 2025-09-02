# api/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import json
from pathlib import Path

from .config import settings
from .deps import get_db, engine
from .models import Base
from .routes import auth, predictions, admin

# Création de l'application FastAPI
app = FastAPI(
    title="ObesiTrack API",
    version="1.0",
    description="API de prédiction et gestion utilisateurs pour l'obésité",
)

# Création de la base de données et des tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Inclusion des routeurs
app.include_router(auth.router)
app.include_router(predictions.router)
app.include_router(admin.router)

# Endpoints généraux
@app.get("/", tags=["general"])
def root():
    """Endpoint racine"""
    return {
        "message": "ObesiTrack API is running!",
        "version": "1.0",
        "docs_url": "/docs",
        "status": "operational"
    }

@app.get("/health", tags=["general"])
def health(db: Session = Depends(get_db)):
    """Vérifie l'état de santé de l'API et de la base de données"""
    try:
        db.execute("SELECT 1")
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "ok", 
        "database": db_status,
        "version": "1.0"
    }

@app.get("/metrics", tags=["model"])
def get_model_metrics():
    """
    Retourne les métriques du modèle ML (nom, date, accuracy, etc.)
    """
    try:
        # Chemin vers le fichier de métriques
        metrics_path = Path("ml/data/metrics.json")
        
        if not metrics_path.exists():
            return {
                "status": "metrics_not_found",
                "message": "Fichier de métriques non trouvé. Veuillez entraîner le modèle."
            }
        
        # Lecture des métriques
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        
        # Informations additionnelles
        model_path = Path(settings.MODEL_PATH)
        model_exists = model_path.exists()
        
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
                "model_file_exists": model_exists,
                "model_path": str(model_path),
                "metrics_file_exists": True
            },
            "api_info": {
                "version": "1.0",
                "status": "operational"
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erreur lors de la lecture des métriques: {str(e)}"
        }
    
# Lancer l'application
#uvicorn api.main:app --reload