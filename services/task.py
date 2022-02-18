import datetime

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import HTTPException, status

from enums.base import RoleEnum, StatusEnum
from models.task import Task
from models.user import User
from schemas.task import TaskIn


async def save_task(task_in: TaskIn, creator_id: int) -> Task:
    if task_in.executor:
        user: User = await User.objects.get_or_none(pk=task_in.executor)
        if user:
            validate_executor_status(task_in, user)

    try:
        data = task_in.dict()
        data['creator'] = creator_id
        task = await Task(**data).save()

        for blocked_task in data['blocks']:
            db_task = await Task.objects.get_or_none(pk=blocked_task['id'])
            if db_task:
                await task.blocks.add(db_task)
        return task
    except ForeignKeyViolationError as ex:
        raise HTTPException(status_code=400, detail=ex.message)


async def update_task(task_update, pk):
    db_task = await Task.objects.get_or_none(pk=pk)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task dont found'
        )

    if task_update.executor:
        executor = await User.objects.get_or_none(pk=task_update.executor)
        if executor:
            validate_executor_status(task_update, executor)

    validate_status_change(db_task.status, task_update.status)
    now = datetime.datetime.now()
    return await db_task.update(**task_update.dict(), update_on=now)


def validate_executor_status(task_in, executor):
    if executor.role == RoleEnum.MANAGER.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The manager cant be the executor of the task.'
        )
    if task_in.status == StatusEnum.IN_PROGRESS.value and not executor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{StatusEnum.IN_PROGRESS.value} must have an executor'
        )
    if (executor.role == RoleEnum.TEST_ENGINEER.value and
            task_in.status in [StatusEnum.IN_PROGRESS.value, StatusEnum.CODE_REVIEW.value, StatusEnum.DEV_TEST.value]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This status cant have test engineer an executor'
        )
    if (executor.role == RoleEnum.DEVELOPER.value and
            task_in.status == StatusEnum.TESTING.value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The testing status cannot have a developer executor'
        )


def validate_status_change(old: str, new: str):
    if new in [StatusEnum.TO_DO.value, StatusEnum.WONTFIX.value]:
        return
    enum_values = [i.value for i in StatusEnum]
    if enum_values.index(old) == enum_values.index(new) + 1:
        return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='wrong status order'
    )
