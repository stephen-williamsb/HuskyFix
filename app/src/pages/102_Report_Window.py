import logging
from http.client import responses

logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests

SideBarLinks()

API_URL = "http://web-api:4000/report/active_requests"


st.title("Active Requests")
st.subheader("Data")

mock_data = {"Data": [1,4], "text": ["womp", "womp"]}
response = requests.get(API_URL)
df = pd.DataFrame(response.json())
st.dataframe(df)
