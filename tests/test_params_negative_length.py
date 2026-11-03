import pytest

from fastapi import Body, FastAPI, Path, Query
from fastapi.testclient import TestClient


def test_query_rejects_negative_min_length():
    with pytest.raises(ValueError, match="`min_length` cannot be negative"):
        Query(None, min_length=-5)


def test_query_rejects_negative_max_length():
    with pytest.raises(ValueError, match="`max_length` cannot be negative"):
        Query(None, max_length=-1)


def test_body_rejects_negative_length():
    with pytest.raises(ValueError, match="cannot be negative"):
        Body(None, min_length=-2)


def test_valid_lengths_still_work():
    app = FastAPI()

    @app.get("/items/")
    def read_items(q: str = Query(None, min_length=1, max_length=5)):
        return {"q": q}

    client = TestClient(app)
    assert client.get("/items/", params={"q": "abc"}).status_code == 200
    assert client.get("/items/", params={"q": ""}).status_code == 422
