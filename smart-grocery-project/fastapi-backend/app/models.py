# app/models.py
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, default="")
    purchase_date = Column(String, nullable=False)  # store ISO date string YYYY-MM-DD
    shelf_life_days = Column(Integer, default=7)
    expiry_date = Column(String, nullable=False)    # ISO date string YYYY-MM-DD

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    basket_json = Column(Text, nullable=False)  # JSON-encoded array of item names
