from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum
from .database import Base


# Tabela saless
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(precision=10, scale=2), nullable=False)
    created_at = Column(DateTime, nullable=False)
