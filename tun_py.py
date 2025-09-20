import asyncio
from dotenv import load_dotenv
from footysim.db.session import AsyncSessionLocal
from footysim.seeds.seed_data import seed_minimal

# 👇 force l’import de tous les modèles pour que les relations soient connues
from footysim.models import club, country, fixture, goal, league, match, player, season, stadium, transfer

load_dotenv()

async def run():
    async with AsyncSessionLocal() as s:
        await seed_minimal(s)

asyncio.run(run())
print("✅ Données seed insérées.")