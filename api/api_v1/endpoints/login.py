from typing import Any

from fastapi import APIRouter, HTTPException, status

from core.security import verify_password, create_access_token
from models.user import User
from schemas.token import Token, TokenData

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        token_data: TokenData,
) -> Any:
    user = await User.objects.get_or_none(login=token_data.login)
    if not user or not verify_password(token_data.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return Token(
        access_token=create_access_token({"sub": user.login}),
        token_type="Bearer"
    )
