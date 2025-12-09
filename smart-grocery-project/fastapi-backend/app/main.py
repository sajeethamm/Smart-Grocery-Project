# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, db_init
import json
from typing import List

db_init.init_db()

app = FastAPI(title="Smart Grocery Backend (FastAPI)")

# Enable CORS (allow local React dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = db_init.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Smart Grocery FastAPI backend. See /docs for API UI."}

# Items
@app.get("/items", response_model=List[schemas.ItemOut])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.post("/items", response_model=schemas.ItemOut)
def create_item(item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item_in)

@app.put("/items/{item_id}", response_model=schemas.ItemOut)
def update_item(item_id: int, changes: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.update_item(db, item_id, changes)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_item(db, item_id)
    return {"deleted": deleted}

# History add basket
@app.post("/history")
def add_history(history_in: schemas.HistoryIn, db: Session = Depends(get_db)):
    if not history_in.basket:
        raise HTTPException(status_code=400, detail="basket required")
    h = crud.add_history_basket(db, history_in.basket)
    return {"ok": True, "id": h.id if h else None}

# Recommendations
@app.post("/recommendations")
def recommendations(recs_in: schemas.RecsIn, db: Session = Depends(get_db)):
    recs = crud.recommend_from_current(db, recs_in.current)
    return {"recommendations": recs}

# Healthy substitution
@app.get("/healthy-subs")
def healthy_sub(item: str = Query(..., alias="item")):
    alt = crud.healthy_substitution(item)
    return {"item": item, "alternative": alt}

# Expiring
@app.get("/expiring")
def expiring(days: int = 7, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    from datetime import datetime
    today = datetime.utcnow().date()
    expiring = []
    for it in items:
        try:
            expiry = datetime.fromisoformat(it.expiry_date).date()
            delta = (expiry - today).days
            if delta <= days:
                expiring.append({
                    "id": it.id,
                    "name": it.name,
                    "expiry_date": it.expiry_date,
                    "days_left": delta
                })
        except Exception:
            continue
    return {"count": len(expiring), "items": expiring}
