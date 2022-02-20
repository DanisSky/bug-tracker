from fastapi.testclient import TestClient

from core.config import settings
from schemas.user import UserIn
from services.user import save_user
from tests.utils.user import random_role
from tests.utils.utils import random_lower_string


def test_get_users_manager_me(
        client: TestClient, manager_token_headers: dict[str, str]
) -> None:
    r = client.get(f'{settings.API_V1_STR}/users', headers=manager_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user['role'] == 'manager'
    assert current_user['login'] == settings.FIRST_MANAGER


def test_create_user_new_login(
        client: TestClient
) -> None:
    login = random_lower_string()
    password = random_lower_string()
    data = {'login': login, 'password': password}
    r = client.post(
        f'{settings.API_V1_STR}/users', json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    assert created_user['id']
    assert login == created_user['login']


def test_create_user_existing_login(
        client: TestClient
) -> None:
    login = random_lower_string()
    password = random_lower_string()

    user_in1 = UserIn(login=login, password=password, role=random_role())
    save_user(user_in1)

    data = {'login': login, 'password': password}
    r = client.post(
        f'{settings.API_V1_STR}/users', json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert 'id' not in created_user
