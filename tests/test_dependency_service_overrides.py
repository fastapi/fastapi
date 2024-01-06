from abc import ABC, abstractmethod
from typing import List, runtime_checkable

import pytest
from fastapi import APIRouter, FastAPI, Service
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import Protocol

app = FastAPI()

router = APIRouter()


class Item(BaseModel):
    name: str
    value: int


@runtime_checkable
class ItemsProtocol(Protocol):
    def get_items(self) -> List[Item]:
        ...  # pragma: nocover


class ItemsInterface(ABC):
    @abstractmethod
    def get_items(self) -> List[Item]:
        ...  # pragma: nocover


class ItemsService(ItemsInterface):
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def get_items(self) -> List[Item]:
        return [Item(name=self.name, value=self.value)]


class ClassNestedProtocol:
    def __init__(self, impl: ItemsProtocol = Service()):
        self.impl = impl


class ClassNestedInterface:
    def __init__(self, impl: ItemsInterface = Service()):
        self.impl = impl


class ClassNested:
    def __init__(self, impl: ItemsService = Service()):
        self.impl = impl


@app.get("/depends-on-protocol/")
async def depends_on_protocol(service: ItemsProtocol = Service()):
    return {"in": "depends-on-protocol", "items": service.get_items()}


@app.get("/depends-on-interface/")
async def depends_on_interface(service: ItemsInterface = Service()):
    return {"in": "depends-on-interface", "items": service.get_items()}


@app.get("/depends-on-class/")
async def depends_on_class(service: ItemsService = Service()):
    return {"in": "depends-on-class", "items": service.get_items()}


@app.get("/depends-on-nested-protocol/")
async def depends_on_nested_protocol(service: ClassNestedProtocol = Service()):
    return {"in": "depends-on-nested-protocol", "items": service.impl.get_items()}


@app.get("/depends-on-nested-interface/")
async def depends_on_nested_interface(service: ClassNestedInterface = Service()):
    return {"in": "depends-on-nested-interface", "items": service.impl.get_items()}


@app.get("/depends-on-nested-class/")
async def depends_on_nested_class(service: ClassNested = Service()):
    return {"in": "depends-on-nested-class", "items": service.impl.get_items()}


app.include_router(router)

client = TestClient(app)


def test_depends_on_protocol_no_override():
    with pytest.raises(TypeError, match="Protocols cannot be instantiated"):
        # not 422 error about missing args and kwargs inputs
        client.get("/depends-on-protocol/")


def test_depends_on_protocol_override():
    app.dependency_overrides[ItemsProtocol] = lambda: ItemsService(name="abc", value=1)
    response = client.get("/depends-on-protocol/")
    assert response.status_code == 200
    assert response.json() == {
        "in": "depends-on-protocol",
        "items": [
            {
                "name": "abc",
                "value": 1,
            },
        ],
    }
    app.dependency_overrides = {}


def test_depends_on_interface_no_override():
    error_msg = "Can't instantiate abstract class ItemsInterface with.*abstract method"
    with pytest.raises(TypeError, match=error_msg):
        client.get("/depends-on-interface/")


def test_depends_on_interface_override():
    app.dependency_overrides[ItemsInterface] = lambda: ItemsService(name="abc", value=1)
    response = client.get("/depends-on-interface/")
    assert response.status_code == 200
    assert response.json() == {
        "in": "depends-on-interface",
        "items": [
            {
                "name": "abc",
                "value": 1,
            },
        ],
    }
    app.dependency_overrides = {}


def test_depends_on_class_no_override():
    error_msg = "missing 2 required positional arguments: 'name' and 'value'"
    with pytest.raises(TypeError, match=error_msg):
        # not 422 error about missing body fields
        client.get("/depends-on-class/")


def test_depends_on_class_override():
    app.dependency_overrides[ItemsService] = lambda: ItemsService(name="abc", value=1)
    response = client.get("/depends-on-class/")
    assert response.status_code == 200
    assert response.json() == {
        "in": "depends-on-class",
        "items": [
            {
                "name": "abc",
                "value": 1,
            },
        ],
    }
    app.dependency_overrides = {}


def test_depends_on_nested_protocol_no_override():
    with pytest.raises(TypeError, match="Protocols cannot be instantiated"):
        client.get("/depends-on-nested-protocol/")


def test_depends_on_nested_protocol_override_top_level():
    service = ClassNestedProtocol(impl=ItemsService(name="abc", value=1))
    app.dependency_overrides[ClassNestedProtocol] = lambda: service
    response = client.get("/depends-on-nested-protocol/")
    assert response.status_code == 200
    assert response.json() == {
        "in": "depends-on-nested-protocol",
        "items": [
            {
                "name": "abc",
                "value": 1,
            },
        ],
    }
    app.dependency_overrides = {}


def test_depends_on_nested_interface_no_override():
    error_msg = "Can't instantiate abstract class ItemsInterface with.*abstract method"
    with pytest.raises(TypeError, match=error_msg):
        client.get("/depends-on-nested-interface/")


def test_depends_on_nested_interface_override_top_level():
    service = ClassNestedInterface(impl=ItemsService(name="abc", value=1))
    app.dependency_overrides[ClassNestedInterface] = lambda: service
    response = client.get("/depends-on-nested-interface/")
    assert response.status_code == 200
    assert response.json() == {
        "in": "depends-on-nested-interface",
        "items": [
            {
                "name": "abc",
                "value": 1,
            },
        ],
    }
    app.dependency_overrides = {}


def test_depends_on_nested_class_no_override():
    error_msg = "missing 2 required positional arguments: 'name' and 'value'"
    with pytest.raises(TypeError, match=error_msg):
        client.get("/depends-on-nested-class/")


def test_depends_on_nested_class_override_top_level():
    service = ClassNested(impl=ItemsService(name="abc", value=1))
    app.dependency_overrides[ClassNested] = lambda: service
    response = client.get("/depends-on-nested-class/")
    assert response.status_code == 200
    assert response.json() == {
        "in": "depends-on-nested-class",
        "items": [
            {
                "name": "abc",
                "value": 1,
            },
        ],
    }
    app.dependency_overrides = {}
