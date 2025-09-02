# api/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from ..models import User, Prediction
from ..deps import get_db, get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

class UserInfo(BaseModel):
    id: str
    email: str
    full_name: str | None
    created_at: str
    predictions_count: int

class AdminStats(BaseModel):
    total_users: int
    total_predictions: int
    predictions_by_class: Dict[str, int]
    recent_users: int  # derniers 7 jours

# Middleware simple pour vérifier les droits admin (à améliorer)
def verify_admin(current_user: User = Depends(get_current_user)):
    """
    Vérification basique admin - À améliorer avec un système de rôles
    Pour l'instant, on considère que les utilisateurs avec un email spécifique sont admins
    """
    admin_emails = ["admin@obesitrack.com", "sara@admin.com"]  # À configurer
    if current_user.email not in admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès admin requis"
        )
    return current_user

@router.get("/users", response_model=List[UserInfo])
def get_all_users(
    limit: int = 100,
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """
    Liste tous les utilisateurs avec le nombre de prédictions
    """
    users_with_count = db.query(
        User,
        func.count(Prediction.id).label('predictions_count')
    ).outerjoin(Prediction).group_by(User.id).limit(limit).all()
    
    return [
        UserInfo(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=str(user.created_at),
            predictions_count=count
        )
        for user, count in users_with_count
    ]

@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """
    Statistiques générales pour l'admin
    """
    # Compteurs généraux
    total_users = db.query(func.count(User.id)).scalar()
    total_predictions = db.query(func.count(Prediction.id)).scalar()
    
    # Répartition par classe de prédiction
    predictions_by_class = {}
    class_counts = db.query(
        Prediction.predicted_class,
        func.count(Prediction.id)
    ).group_by(Prediction.predicted_class).all()
    
    for class_name, count in class_counts:
        predictions_by_class[class_name] = count
    
    # Utilisateurs récents (7 derniers jours)
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = db.query(func.count(User.id))\
        .filter(User.created_at >= seven_days_ago)\
        .scalar()
    
    return AdminStats(
        total_users=total_users,
        total_predictions=total_predictions,
        predictions_by_class=predictions_by_class,
        recent_users=recent_users or 0
    )

@router.get("/users/{user_id}/predictions")
def get_user_predictions_admin(
    user_id: str,
    limit: int = 50,
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """
    Récupère les prédictions d'un utilisateur spécifique (vue admin)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit)\
        .all()
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        },
        "predictions": [
            {
                "id": pred.id,
                "predicted_class": pred.predicted_class,
                "proba": pred.proba,
                "created_at": str(pred.created_at),
                "input_data": pred.payload_json
            }
            for pred in predictions
        ]
    }

@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """
    Supprime un utilisateur et toutes ses prédictions
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Supprimer d'abord les prédictions (FK constraint)
    db.query(Prediction).filter(Prediction.user_id == user_id).delete()
    
    # Supprimer l'utilisateur
    db.delete(user)
    db.commit()
    
    return {"message": f"Utilisateur {user.email} supprimé avec succès"}

@router.get("/predictions/recent")
def get_recent_predictions(
    limit: int = 50,
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """
    Récupère les prédictions récentes (toutes users)
    """
    predictions = db.query(Prediction, User.email)\
        .join(User)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        {
            "id": pred.id,
            "user_email": user_email,
            "predicted_class": pred.predicted_class,
            "created_at": str(pred.created_at)
        }
        for pred, user_email in predictions
    ]