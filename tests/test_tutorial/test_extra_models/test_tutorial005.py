from starlette.testclient import TestClient

from extra_models.tutorial005 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/keyword-weights/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Read Keyword Weights Keyword Weights  Get",
                                    "type": "object",
                                    "additionalProperties": {"type": "number"},
                                }
                            }
                        },
                    }
                },
                "summary": "Read Keyword Weights",
                "operationId": "read_keyword_weights_keyword_weights__get",
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_get_items():
    response = client.get("/keyword-weights/")
    assert response.status_code == 200
    assert response.json() == {"foo": 2.3, "bar": 3.4}
