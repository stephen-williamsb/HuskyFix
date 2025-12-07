import logging
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Student / Tenant Portal")

first_name = st.session_state.get("first_name", "Student")
st.write(f"Welcome, **{first_name}**! What would you like to do?")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, _ = st.columns(2)

with col1:
    st.subheader("Create")
    if st.button("Submit a new maintenance request", use_container_width=True):
        st.switch_page("pages/41_Student_New_Request.py")

with col2:
    st.subheader("Photos")
    if st.button("Attach a photo to a request", use_container_width=True):
        st.switch_page("pages/42_Student_Attach_Photo.py")

with col3:
    st.subheader("View & Manage")
    if st.button("View all of my requests", use_container_width=True):
        st.switch_page("pages/43_Student_View_Requests.py")

with col4:
    st.subheader("Cancel")
    if st.button("Cancel a maintenance request", use_container_width=True):
        st.switch_page("pages/44_Student_Cancel_Request.py")

with col5:
    st.subheader("History & Ratings")
    if st.button("Recently updated requests", use_container_width=True):
        st.switch_page("pages/45_Student_Recent_Requests.py")
    if st.button("Rate a completed request", use_container_width=True):
        st.switch_page("pages/46_Student_Rate_Request.py")