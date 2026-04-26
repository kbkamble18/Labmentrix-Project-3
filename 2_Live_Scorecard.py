import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.db_connection import get_engine

st.title(" Live Scorecard")

engine = get_engine()

# Main matches list
query = """
    SELECT 
        m.match_id,
        m.match_desc,
        m.status,
        m.format,
        m.state,
        t1.team_name AS team1,
        t2.team_name AS team2,
        v.venue_name
    FROM matches m
    LEFT JOIN teams t1 ON m.team1_id = t1.team_id
    LEFT JOIN teams t2 ON m.team2_id = t2.team_id
    LEFT JOIN venues v ON m.venue_id = v.venue_id
    WHERE m.state IN ('In Progress', 'Live') OR m.state = 'Complete'
    ORDER BY m.match_id DESC
"""

with engine.connect() as conn:
    matches_df = pd.read_sql(text(query), conn)

if matches_df.empty:
    st.warning("No matches found. Run `python -m api.fetch_data` to refresh.")
else:
    st.dataframe(matches_df, use_container_width=True)

    # Detailed scorecard
    selected_match = st.selectbox(
        "Select match to view full scorecard", matches_df["match_desc"].unique()
    )
    match_id = int(
        matches_df[matches_df["match_desc"] == selected_match]["match_id"].iloc[0]
    )

    st.subheader(f" Scorecard for: {selected_match} (Match ID: {match_id})")

    # Batting
    batting_query = """
        SELECT p.player_name, b.runs, b.balls, b.fours, b.sixes, b.strike_rate
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.match_id = :mid
        ORDER BY b.runs DESC
    """
    # Bowling
    bowling_query = """
        SELECT p.player_name, b.overs, b.runs_given, b.wickets, b.economy
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.match_id = :mid
        ORDER BY b.wickets DESC
    """

    with engine.connect() as conn:
        batting_df = pd.read_sql(text(batting_query), conn, params={"mid": match_id})
        bowling_df = pd.read_sql(text(bowling_query), conn, params={"mid": match_id})

    # Debug info
    st.caption(
        f" Debug: Found {len(batting_df)} batting rows and {len(bowling_df)} bowling rows for this match"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Batting")
        if batting_df.empty:
            st.info("No batting data available for this match yet.")
            st.warning(
                " Try running `python -m api.fetch_data` again to refresh scorecard data."
            )
        else:
            st.dataframe(batting_df, use_container_width=True)

    with col2:
        st.subheader(" Bowling")
        if bowling_df.empty:
            st.info("No bowling data available for this match yet.")
            st.warning(
                " Try running `python -m api.fetch_data` again to refresh scorecard data."
            )
        else:
            st.dataframe(bowling_df, use_container_width=True)

st.info(" Refresh data anytime with: `python -m api.fetch_data`")
