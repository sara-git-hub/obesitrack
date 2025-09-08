from fastapi import APIRouter, Request, Depends
from ..core.templates import templates

router = APIRouter(prefix="/admin_web", tags=["admin-web"])

@router.get("/dashboard")
def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@router.get("/users")
def admin_users_page(request: Request):
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
