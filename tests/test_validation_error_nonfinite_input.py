import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, FiniteFloat


class EchoInt(BaseModel):
    value: int


class EchoFinite(BaseModel):
    value: FiniteFloat


app = FastAPI()


@app.post("/echo-int")
async def echo_int(payload: EchoInt) -> EchoInt:
    return payload


@app.post("/echo-finite")
async def echo_finite(payload: EchoFinite) -> EchoFinite:
    return payload


client = TestClient(app)


@pytest.mark.parametrize(
    "path,raw,expected_input",
    [
        ("/echo-int", '{"value": NaN}', "nan"),
        ("/echo-int", '{"value": Infinity}', "inf"),
        ("/echo-int", '{"value": -Infinity}', "-inf"),
        ("/echo-finite", '{"value": NaN}', "nan"),
        ("/echo-finite", '{"value": Infinity}', "inf"),
        ("/echo-finite", '{"value": -Infinity}', "-inf"),
    ],
)
def test_nonfinite_json_body_returns_422(path: str, raw: str, expected_input: str):
    response = client.post(
        path, content=raw, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422, response.text
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert detail[0]["loc"] == ["body", "value"]
    assert detail[0]["input"] == expected_input


def test_finite_json_body_still_succeeds():
    response = client.post(
        "/echo-int",
        content='{"value": 1}',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"value": 1}


def test_finite_float_in_validation_error_stays_numeric():
    response = client.post(
        "/echo-int",
        content='{"value": 1.5}',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["input"] == 1.5
