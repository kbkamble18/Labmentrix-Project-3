import requests
import os

# import json
from dotenv import load_dotenv
from processing.transform import extract_all_tables
from processing.transform import extract_matches
from db.db_connection import get_engine

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": API_HOST}


def fetch_live_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            raise Exception(f"API failed: {response.status_code} - {response.text}")

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None


if __name__ == "__main__":
    data = fetch_live_matches()
    matches_df, teams_df, venues_df, series_df = extract_all_tables(data)

    engine = get_engine()

    if engine:
        try:
            # Insert data
            teams_df.to_sql("teams", engine, if_exists="append", index=False)
            venues_df.to_sql("venues", engine, if_exists="append", index=False)
            series_df.to_sql("series", engine, if_exists="append", index=False)
            matches_df.to_sql("matches", engine, if_exists="append", index=False)

            print("✅ Data inserted into PostgreSQL")

        except Exception as e:
            print("❌ Insert failed:", e)
    '''
    if data:
        """
        print("✅ API Connected Successfully\n")
        print(json.dumps(data, indent=2))
        """
        df = extract_matches(data)
        print("\n✅ Structured Data:\n")
        print(df.head())
    else:
        print("❌ Failed to fetch data")

'''
