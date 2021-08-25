from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from pydantic.fields import Undefined

app = FastAPI()


class Customer(BaseModel):
    name: str = Field(None, example="Alan Turing")
    favorite_number: Optional[int] = Field(None, example=Undefined)


@app.get("/foo", response_model=Customer)
def foo():
    return {"name": "Tim Berners-Lee", "favorite_number": 42}


client = TestClient(app)


item_schema = {
    "title": "Customer",
    # "required": ["name"],  TODO: This is missing now for some reason?
    "type": "object",
    "properties": {
        "name": {"title": "Name", "type": "string", "example": "Alan Turing"},
        "favorite_number": {
            "title": "Favorite Number",
            "type": "integer",
            "example": None,
        },
    },
}


def test_shema_null_example():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["components"]["schemas"]["Customer"] == item_schema


def test_response():
    # For coverage
    response = client.get("/foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Tim Berners-Lee", "favorite_number": 42}
