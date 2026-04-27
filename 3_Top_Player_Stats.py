import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.db_connection import get_engine

st.title("🏆 Top Player Stats")

engine = get_engine()

tab1, tab2 = st.tabs(["🥇 Batting Leaders", "🥇 Bowling Leaders"])

with tab1:
    st.subheader("Top Batting Stats")
    batting_query = """
        SELECT p.player_name, 
               SUM(b.runs) as total_runs,
               MAX(b.runs) as highest_score,
               AVG(b.strike_rate) as avg_sr,
               COUNT(*) as innings
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_name
        HAVING COUNT(*) >= 1
        ORDER BY total_runs DESC LIMIT 15
    """
    with engine.connect() as conn:
        bat_df = pd.read_sql(text(batting_query), conn)
    st.dataframe(bat_df, use_container_width=True)

    st.bar_chart(bat_df.set_index("player_name")["total_runs"])

with tab2:
    st.subheader("Top Bowling Stats")
    bowling_query = """
        SELECT p.player_name, 
               SUM(b.wickets) as total_wickets,
               AVG(b.economy) as avg_economy,
               SUM(b.overs) as total_overs
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_name
        HAVING SUM(b.wickets) >= 1
        ORDER BY total_wickets DESC LIMIT 15
    """
    with engine.connect() as conn:
        bowl_df = pd.read_sql(text(bowling_query), conn)
    st.dataframe(bowl_df, use_container_width=True)

    st.bar_chart(bowl_df.set_index("player_name")["total_wickets"])
