from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


# Base
class SaleBase(BaseModel):
    product_name: str = Field(..., min_length=3, description="Nome do produto vendido")
    category: str = Field(..., description="Categoria do produto")
    unit_price: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=2,
        json_schema_extra={"example": 150.50},
        description="Valor unitário (pelo menos 1)",
    )
    quantity: int = Field(..., ge=1, description="Quantidade vendidada (pelo menos 1)")


# Criação
class SaleCreate(SaleBase):
    created_at: datetime = Field(..., description="Data da venda")
    comment: Optional[str] = Field(None, description="Comentário (Opcional)")


class SaleResponse(SaleBase):
    id: int
    created_at: datetime
    comments: List[dict] = []

    # Configuração para permitir que o Pydantic leia modelos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# Busca Textual
class SearchResult(BaseModel):
    comment: str
    sale: SaleResponse
