from typing import List

import fastapi
import pytest

PATH = "/"
ROUTE = {"path": PATH, "endpoint": lambda: {}}


class NonPydanticModel:
    pass


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


def test_apiroute_raises_for_invalid_response_model_type(invalid_response_type):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex_info:
        fastapi.routing.APIRoute(**ROUTE, response_model=invalid_response_type)

    assert ex_info.type is fastapi.exceptions.FastAPIError


def test_apiroute_raises_for_invalid_model_type_in_responses_arg(invalid_responses):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex_info:
        fastapi.routing.APIRoute(**ROUTE, responses=invalid_responses)

    assert ex_info.type is fastapi.exceptions.FastAPIError
