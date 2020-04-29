from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic.error_wrappers import ValidationError

tags: List[Dict[str, Any]] = [
    {"foo": "bar"},
]

app = FastAPI(openapi_tags=tags)

client = TestClient(app)


def test_openapi_schema():
    try:
        client.get("/openapi.json")
    except ValidationError as e:
        assert (
            str(e)
            == "1 validation error for OpenAPI\ntags -> 0 -> name\n  field required (type=value_error.missing)"
        )
    else:
        raise AssertionError("This test should assert an exception, but didn't")
