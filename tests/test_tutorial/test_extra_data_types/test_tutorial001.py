from starlette.testclient import TestClient

from extra_data_types.tutorial001 import app

client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "put": {
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
                "summary": "Read Items",
                "operationId": "read_items_items__item_id__put",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "type": "string",
                            "format": "uuid",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_read_items_items__item_id__put"
                            }
                        }
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_read_items_items__item_id__put": {
                "title": "Body_read_items_items__item_id__put",
                "type": "object",
                "properties": {
                    "start_datetime": {
                        "title": "Start Datetime",
                        "type": "string",
                        "format": "date-time",
                    },
                    "end_datetime": {
                        "title": "End Datetime",
                        "type": "string",
                        "format": "date-time",
                    },
                    "repeat_at": {
                        "title": "Repeat At",
                        "type": "string",
                        "format": "time",
                    },
                    "process_after": {
                        "title": "Process After",
                        "type": "number",
                        "format": "time-delta",
                    },
                },
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_extra_types():
    item_id = "ff97dd87-a4a5-4a12-b412-cde99f33e00e"
    data = {
        "start_datetime": "2018-12-22T14:00:00+00:00",
        "end_datetime": "2018-12-24T15:00:00+00:00",
        "repeat_at": "15:30:00",
        "process_after": 300,
    }
    expected_response = data.copy()
    expected_response.update(
        {
            "start_process": "2018-12-22T14:05:00+00:00",
            "duration": 176_100,
            "item_id": item_id,
        }
    )
    response = client.put(f"/items/{item_id}", json=data)
    assert response.status_code == 200
    assert response.json() == expected_response
