import datetime
from typing import Optional

from pydantic import BaseModel, Field

from enums.base import TypeEnum, PriorityEnum, StatusEnum
from schemas.user import UserOut


class TaskBase(BaseModel):
    type: TypeEnum
    priority: PriorityEnum
    status: StatusEnum
    header: str
    description: str


class TaskId(BaseModel):
    id: int


class TaskOut(TaskBase):
    id: int
    executor: Optional[dict]
    creator: dict
    created_on: datetime.datetime
    update_on: datetime.datetime

    class Config:
        use_enum_values = True


class TaskOutFull(TaskBase):
    id: int
    executor: Optional[UserOut]
    creator: UserOut
    created_on: datetime.datetime
    update_on: datetime.datetime

    sub_tasks: Optional[list[TaskId]] = Field(..., alias='children')
    blocks_by: Optional[list[TaskId]] = None
    blocks: Optional[list[TaskId]] = None

    class Config:
        use_enum_values = True


class TaskIn(TaskBase):
    executor: Optional[int]
    parent_task: Optional[int]
    blocks: Optional[list[TaskId]]

    class Config:
        use_enum_values = True


class TaskUpdate(TaskBase):
    executor: Optional[int]
    parent_task: Optional[int]

    class Config:
        use_enum_values = True
