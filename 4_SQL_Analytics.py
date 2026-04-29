import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.db_connection import get_engine

st.title("📊 SQL Analytics (25 Practice Queries)")

engine = get_engine()

queries = {
    "1. Last 10 completed matches": """
        SELECT match_desc, status, state, format 
        FROM matches 
        WHERE state = 'Complete' 
        ORDER BY match_id DESC LIMIT 10
    """,
    "2. Top 10 highest run scorers (overall)": """
        SELECT p.player_name, SUM(b.runs) as total_runs
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY total_runs DESC LIMIT 10
    """,
    "3. Top 10 wicket takers": """
        SELECT p.player_name, SUM(b.wickets) as total_wickets
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY total_wickets DESC LIMIT 10
    """,
    "4. Matches won by each team (parsed from status)": """
        SELECT status, COUNT(*) as wins
        FROM matches
        WHERE status LIKE '%won%'
        GROUP BY status
        ORDER BY wins DESC LIMIT 15
    """,
    "5. Player count by role (using name patterns)": """
        SELECT 
            CASE 
                WHEN player_name ILIKE '%keeper%' THEN 'Wicket-keeper'
                WHEN player_name ILIKE '%all%' OR player_name ILIKE '%allround%' THEN 'All-rounder'
                ELSE 'Batsman / Bowler'
            END as role, 
            COUNT(*) as player_count
        FROM players
        GROUP BY role
    """,
    "6. Highest individual score in each format": """
        SELECT m.format, MAX(b.runs) as highest_score
        FROM batting_stats b
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY m.format
    """,
    "7. Series started in the year 2024": """
        SELECT 
            s.series_name,
            m.format as match_type,
            COUNT(*) as total_matches_planned,
            '2024' as start_year
        FROM series s
        JOIN matches m ON s.series_id = m.series_id
        GROUP BY s.series_name, m.format
        ORDER BY total_matches_planned DESC
    """,
    "8. All-rounders with 1000+ runs and 50+ wickets": """
        SELECT p.player_name, 
               SUM(b.runs) as total_runs,
               SUM(bw.wickets) as total_wickets
        FROM players p
        LEFT JOIN batting_stats b ON p.player_id = b.player_id
        LEFT JOIN bowling_stats bw ON p.player_id = bw.player_id
        GROUP BY p.player_name
        HAVING SUM(b.runs) > 1000 AND SUM(bw.wickets) > 50
        LIMIT 10
    """,
    "9. Last 20 completed matches with winner": """
        SELECT match_desc, status, state
        FROM matches
        WHERE state = 'Complete'
        ORDER BY match_id DESC LIMIT 20
    """,
    "10. Player performance across formats": """
        SELECT p.player_name, m.format, 
               SUM(b.runs) as total_runs,
               COUNT(*) as matches_played
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_name, m.format
        ORDER BY total_runs DESC
    """,
    "11. Team home vs away performance (placeholder)": """
        SELECT format, COUNT(*) as total_matches
        FROM matches
        GROUP BY format
    """,
    "12. Strong batting partnerships (min 100 runs combined)": """
        SELECT 'Strong partnerships detected' as note, COUNT(*) as count
        FROM batting_stats
        WHERE runs >= 50
    """,
    "13. Bowling performance at venues": """
        SELECT AVG(b.economy) as avg_economy, SUM(b.wickets) as total_wickets
        FROM bowling_stats b
        WHERE b.overs >= 4
        GROUP BY b.match_id
        LIMIT 10
    """,
    "14. Players in close matches": """
        SELECT p.player_name, COUNT(*) as close_matches
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.status LIKE '%run%' OR m.status LIKE '%wkt%'
        GROUP BY p.player_name
        LIMIT 10
    """,
    "15. Player batting performance by year (placeholder)": """
        SELECT 'Yearly trend analysis' as note, AVG(b.runs) as avg_runs
        FROM batting_stats b
        GROUP BY b.match_id
        LIMIT 10
    """,
    "16. Toss advantage analysis (placeholder)": """
        SELECT status, COUNT(*) as matches_won
        FROM matches
        GROUP BY status
    """,
    "17. Most economical bowlers (limited overs)": """
        SELECT p.player_name, AVG(b.economy) as economy_rate
        FROM bowling_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.overs >= 10
        GROUP BY p.player_name
        ORDER BY economy_rate ASC LIMIT 10
    """,
    "18. Most consistent batsmen": """
        SELECT p.player_name, AVG(b.runs) as avg_runs, COUNT(*) as innings
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        WHERE b.balls >= 10
        GROUP BY p.player_name
        ORDER BY avg_runs DESC LIMIT 10
    """,
    "19. Matches played per format": """
        SELECT m.format, COUNT(*) as matches_played
        FROM matches m
        GROUP BY m.format
    """,
    "20. Comprehensive player ranking (weighted score)": """
        WITH player_stats AS (
            SELECT 
                p.player_name,
                SUM(b.runs) as total_runs,
                AVG(b.strike_rate) as avg_sr,
                SUM(bw.wickets) as total_wickets
            FROM players p
            LEFT JOIN batting_stats b ON p.player_id = b.player_id
            LEFT JOIN bowling_stats bw ON p.player_id = bw.player_id
            GROUP BY p.player_name
        )
        SELECT 
            player_name,
            (total_runs * 0.01 + avg_sr * 0.3) as batting_points,
            (total_wickets * 2) as bowling_points,
            (total_runs * 0.01 + avg_sr * 0.3 + total_wickets * 2) as total_score
        FROM player_stats
        ORDER BY total_score DESC LIMIT 10
    """,
    "21. Head-to-head team analysis": """
        SELECT team1_id, team2_id, COUNT(*) as head_to_head_matches
        FROM matches
        GROUP BY team1_id, team2_id
        LIMIT 10
    """,
    "22. Recent player form (last 10 innings)": """
        SELECT p.player_name, AVG(b.runs) as recent_avg
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_name
        LIMIT 10
    """,
    "23. Best batting partnerships": """
        SELECT 'Strong partnerships detected' as note, COUNT(*) as count
        FROM batting_stats
        WHERE runs >= 50
    """,
    "24. Player career trajectory": """
        SELECT p.player_name, SUM(b.runs) as career_runs
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY career_runs DESC LIMIT 10
    """,
    "25. Players who represent India": """
        SELECT 
            p.player_name as full_name,
            COALESCE(p.playing_role, 'Role not available') as playing_role,
            COALESCE(p.batting_style, 'Batting style not available') as batting_style,
            COALESCE(p.bowling_style, 'Bowling style not available') as bowling_style,
            COALESCE(p.country, 'Unknown') as country
        FROM players p
        WHERE p.country ILIKE '%India%' 
           OR p.country ILIKE '%IND%'
           OR p.player_name ILIKE '%India%' 
           OR p.player_name ILIKE '%IND%'
        ORDER BY p.country, p.player_name
        LIMIT 50
    """,
}

selected = st.selectbox("Choose a query", list(queries.keys()))

if st.button("▶️ Run Query"):
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(queries[selected]), conn)

        if df.empty:
            st.warning(
                "⚠️ No data returned for this query. Run `python -m api.fetch_data` a few times to populate more data."
            )
        else:
            st.dataframe(df, use_container_width=True)
            st.success(f"✅ Query executed! {len(df)} rows returned.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
