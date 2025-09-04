from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.templating import Jinja2Templates

from ..deps import get_current_user, get_db
from ..models import User, Prediction
from .admin import verify_admin

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="templates")

# ==============================
#  Page d'accueil
# ==============================
@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ==============================
#  Auth: login / register / logout
# ==============================
@router.get("/auth/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/auth/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/auth/logout")
def logout():
    # Pas de vraie session côté serveur, juste redirection
    return RedirectResponse(url="/", status_code=303)

# ==============================
#  Historique des prédictions
# ==============================
@router.get("/predict", response_class=HTMLResponse)
def prediction_form(request: Request):
    return templates.TemplateResponse("prediction.html", {"request": request})

@router.get("/predict/history", response_class=HTMLResponse)
def predictions_page(request: Request):
    # Pas de current_user ici
    return templates.TemplateResponse("predictions.html", {"request": request})



# ==============================
#  Admin Dashboard
# ==============================

@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    admin_user: User = Depends(verify_admin),
    db: Session = Depends(get_db)
):
    total_users = db.query(func.count(User.id)).scalar()
    total_predictions = db.query(func.count(Prediction.id)).scalar()

    # Répartition par classe
    class_counts = db.query(Prediction.predicted_class, func.count(Prediction.id))\
        .group_by(Prediction.predicted_class).all()
    predictions_by_class = {cls: cnt for cls, cnt in class_counts}

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "admin_user": admin_user,
            "total_users": total_users,
            "total_predictions": total_predictions,
            "predictions_by_class": predictions_by_class
        }
    )
