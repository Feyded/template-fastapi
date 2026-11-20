import asyncio

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.features.users.model import User


async def seed_users() -> None:
    users = [
        {
            "name": "Admin",
            "email": "admin@example.com",
            "role": "admin",
        },
        {
            "name": "John",
            "email": "john.doe@example.com",
            "role": "user",
        },
    ]

    async with SessionLocal() as db:
        try:
            default_password = hash_password("P@ssw0rd")

            statement = select(User.email).where(
                User.email.in_([item["email"] for item in users])
            )

            result = await db.scalars(statement)
            existing_emails = set(result.all())

            for item in users:
                if item["email"] in existing_emails:
                    continue

                print(f"Adding new user with mobile no.: {item['email']}")
                db.add(
                    User(
                        **item,
                        hashed_password=default_password,
                    )
                )

            await db.commit()

        except Exception:
            await db.rollback()
            raise

    print("User seeding completed.")


if __name__ == "__main__":
    asyncio.run(seed_users())
