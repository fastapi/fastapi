from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from starlette.testclient import TestClient

from tests.utils import needs_pydanticv1, needs_pydanticv2

app = FastAPI()


@needs_pydanticv1
class NoExtraFieldsV1(BaseModel, extra="forbid"):
    a: int
    b: int


@needs_pydanticv2
class NoExtraFieldsV2(BaseModel):
    model_config = ConfigDict(extra="forbid")
    a: int
    b: int


@app.get("/v1")
def foov1(foo: NoExtraFieldsV1 = Depends()):
    return foo


@app.get("/v2")
def foov2(foo: NoExtraFieldsV2 = Depends()):
    return foo


client = TestClient(app)


@needs_pydanticv2
def test_validate_extra_field_config_pydantic_v2_additional_field():
    response = client.get("/v2", params={"a": 1, "b": 2, "c": 2})
    assert response.status_code == 422, response.text


@needs_pydanticv1
def test_validate_extra_field_conf_pydantic_v1_additional_field():
    response = client.get("/v1", params={"a": 1, "b": 2, "c": 2})
    assert response.status_code == 422, response.text


@needs_pydanticv2
def test_validate_extra_field_config_pydantic_v2():
    response = client.get("/v2", params={"a": 1, "b": 2})
    assert response.status_code == 200, response.text
    assert response.json() == {"a": 1, "b": 2}


@needs_pydanticv1
def test_validate_extra_field_conf_pydantic_v1():
    response = client.get("/v1", params={"a": 1, "b": 2})
    assert response.status_code == 200, response.text
    assert response.json() == {"a": 1, "b": 2}
