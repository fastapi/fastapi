import sys
from typing import Optional, Union

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
DEFAULT = 1234567890

endpoints = []

if sys.hexversion >= 0x31000000:
    from typing import Annotated

    @app.post("/api1")
    def api1(
        integer_or_null: Annotated[int | None, Body(embed=True)] = DEFAULT,
    ) -> dict:
        return {"received": integer_or_null}

    endpoints.append("/api1")


if sys.hexversion >= 0x30900000:
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


client = TestClient(app)


@pytest.mark.parametrize("api", endpoints)
def test_api1_integer(api):
    response = client.post(api, json={"integer_or_null": 100})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": 100}

    response = client.post(api, json={"integer_or_null": None})
    assert response.status_code == 200, response.text
    assert response.json() == {"received": None}