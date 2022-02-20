import random
import string

from fastapi.testclient import TestClient

from core.config import settings


def get_manager_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        'login': settings.FIRST_MANAGER,
        'password': settings.FIRST_MANAGER_PASSWORD,
        'role': 'manager'
    }
    r = client.post(f'{settings.API_V1_STR}/token', data=login_data)
    tokens = r.json()
    a_token = tokens['access_token']
    headers = {'Authorization': f'Bearer {a_token}'}
    return headers


def random_lower_string() -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=32))
