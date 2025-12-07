import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000/requests"

st.title("Attach a Photo to an Existing Request")

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

with st.form("attach_photo"):
    request_id = st.number_input("Request ID", min_value=1, step=1)
    photo_url = st.text_input("Photo URL", help="https://example.com/photos/request1001.jpg")
    submitted = st.form_submit_button("Attach photo")

if submitted:
    url = f"{API_BASE}/{int(request_id)}"

    # Make sure update_request in Flask maps 'issuePhotos' -> issuePhotos column
    payload = {"issuePhotos": photo_url}

    st.write("Sending:", payload)
    resp = handle_response(requests.put(url, json=payload))
    if resp:
        st.success("Photo attached / issuePhotos updated.")
        if resp.content:
            st.json(resp.json())