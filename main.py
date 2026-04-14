from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import players, insights, trends

app = FastAPI(title="StatTrack API", description="NBA analytics backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router, prefix="/api")
app.include_router(insights.router, prefix="/api")
app.include_router(trends.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "message": "StatTrack API is running"}
