import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000/requests"

st.title("Cancel a Maintenance Request")

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

with st.form("cancel_request"):
    student_id = st.text_input("Student ID", value=st.session_state.get("student_id", ""))
    request_id = st.number_input("Request ID to cancel", min_value=1, step=1)
    reason = st.text_area("Reason for canceling", value="Canceled by student.")
    submitted = st.form_submit_button("Cancel request")

if submitted:
    url = f"{API_BASE}/{int(request_id)}"
    payload = {
        "reason": reason,
        "user_id": student_id,
    }
    st.write("Sending:", payload)
    resp = handle_response(requests.delete(url, json=payload))
    if resp:
        st.success("Request canceled.")
        if resp.content:
            st.json(resp.json())