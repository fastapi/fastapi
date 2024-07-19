import math
from typing import Union

from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()


@app.post("/")
async def get(
    x: Annotated[Union[float, None], Query(gt=0, description="x")] = 1,
    y: Annotated[Union[float, None], Query(allow_inf_nan=False, description="y")] = 0,
    z: Annotated[Union[float, None], Body(allow_inf_nan=False, description="z")] = 0,
) -> str:
    assert x > 0
    assert not math.isnan(y) and not math.isinf(y)
    assert not math.isnan(z) and not math.isinf(z)

    return "OK"


client = TestClient(app)


def test_allow_inf_nan_not_ignored_when_enforcing_params():
    response = client.post("/?x=-1")
    assert response.status_code == 422

    response = client.post("/?y=inf")
    assert response.status_code == 422


def test_allow_inf_nan_not_ignored_when_enforcing_body():
    response = client.post("/", json={"z": "nan"})
    assert response.status_code == 422

    response = client.post("/", json={"z": "inf"})
    assert response.status_code == 422
