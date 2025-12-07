import logging
from datetime import date

import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000/requests"

st.title("Submit a New Maintenance Request")

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

default_student = st.session_state.get("student_id", "")

with st.form("create_request"):
    student_id = st.text_input("Student ID", value=default_student, help="Your studentRequestingID")
    issue_type = st.text_input("Issue type", value="Heating")
    description = st.text_area("Issue description")
    building_id = st.number_input("Building ID", min_value=1, step=1)
    apt_number = st.number_input("Apartment number", min_value=1, step=1)
    priority = st.selectbox("Priority", options=[0, 1, 2, 3], index=0)
    date_requested = st.date_input("Date requested", value=date.today())
    submitted = st.form_submit_button("Submit request")

if submitted:
    payload = {
        "studentID": student_id,
        "issueType": issue_type,
        "description": description,
        "buildingID": int(building_id),
        "aptNumber": int(apt_number),
        "priority": int(priority),
        "dateRequested": date_requested.isoformat(),
    }
    st.write("Sending:", payload)
    resp = handle_response(requests.post(API_BASE, json=payload))
    if resp:
        st.success("Request created successfully.")
        st.json(resp.json())