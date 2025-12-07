import streamlit as st
import requests
from modules.nav import SideBarLinks
from streamlit_extras.app_logo import add_logo

add_logo("assets/logo.png")
SideBarLinks()
st.set_page_config(page_title="Parts & Inventory", layout="wide")
st.title("Parts Inventory & Requests")

API_BASE = "http://web-api:4000"

def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"GET failed: {e}")
        return []

def api_post(path, payload):
    try:
        r = requests.post(f"{API_BASE}{path}", json=payload, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"POST failed: {e}")
        return None

def api_put(path, payload):
    try:
        r = requests.put(f"{API_BASE}{path}", json=payload, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"PUT failed: {e}")
        return None


# -----------------------------
# LOAD PARTS INVENTORY
# -----------------------------
st.subheader("Parts Inventory")
parts = api_get("/employee/parts")
if not parts:
    st.info("No parts loaded.")

q = st.text_input("Search parts")
filtered = [p for p in parts if q.lower() in p.get("name", "").lower()]

for p in filtered:
    cols = st.columns([3, 1, 1, 2])
    cols[0].markdown(f"**{p['name']}** (ID: {p['partID']})")
    cols[1].markdown(f"Qty: {p['quantity']}")
    cols[2].markdown(f"Cost: {p['cost']}")

    # Request a part = subtract 1 quantity using the ACTUAL backend endpoint
    if(p['quantity'] > 0):
        with cols[3]:
            if st.button("Request Part", key=f"req_{p['partID']}"):
                payload = {"quantity_delta": -1}
                resp = api_put(f"/employee/parts/{p['partID']}/status", payload)
                if resp:
                    st.success(f"Requested part '{p['name']}' (quantity -1)")
                    st.rerun()
    else:
        cols[3].markdown("Out of stock")


# -----------------------------
# ADD NEW PART
# -----------------------------
st.markdown("---")
st.subheader("Add New Part to Inventory")

with st.form("add_part"):
    name = st.text_input("Part name")
    qty = st.number_input("Quantity", min_value=0, value=1)
    cost = st.number_input("Cost (cents)", min_value=0, value=0)
    submitted = st.form_submit_button("Add Part")

    if submitted:
        payload = {"name": name, "quantity": qty, "cost": cost}
        result = api_post("/employee/parts", payload)

        if result:
            st.success("Part added.")
            st.rerun()


# -----------------------------
# ADJUST QUANTITY MANUALLY
# -----------------------------
st.markdown("---")
st.subheader("Adjust Part Quantity")

part_id = st.number_input("Part ID", min_value=1, value=1)
adjust = st.number_input(
    "Adjust quantity by (negative = remove, positive = add)",
    value=0
)

if st.button("Apply Adjustment"):
    resp = api_put(
        f"/employee/parts/{int(part_id)}/status",
        {"quantity_delta": adjust}
    )
    if resp:
        st.success("Quantity adjustment applied.")
        st.rerun()
