from enum import Enum
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Depends, status

from api.deps import get_current_manager_user, get_current_user
from enums.base import TypeEnum, StatusEnum, SortOrderEnum
from models.task import Task, TaskBlock
from models.user import User
from schemas.msg import Msg
from schemas.task import TaskOut, TaskIn, TaskOutFull, TaskUpdate
from services.task import save_task, update_task

router = APIRouter()


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
        text: str = '',
        type: Optional[TypeEnum] = None,
        status: Optional[StatusEnum] = None,
        creator: Optional[int] = None,
        executor: Optional[int] = None,
        sort_order: SortOrderEnum = SortOrderEnum.desc,
        limit: int = 100,
        skip: int = 0,
        current_user: User = Depends(get_current_user)  # noqa
) -> Any:
    update_on = 'update_on'
    if sort_order == SortOrderEnum.desc:
        update_on = '-' + update_on
    filters = {
        'type': type,
        'status': status,
        'creator': creator,
        'executor': executor
    }
    filters = {k: v.value if isinstance(v, Enum) else v
               for k, v in filters.items() if v is not None}
    return await Task.objects.order_by(update_on).filter(
        (Task.is_deleted == False) &
        (
                (Task.header.icontains(text)) |
                (Task.description.icontains(text))
        )
    ).filter(**filters).limit(limit).offset(skip).all()


@router.get("/{pk}", response_model=TaskOutFull)
async def get_task(
        pk: int,
        current_user: User = Depends(get_current_user)  # noqa
) -> Any:
    task = await Task.objects.filter(is_deleted=False).select_related(
        ['children', 'executor', 'creator']).fields({'children': {'id'}}).get_or_none(pk=pk)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blocks_by = await TaskBlock.objects.filter(secondary=pk).fields('main').all()
    blocks = await TaskBlock.objects.filter(main=pk).fields('secondary').all()
    return {**task.dict(), 'blocks': blocks, 'blocks_by': blocks_by}


@router.post("/", response_model=TaskOutFull)
async def create_task(
        task_in: TaskIn,
        current_user: User = Depends(get_current_user)  # noqa
) -> Any:
    return await save_task(task_in, current_user.id)


@router.put("/{pk}", response_model=TaskOut)
async def put_task(
        pk: int,
        task_update: TaskUpdate,
        user: User = Depends(get_current_user)  # noqa
) -> Any:
    return await update_task(task_update, pk)


@router.delete("/{pk}", response_model=Msg)
async def delete_task(
        pk: int,
        manager: User = Depends(get_current_manager_user)  # noqa
) -> Msg:
    await Task.objects.filter(pk=pk).update(is_deleted=True)
    return {'msg': 'Deleted successfully'}
