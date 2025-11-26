from fastapi.testclient import TestClient

from docs_src.http_query.tutorial001 import app

client = TestClient(app)


def test_query_items():
    response = client.request(
        "QUERY",
        "/items/",
        json={"keyword": "book", "max_price": 50},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Searching items",
        "search_params": {
            "keyword": "book",
            "min_price": None,
            "max_price": 50.0,
        },
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "query" in schema["paths"]["/items/"]
    operation = schema["paths"]["/items/"]["query"]
    assert "requestBody" in operation
    assert "ItemSearch" in operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
