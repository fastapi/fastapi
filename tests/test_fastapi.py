from typing import List

import fastapi
import pydantic
import pytest
import starlette.testclient


class NonPydanticModel:
    pass


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


@pytest.fixture(
    name="invalid_response_type",
    params=[NonPydanticModel, List[NonPydanticModel]],
    ids=["NonPydanticModel", "List[NonPydanticModel]"],
)
def fixture_invalid_response_type(request):
    return request.param


@pytest.fixture(name="invalid_responses")
def fixture_invalid_responses(invalid_response_type):
    return {"500": {"model": invalid_response_type}}


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


def test_apiroute_raises_for_invalid_response_model_type(invalid_response_type):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex_info:
        fastapi.routing.APIRoute(**ROUTE, response_model=invalid_response_type)

    assert ex_info.type is fastapi.exceptions.FastAPIError


def test_apiroute_raises_for_invalid_model_type_in_responses_arg(invalid_responses):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex_info:
        fastapi.routing.APIRoute(**ROUTE, responses=invalid_responses)

    assert ex_info.type is fastapi.exceptions.FastAPIError
