from decimal import Decimal

from fastapi import FastAPI
from fastapi.responses import SimpleJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class IrrationalNumbersAsString(BaseModel):
    pi: Decimal
    e: Decimal

    class Config:
        json_encoders = {Decimal: str}


class IrrationalNumbersAsUncappedString(BaseModel):
    pi: Decimal
    e: Decimal

    class Config:
        json_encoders = {Decimal: lambda d: d}


@app.get("/")
def get_root():
    return {"msg": "Hello World"}


@app.get("/float_capped")
def float_capped_encode():
    return {
        "pi": Decimal("3.14159265358979323846264338327950288"),
        "e": Decimal("2.71828182845904523536028747135266249"),
    }


@app.get("/str")
def str_encode():
    return IrrationalNumbersAsString(
        pi=Decimal("3.14159265358979323846264338327950288"),
        e=Decimal("2.71828182845904523536028747135266249"),
    )


@app.get("/float_uncapped", response_class=SimpleJSONResponse)
def float_uncapped_encode():
    return IrrationalNumbersAsUncappedString(
        pi=Decimal("3.14159265358979323846264338327950288"),
        e=Decimal("2.71828182845904523536028747135266249"),
    )


client = TestClient(app)
media_type = "application/json"


def test_app():
    with client:
        response = client.get("/")
    assert response.json() == {"msg": "Hello World"}
    assert response.headers["content-type"] == media_type


def test_app_float_capped():
    with client:
        response = client.get("/float_capped")
    assert response.content == b'{"pi":3.141592653589793,"e":2.718281828459045}'
    assert response.headers["content-type"] == media_type


def test_app_str():
    with client:
        response = client.get("/str")
    assert (
        response.content
        == b'{"pi":"3.14159265358979323846264338327950288","e":"2.71828182845904523536028747135266249"}'
    )
    assert response.headers["content-type"] == media_type


def test_app_float_uncapped():
    with client:
        response = client.get("/float_uncapped")
    assert (
        response.content
        == b'{"pi":3.14159265358979323846264338327950288,"e":2.71828182845904523536028747135266249}'
    )
    assert response.headers["content-type"] == media_type
