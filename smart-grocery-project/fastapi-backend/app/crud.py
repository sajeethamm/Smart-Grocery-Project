# app/crud.py
import json
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

# small healthy substitution map
HEALTHY_MAP = {
    "white bread": "brown bread",
    "brown bread": "whole grain bread",
    "full cream milk": "low fat milk",
    "sugar": "honey",
    "white rice": "brown rice",
    "fried chicken": "grilled chicken"
}

def compute_expiry(purchase_date_str: str, shelf_days: int) -> str:
    # expects YYYY-MM-DD
    dt = datetime.fromisoformat(purchase_date_str)
    exp = dt + timedelta(days=int(shelf_days))
    return exp.date().isoformat()

# Items CRUD
def get_items(db: Session):
    return db.query(models.Item).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item_in: schemas.ItemCreate):
    expiry = compute_expiry(item_in.purchase_date, item_in.shelf_life_days or 7)
    item = models.Item(
        name=item_in.name.strip().lower(),
        category=(item_in.category or "").strip(),
        purchase_date=item_in.purchase_date,
        shelf_life_days=item_in.shelf_life_days or 7,
        expiry_date=expiry
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    # add a single-item basket to history for demonstration (keeps behaviour similar to Node version)
    add_history_basket(db, [item.name])
    return item

def update_item(db: Session, item_id: int, changes: schemas.ItemUpdate):
    item = get_item(db, item_id)
    if not item:
        return None
    if changes.name:
        item.name = changes.name.strip().lower()
    if changes.category is not None:
        item.category = changes.category
    if changes.purchase_date:
        item.purchase_date = changes.purchase_date
    if changes.shelf_life_days is not None:
        item.shelf_life_days = changes.shelf_life_days
    # recompute expiry_date
    item.expiry_date = compute_expiry(item.purchase_date, item.shelf_life_days or 7)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    if not item:
        return 0
    db.delete(item)
    db.commit()
    return 1

# History (store baskets as JSON text)
def add_history_basket(db: Session, basket: list[str]):
    # normalize names
    normalized = [x.strip().lower() for x in basket if x]
    if len(normalized) == 0:
        return None
    h = models.History(basket_json=json.dumps(normalized))
    db.add(h)
    db.commit()
    db.refresh(h)
    return h

def get_history_baskets(db: Session):
    rows = db.query(models.History).all()
    baskets = []
    for r in rows:
        try:
            baskets.append(json.loads(r.basket_json))
        except:
            baskets.append([])
    return baskets

# Recommendations (co-occurrence)
def recommend_from_current(db: Session, current: list[str], top_k: int = 10):
    baskets = get_history_baskets(db)
    # build co-occurrence counts
    co = {}  # co[a][b] = count
    for basket in baskets:
        unique = list(set([x.lower() for x in basket]))
        for i in unique:
            co.setdefault(i, {})
            for j in unique:
                if i == j: continue
                co[i][j] = co[i].get(j, 0) + 1
    scores = {}
    curset = set([x.lower() for x in current])
    for item in curset:
        row = co.get(item, {})
        for other, cnt in row.items():
            if other not in curset:
                scores[other] = scores.get(other, 0) + cnt
    recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [{"name": name, "score": score} for name, score in recs[:top_k]]

def healthy_substitution(item_name: str):
    return HEALTHY_MAP.get(item_name.strip().lower())
