import logging
import requests

logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()
API_URL = "http://web-api:4000/report/revenue"

st.title("Revenue Report")
result = None
with st.sidebar:
    st.subheader("Params")
    interval = st.multiselect("By", ["Month", "Year"])
    by_building = st.checkbox("By building")
    include_empty_apartments = st.checkbox("Include empty apartments")
    if st.button("run"):
        params = {
            "interval": interval,
            "by_build": by_building,
            "include_empty": include_empty_apartments,
        }
        result = requests.get(API_URL, params)


st.subheader("Results")
if result:
    df = pd.DataFrame(result.json())
    st.dataframe(df)
else:
    st.caption("Run the report to generate data.")