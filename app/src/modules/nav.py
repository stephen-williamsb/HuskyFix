# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


def ReportsHomeNav():
    st.sidebar.page_link("pages/101_Reports_Home.py", label="Reports", icon=":material/article:")


## ------------------------ Examples for Role of usaid_worker ------------------------

def usaidWorkerHomeNav():
    st.sidebar.page_link(
        "pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠"
    )


def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")


def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )

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

        # ---------------- POL STRAT ADVISOR ----------------
        if role == "data_analyst":
            ReportsHomeNav()

        # ---------------- USAID WORKER ----------------
        elif role == "usaid_worker":
            usaidWorkerHomeNav()
            NgoDirectoryNav()
            AddNgoNav()
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

        # ---------------- ADMIN ----------------
        elif role == "administrator":
            AdminPageNav()

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
