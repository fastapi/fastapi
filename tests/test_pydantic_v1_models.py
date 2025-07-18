from typing import List, Optional

import pytest
from fastapi import Body, FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from typing_extensions import Annotated

from tests.utils import needs_pydanticv2

if PYDANTIC_V2:
    from pydantic import v1

    class Item(v1.BaseModel):
        name: str
        description: Optional[str] = None
        price: float
        tax: Optional[float] = None
        tags: list = []

    class Model(v1.BaseModel):
        name: str

else:
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        description: Optional[str] = None
        price: float
        tax: Optional[float] = None
        tags: list = []

    class Model(BaseModel):
        name: str


app = FastAPI()


@app.post("/request_body")
async def request_body(body: Annotated[Item, Body()]):
    return body


@app.get("/response_model", response_model=Model)
async def response_model():
    return Model(name="valid_model")


@app.get("/response_model__invalid", response_model=Model)
async def response_model__invalid():
    return 1


@app.get("/response_model_list", response_model=List[Model])
async def response_model_list():
    return [Model(name="valid_model")]


@app.get("/response_model_list__invalid", response_model=List[Model])
async def response_model_list__invalid():
    return [1]


client = TestClient(app)


@needs_pydanticv2
class TestResponseModel:
    def test_simple__valid(self):
        response = client.get("/response_model")
        assert response.status_code == 200
        assert response.json() == {"name": "valid_model"}

    def test_simple__invalid(self):
        with pytest.raises(ResponseValidationError):
            client.get("/response_model__invalid")

    def test_list__valid(self):
        response = client.get("/response_model_list")
        assert response.status_code == 200
        assert response.json() == [{"name": "valid_model"}]

    def test_list__invalid(self):
        with pytest.raises(ResponseValidationError):
            client.get("/response_model_list__invalid")


@needs_pydanticv2
class TestRequestBody:
    def test_model__valid(self):
        response = client.post("/request_body", json={"name": "myname", "price": 1.0})
        assert response.status_code == 200, response.text

    def test_model__invalid(self):
        response = client.post("/request_body", json={"name": "myname"})
        assert response.status_code == 422, response.text


@needs_pydanticv2
class TestSchema:
    def test_can_generate(self):
        spec = app.openapi()
        schema = spec["paths"]["/request_body"]["post"]["requestBody"]["content"][
            "application/json"
        ]["schema"]
        # Check that the schema is not empty and contains the expected properties
        assert "$ref" in schema
        ref = schema["$ref"].split("/")[-1]
        assert ref in spec["components"]["schemas"]
        item_schema = spec["components"]["schemas"][ref]
        assert item_schema["properties"]["name"]["type"] == "string"
        assert item_schema["properties"]["description"]["type"] == "string"
        assert item_schema["properties"]["price"]["type"] == "number"
        assert item_schema["properties"]["tax"]["type"] == "number"
        assert item_schema["properties"]["tags"]["type"] == "array"
        assert "required" in item_schema
        assert "name" in item_schema["required"]
        assert "price" in item_schema["required"]
