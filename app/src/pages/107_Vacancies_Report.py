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
    by_building = st.checkbox("By building")

st.subheader("Results")
try:
    mock_data = {"Dates" : [5,4], "Data": [1,4]}
    df = pd.DataFrame(mock_data)
    st.dataframe(df)
except:
    st.caption("Run the report to generate data.")