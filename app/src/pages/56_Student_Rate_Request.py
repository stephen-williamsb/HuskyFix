import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000/requests"

st.title("Rate a Completed Maintenance Request")

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

with st.form("rating_form"):
    student_id = st.text_input("Student ID", value=st.session_state.get("student_id", ""))
    request_id = st.number_input("Completed request ID", min_value=1, step=1)
    rating = st.slider("Rating (1–5)", min_value=1, max_value=5, value=5)
    comment = st.text_area("Comment", value="Very satisfied.")
    submitted = st.form_submit_button("Submit rating")

if submitted:
    url = f"{API_BASE}/{int(request_id)}"
    notes = f"Student {student_id} rating: {rating} - {comment}"

    # Make sure update_request in Flask maps 'completionNotes' → completionNotes column
    payload = {
        "completionNotes": notes,
        "status": "Completed",   # ensure it is marked completed
    }

    st.write("Sending:", payload)
    resp = handle_response(requests.put(url, json=payload))
    if resp:
        st.success("Rating saved.")
        if resp.content:
            st.json(resp.json())