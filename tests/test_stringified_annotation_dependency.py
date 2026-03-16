from __future__ import annotations

from typing import TYPE_CHECKING, Any, Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import AsyncGenerator


class DummyClient:
    async def get_people(self) -> list:
        return ["John Doe", "Jane Doe"]

    async def close(self) -> None:
        pass


async def get_client() -> AsyncGenerator[DummyClient, None]:
    client = DummyClient()
    yield client
    await client.close()


Client = Annotated[DummyClient, Depends(get_client)]


@pytest.fixture(name="client")
def client_fixture() -> TestClient:
    app = FastAPI()

    @app.get("/")
    async def get_people(client: Client) -> list:
        return await client.get_people()

    client = TestClient(app)
    return client


def test_get(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == ["John Doe", "Jane Doe"]


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "summary": "Get People",
                        "operationId": "get_people__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {},
                                            "type": "array",
                                            "title": "Response Get People  Get",
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    )


def test_openapi_schema_for_dependency_with_forward_ref_defined_later():
    namespace: dict[str, Any] = {}
    exec(
        """
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color="red", size=10)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}


@dataclass
class Potato:
    color: str
    size: int
""",
        namespace,
    )

    client = TestClient(namespace["app"])

    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"color": "red", "size": 10}

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert "requestBody" not in response.json()["paths"]["/"]["get"]
