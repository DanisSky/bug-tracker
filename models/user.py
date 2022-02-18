import ormar

from db.base import BaseMeta
from enums.base import RoleEnum


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.BigInteger(primary_key=True, autoincrement=True, index=True)
    login: str = ormar.String(unique=True, max_length=50, min_length=4, nullable=True, index=True)
    hash_password: str = ormar.String(max_length=100, min_length=4, nullable=True)
    role: str = ormar.String(max_length=100, choices=list(RoleEnum), nullable=True)
