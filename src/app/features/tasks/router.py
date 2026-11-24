from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies import CurrentUser, DbSession, require_role
from app.features.tasks import services as task_service
from app.features.tasks.schemas import (
    TaskCreate,
    TaskListResponse,
    TaskSingleResponse,
    TaskUpdate,
)

router = APIRouter(
    prefix="/tasks", tags=["Tasks"], dependencies=[Depends(require_role(["user"]))]
)

@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
):
    tasks = await task_service.list_tasks(db, page, limit)
    return {"message": "Tasks retrieved successfully", "data": tasks}


@router.get("/{task_id}", response_model=TaskSingleResponse)
async def get_task(
    task_id: int,
    db: DbSession,
):
    task = await task_service.get_task(db, task_id)

    return {
        "message": "Task retrieved successfully",
        "data": task,
    }


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: DbSession):
    await task_service.delete_task(db, task_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED
)
async def create_task(payload: TaskCreate, db: DbSession, current_user: CurrentUser):
    task = await task_service.create_task(db, payload, current_user.id)

    return {
        "message": "Task created successfully",
        "data": task,
    }


@router.patch(
    "/{task_id}",
    response_model=TaskSingleResponse,
)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: DbSession,
):

    updated_task = await task_service.update_task(
        db,
        task_id,
        payload,
    )

    return {
        "message": "Task updated successfully",
        "data": updated_task,
    }
