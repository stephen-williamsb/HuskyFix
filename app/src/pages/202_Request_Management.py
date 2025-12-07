import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Request Management (Landlord)")

API_BASE = "http://localhost:5000"


def load_requests():
    """load all maintenance requests from backend"""
    try:
        res = requests.get(f"{API_BASE}/requests")
        if res.status_code == 200:
            return res.json()
        else:
            st.error("Failed to load requests.")
            return []
    except Exception as e:
        st.error(f"Error loading requests: {e}")
        return []


def load_employees():
    """Load employees list for assignment"""
    try:
        res = requests.get(f"{API_BASE}/employees")
        if res.status_code == 200:
            return res.json()
        else:
            st.error("Failed to load employees.")
            return []
    except Exception as e:
        st.error(f"Error loading employees list: {e}")
        return []


def update_request(request_id, payload):
    """Update request fields (priority, status, etc.)"""
    res = requests.put(f"{API_BASE}/requests/{request_id}", json=payload)
    return res.status_code == 200


def assign_employee(request_id, employee_id):
    """assign employee to a request"""
    payload = {"employeeID": employee_id, "requestID": request_id}
    res = requests.post(f"{API_BASE}/employeeAssigned", json=payload)
    return res.status_code == 201 or res.status_code == 200


def archive_request(request_id):
    """archive a request"""
    res = requests.delete(f"{API_BASE}/requests/{request_id}")
    return res.status_code == 200

#UI
requests_data = load_requests()

if not requests_data:
    st.warning("No maintenance requests found.")
    st.stop()

df = pd.DataFrame(requests_data)

# Show summary table
st.subheader("All Requests")
st.dataframe(df[["requestID", "issueType", "issueDescription", "activeStatus", "priority", "dateRequested"]],
             use_container_width=True)

# Select request
st.subheader("Manage a Specific Request")

request_ids = df["requestID"].tolist()
selected_id = st.selectbox("Select a Request ID", request_ids)

if selected_id:
    req = df[df["requestID"] == selected_id].iloc[0]

    st.info(f"Selected Request #{selected_id}")

    st.markdown("Update Priority")
    new_priority = st.number_input("New Priority", value=int(req["priority"]), min_value=0, max_value=10)

    if st.button("Update Priority"):
        if update_request(selected_id, {"priority": new_priority}):
            st.success("Priority updated!")
        else:
            st.error("Failed to update priority.")

    st.markdown("Assign Employee")

    employees = load_employees()
    if employees:
        emp_df = pd.DataFrame(employees)
        emp_ids = emp_df["employeeID"].tolist()

        selected_emp = st.selectbox("Choose Employee", emp_ids)
        if st.button("Assign Employee"):
            if assign_employee(selected_id, selected_emp):
                st.success("Employee assigned!")
            else:
                st.error("Assignment failed.")

    st.markdown("Mark as Verified Completed")
    if st.button("Mark Completed"):
        if update_request(selected_id, {"activeStatus": "Completed"}):
            st.success("Request marked completed!")
        else:
            st.error("Failed to update status.")

    st.markdown("Archive Request")
    if st.button("Archive Request"):
        if archive_request(selected_id):
            st.success("Request archived!")
        else:
            st.error("Failed to archive request.")
