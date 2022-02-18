from core.security import get_password_hash
from models.user import User
from schemas.user import UserIn


async def save_user(user_in: UserIn) -> User:
    hash_password = get_password_hash(user_in.password)
    data = user_in.dict(exclude={'password'})
    data['hash_password'] = hash_password
    return await User.objects.create(**data)
