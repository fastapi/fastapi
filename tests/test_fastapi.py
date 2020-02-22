from typing import List

import fastapi
import pydantic
import pytest
import starlette.testclient

PATH = "/"
ROUTE = {"path": PATH, "endpoint": lambda: {}}


@pytest.fixture(name="client")
def fixture_client():
    app = fastapi.FastAPI()
    return starlette.testclient.TestClient(app)


@pytest.fixture(
    name="valid_responses",
    params=[int, List[int], pydantic.BaseModel, List[pydantic.BaseModel]],
    ids=["int", "List[int]", "pydantic.BaseModel", "List[pydantic.BaseModel]"],
)
def fixture_valid_responses(request):
    return {"500": {"model": request.param}}


def test_additional_responses_documented_in_openapi_schema(client, valid_responses):
    """
    The only stated guarantee w/ additional responses is that they'll be included in the
    auto-generated OpenAPI docs -- so test that guarantee.
    """
    client.app.add_api_route(**ROUTE, responses=valid_responses)
    responses = client.get("/openapi.json").json()["paths"][PATH]["get"]["responses"]
    schemas = [s["content"]["application/json"]["schema"] for s in responses.values()]

    assert valid_responses.keys() <= responses.keys()
    assert all(s is not None for s in schemas)
