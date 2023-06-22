from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.testclient import TestClient

app = FastAPI(default_response_class=ORJSONResponse)


class A:
    def __str__(self):
        return "msg"


@app.get("/orjson_non_str_keys")
def get_orjson_non_str_keys():
    return {A(): "Hello World", 1: 1}


client = TestClient(app)


def test_orjson_non_str_keys():
    with client:
        response = client.get("/orjson_non_str_keys")
    assert response.json() == {"msg": "Hello World", "1": 1}
