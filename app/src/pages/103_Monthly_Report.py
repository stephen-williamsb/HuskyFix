import logging

import requests

logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Average Requests/Month")
API_URL = "http://web-api:4000/report/AVG_Monthly_Requests"
data_col = st.columns(1)
results = None

with st.sidebar:
    st.subheader("Params")
    from_date = st.date_input("From", max_value="today", help="Inclusive")
    until_date = st.date_input("Until", value="today", max_value="today", help="Inclusive")
    selected_type = st.text_input("Request Type", help="Optional")
    descending = st.checkbox("sort descending", value=True)
    if st.button("run"):
        params = {
            "from": from_date,
            "to": until_date,
            "type": selected_type,
            "desc": descending
        }
        results = requests.get(API_URL, params)

st.subheader("Results")
if results:
    df = pd.DataFrame(results.json())
    st.dataframe(df)
else:
    st.caption("Run the report to generate data.")