"""
SQLAlchemy models + DB engine
run:  python site/models.py   -> creates coal.db with tables
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ---------------- boiler-plate -----------------
DB_URL = "sqlite:///coal.db"            # file sits next to app.py
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
# -----------------------------------------------

class Product(Base):
    __tablename__ = "products"
    id    = Column(Integer, primary_key=True)
    name  = Column(String, unique=True)
    grade = Column(String)
    kcal  = Column(Integer)
    price = Column(Float)

class QuoteRequest(Base):
    __tablename__ = "quote_requests"
    id       = Column(Integer, primary_key=True)
    name     = Column(String)
    email    = Column(String)
    tonnes   = Column(Integer)
    created  = Column(DateTime, default=datetime.utcnow)

    product_id = Column(Integer, ForeignKey("products.id"))
    product    = relationship(Product)

# create the tables when run directly
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✓ database + tables ready")
