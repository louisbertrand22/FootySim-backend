from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_session
from footysim.services.table_service import build_table
from footysim.models.club import Club

router = APIRouter(prefix="/table", tags=["Classement"])


@router.get("/{season_id}")
async def get_table(
    season_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Retourne le classement pour une saison donnée.
    Classement trié par points, différence de buts, puis buts marqués.
    """
    try:
        rows = await build_table(session, season_id)

        # On récupère les noms de clubs
        clubs = {
            c.id: c.name
            for c in (await session.execute(Club.__table__.select())).all()
        }

        # Construire une liste pour le tri
        table = []
        for club_id, row in rows.items():
            table.append(
                {
                    "club_id": club_id,
                    "club": clubs.get(club_id, f"Club {club_id}"),
                    "played": row.played,
                    "won": row.won,
                    "draw": row.draw,
                    "lost": row.lost,
                    "gf": row.gf,
                    "ga": row.ga,
                    "gd": row.gf - row.ga,
                    "pts": row.pts,
                }
            )

        # Tri : points desc, diff de buts desc, buts marqués desc
        table.sort(key=lambda x: (x["pts"], x["gd"], x["gf"]), reverse=True)

        # Ajout du rang
        for idx, row in enumerate(table, start=1):
            row["rank"] = idx

        return {"season_id": season_id, "table": table}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
