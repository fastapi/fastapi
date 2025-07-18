from typing import List

import pytest
from starlette.testclient import TestClient
from typing_extensions import Self

from docs_src.dependencies.tutorial013b import MyDatabaseConnection, app


class MockDatabaseConnection:
    def __init__(self):
        self.enter_count = 0
        self.exit_count = 0
        self.get_records_count = 0
        self.get_record_count = 0

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

    def _get_new_connection_mock(*args, **kwargs):
        mock = MockDatabaseConnection()
        connections.append(mock)

        return mock

    monkeypatch.setattr(MyDatabaseConnection, "__new__", _get_new_connection_mock)
    return connections


def test_dependency_usage(database_connection_mocks):
    assert len(database_connection_mocks) == 0

    with TestClient(app) as test_client:
        assert len(database_connection_mocks) == 3
        for connection in database_connection_mocks:
            assert connection.enter_count == 1
            assert connection.exit_count == 0
            assert connection.get_records_count == 0
            assert connection.get_record_count == 0

        response = test_client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

        users_connection = None
        for connection in database_connection_mocks:
            if connection.get_records_count == 1:
                users_connection = connection
                break

        assert users_connection is not None, (
            "No connection was found for users endpoint"
        )

        response = test_client.get("/groups")
        assert response.status_code == 200
        assert response.json() == []

        groups_connection = None
        for connection in database_connection_mocks:
            if connection.get_records_count == 1 and connection is not users_connection:
                groups_connection = connection
                break

        assert groups_connection is not None, (
            "No connection was found for groups endpoint"
        )
        assert groups_connection.get_records_count == 1

        items_connection = None
        for connection in database_connection_mocks:
            if connection.get_records_count == 0:
                items_connection = connection
                break

        assert items_connection is not None, (
            "No connection was found for items endpoint"
        )

        response = test_client.get("/items")
        assert response.status_code == 200
        assert response.json() == []

        assert items_connection.get_records_count == 1
        assert items_connection.get_record_count == 0

        response = test_client.get("/items/asd")
        assert response.status_code == 200
        assert response.json() == {
            "table_name": "items",
            "record_id": "asd",
        }

        assert items_connection.get_records_count == 1
        assert items_connection.get_record_count == 1

        for connection in database_connection_mocks:
            assert connection.enter_count == 1
            assert connection.exit_count == 0

    for connection in database_connection_mocks:
        assert connection.enter_count == 1
        assert connection.exit_count == 1
