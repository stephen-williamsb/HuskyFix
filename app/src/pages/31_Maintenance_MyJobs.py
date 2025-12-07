# app/src/pages/31_Maintenance_MyJobs.py
import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import date, timedelta
from streamlit_extras.app_logo import add_logo

add_logo("assets/logo.png")

SideBarLinks()

st.set_page_config(page_title="My Assigned Jobs", layout="wide")
st.title("My Assigned Jobs (Maintenance)")

API_BASE = "http://web-api:4000"

# default logged-in employee id for testing (use small number like 7)
employee_id = st.session_state.get("employee_id", 7)

# Filters
col1, col2, col3, col4 = st.columns([2,2,2,1])
with col1:
    date_filter = st.date_input("Date", value=date.today())
with col2:
    priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
with col3:
    status_filter = st.selectbox("Status", ["All", "open", "En Route", "In Progress", "Blocked", "Completed"])
with col4:
    refresh = st.button("Refresh")

def api_get(path, params=None):
    try:
        resp = requests.get(f"{API_BASE}{path}", params=params, timeout=6)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API GET failed: {e}")
        return []

# Build params: use employee_id and date. Your /requests route supports filtering by employee via join existence.
params = {"employee_id": employee_id, "limit": 200}
# if your backend supports start/end date format use these:
params["start_date"] = date_filter.isoformat()
params["end_date"] = (date_filter + timedelta(days=1)).isoformat()

jobs = api_get("/requests", params=params)

# client-side priority mapping if your backend uses ints or words:
def priority_rank(p):
    if not p: return 2
    p_low = str(p).lower()
    if "high" in p_low or str(p) in ("5", "4"): return 0
    if "medium" in p_low or str(p) in ("3",): return 1
    return 2

# Filter client-side by priority/status
if priority_filter != "All":
    pf = priority_filter.lower()
    jobs = [j for j in jobs if pf in str(j.get("priority", "")).lower() or pf in str(j.get("priority", "")).lower()]
if status_filter != "All":
    jobs = [j for j in jobs if (j.get("activeStatus") or "").lower() == status_filter.lower()]

# Sort by priority rank then dateRequested desc
jobs_sorted = sorted(jobs, key=lambda j: (priority_rank(j.get("priority")), j.get("dateRequested") or ""), reverse=False)

st.write(f"Showing {len(jobs_sorted)} jobs assigned to employee {employee_id}")

# Table with actions
for job in jobs_sorted:
    with st.expander(f"[{job.get('requestID')}] {job.get('issueType')} — Apt {job.get('aptNumber')} ({job.get('buildingID')}) — Priority {job.get('priority')} — Status {job.get('activeStatus')}"):
        c1, c2, c3, c4 = st.columns([4,2,2,2])
        with c1:
            st.markdown(f"**Description:** {job.get('issueDescription') or '—'}")
            st.markdown(f"**Requested:** {job.get('dateRequested')}")
            st.markdown(f"**Student ID:** {job.get('studentRequestingID')}")
        with c2:
            if st.button("Open Job Detail", key=f"open_{job.get('requestID')}"):
                # store selected id and go to detail page
                st.session_state["selected_request_id"] = job.get("requestID")
                st.experimental_set_query_params(page="job_detail", request_id=job.get("requestID"))
                st.experimental_rerun()
        with c3:
            if st.button("Mark En Route", key=f"enroute_{job.get('requestID')}"):
                try:
                    r = requests.put(f"{API_BASE}/requests/{job.get('requestID')}", json={"status": "En Route"})
                    r.raise_for_status()
                    st.success("Status updated to En Route")
                except Exception as e:
                    st.error(f"Failed to update status: {e}")
        with c4:
            if st.button("Mark Complete", key=f"complete_{job.get('requestID')}"):
                try:
                    r = requests.put(f"{API_BASE}/requests/{job.get('requestID')}", json={"status": "Completed", "dateCompleted": date.today().isoformat()})
                    r.raise_for_status()
                    st.success("Marked completed")
                except Exception as e:
                    st.error(f"Failed to mark complete: {e}")
