import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

st.title(f"Hi, {st.session_state['first_name']}")

reports = [
    # (Link, Name, Type, Description)
    ("pages/102_Report_Window.py" ,"Active Requests", "Maintenance", "Fetches all active maintenance requests with details"),
    ("pages/103_Monthly_Report.py","AVG Requests/Month", "Maintenance", "Returns the average requests per month by request type"),
    ("pages/104_Building_Requests.py", "Requests/Building", "Maintanence", "Number of requests per building in a time frame"),
    ("pages/105_Revenue_Report.py", "Total Revenue", "Finances", "Total revenue by month or year"),
    ("pages/106_Cost_Report.py", "Total Cost", "Finances", "Total maintenance costs optionally grouped by building"),
    ("pages/107_Vacancies_Report.py", "Vacancies", "Management", "Total vacancies optionally grouped by building"),
]

col1, col2, col3 = st.columns([1, 1, 2], gap=None)

col1.caption("Name")
col2.caption("Type")
col3.caption("Description")

for report in reports:
    col1.divider()
    col2.divider()
    col3.divider()

    col1.space(2)
    col2.space(1)
    col3.space(1)
    col1.page_link(report[0], label=report[1], icon=":material/article_shortcut:")
    #col1.page_link(report[0], label=report[1], icon=":material/article_shortcut:")
    col2.markdown(report[2])
    col3.markdown(report[3])
    col1.space(2)
    col2.space(1)
    col3.space(1)

