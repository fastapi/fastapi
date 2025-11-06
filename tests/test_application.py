import pytest
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
    assert "redoc@2" in response.text


def test_enum_status_code_response():
    response = client.get("/enum-status-code")
    assert response.status_code == 201, response.text
    assert response.json() == "foo bar"


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {
                                "$ref": "#/components/schemas/ValidationError",
                            },
                            "title": "Detail",
                            "type": "array",
                        },
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string",
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type",
                    ],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
        "externalDocs": {
            "description": "External API documentation.",
            "url": "https://docs.example.com/api-general",
        },
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/api_route": {
                "get": {
                    "operationId": "non_operation_api_route_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Non Operation",
                },
            },
            "/enum-status-code": {
                "get": {
                    "operationId": "get_enum_status_code_enum_status_code_get",
                    "responses": {
                        "201": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Get Enum Status Code",
                },
            },
            "/non_decorated_route": {
                "get": {
                    "operationId": "non_decorated_route_non_decorated_route_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Non Decorated Route",
                },
            },
            "/path/bool/{item_id}": {
                "get": {
                    "operationId": "get_bool_id_path_bool__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "boolean",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Bool Id",
                },
            },
            "/path/float/{item_id}": {
                "get": {
                    "operationId": "get_float_id_path_float__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Float Id",
                },
            },
            "/path/int/{item_id}": {
                "get": {
                    "operationId": "get_int_id_path_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Int Id",
                },
            },
            "/path/param-ge-int/{item_id}": {
                "get": {
                    "operationId": "get_path_param_ge_int_path_param_ge_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "minimum": 3,
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Ge Int",
                },
            },
            "/path/param-ge/{item_id}": {
                "get": {
                    "operationId": "get_path_param_ge_path_param_ge__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "minimum": 3,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Ge",
                },
            },
            "/path/param-gt-int/{item_id}": {
                "get": {
                    "operationId": "get_path_param_gt_int_path_param_gt_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMinimum": 3,
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Gt Int",
                },
            },
            "/path/param-gt/{item_id}": {
                "get": {
                    "operationId": "get_path_param_gt_path_param_gt__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMinimum": 3,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Gt",
                },
            },
            "/path/param-gt0/{item_id}": {
                "get": {
                    "operationId": "get_path_param_gt0_path_param_gt0__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMinimum": 0,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Gt0",
                },
            },
            "/path/param-le-ge-int/{item_id}": {
                "get": {
                    "operationId": "get_path_param_le_ge_int_path_param_le_ge_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "maximum": 3,
                                "minimum": 1,
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Le Ge Int",
                },
            },
            "/path/param-le-ge/{item_id}": {
                "get": {
                    "operationId": "get_path_param_le_ge_path_param_le_ge__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "maximum": 3,
                                "minimum": 1,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Le Ge",
                },
            },
            "/path/param-le-int/{item_id}": {
                "get": {
                    "operationId": "get_path_param_le_int_path_param_le_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "maximum": 3,
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Le Int",
                },
            },
            "/path/param-le/{item_id}": {
                "get": {
                    "operationId": "get_path_param_le_path_param_le__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "maximum": 3,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Le",
                },
            },
            "/path/param-lt-gt-int/{item_id}": {
                "get": {
                    "operationId": "get_path_param_lt_gt_int_path_param_lt_gt_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMaximum": 3,
                                "exclusiveMinimum": 1,
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Lt Gt Int",
                },
            },
            "/path/param-lt-gt/{item_id}": {
                "get": {
                    "operationId": "get_path_param_lt_gt_path_param_lt_gt__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMaximum": 3,
                                "exclusiveMinimum": 1,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Lt Gt",
                },
            },
            "/path/param-lt-int/{item_id}": {
                "get": {
                    "operationId": "get_path_param_lt_int_path_param_lt_int__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMaximum": 3,
                                "title": "Item Id",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Lt Int",
                },
            },
            "/path/param-lt/{item_id}": {
                "get": {
                    "operationId": "get_path_param_lt_path_param_lt__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMaximum": 3,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Lt",
                },
            },
            "/path/param-lt0/{item_id}": {
                "get": {
                    "operationId": "get_path_param_lt0_path_param_lt0__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "exclusiveMaximum": 0,
                                "title": "Item Id",
                                "type": "number",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Lt0",
                },
            },
            "/path/param-maxlength/{item_id}": {
                "get": {
                    "operationId": "get_path_param_max_length_path_param_maxlength__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "maxLength": 3,
                                "title": "Item Id",
                                "type": "string",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Max Length",
                },
            },
            "/path/param-min_maxlength/{item_id}": {
                "get": {
                    "operationId": "get_path_param_min_max_length_path_param_min_maxlength__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "maxLength": 3,
                                "minLength": 2,
                                "title": "Item Id",
                                "type": "string",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Min Max Length",
                },
            },
            "/path/param-minlength/{item_id}": {
                "get": {
                    "operationId": "get_path_param_min_length_path_param_minlength__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "minLength": 3,
                                "title": "Item Id",
                                "type": "string",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Min Length",
                },
            },
            "/path/param/{item_id}": {
                "get": {
                    "operationId": "get_path_param_id_path_param__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "null",
                                    },
                                ],
                                "title": "Item Id",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Path Param Id",
                },
            },
            "/path/str/{item_id}": {
                "get": {
                    "operationId": "get_str_id_path_str__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "string",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Str Id",
                },
            },
            "/path/{item_id}": {
                "get": {
                    "operationId": "get_id_path__item_id__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Id",
                },
            },
            "/query": {
                "get": {
                    "operationId": "get_query_query_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "title": "Query",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query",
                },
            },
            "/query/frozenset": {
                "get": {
                    "operationId": "get_query_type_frozenset_query_frozenset_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "items": {
                                    "type": "integer",
                                },
                                "title": "Query",
                                "type": "array",
                                "uniqueItems": True,
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Type Frozenset",
                },
            },
            "/query/int": {
                "get": {
                    "operationId": "get_query_type_query_int_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "title": "Query",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Type",
                },
            },
            "/query/int/default": {
                "get": {
                    "operationId": "get_query_type_int_default_query_int_default_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": False,
                            "schema": {
                                "default": 10,
                                "title": "Query",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Type Int Default",
                },
            },
            "/query/int/optional": {
                "get": {
                    "operationId": "get_query_type_optional_query_int_optional_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": False,
                            "schema": {
                                "anyOf": [
                                    {
                                        "type": "integer",
                                    },
                                    {
                                        "type": "null",
                                    },
                                ],
                                "title": "Query",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Type Optional",
                },
            },
            "/query/list": {
                "get": {
                    "operationId": "get_query_list_query_list_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "device_ids",
                            "required": True,
                            "schema": {
                                "items": {
                                    "type": "integer",
                                },
                                "title": "Device Ids",
                                "type": "array",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "type": "integer",
                                        },
                                        "title": "Response Get Query List Query List Get",
                                        "type": "array",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query List",
                },
            },
            "/query/list-default": {
                "get": {
                    "operationId": "get_query_list_default_query_list_default_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "device_ids",
                            "required": False,
                            "schema": {
                                "default": [],
                                "items": {
                                    "type": "integer",
                                },
                                "title": "Device Ids",
                                "type": "array",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "type": "integer",
                                        },
                                        "title": "Response Get Query List Default Query "
                                        "List Default Get",
                                        "type": "array",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query List Default",
                },
            },
            "/query/mapping-params": {
                "get": {
                    "operationId": "get_mapping_query_params_query_mapping_params_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "queries",
                            "required": False,
                            "schema": {
                                "additionalProperties": {
                                    "type": "string",
                                },
                                "default": {},
                                "title": "Queries",
                                "type": "object",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Mapping Query Params",
                },
            },
            "/query/mapping-sequence-params": {
                "get": {
                    "operationId": "get_sequence_mapping_query_params_query_mapping_sequence_params_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "queries",
                            "required": False,
                            "schema": {
                                "additionalProperties": {
                                    "items": {
                                        "type": "integer",
                                    },
                                    "type": "array",
                                },
                                "default": {},
                                "title": "Queries",
                                "type": "object",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Sequence Mapping Query Params",
                },
            },
            "/query/mixed-params": {
                "get": {
                    "operationId": "get_mixed_mapping_query_params_query_mixed_params_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "sequence_mapping_queries",
                            "required": False,
                            "schema": {
                                "additionalProperties": {
                                    "items": {
                                        "anyOf": [
                                            {
                                                "type": "string",
                                            },
                                            {
                                                "type": "integer",
                                            },
                                        ],
                                    },
                                    "type": "array",
                                },
                                "default": {},
                                "title": "Sequence Mapping Queries",
                                "type": "object",
                            },
                        },
                        {
                            "in": "query",
                            "name": "mapping_query",
                            "required": True,
                            "schema": {
                                "additionalProperties": {
                                    "type": "string",
                                },
                                "title": "Mapping Query",
                                "type": "object",
                            },
                        },
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "title": "Query",
                                "type": "string",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Mixed Mapping Query Params",
                },
            },
            "/query/mixed-type-params": {
                "get": {
                    "operationId": "get_mixed_mapping_mixed_type_query_params_query_mixed_type_params_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "sequence_mapping_queries",
                            "required": False,
                            "schema": {
                                "additionalProperties": {
                                    "items": {
                                        "type": "integer",
                                    },
                                    "type": "array",
                                },
                                "default": {},
                                "title": "Sequence Mapping Queries",
                                "type": "object",
                            },
                        },
                        {
                            "in": "query",
                            "name": "mapping_query_str",
                            "required": False,
                            "schema": {
                                "additionalProperties": {
                                    "type": "string",
                                },
                                "default": {},
                                "title": "Mapping Query Str",
                                "type": "object",
                            },
                        },
                        {
                            "in": "query",
                            "name": "mapping_query_int",
                            "required": False,
                            "schema": {
                                "additionalProperties": {
                                    "type": "integer",
                                },
                                "default": {},
                                "title": "Mapping Query Int",
                                "type": "object",
                            },
                        },
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "title": "Query",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Mixed Mapping Mixed Type Query Params",
                },
            },
            "/query/optional": {
                "get": {
                    "operationId": "get_query_optional_query_optional_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": False,
                            "schema": {
                                "title": "Query",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Optional",
                },
            },
            "/query/param": {
                "get": {
                    "operationId": "get_query_param_query_param_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": False,
                            "schema": {
                                "title": "Query",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Param",
                },
            },
            "/query/param-required": {
                "get": {
                    "operationId": "get_query_param_required_query_param_required_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "title": "Query",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Param Required",
                },
            },
            "/query/param-required/int": {
                "get": {
                    "operationId": "get_query_param_required_type_query_param_required_int_get",
                    "parameters": [
                        {
                            "in": "query",
                            "name": "query",
                            "required": True,
                            "schema": {
                                "title": "Query",
                                "type": "integer",
                            },
                        },
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Query Param Required Type",
                },
            },
            "/text": {
                "get": {
                    "operationId": "get_text_text_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Get Text",
                },
            },
        },
    }
