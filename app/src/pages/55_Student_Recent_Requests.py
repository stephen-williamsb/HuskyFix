import logging
from datetime import date

import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000/requests"

st.title("Recently Updated Requests")

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

with st.form("recent_requests"):
    student_id = st.text_input("Student ID", value=st.session_state.get("student_id", ""))
    target_date = st.date_input(
        "Updated on date",
        value=date.today(),
        help="Matches dateCompleted or scheduledDate",
    )
    limit = st.number_input("Max rows", min_value=1, max_value=500, value=200, step=1)
    submitted = st.form_submit_button("Load recent")

if submitted:
    day_str = target_date.isoformat()
    params = {
        "student_id": student_id,
        "start_date": day_str,
        "end_date": day_str,
        "limit": int(limit),
        "offset": 0,
    }
    st.write("Query params:", params)

    resp = handle_response(requests.get(API_BASE, params=params))
    if resp:
        rows = resp.json()
        if not rows:
            st.info("No requests found.")
        else:
            df = pd.DataFrame(rows)
            # Keep only rows where completed or scheduled exactly equals target_date
            mask = (df["dateCompleted"] == day_str) | (df["scheduledDate"] == day_str)
            recent_df = df.loc[mask].sort_values(
                ["dateCompleted", "scheduledDate"], ascending=False
            )
            if recent_df.empty:
                st.info("No requests updated on that date.")
            else:
                st.dataframe(recent_df, use_container_width=True)