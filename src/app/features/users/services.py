from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions import ConflictError, NotFoundError
from app.features.users import repository
from app.features.users.model import User
from app.features.users.schemas import UserCreate


async def list_users(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
) -> list[User]:
    return await repository.get_all(db, page, limit)


async def get_user(
    db: AsyncSession,
    user_id: int,
) -> User:
    user = await repository.get_by_id(db, user_id)

    if user is None:
        raise NotFoundError("User not found.")

    return user


async def create_user(
    db: AsyncSession,
    payload: UserCreate,
) -> User:
    existing_user = await repository.get_by_email(db, payload.email)

    if existing_user is not None:
        raise ConflictError("A user with this email already exists.")

    user_data = payload.model_dump(exclude={"password"})
    user_data["hashed_password"] = hash_password(payload.password)

    user = User(**user_data)

    try:
        user = await repository.create(db, user)
        await db.commit()

        return user

    except Exception:
        await db.rollback()
        raise
