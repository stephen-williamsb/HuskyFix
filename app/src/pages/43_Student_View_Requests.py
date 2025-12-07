import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000/requests"

st.title("View All of My Maintenance Requests")

def handle_response(resp: requests.Response):
    try:
        resp.raise_for_status()
        return resp
    except Exception as exc:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        st.error(f"Request failed ({resp.status_code}): {body}")
        logger.exception("Backend error: %s", exc)
        return None

with st.sidebar:
    st.subheader("Filters")
    student_id = st.text_input("Student ID", value=st.session_state.get("student_id", ""))
    limit = st.number_input("Max rows", min_value=1, max_value=500, value=100, step=1)
    if st.button("Load my requests"):
        params = {
            "student_id": student_id,
            "limit": int(limit),
            "offset": 0,
        }
        st.session_state["view_params"] = params

params = st.session_state.get("view_params")

if not params:
    st.caption("Set your Student ID in the sidebar and click **Load my requests**.")
else:
    st.write("Query params:", params)
    resp = handle_response(requests.get(API_BASE, params=params))
    if resp:
        rows = resp.json()
        if not rows:
            st.info("No requests found for this student.")
        else:
            df = pd.DataFrame(rows)
            df = df.sort_values("dateRequested", ascending=False)
            st.dataframe(df, use_container_width=True)