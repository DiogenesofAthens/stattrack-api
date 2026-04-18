import logging
import traceback

from fastapi import APIRouter, HTTPException
from nba_api.stats.endpoints import PlayerGameLog
import pandas as pd

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/trends/{player_id}")
def get_player_trends(player_id: int):
    """Return the last 14 games for a given player."""
    try:
        game_log = PlayerGameLog(
            player_id=player_id,
            season="2024-25",
            season_type_all_star="Regular Season",
        )
        df: pd.DataFrame = game_log.get_data_frames()[0]

        if df.empty:
            raise HTTPException(status_code=404, detail="No game log found for this player")

        last14 = df.head(14)

        games = []
        for _, row in last14.iterrows():
            games.append(
                {
                    "game_date": row["GAME_DATE"],
                    "matchup": row["MATCHUP"],
                    "wl": row["WL"],
                    "min": row["MIN"],
                    "pts": int(row["PTS"]),
                    "reb": int(row["REB"]),
                    "ast": int(row["AST"]),
                    "stl": int(row["STL"]),
                    "blk": int(row["BLK"]),
                    "fg_pct": float(row["FG_PCT"]) if pd.notna(row["FG_PCT"]) else None,
                    "fg3_pct": float(row["FG3_PCT"]) if pd.notna(row["FG3_PCT"]) else None,
                    "ft_pct": float(row["FT_PCT"]) if pd.notna(row["FT_PCT"]) else None,
                    "plus_minus": int(row["PLUS_MINUS"]),
                }
            )
        return {"player_id": player_id, "games": games}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("500 error in get_player_trends(player_id=%s):\n%s", player_id, traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
