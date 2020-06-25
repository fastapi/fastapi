from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    description: str = None
    price: float


@app.get("/product")
async def create_item(product: Product):
    pass  # pragma: no cover


product_request_body = {
    "content": {
        "application/json": {"schema": {"$ref": "#/components/schemas/Product"}}
    },
    "required": True,
}

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi_schema = response.json()
    assert openapi_schema["paths"]["/product"]["get"]["requestBody"]
    assert (
        openapi_schema["paths"]["/product"]["get"]["requestBody"]
        == product_request_body
    )
