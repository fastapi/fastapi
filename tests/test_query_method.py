from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Payload(BaseModel):
    x: int


def test_query_route_executes_and_openapi_survives():
    app = FastAPI()

    @app.query("/items")
    def query_items(payload: Payload):
        return {"ok": payload.x}

    client = TestClient(app)

    # Runtime: the route is callable with QUERY
    r = client.request("QUERY", "/items", json={"x": 42})
    assert r.status_code == 200
    assert r.json() == {"ok": 42}

    # OpenAPI: does not include the query route (excluded by default), and must not error
    schema = app.openapi()
    # The path is excluded from OpenAPI because include_in_schema=False by default
    assert "/items" not in schema["paths"]
