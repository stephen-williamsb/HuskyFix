##################################################
# Warehouse Manager Home Page
##################################################
# Import Streamlit and sidebar navigation
import streamlit as st
from modules.nav import SideBarLinks

# Configure Streamlit layout
st.set_page_config(
    page_title="Warehouse Manager Portal",
    layout="wide"
)

# Show the sidebar navigation links
SideBarLinks()

# ***************************************************
#    The major content of this page
# ***************************************************



# Page Title
st.title("Warehouse Manager Portal")
st.write("\n")

# ---------------------------------------------------
# Reports Section
# ---------------------------------------------------
st.header("Reports")

if st.button(
        "Show All Reorders",
        type='primary',
        use_container_width=True
):
    st.switch_page("pages/41_Reorders.py")

if st.button(
        "Show Low Stock",
        type='primary',
        use_container_width=True
):

    st.switch_page("pages/42_Low_Stock.py")

# ---------------------------------------------------
# New Products and Categories Section
# ---------------------------------------------------
st.header("New Products and Categories")

if st.button(
        "Add New Product Category",
        type='primary',
        use_container_width=True
):
    
    st.switch_page("pages/43_New_Cat.py")

if st.button(
        "Add New Product",
        type='primary',
        use_container_width=True
):
    
    st.switch_page("pages/44_New_Product.py")
