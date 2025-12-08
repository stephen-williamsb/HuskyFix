import requests
import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()
API_URL = "http://web-api:4000/report/cost"

st.title("Monthly Cost Report")

# 主页面上的月份选择
col1, col2 = st.columns([1, 3])
with col1:
    year_month = st.text_input(
        "Year-Month", 
        value="2024-01",
        placeholder="YYYY-MM"
    )
    
with col2:
    by_building = st.checkbox("By building")

# 运行按钮
if st.button("Run Report", type="primary"):
    if year_month:
        # 构建日期范围
        from_date = f"{year_month}-01"
        until_date = f"{year_month}-31"
        
        params = {
            "from": from_date,
            "to": until_date,
            "by_build": by_building
        }
        
        with st.spinner("Fetching data..."):
            result = requests.get(API_URL, params)
        
        # 显示结果
        st.subheader(f"Results for {year_month}")
        if result.status_code == 200:
            df = pd.DataFrame(result.json())
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("No data found for the selected month")
        else:
            st.error(f"Failed to fetch data: {result.status_code}")
    else:
        st.error("Please enter a month (YYYY-MM)")
else:
    st.caption("Enter month above and click 'Run Report'")