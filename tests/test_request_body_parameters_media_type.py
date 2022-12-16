import typing

from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

media_type = "application/vnd.api+json"


# NOTE: These are not valid JSON:API resources
# but they are fine for testing requestBody with custom media_type
class Product(BaseModel):
    name: str
    price: float


class Shop(BaseModel):
    name: str


@app.post("/products")
async def create_product(data: Product = Body(media_type=media_type, embed=True)):
    pass  # pragma: no cover


@app.post("/shops")
async def create_shop(
    data: Shop = Body(media_type=media_type),
    included: typing.List[Product] = Body(default=[], media_type=media_type),
):
    pass  # pragma: no cover


create_product_request_body = {
    "content": {
        "application/vnd.api+json": {
            "schema": {"$ref": "#/components/schemas/Body_create_product_products_post"}
        }
    },
    "required": True,
}

create_shop_request_body = {
    "content": {
        "application/vnd.api+json": {
            "schema": {"$ref": "#/components/schemas/Body_create_shop_shops_post"}
        }
    },
    "required": True,
}

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()
    assert (
        openapi_schema["paths"]["/products"]["post"]["requestBody"]
        == create_product_request_body
    )
    assert (
        openapi_schema["paths"]["/shops"]["post"]["requestBody"]
        == create_shop_request_body
    )
