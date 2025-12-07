import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Monthly Maintenance Cost")

API_BASE = "http://localhost:5000"

st.subheader("Select Month")
"""select month"""

month = st.text_input("Enter a month (YYYY-MM)", placeholder="2025-11")

if st.button("Generate Report"):
    if not month or len(month) != 7:
        st.error("Not valid month")
        st.stop()

    try:
        # Call backend API
        url = f"{API_BASE}/Employee/reports/monthly-cost?month={month}"
        response = requests.get(url)

        if response.status_code != 200:
            st.error(f"API Error: {response.text}")
            st.stop()

        data = response.json()

        if not data:
            st.warning("No cost data found for this month.")
        else:
            st.success(f"Showing maintenance costs for {month}")

            # Convert to DataFrame
            df = pd.DataFrame(data)
            df = df.rename(columns={
                "buildingID": "Building ID",
                "address": "Building Address",
                "totalcost": "Total Cost ($)"
            })

            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Failed {e}")
