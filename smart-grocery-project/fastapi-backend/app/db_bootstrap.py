# app/db_bootstrap.py
from .db_init import SessionLocal, init_db
from .crud import create_item, add_history_basket
from .schemas import ItemCreate

init_db()
db = SessionLocal()

samples = [
    ItemCreate(name="milk", category="dairy", purchase_date="2025-10-30", shelf_life_days=10),
    ItemCreate(name="white bread", category="bakery", purchase_date="2025-11-01", shelf_life_days=4),
    ItemCreate(name="cereal", category="breakfast", purchase_date="2025-11-02", shelf_life_days=180),
]

for s in samples:
    create_item(db, s)

# Add example history baskets
add_history_basket(db, ["milk","cereal","banana"])
add_history_basket(db, ["white bread","jam","butter"])
add_history_basket(db, ["milk","cookies"])
add_history_basket(db, ["white bread","peanut butter"])
add_history_basket(db, ["milk","cereal"])

db.close()
print("Bootstrap done.")
