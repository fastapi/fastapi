import math
from typing import Optional

import pytest
from dirty_equals import IsFloatNan
from fastapi import FastAPI
from fastapi.responses import PydanticJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI(default_response_class=PydanticJSONResponse)


class CustomResponse(PydanticJSONResponse):
    media_type = "application/x-custom"


class Item(BaseModel):
    name: str
    price: float
    category: str = Field("food", alias="CAT")
    tax: float = 8.875
    description: Optional[str] = None


@app.get("/response-model", response_model=Item)
@app.get(
    "/response-model-include",
    response_model=Item,
    response_model_include={"name", "category"},
)
@app.get(
    "/response-model-exclude",
    response_model=Item,
    response_model_exclude={"tax", "description"},
)
@app.get(
    "/response-model-by-alias-false",
    response_model=Item,
    response_model_by_alias=False,
)
@app.get(
    "/response-model-exclude-unset",
    response_model=Item,
    response_model_exclude_unset=True,
)
@app.get(
    "/response-model-exclude-defaults",
    response_model=Item,
    response_model_exclude_defaults=True,
)
@app.get(
    "/response-model-exclude-none",
    response_model=Item,
    response_model_exclude_none=True,
)
def get_response_model_params():
    return {"name": "cheese", "price": 1.23, "tax": 8.875, "description": None}


class FloatsNone(BaseModel):
    # pydantic converts inf/nan to None by default
    numbers: list[float]


class FloatsNum(FloatsNone):
    model_config = {"ser_json_inf_nan": "constants"}


class FloatsStr(FloatsNone):
    model_config = {"ser_json_inf_nan": "strings"}


@app.get("/floats-none", response_model=FloatsNone)
@app.get("/floats-num", response_model=FloatsNum)
@app.get("/floats-str", response_model=FloatsStr)
@app.get("/custom-class", response_class=CustomResponse, response_model=FloatsStr)
def get_floats():
    return {"numbers": [3.14, math.inf, math.nan, 2.72]}


client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_response",
    [
        (
            "/response-model",
            {
                "name": "cheese",
                "price": 1.23,
                "CAT": "food",
                "tax": 8.875,
                "description": None,
            },
        ),
        ("/response-model-include", {"name": "cheese", "CAT": "food"}),
        ("/response-model-exclude", {"name": "cheese", "price": 1.23, "CAT": "food"}),
        (
            "/response-model-by-alias-false",
            {
                "name": "cheese",
                "price": 1.23,
                "category": "food",
                "tax": 8.875,
                "description": None,
            },
        ),
        (
            "/response-model-exclude-unset",
            {
                "name": "cheese",
                "price": 1.23,
                "tax": 8.875,
                "description": None,
            },
        ),
        ("/response-model-exclude-defaults", {"name": "cheese", "price": 1.23}),
        (
            "/response-model-exclude-none",
            {
                "name": "cheese",
                "price": 1.23,
                "CAT": "food",
                "tax": 8.875,
            },
        ),
    ],
)
def test_response_model_params(path: str, expected_response: dict):
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "path,expected_numbers",
    [
        ("/floats-none", [3.14, None, None, 2.72]),
        ("/floats-num", [3.14, math.inf, IsFloatNan, 2.72]),
        ("/floats-str", [3.14, "Infinity", "NaN", 2.72]),
    ],
)
def test_floats(path: str, expected_numbers: list):
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"numbers": expected_numbers}


def test_custom_response_class():
    response = client.get("/custom-class")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-custom"
    assert response.json() == {"numbers": [3.14, "Infinity", "NaN", 2.72]}
