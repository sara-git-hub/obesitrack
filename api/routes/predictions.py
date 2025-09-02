# api/routes/predictions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas import PredictionRequest, PredictionResponse
from ..models import User, Prediction
from ..deps import get_db, get_current_user
from ..ml.ml_gradient import predict_obesity

router = APIRouter(prefix="/predict", tags=["predictions"])

@router.post("/", response_model=PredictionResponse)
def make_prediction(
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Effectue une prédiction d'obésité pour l'utilisateur connecté
    """
    try:
        # Conversion en dict pour le modèle ML
        input_data = prediction_request.model_dump()
        
        # Appel du modèle ML
        predicted_class, probabilities = predict_obesity(input_data)
        
        # Sauvegarde en base de données
        prediction_record = Prediction(
            user_id=current_user.id,
            payload_json=input_data,
            predicted_class=predicted_class,
            proba=probabilities
        )
        db.add(prediction_record)
        db.commit()
        db.refresh(prediction_record)
        
        return PredictionResponse(
            id=prediction_record.id,
            predicted_class=predicted_class,
            proba=probabilities
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction: {str(e)}"
        )

@router.get("/history", response_model=List[PredictionResponse])
def get_user_predictions(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des prédictions de l'utilisateur connecté
    """
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == current_user.id)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        PredictionResponse(
            id=pred.id,
            predicted_class=pred.predicted_class,
            proba=pred.proba
        )
        for pred in predictions
    ]

@router.get("/history/{prediction_id}", response_model=PredictionResponse)
def get_prediction_detail(
    prediction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère le détail d'une prédiction spécifique de l'utilisateur
    """
    prediction = db.query(Prediction)\
        .filter(
            Prediction.id == prediction_id,
            Prediction.user_id == current_user.id
        )\
        .first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prédiction non trouvée"
        )
    
    return PredictionResponse(
        id=prediction.id,
        predicted_class=prediction.predicted_class,
        proba=prediction.proba
    )

@router.delete("/history/{prediction_id}")
def delete_prediction(
    prediction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime une prédiction de l'utilisateur
    """
    prediction = db.query(Prediction)\
        .filter(
            Prediction.id == prediction_id,
            Prediction.user_id == current_user.id
        )\
        .first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prédiction non trouvée"
        )
    
    db.delete(prediction)
    db.commit()
    
    return {"message": "Prédiction supprimée avec succès"}