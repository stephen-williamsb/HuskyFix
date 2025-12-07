import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Building Overview")

API_BASE = "http://web-api:4000"

try:
    response = requests.get(f"{API_BASE}/buildings")
    if response.status_code != 200:
        st.error(f"Error fetching buildings: {response.text}")
    else:
        data = response.json()

        if not data:
            st.warning("No buildings found.")
        else:
            df = pd.DataFrame(data)

            df = df.rename(columns={
                "buildingID": "Building ID",
                "address": "Address",
                "numApartments": "Total Apartments",
                "vacancies": "Vacancies",
                "totalRequests": "Total Requests"
            })

            st.subheader("Building List")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Failed to load buildings. Error: {e}")
