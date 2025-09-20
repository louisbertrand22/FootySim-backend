from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_session
from footysim.models.match import Match
from footysim.models.fixture import Fixture
from footysim.models.club import Club
from sqlalchemy.orm import aliased


router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/{match_id}")
async def get_match(match_id: int, session: AsyncSession = Depends(get_session)):
    HomeClub = aliased(Club)
    AwayClub = aliased(Club)

    row = await session.execute(
        select(
            Match.id,
            Match.home_goals,
            Match.away_goals,
            Fixture.date,
            Fixture.round,
            HomeClub.name,
            AwayClub.name,
        )
        .join(Fixture, Fixture.id == Match.fixture_id)
        .join(HomeClub, Fixture.home_club_id == HomeClub.id)
        .join(AwayClub, Fixture.away_club_id == AwayClub.id)
        .where(Match.id == match_id)
    )

    r = row.first()
    if not r:
        raise HTTPException(404, detail="Match not found")

    mid, hg, ag, d, rnd, home, away = r
    return {
        "id": mid,
        "date": d,
        "round": rnd,
        "home": home,
        "away": away,
        "score": f"{hg}-{ag}",
    }
