# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of data_analyst ------------------------


def ReportsHomeNav():
    st.sidebar.page_link("pages/101_Reports_Home.py", label="Reports", icon=":material/article:")



#### ------------------------ Employee (Maintenance Worker) Role ------------------------

def EmployeeHomeNav():
    st.sidebar.page_link(
        "pages/40_Employee_Home.py", label="Maintenance Worker Home", icon="🔧"
    )

# Page 1 — View assigned prioritized requests (Stories 2.1, 2.2)
def EmployeeRequestsNav():
    st.sidebar.page_link(
        "pages/31_Maintenance_MyJobs.py",
        label="My Work Orders",
        icon="📋"
    )

# Page 2 — Update job status + ETA + notifications (Stories 2.3, 2.5)
def EmployeeStatusUpdateNav():
    st.sidebar.page_link(
        "pages/32_Maintenance_JobDetail.py",
        label="Update Job Status",
        icon="🚚"
    )

# Page 3 — Parts requests + completion logging (Stories 2.4, 2.6)
def EmployeePartsAndCompletionNav():
    st.sidebar.page_link(
        "pages/33_Maintenance_Parts.py",
        label="Parts & Completion",
        icon="🧰"
    )

# Page 4 -- Landlord Role ------------------------
def LandlordNav():
    st.sidebar.page_link(
        "pages/201_Building_List.py",
        label="Building Overview",
        icon="🏢"
    )
    st.sidebar.page_link(
        "pages/202_Request_Management.py",
        label="Request Management",
        icon="🛠️"
    )
    st.sidebar.page_link(
        "pages/203_Monthly_Cost.py",
        label="Monthly Maintenance Cost",
        icon="💲"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    Controls links displayed on the sidebar based on session user role.
    Safe implementation that prevents sidebar disappearing bugs.
    """

    # Always show logo
    st.sidebar.image("assets/logo.png", width=150)

    # Ensure required session keys exist
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if "role" not in st.session_state:
        st.session_state["role"] = None

    # Redirect ONLY if unauthenticated and not on home page
    if not st.session_state["authenticated"] and not show_home:
        st.switch_page("Home.py")
        return

    # Optionally show Home link
    if show_home:
        HomeNav()

    # Render links for authenticated users
    if st.session_state["authenticated"]:

        role = st.session_state.get("role")

        # ---------------- DATA ANALYST ----------------
        if role == "data_analyst":
            ReportsHomeNav()


        # ---------------- EMPLOYEE ----------------
        elif role == "employee":
            EmployeeHomeNav()
            EmployeeRequestsNav()
            EmployeeStatusUpdateNav()
            EmployeePartsAndCompletionNav()

        # ---------------- LANDLORD ----------------
        elif role == "landlord":
            LandlordNav()

    # Always show About
    AboutPageNav()

    # Logout button for any authenticated user
    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.switch_page("Home.py")
