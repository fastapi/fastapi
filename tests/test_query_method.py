from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class QueryPayload(BaseModel):
    expression: str
    limit: int = 10


app = FastAPI()


@app.query("/items")
def query_items(payload: QueryPayload):
    return {"expression": payload.expression, "limit": payload.limit}


client = TestClient(app)


def test_query_method_accepts_body():
    response = client.request(
        "QUERY", "/items", json={"expression": "status = 'active'", "limit": 5}
    )
    assert response.status_code == 200
    assert response.json() == {"expression": "status = 'active'", "limit": 5}


def test_query_method_in_openapi():
    schema = client.get("/openapi.json").json()
    assert "/items" in schema["paths"]
    assert "query" in schema["paths"]["/items"]
    request_body = schema["paths"]["/items"]["query"]["requestBody"]
    assert request_body["required"] is True
    content_schema = request_body["content"]["application/json"]["schema"]
    assert content_schema == {"$ref": "#/components/schemas/QueryPayload"}

