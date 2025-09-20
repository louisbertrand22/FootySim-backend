from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes_seasons import router as seasons
from app.api.v1.routes_matches import router as matches
from app.api.v1.routes_table import router as routes_table
from app.api.v1.routes_players import router as routes_players
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title=settings.APP_NAME)

app.include_router(seasons, prefix=settings.API_PREFIX)
app.include_router(matches, prefix=settings.API_PREFIX)
app.include_router(routes_table, prefix=settings.API_PREFIX)
app.include_router(routes_players, prefix=settings.API_PREFIX)

# Swagger: /docs — Redoc: /redoc
