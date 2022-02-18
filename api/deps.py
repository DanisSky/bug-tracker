from fastapi import Depends, HTTPException, status

from core.security import JWTBearer, decode_access_token
from enums.base import RoleEnum
from models.user import User


async def get_current_user(
        token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Credentials are not valid"
    )
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    login: str = payload.get("sub")
    if login is None:
        raise cred_exception
    user = await User.objects.get(login=login)
    if user is None:
        raise cred_exception
    return user


async def get_current_manager_user(
        current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != RoleEnum.MANAGER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
