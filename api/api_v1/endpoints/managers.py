from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_manager_user
from models.user import User
from schemas.user import UserOut, UserUpdate

router = APIRouter(
    dependencies=[Depends(get_current_manager_user)]
)


@router.get("/", response_model=list[UserOut])
async def list_users(
        limit: int = 100,
        skip: int = 0,
) -> Any:
    return await User.objects.limit(limit).offset(skip).all()


@router.put("/{pk}", response_model=UserOut)
async def update_user(
        pk: int,
        user_update: UserUpdate
) -> Any:
    user = await User.objects.get_or_none(pk=pk)
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found",
        )
    return await user.update(**user_update.dict())
