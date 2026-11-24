from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.tasks.model import Task


async def get_all(db: AsyncSession, page, limit):
    offset = (page - 1) * limit
    statement = select(Task).offset(offset).limit(limit)

    result = await db.scalars(statement)

    return result.all()


async def get_by_id(db: AsyncSession, task_id, user_id):
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
    )

    return await db.scalar(statement)


async def create(db: AsyncSession, task: Task):
    db.add(task)
    await db.flush()
    await db.refresh(task)

    return task


async def update(db: AsyncSession, task: Task):
    await db.flush()
    await db.refresh(task)

    return task


async def delete(db: AsyncSession, task: Task):
    await db.delete(task)
    await db.flush()
