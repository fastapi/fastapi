from typing import Tuple

import pytest
from fastapi import APIRouter, FastAPI, Query
from fastapi.openapi import utils as openapi_utils
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.datastructures import Headers
from starlette.routing import Match
from starlette.types import Scope


class APIAcceptRoute(APIRoute):

    match_media_type: str

    def accept_matches(self, scope: Scope) -> Tuple[Match, Scope]:
        # simplified parsing and matching of the accept header for this test
        accept_header = Headers(scope=scope).get("Accept", None)
        if not accept_header:
            return Match.PARTIAL, scope
        if self.match_media_type not in accept_header:
            return Match.NONE, scope
        return Match.FULL, scope

    def matches(self, scope: Scope) -> Tuple[Match, Scope]:
        accept_match, accept_scope = self.accept_matches(scope)
        if accept_match == Match.NONE:
            return accept_match, accept_scope
        match, child_scope = super().matches(accept_scope)
        return (
            match if match.value < accept_match.value else accept_match,
            child_scope,
        )


class APIAcceptTextRoute(APIAcceptRoute):
    match_media_type = "text/plain"


class APIAcceptJsonRoute(APIAcceptRoute):
    match_media_type = "application/json"


class APIAcceptCsvRoute(APIAcceptRoute):
    match_media_type = "text/csv"


class Message(BaseModel):
    text: str


def greet_text(message: str = Query("Hi")) -> PlainTextResponse:
    """Greet with a text message"""
    return PlainTextResponse(message)


def greet_json(message: str = Query("Hi")) -> Message:
    """Greet with a json message"""
    return Message(text=message)


def greet_csv(
    message: str = Query("Hi"), header: bool = Query(True)
) -> PlainTextResponse:
    return PlainTextResponse(f"TEXT\n{message}" if header else message)


router = APIRouter()
router.add_api_route(
    "/greet",
    greet_json,
    route_class_override=APIAcceptJsonRoute,
    response_description="A simple JSON message.",
    response_model=Message,
    tags=["test"],
)
router.add_api_route(
    "/greet",
    greet_text,
    route_class_override=APIAcceptTextRoute,
    response_description="A simple text message.",
    responses={200: {"content": {"text/plain": {"example": "hi"}}}},
    tags=["test", "fallback"],
    deprecated=True,
)
router.add_api_route(
    "/greet",
    greet_csv,
    route_class_override=APIAcceptCsvRoute,
    responses={200: {"content": {"text/csv": {"example": "TEXT\nhi"}}}},
)

app = FastAPI()
app.include_router(router)
client = TestClient(app)

openapi_schema_paths = {
    "/greet": {
        "get": {
            "tags": ["test", "fallback"],
            "summary": "Greet Json / Greet Text / Greet Csv",
            "description": "Greet with a json message\n\n OR \n\n Greet with a text message",
            "operationId": "greet_json_greet_get+greet_text_greet_get+greet_csv_greet_get",
            "parameters": [
                {
                    "required": False,
                    "schema": {"title": "Message", "type": "string", "default": "Hi"},
                    "name": "message",
                    "in": "query",
                },
                {
                    "required": False,
                    "schema": {"title": "Header", "type": "boolean", "default": True},
                    "name": "header",
                    "in": "query",
                },
            ],
            "responses": {
                "200": {
                    "description": "A simple JSON message.\n\n OR \n\n A simple text message.\n\n OR \n\n Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Message"}
                        },
                        "text/csv": {"example": "TEXT\nhi"},
                        "text/plain": {"example": "hi"},
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
            "deprecated": True,
        }
    }
}


def test_openapi():
    with pytest.warns(UserWarning) as w:
        response = client.get("/openapi.json")
    assert w[0].message.args[0] == (
        "Merging operation with id greet_json_greet_get "
        "with operation with id greet_text_greet_get."
    )
    assert response.status_code == 200, response.text
    print(response.text)
    assert response.json()["paths"] == openapi_schema_paths


def test_get_route_text():
    response = client.get("/greet", headers={"Accept": "text/plain"})
    assert response.status_code == 200, response.text
    assert response.text == "Hi"


def test_get_route_json():
    response = client.get("/greet", headers={"Accept": "application/json"})
    assert response.status_code == 200, response.text
    assert response.json() == {"text": "Hi"}


dup_app = FastAPI()


@dup_app.get("/duplicate")
def duplicate_1():
    return 1


@dup_app.get("/duplicate")
def duplicate_2():
    return 2


dup_client = TestClient(dup_app)


def test_dup_app_openapi():
    with pytest.warns(UserWarning) as w:
        response = dup_client.get("/openapi.json")
    assert w[0].message.args[0] == (
        "Merging operation with id duplicate_1_duplicate_get "
        "with operation with id duplicate_2_duplicate_get."
    )
    assert response.status_code == 200, response.text
    print(response.text)
    assert response.json()["paths"] == {
        "/duplicate": {
            "get": {
                "summary": "Duplicate 1 / Duplicate 2",
                "operationId": "duplicate_1_duplicate_get+duplicate_2_duplicate_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
            }
        }
    }


CASES = [
    ("empty", {}, {}),
    (
        "one_params",
        {"a": {"parameters": [{"name": "x"}]}, "b": {}},
        {"parameters": [{"name": "x"}]},
    ),
    ("no_params", {"a": {"parameters": []}, "b": {"parameters": []}}, {}),
    ("deprecated_none", {"a": {"deprecated": None}, "b": {"deprecated": None}}, {}),
    ("deprecated_false", {"a": {"deprecated": False}, "b": {"deprecated": False}}, {}),
    (
        "deprecated_true",
        {"a": {"deprecated": True}, "b": {"deprecated": None}},
        {"deprecated": True},
    ),
]


@pytest.mark.parametrize("id,input,expected", CASES, ids=[c[0] for c in CASES])
def test_deep_dict_operation_merge(id: str, input, expected):
    assert openapi_utils.deep_dict_operation_merge(input) == expected
