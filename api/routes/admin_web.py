# api/routes/admin_web.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/admin_web", tags=["admin-web"])

@router.get("/dashboard")
def admin_dashboard(request: Request):
    # Le front-end utilisera fetch() vers /admin/stats pour récupérer les données
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@router.get("/users")
def admin_users_page(request: Request):
    # Le front-end utilisera fetch() vers /admin/users pour récupérer les utilisateurs
    return templates.TemplateResponse(
        "users.html",
        {"request": request}
    )

@router.get("/predictions/recent")
def admin_recent_predictions_page(request: Request):
    # Le front-end utilisera fetch() vers /admin/predictions/recent
    return templates.TemplateResponse(
        "recent_predictions.html",
        {"request": request}
    )
