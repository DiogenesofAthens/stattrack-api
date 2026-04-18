import logging
import traceback

from fastapi import APIRouter, HTTPException
from nba_api.stats.endpoints import LeagueLeaders
import pandas as pd

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/scoring-leaders")
def get_scoring_leaders():
    """Return the top 10 scorers with name, team, PPG, and player ID."""
    try:
        leaders = LeagueLeaders(
            league_id="00",
            per_mode48="PerGame",
            scope="S",
            season="2025-26",
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
                    "pts": float(row["PTS"]),
                }
            )
        return {"players": players}
    except Exception as e:
        logger.error("500 error in get_scoring_leaders():\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
