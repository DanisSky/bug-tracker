import datetime
from typing import ForwardRef, Optional

import ormar
from sqlalchemy.sql import func

from db.base import BaseMeta
from enums.base import TypeEnum, PriorityEnum, StatusEnum
from models.user import User

TaskRef = ForwardRef("Task")


class TaskBlock(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.BigInteger(primary_key=True, autoincrement=True, index=True)


class Task(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.BigInteger(primary_key=True, autoincrement=True, index=True)
    type: str = ormar.String(max_length=30, choices=list(TypeEnum), nullable=True)
    priority: str = ormar.String(max_length=30, choices=list(PriorityEnum), nullable=True)
    status: str = ormar.String(max_length=30, choices=list(StatusEnum), nullable=True)
    header: str = ormar.String(max_length=100, nullable=True)
    description: str = ormar.Text(nullable=True)
    executor: User = ormar.ForeignKey(User, related_name='to_do', nullable=True)
    creator: User = ormar.ForeignKey(User, related_name='tasks')
    created_on: datetime.datetime = ormar.DateTime(server_default=func.now())
    update_on: datetime.datetime = ormar.DateTime(server_default=func.now())
    parent_task: Optional[TaskRef] = ormar.ForeignKey(TaskRef, related_name='children', nullable=True)
    is_deleted: Optional[bool] = ormar.Boolean(nullable=True, default=False)
    blocks = ormar.ManyToMany(TaskRef, through=TaskBlock, related_name='blocks_by')


Task.update_forward_refs()
