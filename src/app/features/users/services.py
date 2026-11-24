from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions import ConflictError, NotFoundError
from app.features.users.model import User
from app.features.users.schemas import UserCreate


async def list_users(db: AsyncSession, page: int = 1, limit: int = 10) -> list[User]:
    offset = (page - 1) * limit
    statement = select(User).offset(offset).limit(limit)
    return (await db.scalars(statement)).all()


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)

    if user is None:
        raise NotFoundError("User not found.")

    return user


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    existing_user = await db.scalar(select(User).where(User.email == payload.email))

    if existing_user is not None:
        raise ConflictError("A user with this email already exists.")

    user_data = payload.model_dump(exclude=["password"])
    user_data["hashed_password"] = hash_password(payload.password)

    user = User(**user_data)

    await db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
