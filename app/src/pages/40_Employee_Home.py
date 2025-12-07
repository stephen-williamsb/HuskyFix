import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# ---------------- Page Config ----------------
st.set_page_config(layout="wide")

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

# ---------------- Page Title ----------------
st.title(f"Welcome Maintenance Worker, {st.session_state['first_name']}.")

st.write("")
st.write("")
st.write("### What would you like to do today?")

# ---------------- Actions / Navigation Buttons ----------------

# View assigned prioritized work orders (Stories 2.1 & 2.2)
if st.button(
    "View My Work Orders",
    type="primary",
    use_container_width=True,
):
    st.switch_page("pages/31_Maintenance_MyJobs.py")


# Update job status and ETA (Stories 2.3 & 2.5)
if st.button(
    "Update Job Status & ETA",
    type="primary",
    use_container_width=True,
):
    st.switch_page("pages/32_Maintenance_JobDetail.py")


# Parts inventory, requests, and job completion (Stories 2.4 & 2.6)
if st.button(
    "Parts Inventory & Job Completion",
    type="primary",
    use_container_width=True,
):
    st.switch_page("pages/33_Maintenance_Parts.py")
