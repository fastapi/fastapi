import sys
from typing import List

import pytest
from starlette.testclient import TestClient
from typing_extensions import Self

if sys.version_info >= (3, 9):
    from docs_src.dependencies.tutorial013c_an_py39 import MyDatabaseConnection, app

from ...utils import needs_py39


class MockDatabaseConnection:
    def __init__(self, url: str):
        self.url = url
        self.enter_count = 0
        self.exit_count = 0
        self.get_record_count = 0

    async def __aenter__(self) -> Self:
        self.enter_count += 1
        # Called for the sake of coverage.
        return await MyDatabaseConnection.__aenter__(self)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exit_count += 1
        # Called for the sake of coverage.
        return await MyDatabaseConnection.__aexit__(self, exc_type, exc_val, exc_tb)

    async def get_record(self, table_name: str, record_id: str) -> dict:
        self.get_record_count += 1
        # Called for the sake of coverage.
        await MyDatabaseConnection.get_record(self, table_name, record_id)
        return {
            "table_name": table_name,
            "record_id": record_id,
        }


@pytest.fixture
def database_connection_mocks(monkeypatch) -> List[MockDatabaseConnection]:
    connections = []

    def _get_new_connection_mock(cls, url):
        mock = MockDatabaseConnection(url)
        connections.append(mock)

        return mock

    monkeypatch.setattr(MyDatabaseConnection, "__new__", _get_new_connection_mock)
    return connections


@needs_py39
def test_dependency_usage(database_connection_mocks):
    assert len(database_connection_mocks) == 0

    with TestClient(app) as test_client:
        assert len(database_connection_mocks) == 1
        [database_connection_mock] = database_connection_mocks

        assert database_connection_mock.url == "sqlite:///database.db"
        assert database_connection_mock.enter_count == 1
        assert database_connection_mock.exit_count == 0
        assert database_connection_mock.get_record_count == 0

        response = test_client.get("/users/user")
        assert response.status_code == 200
        assert response.json() == {
            "table_name": "users",
            "record_id": "user",
        }

        assert database_connection_mock.enter_count == 1
        assert database_connection_mock.exit_count == 0
        assert database_connection_mock.get_record_count == 1

    assert database_connection_mock.enter_count == 1
    assert database_connection_mock.exit_count == 1
    assert database_connection_mock.get_record_count == 1

    assert len(database_connection_mocks) == 1
