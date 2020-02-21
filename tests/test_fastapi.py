from typing import List

import fastapi
import pydantic
import pytest
import starlette.testclient


class NonPydanticModel:
    pass


PATH = "/"
ROUTE = {"path": PATH, "endpoint": lambda: {}}


def fixture_id(fixture):
    if isinstance(fixture, type):
        return fixture.__name__
    else:
        return str(fixture)


@pytest.fixture(name="app")
def fixture_app():
    return fastapi.FastAPI()


@pytest.fixture(
    name="valid_responses",
    params=[int, List[int], pydantic.BaseModel, List[pydantic.BaseModel]],
    ids=fixture_id,
)
def fixture_valid_responses(request):
    return {"500": {"model": request.param}}


@pytest.fixture(
    name="invalid_response_type",
    params=[NonPydanticModel, List[NonPydanticModel]],
    ids=fixture_id,
)
def fixture_invalid_response_type(request):
    return request.param


@pytest.fixture(name="invalid_responses_arg")
def fixture_invalid_responses_arg(invalid_response_type):
    return {"500": {"model": invalid_response_type}}


def test_additional_responses_documented_in_openapi_schema(app, valid_responses):
    """
    The only stated guarantee w/ additional responses is that they'll be included in the
    auto-generated OpenAPI docs -- so test that guarantee.
    """
    app.add_api_route(**ROUTE, responses=valid_responses)

    client = starlette.testclient.TestClient(app)
    responses = client.get("/openapi.json").json()["paths"][PATH]["get"]["responses"]
    schemas = [s["content"]["application/json"]["schema"] for s in responses.values()]

    assert valid_responses.keys() <= responses.keys()
    assert all(s is not None for s in schemas)


def test_fastapi_raises_for_invalid_response_model_type(app, invalid_response_type):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex_info:
        app.add_api_route(**ROUTE, response_model=invalid_response_type)

    assert ex_info.type is fastapi.exceptions.FastAPIError


def test_fastapi_raises_for_invalid_model_type_in_responses_arg(
    app, invalid_responses_arg
):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex_info:
        app.add_api_route(**ROUTE, responses=invalid_responses_arg)

    assert ex_info.type is fastapi.exceptions.FastAPIError
