# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class ItemCreate(BaseModel):
    name: str
    category: Optional[str] = ""
    purchase_date: str   # "YYYY-MM-DD"
    shelf_life_days: Optional[int] = 7

class ItemUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    purchase_date: Optional[str]
    shelf_life_days: Optional[int]

class ItemOut(BaseModel):
    id: int
    name: str
    category: Optional[str]
    purchase_date: str
    shelf_life_days: int
    expiry_date: str

    class Config:
        orm_mode = True

class HistoryIn(BaseModel):
    basket: List[str]

class RecsIn(BaseModel):
    current: List[str] = []
