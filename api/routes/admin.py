# api/routes/admin_api.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from datetime import datetime, timedelta

from ..models import User, Prediction
from ..schemas import UserInfo, AdminStats, UserCreate,UserUpdate
from ..deps import get_db, get_current_user
from ..security import hash_password

router = APIRouter(prefix="/admin", tags=["admin-api"])

def verify_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès admin requis"
        )
    return current_user

@router.get("/users", response_model=List[UserInfo])
def get_all_users(limit: int = 100, admin_user: User = Depends(verify_admin), db: Session = Depends(get_db)):
    users_with_count = db.query(
        User,
        func.count(Prediction.id).label('predictions_count')
    ).outerjoin(Prediction).group_by(User.id).limit(limit).all()

    return [
        UserInfo(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at.isoformat(),
            predictions_count=count
        )
        for user, count in users_with_count
    ]

@router.get("/stats", response_model=AdminStats)
def get_admin_stats(admin_user: User = Depends(verify_admin), db: Session = Depends(get_db)):
    total_users = db.query(func.count(User.id)).scalar()
    total_predictions = db.query(func.count(Prediction.id)).scalar()
    
    predictions_by_class = dict(
        db.query(Prediction.predicted_class, func.count(Prediction.id)).group_by(Prediction.predicted_class).all()
    )
    
    recent_users = db.query(func.count(User.id))\
        .filter(User.created_at >= datetime.utcnow() - timedelta(days=7))\
        .scalar()
    
    return AdminStats(
        total_users=total_users,
        total_predictions=total_predictions,
        predictions_by_class=predictions_by_class,
        recent_users=recent_users or 0
    )

@router.get("/users/{user_id}/predictions")
def get_user_predictions_admin(user_id: str, limit: int = 50,
                               admin_user: User = Depends(verify_admin),
                               db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit).all()
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        },
        "predictions": [
            {
                "id": p.id,
                "predicted_class": p.predicted_class,
                "proba": p.proba,
                "created_at": p.created_at.isoformat(),
                "input_data": p.payload_json
            } for p in predictions
        ]
    }

@router.delete("/users/{user_id}")
def delete_user(user_id: str, admin_user: User = Depends(verify_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db.query(Prediction).filter(Prediction.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    
    return {"message": f"Utilisateur {user.email} supprimé avec succès"}

@router.get("/predictions/recent")
def get_recent_predictions(limit: int = 50, admin_user: User = Depends(verify_admin), db: Session = Depends(get_db)):
    predictions = db.query(Prediction, User.email)\
        .join(User)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit).all()
    
    return [
        {
            "id": p.id,
            "user_email": email,
            "predicted_class": p.predicted_class,
            "created_at": p.created_at.isoformat()
        } for p, email in predictions
    ]

@router.post("/users", response_model=UserInfo)
def create_user(
    user_data: UserCreate = Body(...),
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel utilisateur (accessible uniquement aux admins)
    """
    # Vérifier que l'email n'existe pas déjà
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    # Hasher le mot de passe
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role or "user"  # par défaut 'user'
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserInfo(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role,
        created_at=new_user.created_at.isoformat(),
        predictions_count=0
    )

@router.get("/users/{user_id}/predictions")
def get_user_predictions_admin(user_id: str, limit: int = 50,
                               admin_user: User = Depends(verify_admin),
                               db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit).all()
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        },
        "predictions": [
            {
                "id": p.id,
                "predicted_class": p.predicted_class,
                "proba": p.proba,  # ← Assurez-vous que ce champ existe
                "created_at": p.created_at.isoformat(),
                "input_data": p.payload_json
            } for p in predictions
        ]
    }

@router.delete("/predictions/{prediction_id}")
def delete_prediction(
    prediction_id: str, 
    admin_user: User = Depends(verify_admin), 
    db: Session = Depends(get_db)
):
    """
    Supprime une prédiction spécifique (admin uniquement)
    """
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    
    db.delete(prediction)
    db.commit()
    
    return {"message": f"Prédiction {prediction_id} supprimée avec succès"}