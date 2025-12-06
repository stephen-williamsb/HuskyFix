import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Cost Report")

with st.sidebar:
    st.subheader("Params")
    from_date = st.date_input("From", max_value="today", help="Inclusive")
    until_date = st.date_input("Until", value="today", max_value="today", help="Inclusive")
    by_building = st.checkbox("By building")


st.subheader("Results")
try:
    mock_data = {"Dates" : [from_date, until_date], "Data": [1,4]}
    df = pd.DataFrame(mock_data)
    st.dataframe(df)
except:
    st.caption("Run the report to generate data.")