import streamlit as st
from datetime import datetime, date
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Grocery Assistant", page_icon="🛒", layout="wide")

DB_FILE = "grocery_db.json"

# ---------------- CATEGORY ICONS ----------------
CATEGORIES = {
    "Vegetables": "🥦 Vegetables",
    "Fruits": "🍎 Fruits",
    "Dairy": "🥛 Dairy",
    "Snacks": "🍿 Snacks",
    "Beverages": "🥤 Beverages",
    "Bakery": "🍞 Bakery",
    "Others": "📦 Others"
}

CATEGORY_ICONS = {
    "Vegetables": "🥦",
    "Fruits": "🍎",
    "Dairy": "🥛",
    "Snacks": "🍿",
    "Beverages": "🥤",
    "Bakery": "🍞",
    "Others": "📦"
}

CATEGORY_COLORS = {
    "Vegetables": "#28a745",
    "Fruits": "#dc3545",
    "Dairy": "#007bff",
    "Snacks": "#ffc107",
    "Beverages": "#17a2b8",
    "Bakery": "#fd7e14",
    "Others": "#6c757d"
}

# ---------------- HEALTH AI ----------------
HEALTH_AI = {
    "white bread": "whole wheat bread",
    "soda": "fresh juice",
    "burger": "salad wrap",
    "chips": "air-popped popcorn",
    "coke": "fresh lime juice",
    "ice cream": "frozen yogurt",
    "biscuits": "oat cookies",
    "candy": "fruit salad",
    "chocolate": "dark chocolate",
    "french fries": "baked sweet potato fries",
    "pizza": "whole wheat veggie pizza",
    "donuts": "banana pancakes",
    "margarine": "olive oil",
    "cream": "low-fat yogurt",
    "mayonnaise": "avocado spread",
    "sugar": "honey",
    "white rice": "brown rice",
    "instant noodles": "whole grain pasta",
    "energy drinks": "green tea"
}

# ---------------- DATA ----------------
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"inventory": [], "history": [], "shopping_list": []}

def save_data():
    with open(DB_FILE, "w") as f:
        json.dump({
            "inventory": st.session_state.inventory,
            "history": st.session_state.history,
            "shopping_list": st.session_state.shopping_list
        }, f, indent=4)

# ---------------- SESSION ----------------
if "loaded" not in st.session_state:
    data = load_data()
    st.session_state.inventory = data["inventory"]
    st.session_state.history = data["history"]
    st.session_state.shopping_list = data["shopping_list"]
    st.session_state.loaded = True

if "pending_item" not in st.session_state:
    st.session_state.pending_item = None
    st.session_state.pending_better = None

# ---------------- SIDEBAR: Add Inventory ----------------
with st.sidebar:
    st.header("➕ Add Inventory")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Item Name")
        st.markdown("**Select Category:**")
        category_friendly = st.radio("", options=list(CATEGORIES.values()))
        category_key = [k for k, v in CATEGORIES.items() if v == category_friendly][0]

        qty = st.number_input("Quantity", 1, 100, 1)
        unit = st.selectbox("Unit", ["pcs", "Kg", "g", "L"])
        expiry = st.date_input("Expiry Date", min_value=date.today())

        submit = st.form_submit_button("Add Item")
        if submit and name:
            st.session_state.inventory.append({
                "item": name,
                "category": category_key,
                "qty": qty,
                "unit": unit,
                "expiry": str(expiry)
            })
            save_data()
            st.success(f"{name} added to inventory under {category_friendly}!")

# ---------------- MAIN ----------------
st.title("🛒 Smart Grocery Shopping Assistant")

tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🗑️ Manage Inventory",
    "📝 Shopping List"
])

