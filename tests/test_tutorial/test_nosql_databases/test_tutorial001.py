import importlib
from typing import Any, List
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from dirty_equals import IsDict, IsUUID
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


class MockRow:
    def __init__(self, id: UUID, title: str, description: str, status: str):
        self.id = id
        self.title = title
        self.description = description
        self.status = status


class MockResult:
    def __init__(self, rows: List[MockRow]):
        self._rows = rows
        self._iter = iter(rows)

    def __iter__(self):
        return self._iter

    def one(self):
        if self._rows:
            return self._rows[0]
        return None


@pytest.fixture(
    name="client",
    params=["tutorial001", "tutorial001_scylla"],
)
def get_client(request: pytest.FixtureRequest):
    mock_session = MagicMock()
    mock_cluster_instance = MagicMock()
    mock_cluster_instance.connect.return_value = mock_session

    tasks_store: dict[UUID, dict[str, Any]] = {}

    with patch("cassandra.cluster.Cluster") as mock_cluster:
        mock_cluster.return_value = mock_cluster_instance

        def mock_execute(query: str, params: tuple = ()):
            if "DELETE FROM tasks" in query:
                task_id = params[0]
                if task_id in tasks_store:
                    del tasks_store[task_id]
                return None

            if "UPDATE tasks" in query:
                title, description, status, task_id = params
                if task_id in tasks_store:
                    tasks_store[task_id].update(
                        {"title": title, "description": description, "status": status}
                    )
                return None

            if "INSERT INTO tasks" in query:
                task_id, title, description, status = params
                tasks_store[task_id] = {
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "status": status,
                }
                return None

            if "SELECT" in query and "WHERE" not in query:
                rows = [
                    MockRow(
                        id=task["id"],
                        title=task["title"],
                        description=task["description"],
                        status=task["status"],
                    )
                    for task in tasks_store.values()
                ]
                return MockResult(rows)

            if "SELECT" in query and "WHERE id = %s" in query:
                task_id = params[0]
                if task_id in tasks_store:
                    task = tasks_store[task_id]
                    return MockResult(
                        [
                            MockRow(
                                id=task["id"],
                                title=task["title"],
                                description=task["description"],
                                status=task["status"],
                            )
                        ]
                    )
                return MockResult([])

            return None

        mock_session.execute.side_effect = mock_execute

        mod = importlib.import_module(f"docs_src.nosql_databases.{request.param}")
        importlib.reload(mod)

        with TestClient(mod.app) as c:
            yield c


def test_crud_app(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 200, response.text
    assert response.json() == []

    response = client.post(
        "/tasks/",
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["status"] == "pending"

    task_id = data["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "id": IsUUID(4),
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "pending",
        }
    )

    response = client.post(
        "/tasks/",
        json={
            "title": "Walk the dog",
            "description": "In the park",
            "status": "pending",
        },
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "/tasks/",
        json={"title": "Write code", "description": None, "status": "in_progress"},
    )
    assert response.status_code == 200, response.text

    response = client.get("/tasks/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Buy groceries (Updated)",
            "description": "Milk, eggs, bread, cheese",
            "status": "completed",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "id": IsUUID(4),
            "title": "Buy groceries (Updated)",
            "description": "Milk, eggs, bread, cheese",
            "status": "completed",
        }
    )

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot({"ok": True})

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404, response.text

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404, response.text
    assert response.json() == snapshot({"detail": "Task not found"})

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated non-existent task",
            "description": "This should fail",
            "status": "pending",
        },
    )
    assert response.status_code == 404, response.text
    assert response.json() == snapshot({"detail": "Task not found"})


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/tasks/": {
                    "post": {
                        "summary": "Create Task",
                        "operationId": "create_task_tasks__post",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TaskCreate"
                                    }
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Task"}
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                    "get": {
                        "summary": "Read Tasks",
                        "operationId": "read_tasks_tasks__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Task"
                                            },
                                            "title": "Response Read Tasks Tasks  Get",
                                        }
                                    }
                                },
                            }
                        },
                    },
                },
                "/tasks/{task_id}": {
                    "get": {
                        "summary": "Read Task",
                        "operationId": "read_task_tasks__task_id__get",
                        "parameters": [
                            {
                                "name": "task_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                    "format": "uuid",
                                    "title": "Task Id",
                                },
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Task"}
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                    "put": {
                        "summary": "Update Task",
                        "operationId": "update_task_tasks__task_id__put",
                        "parameters": [
                            {
                                "name": "task_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                    "format": "uuid",
                                    "title": "Task Id",
                                },
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TaskCreate"
                                    }
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Task"}
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                    "delete": {
                        "summary": "Delete Task",
                        "operationId": "delete_task_tasks__task_id__delete",
                        "parameters": [
                            {
                                "name": "task_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                    "format": "uuid",
                                    "title": "Task Id",
                                },
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                },
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "Task": {
                        "properties": {
                            "title": {"type": "string", "title": "Title"},
                            "description": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Description",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"type": "string", "title": "Description"}
                            ),
                            "status": {
                                "type": "string",
                                "default": "pending",
                                "title": "Status",
                            },
                            "id": {"type": "string", "format": "uuid", "title": "Id"},
                        },
                        "type": "object",
                        "required": ["title"],
                        "title": "Task",
                    },
                    "TaskCreate": {
                        "properties": {
                            "title": {"type": "string", "title": "Title"},
                            "description": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Description",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"type": "string", "title": "Description"}
                            ),
                            "status": {
                                "type": "string",
                                "default": "pending",
                                "title": "Status",
                            },
                        },
                        "type": "object",
                        "required": ["title"],
                        "title": "TaskCreate",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
