import sys
from typing import Optional, Union

import pytest
from dirty_equals import IsDict
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
DEFAULT = 1234567890

endpoints = []

if sys.hexversion >= 0x30A0000:
    from typing import Annotated

    @app.post("/api1")
    def api1(
        integer_or_null: Annotated[int | None, Body(embed=True)] = DEFAULT,
    ) -> dict:
        return {"received": integer_or_null}

    endpoints.append("/api1")


if sys.hexversion >= 0x3090000:
    from typing import Annotated

    @app.post("/api2")
    def api2(
        integer_or_null: Annotated[Optional[int], Body(embed=True)] = DEFAULT,
    ) -> dict:
        return {"received": integer_or_null}

    endpoints.append("/api2")

    @app.post("/api3")
    def api3(
        integer_or_null: Annotated[Union[int, None], Body(embed=True)] = DEFAULT,
    ) -> dict:
        return {"received": integer_or_null}

    endpoints.append("/api3")


@app.post("/api4")
def api4(integer_or_null: Optional[int] = Body(embed=True, default=DEFAULT)) -> dict:
    return {"received": integer_or_null}


endpoints.append("/api4")


@app.post("/api5")
def api5(integer: int = Body(embed=True)) -> dict:
    return {"received": integer}


client = TestClient(app)


@pytest.mark.parametrize("api", endpoints)
def test_apis(api):
    response = client.post(api, json={"integer_or_null": 100})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": 100}

    response = client.post(api, json={"integer_or_null": None})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": None}


def test_required_field():
    response = client.post("/api5", json={"integer": 100})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": 100}

    response = client.post("/api5", json={"integer": None})
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "loc": ["body", "integer"],
                    "msg": "Field required",
                    "type": "missing",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        {
            "detail": [
                {
                    "loc": ["body", "integer"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )
