from typing import Generator

import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from core.config import settings
from db.base import metadata
from main import app
from tests.utils.utils import get_manager_token_headers


@pytest.fixture(autouse=True, scope='module')
def create_test_database():
    engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='module')
def manager_token_headers(client: TestClient) -> dict[str, str]:
    return get_manager_token_headers(client)
