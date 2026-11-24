from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.users.model import User


async def get_all(
    db: AsyncSession,
    page: int,
    limit: int,
) -> list[User]:
    offset = (page - 1) * limit

    statement = select(User).order_by(User.id.desc()).offset(offset).limit(limit)

    result = await db.scalars(statement)

    return result.all()


async def get_by_id(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    return await db.get(User, user_id)


async def get_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return await db.scalar(statement)


async def create(
    db: AsyncSession,
    user: User,
) -> User:
    db.add(user)

    await db.flush()
    await db.refresh(user)

    return user
