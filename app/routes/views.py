from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app import models

router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
def render_dashboard(request: Request, db: Session = Depends(get_db)):

    vendas = db.query(models.Sale).all()

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "vendas": vendas}
    )
