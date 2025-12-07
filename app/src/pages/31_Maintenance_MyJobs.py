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

# Try to fetch employee list from API (non-fatal). If not available, fall back to small list.
employees = None
try:
    resp = requests.get(f"{API_BASE}/employee", timeout=3)
    if resp.status_code == 200:
        employees = resp.json()
        # if the API returns objects, map to display strings
        if isinstance(employees, list) and employees and isinstance(employees[0], dict):
            emp_options = {str(e.get("employeeID")): f"{e.get('firstName','')} {e.get('lastName','')} (#{e.get('employeeID')})" for e in employees}
        else:
            # if it's just a list of ids
            emp_options = {str(e): f"Employee {e}" for e in employees}
    else:
        employees = None
except Exception:
    employees = None

if employees:
    # Build selectbox values as (display, id)
    emp_items = list(emp_options.items())
    emp_display = [v for k, v in emp_items]
    emp_ids = [int(k) for k, v in emp_items]
    # default index
    try:
        default_idx = emp_ids.index(int(default_emp))
    except Exception:
        default_idx = 0
    selected_idx = st.selectbox("Select employee (filter assigned jobs)", emp_display, index=default_idx)
    employee_id = emp_ids[selected_idx]
else:
    # fallback small list including 7
    # default to 7 if available
    fallback_options = [7, 1, 2, 3]
    try:
        fallback_index = fallback_options.index(int(default_emp))
    except Exception:
        fallback_index = 0
    employee_id = st.selectbox("Select employee (filter assigned jobs)", options=fallback_options, index=fallback_index)

# Filters
col1, col2, col3, col4 = st.columns([2,2,2,1])
with col1:
    # NEW: allow "All dates" checkbox (default True) so the backend is queried for all days for this employee
    all_dates = st.checkbox("All dates", value=True, help="When checked, fetch jobs for all dates for the selected employee.")
    # show date_input only when user unchecks "All dates"
    if not all_dates:
        date_filter = st.date_input("Date", value=date.today())
    else:
        date_filter = None
with col2:
    priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
with col3:
    status_filter = st.selectbox("Status", ["All", "In Progress", "En Route", "Blocked", "Open", "Completed"])
with col4:
    refresh = st.button("Refresh")

def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API GET failed: {e}")
        return []

# Build params to ask the backend to filter by assigned employee
params = {"limit": 500, "employee_id": employee_id}

# Only include date range params if the user requested a specific date (i.e., all_dates is False)
if not all_dates and date_filter is not None:
    # date range: request route expects start_date and end_date in YYYY-MM-DD
    params["start_date"] = date_filter.isoformat()
    params["end_date"] = (date_filter + timedelta(days=1)).isoformat()

# Add server-side status filter if user selected one
if status_filter != "All":
    # normalize small variations: backend compares exact value, so we send the selected label
    params["status"] = status_filter

# Get jobs from API (backend will check employeeAssigned via employee_id param)
jobs = api_get("/requests", params=params)

# Helper ranking functions (status order & priority)
def status_rank(status):
    s = (status or "").lower()
    if s in ("in progress", "in-progress"):
        return 0
    if s in ("en route", "enroute", "en route"):
        return 1
    if s == "blocked":
        return 2
    if s == "open":
        return 3
    if s in ("completed", "closed", "complete"):
        return 4
    return 5

def priority_rank(p):
    if p is None:
        return 2
    p_low = str(p).lower()
    if p_low in ("high", "5", "4"):
        return 0
    if p_low in ("medium", "3"):
        return 1
    return 2

# Client-side priority filter (if user asked)
if priority_filter != "All":
    pf = priority_filter.lower()
    jobs = [j for j in (jobs or []) if pf in str(j.get("priority", "")).lower() or pf in (str(j.get("priority", "")) or "").lower()]

# If the backend didn't apply status (because it didn't accept it), attempt client-side filter too
if status_filter != "All":
    sf = status_filter.lower()
    jobs = [j for j in (jobs or []) if sf == (j.get("activeStatus") or "").lower()]

# Final sort: status (desired order), then higher priority, then most recent dateRequested first
def date_key(d):
    # return string (ISO) or empty so sorting is stable
    return d or ""

jobs_sorted = sorted(
    jobs or [],
    key=lambda j: (
        status_rank(j.get("activeStatus")),
        priority_rank(j.get("priority")),
    ),
)

# To make dateRequested descending inside groups, we'll stable-sort again by dateRequested desc
jobs_sorted = sorted(jobs_sorted, key=lambda j: date_key(j.get("dateRequested")), reverse=True)

st.write(f"Showing {len(jobs_sorted)} jobs assigned to employee {employee_id}")

if not jobs_sorted:
    if all_dates:
        st.info("No jobs found for this employee (for all dates).")
    else:
        st.info("No jobs found for this employee and selected date/filter. You can try 'All dates' or a wider date range.")

# Table with actions
for job in jobs_sorted:
    with st.expander(f"[{job.get('requestID')}] {job.get('issueType')} — Apt {job.get('aptNumber')} ({job.get('buildingID')}) — Priority {job.get('priority')} — Status {job.get('activeStatus')}"):
        c1, c2, c3, c4 = st.columns([4,2,2,2])
        with c1:
            st.markdown(f"**Description:** {job.get('issueDescription') or '—'}")
            st.markdown(f"**Requested:** {job.get('dateRequested')}")
            st.markdown(f"**Student ID:** {job.get('studentRequestingID')}")
            # show assigned employees if backend included them in detail (it doesn't in list endpoint by default)
        with c2:
            if st.button("Open Job Detail", key=f"open_{job.get('requestID')}"):
                # store selected id and go to detail page
                st.session_state["selected_request_id"] = job.get("requestID")
                st.query_params = {"page": "job_detail", "request_id": job.get("requestID")}
                st.rerun()
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
