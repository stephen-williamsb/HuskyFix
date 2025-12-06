import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Revenue Report")

with st.sidebar:
    st.subheader("Params")
    interval = st.multiselect("By", ["Month", "Year"])
    by_building = st.checkbox("By building")
    include_empty_apartments = st.checkbox("Include empty apartments")

st.subheader("Results")
try:
    mock_data = {"Dates" : [interval, by_building], "Data": [1,4]}
    df = pd.DataFrame(mock_data)
    st.dataframe(df)
except:
    st.caption("Run the report to generate data.")