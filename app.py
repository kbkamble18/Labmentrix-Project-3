import streamlit as st

# Set page config (this runs first)
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Immediately redirect to Home page so "app" never appears in sidebar
st.switch_page("pages/1_Home.py")
