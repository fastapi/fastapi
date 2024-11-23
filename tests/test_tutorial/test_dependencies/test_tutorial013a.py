from typing import List

import pytest
from starlette.testclient import TestClient
from typing_extensions import Self

from docs_src.dependencies.tutorial013a import MyDatabaseConnection, app


class MockDatabaseConnection:
    def __init__(self):
        self.enter_count = 0
        self.exit_count = 0
        self.get_records_count = 0

    async def __aenter__(self) -> Self:
        self.enter_count += 1
        # Called for the sake of coverage.
        return await MyDatabaseConnection.__aenter__(self)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exit_count += 1
        # Called for the sake of coverage.
        return await MyDatabaseConnection.__aexit__(self, exc_type, exc_val, exc_tb)

    async def get_records(self, table_name: str) -> List[dict]:
        self.get_records_count += 1
        # Called for the sake of coverage.
        await MyDatabaseConnection.get_records(self, table_name)
        return []


@pytest.fixture
def database_connection_mock(monkeypatch) -> MockDatabaseConnection:
    mock = MockDatabaseConnection()

    monkeypatch.setattr(MyDatabaseConnection, "__new__", lambda *args, **kwargs: mock)

    return mock


def test_dependency_usage(database_connection_mock):
    assert database_connection_mock.enter_count == 0
    assert database_connection_mock.exit_count == 0
    with TestClient(app) as test_client:
        assert database_connection_mock.enter_count == 1
        assert database_connection_mock.exit_count == 0

        response = test_client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

        assert database_connection_mock.get_records_count == 1

        response = test_client.get("/items")
        assert response.status_code == 200
        assert response.json() == []

        assert database_connection_mock.get_records_count == 2

        assert database_connection_mock.enter_count == 1
        assert database_connection_mock.exit_count == 0

    assert database_connection_mock.enter_count == 1
    assert database_connection_mock.exit_count == 1
