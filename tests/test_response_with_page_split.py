import pytest
from fastapi import APIRouter, Depends, FastAPI, Response
from fastapi.pagination import PaginationParam
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()
router = APIRouter()


class TmpPagination(PaginationParam):
    page_query_param = "page"


async def response_status_setter(response: Response):
    response.status_code = 200


async def parent_dep(result=Depends(response_status_setter)):
    return result


class User(BaseModel):
    id: int
    name: str


Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True)
    name = Column(String)


@app.get("/", with_page_split=True)
async def get_main():
    return [i for i in range(20)]


@router.get("/router/with-page-model", with_page_split=True, page_model=TmpPagination)
async def get_with_model():
    return [i for i in range(20)]


@router.get("/router/with-response-model", response_model=User, with_page_split=True)
async def get_model():
    return [
        User(id=0, name="Alpha"),
        User(id=1, name="Bravo"),
        User(id=2, name="Charlie"),
        User(id=3, name="Delta"),
        User(id=4, name="Echo"),
        User(id=5, name="Foxtrot"),
        User(id=6, name="Golf"),
        User(id=7, name="Hotel"),
        User(id=8, name="India"),
        User(id=9, name="Juliet"),
        User(id=0, name="Kilo"),
        User(id=10, name="Lima"),
        User(id=11, name="Mike"),
        User(id=12, name="November"),
        User(id=13, name="Oscar"),
    ]


@router.get("/sqlalchemy", response_model=User, with_page_split=True)
async def get_sqlalchemy():
    return [
        UserInfo(id=0, name="Alpha"),
        UserInfo(id=1, name="Bravo"),
        UserInfo(id=2, name="Charlie"),
        UserInfo(id=3, name="Delta"),
        UserInfo(id=4, name="Echo"),
        UserInfo(id=5, name="Foxtrot"),
        UserInfo(id=6, name="Golf"),
        UserInfo(id=7, name="Hotel"),
        UserInfo(id=8, name="India"),
        UserInfo(id=9, name="Juliet"),
        UserInfo(id=0, name="Kilo"),
        UserInfo(id=10, name="Lima"),
        UserInfo(id=11, name="Mike"),
        UserInfo(id=12, name="November"),
        UserInfo(id=13, name="Oscar"),
    ]


app.include_router(router)

client = TestClient(app)


def test_dependency_set_status_code():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 20,
        "next": "http://testserver/?page_num=2",
        "previous": None,
        "results": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    }

    response = client.get("/?page_num=2")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 20,
        "next": None,
        "previous": "http://testserver/?page_num=1",
        "results": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    }

    response = client.get("/?page_size=5")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 20,
        "next": "http://testserver/?page_size=5&page_num=2",
        "previous": None,
        "results": [0, 1, 2, 3, 4],
    }

    response = client.get("/?page_size=5&page_num=2")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 20,
        "next": "http://testserver/?page_size=5&page_num=3",
        "previous": "http://testserver/?page_size=5&page_num=1",
        "results": [5, 6, 7, 8, 9],
    }

    with pytest.raises(ValueError):
        client.get("/?page_size=-1")

    response = client.get("/router/with-page-model")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 20,
        "next": "http://testserver/router/with-page-model?page=2",
        "previous": None,
        "results": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    }

    response = client.get("/router/with-response-model")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 15,
        "next": "http://testserver/router/with-response-model?page_num=2",
        "previous": None,
        "results": [
            {"id": 0, "name": "Alpha"},
            {"id": 1, "name": "Bravo"},
            {"id": 2, "name": "Charlie"},
            {"id": 3, "name": "Delta"},
            {"id": 4, "name": "Echo"},
            {"id": 5, "name": "Foxtrot"},
            {"id": 6, "name": "Golf"},
            {"id": 7, "name": "Hotel"},
            {"id": 8, "name": "India"},
            {"id": 9, "name": "Juliet"},
        ],
    }

    response = client.get("/sqlalchemy")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "count": 15,
        "next": "http://testserver/sqlalchemy?page_num=2",
        "previous": None,
        "results": [
            {"id": 0, "name": "Alpha"},
            {"id": 1, "name": "Bravo"},
            {"id": 2, "name": "Charlie"},
            {"id": 3, "name": "Delta"},
            {"id": 4, "name": "Echo"},
            {"id": 5, "name": "Foxtrot"},
            {"id": 6, "name": "Golf"},
            {"id": 7, "name": "Hotel"},
            {"id": 8, "name": "India"},
            {"id": 9, "name": "Juliet"},
        ],
    }
