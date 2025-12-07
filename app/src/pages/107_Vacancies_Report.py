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
API_URL = "http://web-api:4000/report/vacancies"
st.title("Vacancy Report")
result = None
with st.sidebar:
    st.subheader("Params")
    by_building = st.checkbox("By building")
    if st.button("run"):
        params = {"by_build": by_building}
        result = requests.get(API_URL, params)

st.subheader("Results")
if result:
    df = pd.DataFrame(result.json())
    st.dataframe(df)
else:
    st.caption("Run the report to generate data.")