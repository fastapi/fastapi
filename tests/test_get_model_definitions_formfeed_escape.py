import warnings

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from .utils import needs_pydanticv1


@pytest.fixture(
    name="client",
    params=[
        pytest.param("pydantic-v1", marks=needs_pydanticv1),
        "pydantic-v2",
    ],
)
def client_fixture(request: pytest.FixtureRequest) -> TestClient:
    if request.param == "pydantic-v1":
        from pydantic.v1 import BaseModel
    else:
        from pydantic import BaseModel

    class Address(BaseModel):
        """
        This is a public description of an Address
        \f
        You can't see this part of the docstring, it's private!
        """

        line_1: str
        city: str
        state_province: str

    class Facility(BaseModel):
        id: str
        address: Address

    app = FastAPI()

    if request.param == "pydantic-v1":
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            @app.get("/facilities/{facility_id}")
            def get_facility(facility_id: str) -> Facility:
                return Facility(
                    id=facility_id,
                    address=Address(
                        line_1="123 Main St", city="Anytown", state_province="CA"
                    ),
                )
    else:

        @app.get("/facilities/{facility_id}")
        def get_facility(facility_id: str) -> Facility:
            return Facility(
                id=facility_id,
                address=Address(
                    line_1="123 Main St", city="Anytown", state_province="CA"
                ),
            )

    client = TestClient(app)
    return client


def test_get(client: TestClient):
    response = client.get("/facilities/42")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": "42",
        "address": {
            "line_1": "123 Main St",
            "city": "Anytown",
            "state_province": "CA",
        },
    }


def test_openapi_schema(client: TestClient):
    """
    Sanity check to ensure our app's openapi schema renders as we expect
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "components": {
                "schemas": {
                    "Address": {
                        # NOTE: the description of this model shows only the public-facing text, before the `\f` in docstring
                        "description": "This is a public description of an Address\n",
                        "properties": {
                            "city": {"title": "City", "type": "string"},
                            "line_1": {"title": "Line 1", "type": "string"},
                            "state_province": {
                                "title": "State Province",
                                "type": "string",
                            },
                        },
                        "required": ["line_1", "city", "state_province"],
                        "title": "Address",
                        "type": "object",
                    },
                    "Facility": {
                        "properties": {
                            "address": {"$ref": "#/components/schemas/Address"},
                            "id": {"title": "Id", "type": "string"},
                        },
                        "required": ["id", "address"],
                        "title": "Facility",
                        "type": "object",
                    },
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "title": "Detail",
                                "type": "array",
                            }
                        },
                        "title": "HTTPValidationError",
                        "type": "object",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "title": "Location",
                                "type": "array",
                            },
                            "msg": {"title": "Message", "type": "string"},
                            "type": {"title": "Error Type", "type": "string"},
                        },
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                        "type": "object",
                    },
                }
            },
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "openapi": "3.1.0",
            "paths": {
                "/facilities/{facility_id}": {
                    "get": {
                        "operationId": "get_facility_facilities__facility_id__get",
                        "parameters": [
                            {
                                "in": "path",
                                "name": "facility_id",
                                "required": True,
                                "schema": {"title": "Facility Id", "type": "string"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Facility"
                                        }
                                    }
                                },
                                "description": "Successful Response",
                            },
                            "422": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                                "description": "Validation Error",
                            },
                        },
                        "summary": "Get Facility",
                    }
                }
            },
        }
    )
