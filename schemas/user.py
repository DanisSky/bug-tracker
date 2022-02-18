from typing import Optional, Any

from pydantic import BaseModel, Field, validator

from enums.base import RoleEnum


class UserBase(BaseModel):

    class Config:
        orm_mode = True


class UserIn(UserBase):
    login: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)
    role: RoleEnum

    class Config:
        use_enum_values = True


class UserUpdate(UserBase):
    login: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)
    role: RoleEnum

    class Config:
        use_enum_values = True


class UserUpdatePassword(UserBase):
    password_1: str = Field(..., min_length=4, max_length=100)
    password_2: str

    @validator('password_2')
    def password_match(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if 'password_1' in values and v != values["password_1"]:
            raise ValueError("passwords don't match")
        return v


class UserOut(UserBase):
    id: int
    login: Optional[str]
    role: Optional[RoleEnum]

    class Config:
        use_enum_values = True
