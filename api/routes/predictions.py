from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import PredictionRequest, PredictionResponse
from ..models import User, Prediction
from ..deps import get_db, get_current_user
from ..ml.ml_gradient import predict_obesity
from ..core.templates import templates

router = APIRouter(prefix="/predict", tags=["predictions"])

# Envoie le formulaire de prediction
@router.post("/", response_model=PredictionResponse)
def make_prediction(prediction_request: PredictionRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    input_data = prediction_request.model_dump()
    predicted_class, probabilities = predict_obesity(input_data)
    record = Prediction(user_id=current_user.id, payload_json=input_data, predicted_class=predicted_class, proba=probabilities)
    db.add(record)
    db.commit()
    db.refresh(record)
    return PredictionResponse(id=record.id, predicted_class=predicted_class, proba=probabilities)

# Supprime une prediction
@router.delete("/history/{prediction_id}")
def delete_prediction(prediction_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pred = db.query(Prediction).filter(Prediction.id == prediction_id, Prediction.user_id == current_user.id).first()
    if not pred:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prédiction non trouvée")
    db.delete(pred)
    db.commit()
    return {"message": "Prédiction supprimée avec succès"}

# Retourne l'historique des predictions
@router.get("/history/data")
def get_predictions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retourne les prédictions de l'utilisateur connecté.
    JWT requis via get_current_user.
    """
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == current_user.id)\
        .order_by(Prediction.created_at.desc())\
        .all()

    return {
        "user_name": current_user.full_name,  # <-- nom de l'utilisateur
        "predictions": [
            {
                "predicted_class": p.predicted_class,
                "proba": p.proba,
                "created_at": p.created_at
            } for p in predictions
        ]
    }
