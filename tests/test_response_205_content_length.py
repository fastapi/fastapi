from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/reset", status_code=205)
def reset():
    return {"ok": True}


@app.post("/reset-dependency")
def reset_dependency(response: Response):
    response.status_code = 205
    return {"ok": True}


client = TestClient(app)


def test_205_has_no_body_and_zero_content_length():
    response = client.post("/reset")
    assert response.status_code == 205
    assert response.content == b""
    assert response.headers["content-length"] == "0"


def test_205_set_via_response_parameter():
    response = client.post("/reset-dependency")
    assert response.status_code == 205
    assert response.content == b""
    assert response.headers["content-length"] == "0"
