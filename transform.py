import pandas as pd


def extract_all_tables(data):
    matches = []
    teams = {}
    venues = {}
    series_list = {}

    for type_match in data.get("typeMatches", []):
        for series in type_match.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper")
            if not wrapper:
                continue

            series_id = wrapper.get("seriesId")
            series_name = wrapper.get("seriesName")

            series_list[series_id] = {
                "series_id": series_id,
                "series_name": series_name,
            }

            for match in wrapper.get("matches", []):
                info = match.get("matchInfo", {})

                team1 = info.get("team1", {})
                team2 = info.get("team2", {})
                venue = info.get("venueInfo", {})

                # Teams
                teams[team1.get("teamId")] = {
                    "team_id": team1.get("teamId"),
                    "team_name": team1.get("teamName"),
                    "team_short_name": team1.get("teamSName"),
                }

                teams[team2.get("teamId")] = {
                    "team_id": team2.get("teamId"),
                    "team_name": team2.get("teamName"),
                    "team_short_name": team2.get("teamSName"),
                }

                # Venues
                venues[venue.get("id")] = {
                    "venue_id": venue.get("id"),
                    "venue_name": venue.get("ground"),
                    "city": venue.get("city"),
                }

                # Matches
                matches.append(
                    {
                        "match_id": info.get("matchId"),
                        "series_id": info.get("seriesId"),
                        "match_desc": info.get("matchDesc"),
                        "format": info.get("matchFormat"),
                        "state": info.get("state"),
                        "status": info.get("status"),
                        "team1_id": team1.get("teamId"),
                        "team2_id": team2.get("teamId"),
                        "venue_id": venue.get("id"),
                    }
                )

    return (
        pd.DataFrame(matches),
        pd.DataFrame(teams.values()),
        pd.DataFrame(venues.values()),
        pd.DataFrame(series_list.values()),
    )


def extract_matches(data):
    matches_list = []

    try:
        for type_match in data.get("typeMatches", []):
            for series in type_match.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper")
                if not wrapper:
                    continue

                for match in wrapper.get("matches", []):
                    info = match.get("matchInfo", {})

                    team1 = info.get("team1", {})
                    team2 = info.get("team2", {})
                    venue = info.get("venueInfo", {})

                    match_record = {
                        "match_id": info.get("matchId"),
                        "series_id": info.get("seriesId"),
                        "series_name": info.get("seriesName"),
                        "match_desc": info.get("matchDesc"),
                        "format": info.get("matchFormat"),
                        "state": info.get("state"),
                        "status": info.get("status"),
                        "team1_id": team1.get("teamId"),
                        "team1_name": team1.get("teamName"),
                        "team2_id": team2.get("teamId"),
                        "team2_name": team2.get("teamName"),
                        "venue_id": venue.get("id"),
                        "venue_name": venue.get("ground"),
                        "city": venue.get("city"),
                    }

                    matches_list.append(match_record)

    except Exception as e:
        print("Error extracting matches:", e)

    return pd.DataFrame(matches_list)
