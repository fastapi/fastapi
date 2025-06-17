import pytest
from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()


@app.post("/")
async def get(
    x: Annotated[float, Query(allow_inf_nan=True)] = 0,
    y: Annotated[float, Query(allow_inf_nan=False)] = 0,
    z: Annotated[float, Query()] = 0,
    b: Annotated[float, Body(allow_inf_nan=False)] = 0,
) -> str:
    return "OK"


client = TestClient(app)


@pytest.mark.parametrize(
    "value,code",
    [
        ("-1", 200),
        ("inf", 200),
        ("-inf", 200),
        ("nan", 200),
        ("0", 200),
        ("342", 200),
    ],
)
def test_allow_inf_nan_param_true(value: str, code: int):
    response = client.post(f"/?x={value}")
    assert response.status_code == code, response.text


@pytest.mark.parametrize(
    "value,code",
    [
        ("-1", 200),
        ("inf", 422),
        ("-inf", 422),
        ("nan", 422),
        ("0", 200),
        ("342", 200),
    ],
)
def test_allow_inf_nan_param_false(value: str, code: int):
    response = client.post(f"/?y={value}")
    assert response.status_code == code, response.text


@pytest.mark.parametrize(
    "value,code",
    [
        ("-1", 200),
        ("inf", 200),
        ("-inf", 200),
        ("nan", 200),
        ("0", 200),
        ("342", 200),
    ],
)
def test_allow_inf_nan_param_default(value: str, code: int):
    response = client.post(f"/?z={value}")
    assert response.status_code == code, response.text


@pytest.mark.parametrize(
    "value,code",
    [
        ("-1", 200),
        ("inf", 422),
        ("-inf", 422),
        ("nan", 422),
        ("0", 200),
        ("342", 200),
    ],
)
def test_allow_inf_nan_body(value: str, code: int):
    response = client.post("/", json=value)
    assert response.status_code == code, response.text
