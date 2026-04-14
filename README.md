# StatTrack API

FastAPI backend for the StatTrack NBA analytics dashboard.

## Requirements

- Python 3.10+

## Setup & Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/players` | Top 10 scorers this season |
| GET | `/api/trends/{player_id}` | Last 14 games for a player |
| GET | `/api/insights` | Hot / cold / watch alerts for top scorers |

## Example Requests

```bash
# Top 10 scorers
curl http://localhost:8000/api/players

# Last 14 games for Shai Gilgeous-Alexander (player_id: 1628983)
curl http://localhost:8000/api/trends/1628983

# Insights / alerts
curl http://localhost:8000/api/insights
```

## Notes

- Data is fetched live from `stats.nba.com` via the `nba_api` package — no API key needed.
- Expect 1–3 seconds of latency per endpoint due to upstream NBA API calls.
- Season is hardcoded to `2024-25` in each router; update for future seasons.
