from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from .main import app

client = TestClient(app)


def test_v1_to_v2_item():
    response = client.post(
        "/v1-to-v2/item",
        json={"title": "Test", "size": 10, "sub": {"name": "SubTest"}},
    )
    assert response.status_code == 200
    assert response.json() == {
        "new_title": "Test",
        "new_size": 10,
        "new_description": None,
        "new_sub": {"new_sub_name": "SubTest"},
        "new_multi": [],
    }


def test_v2_to_v1_item():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "NewTest",
            "new_size": 20,
            "new_sub": {"new_sub_name": "NewSubTest"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "NewTest",
        "size": 20,
        "description": None,
        "sub": {"name": "NewSubTest"},
        "multi": [],
    }


def test_v1_to_v2_item_to_list():
    response = client.post(
        "/v1-to-v2/item-to-list",
        json={"title": "ListTest", "size": 30, "sub": {"name": "SubListTest"}},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "new_title": "ListTest",
            "new_size": 30,
            "new_description": None,
            "new_sub": {"new_sub_name": "SubListTest"},
            "new_multi": [],
        },
        {
            "new_title": "ListTest",
            "new_size": 30,
            "new_description": None,
            "new_sub": {"new_sub_name": "SubListTest"},
            "new_multi": [],
        },
    ]


def test_v1_to_v2_list_to_list():
    response = client.post(
        "/v1-to-v2/list-to-list",
        json=[
            {"title": "Item1", "size": 40, "sub": {"name": "Sub1"}},
            {"title": "Item2", "size": 50, "sub": {"name": "Sub2"}},
        ],
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "new_title": "Item1",
            "new_size": 40,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub1"},
            "new_multi": [],
        },
        {
            "new_title": "Item2",
            "new_size": 50,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub2"},
            "new_multi": [],
        },
    ]


def test_v1_to_v2_list_to_item():
    response = client.post(
        "/v1-to-v2/list-to-item",
        json=[
            {"title": "FirstItem", "size": 60, "sub": {"name": "FirstSub"}},
            {"title": "SecondItem", "size": 70, "sub": {"name": "SecondSub"}},
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "new_title": "FirstItem",
        "new_size": 60,
        "new_description": None,
        "new_sub": {"new_sub_name": "FirstSub"},
        "new_multi": [],
    }


def test_v2_to_v1_item_to_list():
    response = client.post(
        "/v2-to-v1/item-to-list",
        json={
            "new_title": "ListNew",
            "new_size": 80,
            "new_sub": {"new_sub_name": "SubListNew"},
        },
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "ListNew",
            "size": 80,
            "description": None,
            "sub": {"name": "SubListNew"},
            "multi": [],
        },
        {
            "title": "ListNew",
            "size": 80,
            "description": None,
            "sub": {"name": "SubListNew"},
            "multi": [],
        },
    ]


def test_v2_to_v1_list_to_list():
    response = client.post(
        "/v2-to-v1/list-to-list",
        json=[
            {
                "new_title": "New1",
                "new_size": 90,
                "new_sub": {"new_sub_name": "NewSub1"},
            },
            {
                "new_title": "New2",
                "new_size": 100,
                "new_sub": {"new_sub_name": "NewSub2"},
            },
        ],
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "New1",
            "size": 90,
            "description": None,
            "sub": {"name": "NewSub1"},
            "multi": [],
        },
        {
            "title": "New2",
            "size": 100,
            "description": None,
            "sub": {"name": "NewSub2"},
            "multi": [],
        },
    ]


def test_v2_to_v1_list_to_item():
    response = client.post(
        "/v2-to-v1/list-to-item",
        json=[
            {
                "new_title": "FirstNew",
                "new_size": 110,
                "new_sub": {"new_sub_name": "FirstNewSub"},
            },
            {
                "new_title": "SecondNew",
                "new_size": 120,
                "new_sub": {"new_sub_name": "SecondNewSub"},
            },
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "FirstNew",
        "size": 110,
        "description": None,
        "sub": {"name": "FirstNewSub"},
        "multi": [],
    }


def test_v1_to_v2_list_to_item_empty():
    response = client.post("/v1-to-v2/list-to-item", json=[])
    assert response.status_code == 200
    assert response.json() == {
        "new_title": "",
        "new_size": 0,
        "new_description": None,
        "new_sub": {"new_sub_name": ""},
        "new_multi": [],
    }


def test_v2_to_v1_list_to_item_empty():
    response = client.post("/v2-to-v1/list-to-item", json=[])
    assert response.status_code == 200
    assert response.json() == {
        "title": "",
        "size": 0,
        "description": None,
        "sub": {"name": ""},
        "multi": [],
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot()
