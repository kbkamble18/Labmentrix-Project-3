import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.db_connection import get_engine

st.title("🔧 CRUD Operations - Players")

engine = get_engine()

# ====================== VIEW ALL PLAYERS ======================
st.subheader("📋 All Players")

search = st.text_input("🔍 Search by player name or country", "")

query = """
    SELECT 
        player_id,
        player_name as full_name,
        country,
        playing_role,
        batting_style,
        bowling_style
    FROM players
"""
if search:
    query += f" WHERE player_name ILIKE '%{search}%' OR country ILIKE '%{search}%'"

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No players found yet. Run `python -m api.fetch_data` first.")

# ====================== ADD NEW PLAYER ======================
st.subheader("➕ Add New Player")

with st.form("add_player_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *", key="add_name")
        country = st.text_input("Country", key="add_country")
    with col2:
        role = st.selectbox(
            "Playing Role",
            ["Batsman", "Bowler", "All-rounder", "Wicket-keeper", "Not Available"],
        )
        bat_style = st.text_input("Batting Style", key="add_bat")
    bowl_style = st.text_input("Bowling Style", key="add_bowl")

    submitted = st.form_submit_button("Add Player")
    if submitted and name:
        try:
            with engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO players (player_name, country, playing_role, batting_style, bowling_style)
                    VALUES (:name, :country, :role, :bat_style, :bowl_style)
                """),
                    {
                        "name": name,
                        "country": country or "Unknown",
                        "role": role,
                        "bat_style": bat_style or "Not Available",
                        "bowl_style": bowl_style or "Not Available",
                    },
                )
            st.success(f"✅ Player '{name}' added successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ====================== EDIT PLAYER ======================
st.subheader("✏️ Edit Player")

if not df.empty:
    player_list = df["full_name"].tolist()
    selected_player = st.selectbox(
        "Select player to edit", player_list, key="edit_select"
    )

    if selected_player:
        # Fetch current player using player_name (safe)
        edit_query = text("SELECT * FROM players WHERE player_name = :name")
        with engine.connect() as conn:
            current_df = pd.read_sql(edit_query, conn, params={"name": selected_player})
            if not current_df.empty:
                current = current_df.iloc[0]

                with st.form("edit_player_form"):
                    new_name = st.text_input("Full Name", value=current["player_name"])
                    new_country = st.text_input(
                        "Country", value=current.get("country") or ""
                    )
                    new_role = st.selectbox(
                        "Playing Role",
                        [
                            "Batsman",
                            "Bowler",
                            "All-rounder",
                            "Wicket-keeper",
                            "Not Available",
                        ],
                        index=[
                            "Batsman",
                            "Bowler",
                            "All-rounder",
                            "Wicket-keeper",
                            "Not Available",
                        ].index(current.get("playing_role") or "Not Available"),
                    )
                    new_bat = st.text_input(
                        "Batting Style", value=current.get("batting_style") or ""
                    )
                    new_bowl = st.text_input(
                        "Bowling Style", value=current.get("bowling_style") or ""
                    )

                    if st.form_submit_button("Update Player"):
                        try:
                            with engine.connect() as conn:
                                conn.execute(
                                    text("""
                                    UPDATE players 
                                    SET player_name = :name, 
                                        country = :country, 
                                        playing_role = :role, 
                                        batting_style = :bat, 
                                        bowling_style = :bowl
                                    WHERE player_id = :pid
                                """),
                                    {
                                        "name": new_name,
                                        "country": new_country or "Unknown",
                                        "role": new_role,
                                        "bat": new_bat or "Not Available",
                                        "bowl": new_bowl or "Not Available",
                                        "pid": current["player_id"],
                                    },
                                )
                            st.success("✅ Player updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                st.error("Could not load player data.")
else:
    st.info("No players to edit yet.")

# ====================== DELETE PLAYER ======================
st.subheader("🗑️ Delete Player")

if not df.empty:
    delete_player = st.selectbox(
        "Select player to delete", df["full_name"].tolist(), key="delete_select"
    )
    if st.button("🗑️ Delete Selected Player", type="secondary"):
        if st.checkbox("⚠️ I confirm I want to permanently delete this player"):
            try:
                with engine.connect() as conn:
                    conn.execute(
                        text("DELETE FROM players WHERE player_name = :name"),
                        {"name": delete_player},
                    )
                st.success(f"✅ Player '{delete_player}' deleted!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
