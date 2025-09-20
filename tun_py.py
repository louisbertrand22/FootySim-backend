import asyncio
from footysim.db.session import init_models
asyncio.run(init_models())
print("✅ tables créées")