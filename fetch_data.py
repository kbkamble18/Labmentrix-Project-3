import requests
import os
import pandas as pd
import time
from dotenv import load_dotenv
from datetime import datetime

from processing.transform import extract_all_tables
from processing.scorecard_transform import extract_live_scorecard
from db.db_connection import get_engine
from db.insert_data import upsert_dataframe

from sqlalchemy import MetaData

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

print(f"🔑 Using API Key: {API_KEY[:8]}...{API_KEY[-4:]}")

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
    "Content-Type": "application/json",
}

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"


def fetch_with_retry(url, name="API", params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=20)
        if response.status_code == 429:
            print(f"🚨 Rate limit on {name}")
            time.sleep(8)
            return None
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ {name} error: {e}")
        return None


def fetch_live_matches():
    url = f"{BASE_URL}/matches/v1/live"
    return fetch_with_retry(url, "Live Matches")


def fetch_live_scorecard(match_id):
    url = f"{BASE_URL}/mcenter/v1/{match_id}/hscard"
    return fetch_with_retry(url, f"Live Scorecard {match_id}")


def fetch_live_commentary(match_id):
    url = f"{BASE_URL}/mcenter/v1/{match_id}/hcomm"
    return fetch_with_retry(url, f"Commentary {match_id}")


# ======================== MAIN ========================
if __name__ == "__main__":
    print(f"\n🚀 LIVE Fetch started at {datetime.now().strftime('%H:%M:%S')}\n")

    live_data = fetch_live_matches()
    if not live_data:
        print("❌ No live data. Exiting.")
        exit()

    matches_df, teams_df, venues_df, series_df = extract_all_tables(live_data)

    if matches_df.empty:
        print("⚠️ No live matches.")
        exit()

    matches_df.drop_duplicates(subset=["match_id"], inplace=True)
    print(f"✅ Live Matches: {len(matches_df)}")

    engine = get_engine()
    if not engine:
        print("❌ DB failed.")
        exit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    MAX_LIVE = 3
    live_matches = matches_df.head(MAX_LIVE)

    players_df = pd.DataFrame()
    batting_df = pd.DataFrame()
    bowling_df = pd.DataFrame()

    debug_done = False

    for _, row in live_matches.iterrows():
        match_id = row["match_id"]
        print(f"\n➡️ Processing LIVE Match: {match_id}")

        scorecard = fetch_live_scorecard(match_id)

        if scorecard:
            # === DEEP DEBUG (only first match) ===
            if not debug_done:
                print("\n========== DEEP DEBUG ==========")
                print(f"Top level keys: {list(scorecard.keys())}")

                if "scorecard" in scorecard and len(scorecard["scorecard"]) > 0:
                    first_innings = scorecard["scorecard"][0]
                    print(f"\nFirst innings keys: {list(first_innings.keys())}")

                    # Check for batting
                    if "batTeamDetails" in first_innings:
                        print("Found: batTeamDetails")
                        print(
                            f"  batTeamDetails keys: {list(first_innings['batTeamDetails'].keys())}"
                        )
                    elif "battingTeam" in first_innings:
                        print("Found: battingTeam")
                    else:
                        print("No standard batting section found")

                    # Check for bowling
                    if "bowlTeamDetails" in first_innings:
                        print("Found: bowlTeamDetails")
                    elif "bowlingTeam" in first_innings:
                        print("Found: bowlingTeam")
                    else:
                        print("No standard bowling section found")
                print("========== END DEBUG ==========\n")
                debug_done = True

            p, b, bw = extract_live_scorecard(scorecard, match_id)
            players_df = pd.concat([players_df, p], ignore_index=True)
            batting_df = pd.concat([batting_df, b], ignore_index=True)
            bowling_df = pd.concat([bowling_df, bw], ignore_index=True)

            print(f"   ✅ Scorecard: {len(b)} batting, {len(bw)} bowling rows")
        else:
            print("   ⚠️ No scorecard data")

    print(
        f"\n📊 Final → Players: {len(players_df)} | Batting: {len(batting_df)} | Bowling: {len(bowling_df)}"
    )

    # Upsert (safe)
    try:
        if not players_df.empty:
            upsert_dataframe(
                players_df, metadata.tables["players"], engine, "player_id"
            )
        if not batting_df.empty:
            upsert_dataframe(
                batting_df,
                metadata.tables["batting_stats"],
                engine,
                ["match_id", "player_id"],
            )
        if not bowling_df.empty:
            upsert_dataframe(
                bowling_df,
                metadata.tables["bowling_stats"],
                engine,
                ["match_id", "player_id"],
            )

        if not matches_df.empty:
            upsert_dataframe(matches_df, metadata.tables["matches"], engine, "match_id")

        print("\n🎉 SUCCESS!")
    except Exception as e:
        print(f"❌ DB Error: {e}")
