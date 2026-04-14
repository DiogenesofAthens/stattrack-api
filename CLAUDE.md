# StatTrack Backend

FastAPI backend for the StatTrack NBA analytics dashboard.

## Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Data source**: `nba_api` (no API key required — scrapes stats.nba.com)
- **Data processing**: pandas

## CORS

CORS is open to `http://localhost:3000` (the Next.js frontend).

## Routers

| File | Prefix | Description |
|------|--------|-------------|
| `routers/players.py` | `/api/players` | Top 10 scorers this season |
| `routers/trends.py` | `/api/trends/{player_id}` | Last 14 games for a player |
| `routers/insights.py` | `/api/insights` | Hot / cold / watch alerts |

## nba_api Notes

- Uses `LeagueLeaders` for season-aggregate stats.
- Uses `PlayerGameLog` for per-game data.
- Hardcoded season: `"2024-25"`. Update this each season.
- nba_api calls hit `stats.nba.com` — expect 1-3 s latency per request.
