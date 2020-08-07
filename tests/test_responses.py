import orjson
from fastapi import FastAPI
from fastapi.responses import create_orjson_class
from fastapi.testclient import TestClient

app = FastAPI()

PAYLOAD = {"payload": {"message": "Hello World"}}


@app.get("/orjson", response_class=create_orjson_class())
def get_orjson():
    return PAYLOAD


@app.get("/orjson_with_option", response_class=create_orjson_class(orjson.OPT_INDENT_2))
def get_orjson_with_option():
    return PAYLOAD


@app.get("/json")
def get_json():
    return PAYLOAD


client = TestClient(app)


def test_orjson_response():
    response = client.get("/orjson")
    assert response.status_code == 200
    assert response.content == b'{"payload":{"message":"Hello World"}}'

    response = client.get("/orjson_with_option")
    assert response.status_code == 200
    assert (
        response.content == b'{\n  "payload": {\n    "message": "Hello World"\n  }\n}'
    )

    response = client.get("/json")
    assert response.status_code == 200
    assert response.content == b'{"payload":{"message":"Hello World"}}'
