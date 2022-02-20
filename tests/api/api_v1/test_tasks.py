from fastapi.testclient import TestClient

from core.config import settings
from schemas.task import TaskIn
from services.task import save_task
from tests.utils.task import random_status, random_priority, random_type
from tests.utils.utils import random_lower_string


def test_list_tasks(
        client: TestClient, manager_token_headers: dict[str, str]
) -> None:
    task_in1 = TaskIn(type=random_type(), priority=random_priority(), status=random_status(),
                      header=random_lower_string(), description=random_lower_string())
    save_task(task_in1, 1)
    task_in2 = TaskIn(type=random_type(), priority=random_priority(), status=random_status(),
                      header=random_lower_string(), description=random_lower_string())
    save_task(task_in2, 1)

    r = client.get(f'{settings.API_V1_STR}/tasks', headers=manager_token_headers)
    all_tasks = r.json()
    assert len(all_tasks) > 1
    for item in all_tasks:
        assert 'type' in item


def test_create_task(
        client: TestClient, manager_token_headers: dict[str, str]
) -> None:
    data = {
        'type': random_type(),
        'priority': random_priority(),
        'status': random_status(),
        'header': random_lower_string(),
        'description': random_lower_string()
    }
    response = client.post(
        f'{settings.API_V1_STR}/tasks', headers=manager_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content['type'] == data['type']
    assert content['priority'] == data['description']
    assert 'id' in content
    assert 'creator' in content
