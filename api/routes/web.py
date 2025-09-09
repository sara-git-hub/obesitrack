
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func

from ..core.templates import templates

router = APIRouter(tags=["web"])

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

# ==============================
#  Historique des prédictions
# ==============================
@router.get("/predict", response_class=HTMLResponse)
def prediction_form(request: Request):
    return templates.TemplateResponse("prediction.html", {"request": request})

@router.get("/predict/history", response_class=HTMLResponse)
def predictions_page(request: Request):
    return templates.TemplateResponse("predictions.html", {"request": request})
