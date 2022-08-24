import sys
from pathlib import Path

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Main",
                "operationId": "read_main__get",
            }
        }
    },
}


def test_testing():
    current_path = sys.path.copy()
    import docs_src.app_testing

    testing_path = Path(docs_src.app_testing.__file__).parent
    sys.path.append(str(testing_path))
    from docs_src.app_testing.test_main import client, test_read_main

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema
    test_read_main()
    sys.path = current_path
