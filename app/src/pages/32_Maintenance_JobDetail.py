import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime
from streamlit_extras.app_logo import add_logo

add_logo("assets/logo.png")
SideBarLinks()
st.set_page_config(page_title="Job Detail", layout="wide")
st.title("Job Detail & Status Update")

API_BASE = "http://web-api:4000"
request_id = st.session_state.get("selected_request_id")

if not request_id:
    st.warning("No request selected. Go to 'My Assigned Jobs' and click 'Open Job Detail'.")
    st.stop()

def api_get(path):
    try:
        resp = requests.get(f"{API_BASE}{path}", timeout=6)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API GET failed: {e}")
        return None

def api_put(path, payload):
    try:
        resp = requests.put(f"{API_BASE}{path}", json=payload, timeout=6)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API PUT failed: {e}")
        return None

# Load request detail
detail = api_get(f"/requests/{request_id}")
if not detail:
    st.error("Could not load request details.")
    st.stop()

col1, col2 = st.columns([2,1])
with col1:
    st.subheader(f"Request {detail.get('requestID')} — {detail.get('issueType')}")
    st.markdown(f"**Apartment:** Building {detail.get('buildingID')} Apt {detail.get('aptNumber')}")
    st.markdown(f"**Submitted by student:** {detail.get('studentRequestingID')}")
    st.markdown(f"**Requested at:** {detail.get('dateRequested')}")
    st.markdown(f"**Current Status:** {detail.get('activeStatus')}")
    st.markdown("**Description:**")
    st.write(detail.get('issueDescription') or "-")
    st.markdown("**Completion Notes:**")
    st.write(detail.get('completionNotes') or "-")
with col2:
    st.subheader("Photos")
    photos = detail.get('photos', [])
    if photos:
        for p in photos:
            # expecting either filePath or embedded
            file_path = p.get("filePath") or p.get("embedded")
            if file_path:
                st.image(file_path, width=250)
    else:
        st.info("No photos attached")

# Status update form
st.markdown("---")
st.subheader("Update Status / ETA")
status = st.selectbox("Status", ["open", "En Route", "In Progress", "Blocked", "Completed"], index=0)
eta = st.datetime_input("ETA (optional)", value=None)


if st.button("Update Status"):
    payload = {"status": status}
    if eta:
        # map to scheduledDate in API; your endpoint accepts scheduledDate per spec
        payload["scheduledDate"] = eta.strftime("%Y-%m-%d %H:%M:%S")
    res = api_put(f"/requests/{request_id}", payload)
    if res is not None:
        st.success("Request updated")
        
        

# Add a work log / completion notes and photos
st.markdown("---")
st.subheader("Add Completion Notes / Time Spent / Photos")
time_spent = st.number_input("Time spent (minutes)", min_value=0, step=5)
completion_notes = st.text_area("Completion notes")
uploaded = st.file_uploader("Upload final photos", accept_multiple_files=True, type=["png","jpg","jpeg"])

if st.button("Save Completion Info"):
    put_payload = {"completionNotes": completion_notes, "dateCompleted": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
    # Optionally include time spent as a custom field or append to notes
    put_payload["completionNotes"] = (f"Time spent: {time_spent} minutes\n\n" + (completion_notes or ""))
    r = api_put(f"/requests/{request_id}", put_payload)
    if r is not None:
        # If you want to upload files, you may need a dedicated upload route:
        # Suggested route:
        # POST /requests/{id}/photos  --> form-data with file inputs. Backend should save and return file paths.
        # Below is an attempt; if backend lacks this endpoint it'll warn in except.
        if uploaded:
            try:
                files = []
                for f in uploaded:
                    files.append(("photos", (f.name, f.getvalue(), f.type)))
                resp = requests.post(f"{API_BASE}/requests/{request_id}/photos", files=files, timeout=10)
                resp.raise_for_status()
                st.success("Photos uploaded")
            except Exception as e:
                st.warning(f"Photo upload failed (route may be missing): {e}")
        st.success("Completion notes saved")

# Cancel request (soft-delete)
st.markdown("---")
if st.button("Cancel / Archive Request (mark canceled)"):
    # call DELETE /requests/{id}
    try:
        resp = requests.delete(f"{API_BASE}/requests/{request_id}", json={"user_id": st.session_state.get("employee_id", 7), "reason": "Canceled by technician"})
        resp.raise_for_status()
        st.success("Request canceled")
    except Exception as e:
        st.error(f"Cancel failed: {e}")
