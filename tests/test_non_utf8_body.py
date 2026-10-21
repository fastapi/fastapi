from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    foo: int


@app.post("/items/")
async def create_item(item: Item):
    return item


client = TestClient(app)


def test_non_utf8_body_with_non_json_content_type():
    """A non-UTF-8 body sent with a non-JSON content type must not crash the app."""
    response = client.post(
        "/items/",
        content=b"\x08\x01\x10\xa0\xe1\x82\x9f\x814",
        headers={"Content-Type": "application/x-protobuf"},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                }
            ]
        }
    )
