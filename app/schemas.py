from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


# Sale Base
class SaleBase(BaseModel):
    product_name: str = Field(..., min_length=3, description="Nome do produto vendido")
    category: str = Field(..., description="Categoria do produto")
    unit_price: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=2,
        json_schema_extra={"example": 150.50},
        description="Valor unitário (positivo)",
    )
    quantity: int = Field(..., ge=1, description="Quantidade vendidada (pelo menos 1)")
    comments: List[CommentSchema] = []

    class Config:
        from_attributes = True


# Sale Criação
class SaleCreate(SaleBase):
    created_at: datetime = Field(..., description="Data da Venda")


class SaleResponse(SaleBase):
    id: int
    created_at: datetime = Field(..., description="Data da Venda")
    comments: List[dict] = []

    # Configuração para permitir que o Pydantic leia modelos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# Busca Textual
class SearchResult(BaseModel):
    comment: str = Field(..., description="Comentário da Venda")
    sale: SaleResponse


# Comment base
class CommentSchema(BaseModel):
    sale_id: int = Field(..., description="Id da Venda")
    comment: str = Field(..., description="Comentário da Venda")

    class Config:
        from_attributes = True
