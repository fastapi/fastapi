import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/api_route", 200, {"message": "Hello World"}),
        ("/non_decorated_route", 200, {"message": "Hello World"}),
        ("/nonexistent", 404, {"detail": "Not Found"}),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_swagger_ui():
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text
    assert (
        "oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect'"
        in response.text
    )


def test_swagger_ui_oauth2_redirect():
    response = client.get("/docs/oauth2-redirect")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "window.opener.swaggerUIRedirectOauth2" in response.text


def test_redoc():
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "redoc@next" in response.text


def test_enum_status_code_response():
    response = client.get("/enum-status-code")
    assert response.status_code == 201, response.text
    assert response.json() == "foo bar"


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/api_route": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Non Operation",
                    "operationId": "non_operation_api_route_get",
                }
            },
            "/non_decorated_route": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Non Decorated Route",
                    "operationId": "non_decorated_route_non_decorated_route_get",
                }
            },
            "/text": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Get Text",
                    "operationId": "get_text_text_get",
                }
            },
            "/path/{item_id}": {
                "get": {
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
                    "summary": "Get Id",
                    "operationId": "get_id_path__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/str/{item_id}": {
                "get": {
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
                    "summary": "Get Str Id",
                    "operationId": "get_str_id_path_str__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "string"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/int/{item_id}": {
                "get": {
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
                    "summary": "Get Int Id",
                    "operationId": "get_int_id_path_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "integer"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/float/{item_id}": {
                "get": {
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
                    "summary": "Get Float Id",
                    "operationId": "get_float_id_path_float__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "number"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/bool/{item_id}": {
                "get": {
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
                    "summary": "Get Bool Id",
                    "operationId": "get_bool_id_path_bool__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "boolean"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Id",
                    "operationId": "get_path_param_id_path_param__item_id__get",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Item Id",
                                }
                            )
                            # TODO: remove when deprecating Pydantic v1
                            | IsDict({"title": "Item Id", "type": "string"}),
                        }
                    ],
                }
            },
            "/path/param-minlength/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Min Length",
                    "operationId": "get_path_param_min_length_path_param_minlength__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "minLength": 3,
                                "type": "string",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-maxlength/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Max Length",
                    "operationId": "get_path_param_max_length_path_param_maxlength__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "maxLength": 3,
                                "type": "string",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-min_maxlength/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Min Max Length",
                    "operationId": "get_path_param_min_max_length_path_param_min_maxlength__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "maxLength": 3,
                                "minLength": 2,
                                "type": "string",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-gt/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Gt",
                    "operationId": "get_path_param_gt_path_param_gt__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMinimum": 3.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-gt0/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Gt0",
                    "operationId": "get_path_param_gt0_path_param_gt0__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMinimum": 0.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-ge/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Ge",
                    "operationId": "get_path_param_ge_path_param_ge__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "minimum": 3.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-lt/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Lt",
                    "operationId": "get_path_param_lt_path_param_lt__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMaximum": 3.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-lt0/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Lt0",
                    "operationId": "get_path_param_lt0_path_param_lt0__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMaximum": 0.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-le/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Le",
                    "operationId": "get_path_param_le_path_param_le__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "maximum": 3.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-lt-gt/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Lt Gt",
                    "operationId": "get_path_param_lt_gt_path_param_lt_gt__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMaximum": 3.0,
                                "exclusiveMinimum": 1.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-le-ge/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Le Ge",
                    "operationId": "get_path_param_le_ge_path_param_le_ge__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "maximum": 3.0,
                                "minimum": 1.0,
                                "type": "number",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-lt-int/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Lt Int",
                    "operationId": "get_path_param_lt_int_path_param_lt_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMaximum": 3.0,
                                "type": "integer",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-gt-int/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Gt Int",
                    "operationId": "get_path_param_gt_int_path_param_gt_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMinimum": 3.0,
                                "type": "integer",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-le-int/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Le Int",
                    "operationId": "get_path_param_le_int_path_param_le_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "maximum": 3.0,
                                "type": "integer",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-ge-int/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Ge Int",
                    "operationId": "get_path_param_ge_int_path_param_ge_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "minimum": 3.0,
                                "type": "integer",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-lt-gt-int/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Lt Gt Int",
                    "operationId": "get_path_param_lt_gt_int_path_param_lt_gt_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "exclusiveMaximum": 3.0,
                                "exclusiveMinimum": 1.0,
                                "type": "integer",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/path/param-le-ge-int/{item_id}": {
                "get": {
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
                    "summary": "Get Path Param Le Ge Int",
                    "operationId": "get_path_param_le_ge_int_path_param_le_ge_int__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "maximum": 3.0,
                                "minimum": 1.0,
                                "type": "integer",
                            },
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                }
            },
            "/query": {
                "get": {
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
                    "summary": "Get Query",
                    "operationId": "get_query_query_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Query"},
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/query/optional": {
                "get": {
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
                    "summary": "Get Query Optional",
                    "operationId": "get_query_optional_query_optional_get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {"title": "Query"},
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/query/int": {
                "get": {
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
                    "summary": "Get Query Type",
                    "operationId": "get_query_type_query_int_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Query", "type": "integer"},
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/query/int/optional": {
                "get": {
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
                    "summary": "Get Query Type Optional",
                    "operationId": "get_query_type_optional_query_int_optional_get",
                    "parameters": [
                        {
                            "name": "query",
                            "in": "query",
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Query",
                                }
                            )
                            # TODO: remove when deprecating Pydantic v1
                            | IsDict({"title": "Query", "type": "integer"}),
                        }
                    ],
                }
            },
            "/query/int/default": {
                "get": {
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
                    "summary": "Get Query Type Int Default",
                    "operationId": "get_query_type_int_default_query_int_default_get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Query",
                                "type": "integer",
                                "default": 10,
                            },
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/query/param": {
                "get": {
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
                    "summary": "Get Query Param",
                    "operationId": "get_query_param_query_param_get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {"title": "Query"},
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/query/param-required": {
                "get": {
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
                    "summary": "Get Query Param Required",
                    "operationId": "get_query_param_required_query_param_required_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Query"},
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/query/param-required/int": {
                "get": {
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
                    "summary": "Get Query Param Required Type",
                    "operationId": "get_query_param_required_type_query_param_required_int_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Query", "type": "integer"},
                            "name": "query",
                            "in": "query",
                        }
                    ],
                }
            },
            "/enum-status-code": {
                "get": {
                    "responses": {
                        "201": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                    },
                    "summary": "Get Enum Status Code",
                    "operationId": "get_enum_status_code_enum_status_code_get",
                }
            },
            "/query/frozenset": {
                "get": {
                    "summary": "Get Query Type Frozenset",
                    "operationId": "get_query_type_frozenset_query_frozenset_get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "Query",
                                "uniqueItems": True,
                                "type": "array",
                                "items": {"type": "integer"},
                            },
                            "name": "query",
                            "in": "query",
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
                }
            },
            "/query/list": {
                "get": {
                    "summary": "Get Query List",
                    "operationId": "get_query_list_query_list_get",
                    "parameters": [
                        {
                            "name": "device_ids",
                            "in": "query",
                            "required": True,
                            "schema": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "title": "Device Ids",
                            },
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"type": "integer"},
                                        "title": "Response Get Query List Query List Get",
                                    }
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
                }
            },
            "/query/list-default": {
                "get": {
                    "summary": "Get Query List Default",
                    "operationId": "get_query_list_default_query_list_default_get",
                    "parameters": [
                        {
                            "name": "device_ids",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "default": [],
                                "title": "Device Ids",
                            },
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"type": "integer"},
                                        "title": "Response Get Query List Default Query List Default Get",
                                    }
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
                }
            },
        },
        "components": {
            "schemas": {
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
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
