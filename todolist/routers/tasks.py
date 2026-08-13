from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todolist.database import get_session
from todolist.models import Task, User
from todolist.schemas import (
    FilterTask,
    Message,
    TaskList,
    TasksPublic,
    TasksSchema,
    TaskUpdate,
)
from todolist.security import get_current_user

router = APIRouter(tags=['tasks'], prefix='/tasks')

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TasksPublic, status_code=HTTPStatus.CREATED)
async def create_task(
    task: TasksSchema,
    session: Session,
    user: CurrentUser,
):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


@router.get('/', response_model=TaskList)
async def list_tasks(
    session: Session,
    user: CurrentUser,
    task_filter: Annotated[FilterTask, Depends()],
):
    sttm = select(Task).where(Task.user_id == user.id)

    if task_filter.title:
        sttm = sttm.where(Task.title.contains(task_filter.title))
    if task_filter.description:
        sttm = sttm.where(Task.description.contains(task_filter.description))
    if task_filter.state:
        sttm = sttm.where(Task.state == task_filter.state)

    tasks = await session.scalars(
        sttm.limit(task_filter.limit).offset(task_filter.offset)
    )

    return {'tasks': tasks.all()}


@router.delete('/{task_id}', response_model=Message)
async def delete_task(task_id: int, session: Session, user: CurrentUser):
    task = await session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    await session.delete(task)
    await session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{task_id}', response_model=TasksPublic)
async def patch_task(
    task_id: int, session: Session, user: CurrentUser, task: TaskUpdate
):
    db_task = await session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task
