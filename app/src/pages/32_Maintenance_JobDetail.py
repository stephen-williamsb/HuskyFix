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

# Try to get current employee id from session_state, default to 7
default_emp = st.session_state.get("employee_id", 7)

# Minimal employee selector (tries API, falls back to fixed list)
employees = None
emp_options = None
try:
    resp = requests.get(f"{API_BASE}/employee", timeout=3)
    if resp.status_code == 200:
        employees = resp.json()
        if isinstance(employees, list) and employees and isinstance(employees[0], dict):
            emp_options = {str(e.get("employeeID")): f"{e.get('firstName','')} {e.get('lastName','')} (#{e.get('employeeID')})" for e in employees}
        else:
            emp_options = {str(e): f"Employee {e}" for e in employees}
except Exception:
    employees = None
    emp_options = None

if emp_options:
    emp_items = list(emp_options.items())
    emp_display = [v for k, v in emp_items]
    emp_ids = [int(k) for k, v in emp_items]
    try:
        default_idx = emp_ids.index(int(default_emp))
    except Exception:
        default_idx = 0
    selected_idx = st.selectbox("Select employee (for assigned-only filter)", emp_display, index=default_idx)
    selected_employee_id = emp_ids[selected_idx]
else:
    # fallback small list including 7
    selected_employee_id = st.selectbox("Select employee (for assigned-only filter)", options=[7, 1, 2, 3], index=0 if default_emp == 7 else 0)

# Option to restrict to assigned-only (DEFAULT: ON so page shows employee's jobs across ALL dates)
assigned_only = st.checkbox("Only show jobs assigned to selected employee", value=True)

# Make date filtering opt-in (default OFF). If user enables, we will send start/end to API.
filter_by_date = st.checkbox("Filter by date (optional)", value=False)

# Filters UI
col1, col2, col3, col4 = st.columns([2,2,2,1])
with col1:
    # show date picker only if the user opted into date filtering
    if filter_by_date:
        date_filter = st.date_input("Date", value=date.today())
    else:
        date_filter = None
with col2:
    priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
with col3:
    # Provide the statuses in the order you want presented.
    status_filter = st.selectbox("Status", ["All", "In Progress", "En Route", "Blocked", "Open", "Completed"])
with col4:
    refresh = st.button("Refresh")

# Simple API helpers
def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # don't spam UI on fallback detail checks; return None to indicate failure
        st.error(f"API GET failed: {e}")
        return None

# cached detail fetch to avoid repeated network calls
@st.cache_data(ttl=60)
def get_request_detail_cached(request_id):
    try:
        r = requests.get(f"{API_BASE}/requests/{request_id}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

# Build base params (no date by default)
base_params = {"limit": 500}
if status_filter != "All":
    base_params["status"] = status_filter

# Add date range if user turned on date filtering
if filter_by_date and date_filter:
    base_params["start_date"] = date_filter.isoformat()
    base_params["end_date"] = (date_filter + timedelta(days=1)).isoformat()

jobs = []
debug_info = {
    "attempted_server_employee_filter": False,
    "server_employee_results_count": None,
    "used_detail_fallback": False,
    "detail_matched_count": 0,
    "params_sent": base_params.copy(),
}

# If the user wants only assigned jobs, first try server-side employee filter (fast).
# If server returns [] (or None), fall back to retrieving all (with same base params) and checking each detail for assignedEmployees.
if assigned_only:
    debug_info["attempted_server_employee_filter"] = True
    server_params = base_params.copy()
    server_params["employee_id"] = selected_employee_id
    server_resp = api_get("/requests", params=server_params)
    # if server_resp is a list with items, trust it
    if isinstance(server_resp, list) and server_resp:
        jobs = server_resp
        debug_info["server_employee_results_count"] = len(server_resp)
    else:
        # fallback: fetch requests (without employee_id) then pull detail for each and inspect assignedEmployees
        debug_info["used_detail_fallback"] = True
        all_jobs = api_get("/requests", params=base_params)
        matched = []
        if isinstance(all_jobs, list):
            for j in all_jobs:
                rid = j.get("requestID")
                if rid is None:
                    continue
                detail = get_request_detail_cached(rid)
                if not detail:
                    continue
                assigned = detail.get("assignedEmployees") or []
                found = False
                for a in assigned:
                    if str(a.get("employeeID") or a.get("employeeId") or "") == str(selected_employee_id):
                        found = True
                        break
                if found:
                    matched.append(j)
        jobs = matched
        debug_info["detail_matched_count"] = len(matched)
        debug_info["server_employee_results_count"] = 0
else:
    # not assigned_only -> just ask server for requests with base_params
    resp = api_get("/requests", params=base_params)
    jobs = resp if isinstance(resp, list) else []

# Apply client-side priority filter if selected
if priority_filter != "All":
    pf = priority_filter.lower()
    jobs = [j for j in (jobs or []) if pf in str(j.get("priority", "")).lower() or pf in str(j.get("priority", "")).lower()]

# If backend didn't apply status or we need extra safety, apply client-side status filter
if status_filter != "All":
    sf = status_filter.lower()
    jobs = [j for j in (jobs or []) if sf == (j.get("activeStatus") or "").lower()]

# Sorting: status order (In Progress, En Route, Blocked, Open, Completed last) -> higher priority first -> dateRequested desc
def status_rank(status):
    s = (status or "").lower()
    if "in progress" in s or "in-progress" in s:
        return 0
    if "en route" in s or "enroute" in s:
        return 1
    if "blocked" in s:
        return 2
    if "open" in s:
        return 3
    if "complete" in s or "completed" in s or "closed" in s:
        return 4
    return 5

def priority_rank(p):
    # numeric priorities: higher is more urgent -> we return negative for descending
    try:
        num = int(p)
        return -num
    except Exception:
        p_low = str(p).lower() if p is not None else ""
        if "high" in p_low:
            return -5
        if "medium" in p_low:
            return -3
        return 0

def date_key(d):
    return d or ""

jobs_sorted = sorted(
    jobs or [],
    key=lambda j: (status_rank(j.get("activeStatus")), priority_rank(j.get("priority")))
)
# stable-sort by dateRequested descending so newest appear first within same status/priority group
jobs_sorted = sorted(jobs_sorted, key=lambda j: date_key(j.get("dateRequested")), reverse=True)

st.write(f"Showing {len(jobs_sorted)} jobs (assigned-only = {assigned_only})")

# show debug info when requested
if st.checkbox("Show debug info (params & counts)", value=False):
    st.json(debug_info)

if not jobs_sorted:
    st.info("No jobs found for these filters. If you expected assigned jobs for the selected employee, try removing other filters or toggling the 'Only show jobs assigned...' checkbox to OFF to view all jobs.")

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
                st.session_state["selected_request_id"] = job.get("requestID")
                st.experimental_set_query_params(page="job_detail", request_id=job.get("requestID"))
                st.experimental_rerun()
        with c3:
            if st.button("Mark En Route", key=f"enroute_{job.get('requestID')}"):
                try:
                    r = requests.put(f"{API_BASE}/requests/{job.get('requestID')}", json={"status": "En Route"})
                    r.raise_for_status()
                    st.success("Status updated to En Route")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to update status: {e}")
        with c4:
            if st.button("Mark Complete", key=f"complete_{job.get('requestID')}"):
                try:
                    r = requests.put(f"{API_BASE}/requests/{job.get('requestID')}", json={"status": "Completed"})
                    r.raise_for_status()
                    st.success("Marked completed")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to mark complete: {e}")
