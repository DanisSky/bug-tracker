from fastapi.testclient import TestClient

from core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        'login': settings.FIRST_MANAGER,
        'password': settings.FIRST_MANAGER_PASSWORD,
        'role': 'manager'
    }
    r = client.post(f'{settings.API_V1_STR}/token', data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert 'access_token' in tokens
    assert tokens['access_token']
