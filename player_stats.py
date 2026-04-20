import requests
import os
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
}


def fetch_player_batting(player_id):
    url = "https://cricbuzz-cricket.p.rapidapi.com/players/get-batting"
    params = {"playerId": player_id}

    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()


def fetch_player_bowling(player_id):
    url = "https://cricbuzz-cricket.p.rapidapi.com/players/get-bowling"
    params = {"playerId": player_id}

    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()
