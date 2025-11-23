import bson
from fastapi import FastAPI
from fastapi.responses import BSONResponse
from fastapi.testclient import TestClient

app = FastAPI(default_response_class=BSONResponse)


@app.get("/bson_keys")
def get_bson_serialized_data():
    return {"key": "Hello World", 1: 1}


client = TestClient(app)


def test_bson_serialized_data():
    with client:
        response = client.get("/bson_keys")
    assert response.content == bson.dumps({"key": "Hello World", 1: 1})
