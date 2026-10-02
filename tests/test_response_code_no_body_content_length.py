import pytest
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/reset", status_code=205)
def reset():
    return {"message": "Form submitted"}


@app.post("/reset-none", status_code=205)
def reset_none():
    return None


@app.post("/reset-response-param")
def reset_response_param(response: Response):
    response.status_code = 205
    return {"message": "Form submitted"}


@app.get("/not-modified")
def not_modified(response: Response):
    # A 304 can carry the Content-Length of the 200 representation
    response.status_code = 304
    response.headers["content-length"] = "17"


client = TestClient(app)


@pytest.mark.parametrize("path", ["/reset", "/reset-none", "/reset-response-param"])
def test_205_content_length_is_zero(path: str):
    response = client.post(path)
    assert response.status_code == 205, response.text
    assert response.content == b""
    assert response.headers.get_list("content-length") == ["0"]


def test_304_keeps_content_length():
    response = client.get("/not-modified")
    assert response.status_code == 304, response.text
    assert response.content == b""
    assert response.headers.get_list("content-length") == ["17"]
