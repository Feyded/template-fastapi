from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from app.features.tasks import repository
from app.features.tasks.model import Task
from app.features.tasks.schemas import TaskCreate, TaskUpdate


async def list_tasks(db: AsyncSession, page, limit):
    return await repository.get_all(db, page, limit)

async def create_task(
    db: AsyncSession,
    payload: TaskCreate,
    user_id,
):
    task = Task(
        title=payload.title,
        description=payload.description,
        user_id=user_id,
    )

    task = await repository.create(db, task)

    await db.commit()

    return task


async def update_task(
    db: AsyncSession,
    task_id,
    payload: TaskUpdate,
    user_id,
):
    task = await repository.get_by_id(db, task_id, user_id)

    if not task:
        raise NotFoundError("Task not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    task = await repository.update(db, task)

    await db.commit()

    return task


async def delete_task(db: AsyncSession, task_id, user_id):
    task = await repository.get_by_id(db, task_id, user_id)

    if not task:
        raise NotFoundError("Task not found")

    await repository.delete(db, task)

    await db.commit()
