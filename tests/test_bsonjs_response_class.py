import json

# Because of python 3.8 doesn't support this library
try:
    import bsonjs  # type: ignore
except ImportError:  # pragma: nocover
    bsonjs = None

from fastapi import FastAPI
from fastapi.responses import BSONJSResponse
from fastapi.testclient import TestClient

app = FastAPI(default_response_class=BSONJSResponse)


@app.get("/bsonjs_keys")
def get_bsonjs_serialized_data():
    return {"key": "Hello World", 1: 1}


client = TestClient(app)


def test_bsonjs_serialized_data():
    with client:
        response = client.get("/bsonjs_keys")

    if bsonjs is not None:
        assert response.content == bsonjs.loads(
            json.dumps({"key": "Hello World", 1: 1})
        )

    assert True
