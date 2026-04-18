import pandas as pd


def extract_scorecard(data, match_id):
    players = {}
    batting = []
    bowling = []

    scorecard = data.get("scoreCard")

    if not scorecard:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    for innings in scorecard:
        # ---------- BATTING ----------
        batsmen = innings.get("batTeamDetails", {}).get("batsmenData", {})

        for b in batsmen.values():
            player_id = b.get("batId")

            if not player_id:
                continue

            players[player_id] = {
                "player_id": player_id,
                "player_name": b.get("batName"),
            }

            batting.append(
                {
                    "match_id": match_id,
                    "player_id": player_id,
                    "runs": int(b.get("runs", 0)),
                    "balls": int(b.get("balls", 0)),
                    "fours": int(b.get("fours", 0)),
                    "sixes": int(b.get("sixes", 0)),
                    "strike_rate": float(b.get("strikeRate", 0)),
                }
            )

        # ---------- BOWLING ----------
        bowlers = innings.get("bowlTeamDetails", {}).get("bowlersData", {})

        for bw in bowlers.values():
            player_id = bw.get("bowlerId")

            if not player_id:
                continue

            players[player_id] = {
                "player_id": player_id,
                "player_name": bw.get("bowlName"),
            }

            bowling.append(
                {
                    "match_id": match_id,
                    "player_id": player_id,
                    "overs": float(bw.get("overs", 0)),
                    "runs_given": int(bw.get("runs", 0)),
                    "wickets": int(bw.get("wickets", 0)),
                    "economy": float(bw.get("economy", 0)),
                }
            )

    return (
        pd.DataFrame(players.values()),
        pd.DataFrame(batting),
        pd.DataFrame(bowling),
    )
