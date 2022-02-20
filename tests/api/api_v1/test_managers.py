from fastapi.testclient import TestClient

from core.config import settings
from schemas.user import UserIn
from services.user import save_user
from tests.utils.user import random_role
from tests.utils.utils import random_lower_string


def test_list_users(
        client: TestClient, manager_token_headers: dict[str, str]
) -> None:
    user_in1 = UserIn(login=random_lower_string(), password=random_lower_string(), role=random_role())
    save_user(user_in1)
    user_in2 = UserIn(login=random_lower_string(), password=random_lower_string(), role=random_role())
    save_user(user_in2)

    r = client.get(f'{settings.API_V1_STR}/users/control', headers=manager_token_headers)
    all_users = r.json()
    assert len(all_users) > 1
    for item in all_users:
        assert 'login' in item
