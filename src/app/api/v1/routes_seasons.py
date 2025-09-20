from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
# On suppose que ta lib expose ces services
from footysim.services.schedule_service import generate_round_robin
from footysim.services.match_engine import simulate_match
from footysim.models.fixture import Fixture
from footysim.models.match import Match
from footysim.models.club import Club
from sqlalchemy import select

router = APIRouter(prefix="/seasons", tags=["seasons"])

@router.post("/{season_id}/schedule")
async def create_schedule(
    season_id: int,
    rounds: int = 2,
    start_date: str | None = None,
    force: bool = False,
    session: AsyncSession = Depends(get_session),
):
    from datetime import date
    start = date.fromisoformat(start_date) if start_date else date(2024,8,1)
    cnt = await generate_round_robin(
        session, season_id=season_id, start_date=start, rounds=rounds, clear_existing=force
    )
    return {"added_fixtures": cnt}

@router.post("/{season_id}/simulate")
async def simulate_season(season_id: int, reset: bool = False, session: AsyncSession = Depends(get_session)):
    # récup fixtures de la saison sans match (ou reset si demandé)
    from sqlalchemy import delete
    if reset:
        match_ids = (
            (await session.execute(
                select(Match.id).join(Fixture, Match.fixture_id == Fixture.id).where(Fixture.season_id == season_id)
            )).scalars().all()
        )
        if match_ids:
            from footysim.models.goal import Goal
            await session.execute(delete(Goal).where(Goal.match_id.in_(match_ids)))
            await session.execute(delete(Match).where(Match.id.in_(match_ids)))
            await session.commit()

    fixtures = (
        (await session.execute(
            select(Fixture).where(Fixture.season_id == season_id).order_by(Fixture.round, Fixture.date, Fixture.id)
        )).scalars().all()
    )
    if not fixtures:
        raise HTTPException(404, "Aucune fixture")
    # si pas reset: ne simule que celles sans match
    if not reset:
        from sqlalchemy import select as sel
        filtered = []
        for f in fixtures:
            mid = (await session.execute(sel(Match.id).where(Match.fixture_id == f.id))).scalar_one_or_none()
            if mid is None:
                filtered.append(f)
        fixtures = filtered
        if not fixtures:
            return {"status": "no-op", "message": "rien à simuler"}

    for f in fixtures:
        await simulate_match(session, f.id)
    return {"status": "ok", "simulated": len(fixtures)}
