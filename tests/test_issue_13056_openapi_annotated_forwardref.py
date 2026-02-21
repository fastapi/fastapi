from typing import Annotated, Union

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    # This is the ForwardRef issue context
    next_item: Annotated[Union["Item", None], None] = None


@app.get("/", response_model=Item)
def read_root():
    return Item(name="root")


client = TestClient(app)


def test_issue_13056_openapi_annotated_forwardref():
    # This triggers the schema generation where the crash usually happens
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["components"]["schemas"]["Item"]
