from fastapi import APIRouter, HTTPException
from nba_api.stats.endpoints import LeagueLeaders, PlayerGameLog
import pandas as pd

router = APIRouter()

ALERT_THRESHOLD_HOT = 0.15   # last-5 avg >= 15% above season avg
ALERT_THRESHOLD_COLD = -0.15  # last-5 avg <= 15% below season avg


def _classify(last5_pts: float, season_pts: float) -> str:
    if season_pts == 0:
        return "watch"
    delta = (last5_pts - season_pts) / season_pts
    if delta >= ALERT_THRESHOLD_HOT:
        return "hot"
    if delta <= ALERT_THRESHOLD_COLD:
        return "cold"
    return "watch"


@router.get("/insights")
def get_insights():
    """
    For each of the top 10 scorers, compare their last-5-game average
    points to their season average and emit a hot / cold / watch alert.
    """
    try:
        leaders = LeagueLeaders(
            league_id="00",
            per_mode48="PerGame",
            scope="S",
            season="2025-26",
            season_type_all_star="Regular Season",
            stat_category_abbreviation="PTS",
        )
        df: pd.DataFrame = leaders.get_data_frames()[0].head(10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch league leaders: {e}")

    alerts = []
    for _, row in df.iterrows():
        player_id = int(row["PLAYER_ID"])
        player_name = row["PLAYER"]
        season_pts = float(row["PTS"])

        try:
            game_log = PlayerGameLog(
                player_id=player_id,
                season="2025-26",
                season_type_all_star="Regular Season",
            )
            gl_df: pd.DataFrame = game_log.get_data_frames()[0]
            if gl_df.empty or len(gl_df) < 1:
                last5_pts = season_pts
            else:
                last5_pts = float(gl_df.head(5)["PTS"].mean())
        except Exception:
            last5_pts = season_pts

        alert_type = _classify(last5_pts, season_pts)
        delta_pct = round((last5_pts - season_pts) / season_pts * 100, 1) if season_pts else 0

        alerts.append(
            {
                "player_id": player_id,
                "name": player_name,
                "team": row["TEAM"],
                "alert": alert_type,
                "season_avg_pts": round(season_pts, 1),
                "last5_avg_pts": round(last5_pts, 1),
                "delta_pct": delta_pct,
            }
        )

    # Sort: hot first, then cold, then watch
    order = {"hot": 0, "cold": 1, "watch": 2}
    alerts.sort(key=lambda x: order[x["alert"]])

    return {"insights": alerts}
