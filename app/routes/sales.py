from app import models, schemas
from app.database import engine, nosql_db, get_db
from datetime import date, datetime, time
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter()


# --- ENDPOINTS ---
# Criar Venda
@router.post("/sales/", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_sale = models.Sale(
        product_name=sale.product_name,
        category=sale.category,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        created_at=sale.created_at,
    )

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    results_comment = []
    if sale.comment:
        nosql_db.comments.insert_one({"sale_id": db_sale.id, "comment": sale.comment})
        results_comment.append({"comment": sale.comment})

    response_data = jsonable_encoder(db_sale)
    response_data["comments"] = results_comment

    return response_data


# Listar Vendas
@router.get("/sales/", response_model=List[schemas.SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    sales = db.query(models.Sale).all()
    results = []

    for sale in sales:
        sale_dict = jsonable_encoder(sale)
        comments = list(nosql_db.comments.find({"sale_id": sale.id}, {"_id": 0}))
        sale_dict["comments"] = comments
        results.append(sale_dict)

    return results


# Procurar em comentários
@router.get("/sales/search", response_model=List[schemas.SearchResult])
def search_comments(
    q: str = Query(..., description="Texto para buscar nos comentários"),
    db: Session = Depends(get_db),
):
    cursor = nosql_db.comments.find(
        {"comment": {"$regex": q, "$options": "i"}}, {"_id": 0}
    )

    comments_found = list(cursor)

    if not comments_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="o termo não foi encontrado"
        )

    results = []
    for doc in comments_found:
        sale = db.query(models.Sale).filter(models.Sale.id == doc["sale_id"]).first()

        sale_dict = jsonable_encoder(sale)
        comments = list(nosql_db.comments.find({"sale_id": sale.id}, {"_id": 0}))
        sale_dict["comments"] = comments

        if sale:
            results.append(
                {"comment": doc["comment"], "sale": jsonable_encoder(sale_dict)}
            )

    return results


# Total de vendas
@router.get("/sales/total_revenue")
def total_revenue(db: Session = Depends(get_db)):
    result = db.query(
        func.sum(models.Sale.quantity * models.Sale.unit_price)
    ).scalar()

    total = float(result) if result else 0.0

    return {"total_revenue": total}


# Total de vendas por categoria
@router.get("/sales/quantity_categories")
def quantity_by_all_categories(db: Session = Depends(get_db)):
    results = (
        db.query(models.Sale.category, func.sum(models.Sale.quantity).label("total"))
        .group_by(models.Sale.category)
        .all()
    )

    return [{"category": row.category, "total": int(row.total)} for row in results]


# Total de vendas por produto
@router.get("/sales/quantity_products")
def quantity_all_products(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Sale.product_name, func.sum(models.Sale.quantity).label("total")
        )
        .group_by(models.Sale.product_name)
        .all()
    )

    return [
        {"product_name": row.product_name, "total": int(row.total)} for row in results
    ]
