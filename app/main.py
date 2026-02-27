from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes import views, sales
from app.database import engine
from app import models
import os

# Banco de dados
models.Base.metadata.create_all(bind=engine)

base_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(base_dir, "..", "templates")
templates = Jinja2Templates(directory=template_path)

app = FastAPI()
app.include_router(views.router, tags=["Páginas HTML"])
app.include_router(sales.router, prefix="/api", tags=["API de Vendas"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "titulo": "Bem-vindo ao Sistema Vidya"}
    )
