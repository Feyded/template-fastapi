import asyncio

import app.models
from app.seeders.users import seed_users


async def seed() -> None:
    await seed_users()



if __name__ == "__main__":
    asyncio.run(seed())
