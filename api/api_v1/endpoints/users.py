from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user
from core.security import get_password_hash
from models.user import User
from schemas.user import UserOut, UserIn, UserUpdatePassword
from services.user import save_user

router = APIRouter()


@router.get("/", response_model=UserOut)
async def get_me(
        current_user: User = Depends(get_current_user),
) -> Any:
    return current_user


@router.post("/", response_model=UserOut)
async def create_user(
        user_in: UserIn
) -> Any:
    user = await User.objects.get_or_none(login=user_in.login)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this login already exists in the system.",
        )
    return await save_user(user_in=user_in)


@router.put("/", response_model=UserOut)
async def change_password(
        user: UserUpdatePassword,
        current_user: User = Depends(get_current_user),
) -> Any:
    return await current_user.update(
        hash_password=get_password_hash(user.password_1))
