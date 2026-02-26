from app import models, schemas
from app.database import engine, nosql_db, get_db
from datetime import date, datetime, time
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from typing import List, Optional
from collections import defaultdict

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

    comments_map = defaultdict(list)
    comments = nosql_db.comments.find({}, {"_id": 0})
    for comment in comments:
        comments_map[comment["sale_id"]].append(comment)

    for sale in sales:
        sale.comments = comments_map.get(sale.id, [])

    return sales


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

    sale_ids = list(set(c["sale_id"] for c in comments_found))
    sales = db.query(models.Sale).filter(models.Sale.id.in_(sale_ids)).all()
    comments = list(nosql_db.comments.find(
        {"sale_id": {"$in": sale_ids}},
        {"_id": 0}
    ))

    comments_map = defaultdict(list)
    for comment in comments:
        comments_map[comment["sale_id"]].append(comment)

    sales_map = {}
    for sale in sales:
        sale.comments = comments_map.get(sale.id, [])
        sales_map[sale.id] = sale

    results = []
    for comment in comments_found:
        sale_obj = sales_map.get(comment["sale_id"])

        sale = db.query(models.Sale).filter(models.Sale.id == comment["sale_id"]).first()

        if sale_obj:
            results.append(
                {"comment": comment["comment"], "sale": sale_obj}
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
def quantity_by_all_products(db: Session = Depends(get_db)):
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
