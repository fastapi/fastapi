from fastapi.testclient import TestClient

from .app import app

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    schema = response.json()
    component_names = schema["components"]["schemas"].keys()

    # Hashed fully qualified names due to conflict
    assert set(component_names) == {
        "User_46cbb9d5ba5400ba253a3caa105ccc482d1388ff",
        "User_42908c96f764fbf5360c1ae9d3a2a96d90d97bef",
        "User_3c4b81c0ed34bf97eb9b4ac8ced9dc17e0dccbb7",
    }

    assert schema == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/a": {
                "get": {
                    "summary": "User A",
                    "operationId": "user_a_a_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/User_42908c96f764fbf5360c1ae9d3a2a96d90d97bef"
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/b": {
                "get": {
                    "summary": "User B",
                    "operationId": "user_b_b_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/User_3c4b81c0ed34bf97eb9b4ac8ced9dc17e0dccbb7"
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/c": {
                "get": {
                    "summary": "User C",
                    "operationId": "user_c_c_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/User_46cbb9d5ba5400ba253a3caa105ccc482d1388ff"
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "User_3c4b81c0ed34bf97eb9b4ac8ced9dc17e0dccbb7": {
                    "properties": {"b": {"type": "integer", "title": "B"}},
                    "type": "object",
                    "required": ["b"],
                    "title": "User",
                },
                "User_42908c96f764fbf5360c1ae9d3a2a96d90d97bef": {
                    "properties": {"a": {"type": "integer", "title": "A"}},
                    "type": "object",
                    "required": ["a"],
                    "title": "User",
                },
                "User_46cbb9d5ba5400ba253a3caa105ccc482d1388ff": {
                    "properties": {"c": {"type": "integer", "title": "C"}},
                    "type": "object",
                    "required": ["c"],
                    "title": "User",
                },
            }
        },
    }
