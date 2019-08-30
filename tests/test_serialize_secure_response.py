from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class SubItem(BaseModel):
    sub_name: str


class Item(BaseModel):
    name: str
    sub_item: SubItem


class SensitiveSubItem(SubItem):
    sub_secret: str


class SensitiveItem(Item):
    secret: str
    sub_item: SensitiveSubItem


@app.get("/item/insecure", response_model=SensitiveItem)
def get_insecure():
    sub_item = SensitiveSubItem(sub_name="sub_item", sub_secret="sub_secret")
    item = SensitiveItem(name="item", sub_item=sub_item, secret="secret")
    return item


@app.get("/item/secure", response_model=Item)
def get_secure():
    sub_item = SensitiveSubItem(sub_name="sub_item", sub_secret="sub_secret")
    item = SensitiveItem(name="item", sub_item=sub_item, secret="secret")
    return item


@app.get("/item/secure-list", response_model=List[Item])
def get_secure():
    sub_item = SensitiveSubItem(sub_name="sub_item", sub_secret="sub_secret")
    item = SensitiveItem(name="item", sub_item=sub_item, secret="secret")
    return [item]


client = TestClient(app)


def test_secure_serialization():
    assert client.get("/item/secure").json() == {
        "name": "item",
        "sub_item": {"sub_name": "sub_item"},
    }


def test_secure_list_serialization():
    assert client.get("/item/secure").json() == [
        {"name": "item", "sub_item": {"sub_name": "sub_item"}}
    ]


def test_insecure_serialization():
    assert client.get("/item/insecure").json() == {
        "name": "item",
        "sub_item": {"sub_name": "sub_item", "sub_secret": "sub_secret"},
        "secret": "secret",
    }
