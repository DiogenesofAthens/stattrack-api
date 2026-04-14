from fastapi import APIRouter, HTTPException
from nba_api.stats.endpoints import LeagueLeaders
import pandas as pd

router = APIRouter()


@router.get("/players")
def get_top_scorers():
    """Return the top 10 scorers in the current NBA season."""
    try:
        leaders = LeagueLeaders(
            league_id="00",
            per_mode48="PerGame",
            scope="S",
            season="2024-25",
            season_type_all_star="Regular Season",
            stat_category_abbreviation="PTS",
        )
        df: pd.DataFrame = leaders.get_data_frames()[0]
        top10 = df.head(10)

        players = []
        for _, row in top10.iterrows():
            players.append(
                {
                    "player_id": int(row["PLAYER_ID"]),
                    "name": row["PLAYER"],
                    "team": row["TEAM"],
                    "gp": int(row["GP"]),
                    "pts": float(row["PTS"]),
                    "reb": float(row["REB"]),
                    "ast": float(row["AST"]),
                    "fg_pct": float(row["FG_PCT"]),
                    "fg3_pct": float(row["FG3_PCT"]),
                    "ft_pct": float(row["FT_PCT"]),
                    "rank": int(row["RANK"]),
                }
            )
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
