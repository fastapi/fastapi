from fastapi.testclient import TestClient

from custom_response.tutorial004 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"text/html": {"schema": {"type": "string"}}},
                    }
                },
                "summary": "Read Items",
                "operationId": "read_items_items__get",
            }
        }
    },
}

html_contents = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_get_custom_response():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.text == html_contents
