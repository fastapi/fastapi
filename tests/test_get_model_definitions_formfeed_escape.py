from typing import Any, Iterator, Set, Type

import fastapi._compat
import fastapi.openapi.utils
import pydantic.schema
import pytest
from fastapi import FastAPI
from fastapi._compat import v1
from pydantic import BaseModel
from starlette.testclient import TestClient

from .utils import needs_pydanticv1


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

client = TestClient(app)


@app.get("/facilities/{facility_id}")
def get_facility(facility_id: str) -> Facility: ...


openapi_schema = {
    "components": {
        "schemas": {
            "Address": {
                # NOTE: the description of this model shows only the public-facing text, before the `\f` in docstring
                "description": "This is a public description of an Address\n",
                "properties": {
                    "city": {"title": "City", "type": "string"},
                    "line_1": {"title": "Line 1", "type": "string"},
                    "state_province": {"title": "State Province", "type": "string"},
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
                        "items": {"$ref": "#/components/schemas/ValidationError"},
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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
                                "schema": {"$ref": "#/components/schemas/Facility"}
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


def test_openapi_schema():
    """
    Sanity check to ensure our app's openapi schema renders as we expect
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


class SortedTypeSet(set):
    """
    Set of Types whose `__iter__()` method yields results sorted by the type names
    """

    def __init__(self, seq: Set[Type[Any]], *, sort_reversed: bool):
        super().__init__(seq)
        self.sort_reversed = sort_reversed

    def __iter__(self) -> Iterator[Type[Any]]:
        members_sorted = sorted(
            super().__iter__(),
            key=lambda type_: type_.__name__,
            reverse=self.sort_reversed,
        )
        yield from members_sorted


@needs_pydanticv1
@pytest.mark.parametrize("sort_reversed", [True, False])
def test_model_description_escaped_with_formfeed(sort_reversed: bool):
    """
    Regression test for bug fixed by https://github.com/fastapi/fastapi/pull/6039.

    Test `get_model_definitions` with models passed in different order.
    """
    all_fields = fastapi.openapi.utils.get_fields_from_routes(app.routes)

    flat_models = v1.get_flat_models_from_fields(all_fields, known_models=set())
    model_name_map = pydantic.schema.get_model_name_map(flat_models)

    expected_address_description = "This is a public description of an Address\n"

    models = v1.get_model_definitions(
        flat_models=SortedTypeSet(flat_models, sort_reversed=sort_reversed),
        model_name_map=model_name_map,
    )
    assert models["Address"]["description"] == expected_address_description
