import streamlit as st

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")

st.title(" Cricbuzz LiveStats Dashboard")
st.markdown("### *Real-time Cricket Analytics Platform*")

# Hero section
st.markdown("""
**Welcome to the ultimate Cricbuzz LiveStats Dashboard!**  

This dashboard fetches live cricket data from Cricbuzz RapidAPI, stores it in PostgreSQL, and gives you:
- Real-time scorecards
- 25 SQL practice queries
- Top player stats with charts
- Full CRUD operations on players

This project fetches live cricket matches from RapidAPI Cricbuzz, stores them in PostgreSQL, and provides powerful analytics through Streamlit.
""")

# Project Description
st.subheader(" About the Project")
st.write("""
This is a full-stack cricket analytics web application that:
- Fetches live & recent matches in real-time
- Stores match, player, batting & bowling data
- Offers 25 SQL practice queries
- Provides full CRUD operations on players
- Delivers interactive dashboards and insights
""")

# Tools Used
st.subheader(" Tools & Technologies")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **Frontend**: Streamlit
    - **Backend**: Python 3
    - **Database**: PostgreSQL
    - **API**: RapidAPI Cricbuzz
    """)
with col2:
    st.markdown("""
    - **Data Processing**: Pandas + SQLAlchemy
    - **Visualization**: Streamlit native components
    - **ORM**: SQLAlchemy
    - **Deployment**: Local (ready for Streamlit Cloud / Docker)
    """)

# Instructions
st.subheader(" How to Use")
st.markdown("""
1. **Refresh Data** → Run `python -m api.fetch_data` in terminal
2. **Live Scorecard** → View current matches
3. **SQL Analytics** → Practice 25 queries
4. **Top Player Stats** → Rankings & insights
5. **CRUD Operations** → Add / Edit / Delete players
""")

# Navigation
st.subheader(" Navigation")
st.info("""
Use the **sidebar** to jump between:
- **Home** (you are here)
- **Live Scorecard**
- **Top Player Stats**
- **SQL Analytics (25 Queries)**
- **CRUD Operations**
""")

# Documentation & Folder Structure
st.subheader(" Project Documentation & Structure")
st.markdown("""
**Key Folders:**
- `api/` → `fetch_data.py` (main ETL script)
- `db/` → Database connection & schema
- `pages/` → All Streamlit pages
- `processing/` → Data transformation logic

**Documentation:**
- Full project spec is in the original PDF
- Database schema → `CricBuzz.sql`
- Requirements → `requirements.txt`
""")

st.markdown("---")
st.caption(
    "Cricket analytics experience | Last updated: "
    + st.session_state.get("last_refresh", "Now")
)