# ---------------- TAB 1: DASHBOARD ----------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Inventory Summary")
    st.markdown("<br>", unsafe_allow_html=True)

    today = date.today()
    expired = 0
    expiring_soon = 0
    low_stock = 0

    for item in st.session_state.inventory:
        exp = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
        days_left = (exp - today).days
        if days_left < 0:
            expired += 1
        elif days_left <= 7:
            expiring_soon += 1
        if item["qty"] <= 2:
            low_stock += 1

    # --- Dashboard metrics in cards ---
    metrics = [
        ("Total Items", len(st.session_state.inventory), "#007bff"),
        ("Expired", expired, "#dc3545"),
        ("Expiring Soon", expiring_soon, "#ffc107"),
        ("Low Stock", low_stock, "#28a745")
    ]
    cols = st.columns(len(metrics))
    for col, (title, value, color) in zip(cols, metrics):
        col.markdown(
            f"""
            <div style='background-color:{color}; padding:15px; border-radius:10px; text-align:center'>
                <h3 style='color:white'>{title}</h3>
                <h2 style='color:white'>{value}</h2>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Inventory by Category")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Grid view for inventory ---
    if st.session_state.inventory:
        num_cols = 3
        rows = (len(st.session_state.inventory) + num_cols - 1) // num_cols
        for r in range(rows):
            cols = st.columns(num_cols)
            for c in range(num_cols):
                idx = r * num_cols + c
                if idx < len(st.session_state.inventory):
                    item = st.session_state.inventory[idx]
                    color = CATEGORY_COLORS.get(item['category'], "#6c757d")
                    icon = CATEGORY_ICONS.get(item['category'], "📦")
                    exp = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    days_left = (exp - today).days
                    cols[c].markdown(
                        f"""
                        <div style='background-color:{color}; border-radius:10px; padding:15px; margin-bottom:10px;'>
                        <h4 style='color:white'>{icon} {item['item']}</h4>
                        <p style='color:white'>Qty: {item['qty']} {item['unit']}</p>
                        <p style='color:white'>Category: {item['category']}</p>
                        <p style='color:white'>Expires in {days_left} days</p>
                        </div>
                        """, unsafe_allow_html=True
                    )
    else:
        st.info("Inventory is empty.")

# ---------------- TAB 2: MANAGE INVENTORY ----------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🗑️ Manage Inventory")
    st.markdown("<br>", unsafe_allow_html=True)

    inventory = st.session_state.inventory
    if not inventory:
        st.info("Inventory is empty.")
    else:
        num_cols = 3
        rows = (len(inventory) + num_cols - 1) // num_cols
        today = date.today()

        for r in range(rows):
            cols = st.columns(num_cols)
            for c in range(num_cols):
                idx = r * num_cols + c
                if idx < len(inventory):
                    item = inventory[idx]
                    color = CATEGORY_COLORS.get(item['category'], "#6c757d")
                    icon = CATEGORY_ICONS.get(item['category'], "📦")
                    exp_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    days_left = (exp_date - today).days
                    status = "✅ Fresh" if days_left > 7 else ("⚠️ Soon" if days_left > 0 else "❌ Expired")

                    with cols[c]:
                        st.markdown(
                            f"""
                            <div style='background-color:{color}; border-radius:10px; padding:15px; min-height:150px; color:white;'>
                                <h4 style='margin:0'>{icon} {item['item']}</h4>
                                <p style='margin:0'>Qty: {item['qty']} {item['unit']}</p>
                                <p style='margin:0'>Category: {item['category']}</p>
                                <p style='margin:0'>Expires in {days_left} days ({status})</p>
                            </div>
                            """, unsafe_allow_html=True
                        )

                        # Buttons below each card
                        col_btn1, col_btn2 = st.columns([1,1])
                        with col_btn1:
                            if st.button("🗑 Remove", key=f"rm_{idx}"):
                                st.session_state.inventory.pop(idx)
                                save_data()
                                st.experimental_rerun()
                        with col_btn2:
                            if st.button("➕ Purchased", key=f"buy_{idx}"):
                                item["qty"] += 1
                                st.session_state.history.append({
                                    "item": item["item"],
                                    "date": str(today)
                                })
                                save_data()
                                st.experimental_rerun()

# ---------------- TAB 3: SHOPPING LIST ----------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📝 AI-Powered Shopping List")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Predict Missing Items from history ---
    if st.session_state.history:
        with st.expander("🤖 Suggested Restock Based on History"):
            for record in st.session_state.history:
                last_bought = datetime.strptime(record['date'], "%Y-%m-%d").date()
                days_since = (today - last_bought).days
                if days_since > 30 and record['item'] not in st.session_state.shopping_list:
                    st.info(f"Restock **{record['item']}**? (last bought {days_since} days ago)")
                    if st.button(f"➕ Add {record['item']}", key=f"hist_{record['item']}"):
                        st.session_state.shopping_list.append(record['item'])
                        save_data()
                        st.success(f"{record['item']} added!")

    # --- Add new item form ---
    with st.form("shop_form"):
        shop_item = st.text_input("Add item to buy")
        submit = st.form_submit_button("➕ Add")
        if submit and shop_item:
            clean = shop_item.lower().strip()
            if clean in HEALTH_AI:
                st.session_state.pending_item = shop_item
                st.session_state.pending_better = HEALTH_AI[clean]
            else:
                st.session_state.shopping_list.append(shop_item)
                save_data()
                st.success(f"{shop_item} added!")

    # --- Health AI suggestions ---
    if st.session_state.pending_item:
        with st.expander(f"⚠️ Healthier Option for {st.session_state.pending_item}"):
            st.info(f"💡 Suggested: {st.session_state.pending_better}")
            c1, c2 = st.columns(2)
            if c1.button("✔ Use Healthy Option"):
                st.session_state.shopping_list.append(st.session_state.pending_better)
                st.session_state.pending_item = None
                save_data()
            if c2.button("❌ Keep Original"):
                st.session_state.shopping_list.append(st.session_state.pending_item)
                st.session_state.pending_item = None
                save_data()

    # --- Show final list with individual remove buttons ---
    if st.session_state.shopping_list:
        st.divider()
        st.markdown("### 📝 Shopping List")
        for i, x in enumerate(st.session_state.shopping_list):
            c1, c2 = st.columns([6, 1])
            c1.write(f"{i+1}. {x}")
            if c2.button("🧹 Remove", key=f"clear_{i}"):
                st.session_state.shopping_list.pop(i)
                save_data()
                st.success(f"Removed {x}")
                break
