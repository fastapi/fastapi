from typing import Annotated, Optional, Union

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
DEFAULT = 1234567890


@app.post("/api1")
def api1(integer_or_null: Annotated[int | None, Body(embed=True)] = DEFAULT) -> dict:
    return {"received": integer_or_null}


@app.post("/api2")
def api2(integer_or_null: Annotated[Optional[int], Body(embed=True)] = DEFAULT) -> dict:
    return {"received": integer_or_null}


@app.post("/api3")
def api3(
    integer_or_null: Annotated[Union[int, None], Body(embed=True)] = DEFAULT,
) -> dict:
    return {"received": integer_or_null}


@app.post("/api4")
def api4(integer_or_null: Optional[int] = Body(embed=True, default=DEFAULT)) -> dict:
    return {"received": integer_or_null}


client = TestClient(app)


@pytest.mark.parametrize("api", ["/api1", "/api2", "/api3", "/api4"])
def test_api1_integer(api):
    response = client.post(api, json={"integer_or_null": 100})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": 100}

    response = client.post(api, json={"integer_or_null": None})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": None}
