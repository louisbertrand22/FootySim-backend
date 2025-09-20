from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from footysim.services.players_service import best_players as svc_best_players

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/best")
async def best_players(
    season_id: int | None = Query(default=None, description="Filtrer par saison (ID)."),
    position: str | None = Query(default=None, description="Filtrer par poste : GK/DF/MF/FW"),
    limit: int = Query(default=20, ge=1, le=200, description="Nombre de joueurs à retourner (1–200)"),
    session: AsyncSession = Depends(get_session),
):
    try:
        players = await svc_best_players(
            session, season_id=season_id, position=position, limit=limit
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {
        "season_id": season_id,
        "position": position.upper() if position else None,
        "limit": limit,
        "players": players,
    }
