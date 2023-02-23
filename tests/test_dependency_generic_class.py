from typing import Dict, Generic, List, TypeVar

from fastapi import Depends, FastAPI
from starlette.testclient import TestClient

T = TypeVar("T")
C = TypeVar("C")


class FirstGenericType(Generic[T]):
    def __init__(self, simple: T, lst: List[T]):
        self.simple = simple
        self.lst = lst


class SecondGenericType(Generic[T, C]):
    def __init__(
        self,
        simple: T,
        lst: List[T],
        dct: Dict[T, C],
        custom_class: FirstGenericType[T] = Depends(),
    ):
        self.simple = simple
        self.lst = lst
        self.dct = dct
        self.custom_class = custom_class


app = FastAPI()


@app.post("/test_generic_class")
def depend_generic_type(obj: SecondGenericType[str, int] = Depends()):
    return {
        "simple": obj.simple,
        "lst": obj.lst,
        "dct": obj.dct,
        "custom_class": {
            "simple": obj.custom_class.simple,
            "lst": obj.custom_class.lst,
        },
    }


client = TestClient(app)


def test_generic_class_dependency():
    response = client.post(
        "/test_generic_class?simple=simple",
        json={
            "lst": ["string_1", "string_2"],
            "dct": {"key": 1},
        },
    )
    assert response.status_code == 200, response.json()
    assert response.json() == {
        "custom_class": {
            "lst": ["string_1", "string_2"],
            "simple": "simple",
        },
        "lst": ["string_1", "string_2"],
        "dct": {"key": 1},
        "simple": "simple",
    }
