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
    return "OK"


client = TestClient(app)


def test_allow_inf_nan_not_ignored_when_enforcing_params():
    response = client.post("/?x=-1")
    assert response.status_code == 422, response.text

    response = client.post("/?y=inf")
    assert response.status_code == 422, response.text

    response = client.post("/?y=5")
    assert response.status_code == 200, response.text


def test_allow_inf_nan_not_ignored_when_enforcing_body():
    response = client.post("/", json="nan")
    assert response.status_code == 422, response.text
    print(response.text)

    response = client.post("/", json="inf")
    assert response.status_code == 422, response.text

    response = client.post("/", json="4")
    assert response.status_code == 200, response.text
