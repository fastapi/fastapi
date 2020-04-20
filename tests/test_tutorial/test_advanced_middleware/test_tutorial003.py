from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient

from advanced_middleware.tutorial003 import app


@app.get("/large")
async def large():
    return PlainTextResponse("x" * 4000, status_code=200)


client = TestClient(app)


def test_middleware():
    response = client.get("/large", headers={"accept-encoding": "gzip"})
    assert response.status_code == 200, response.text
    assert response.text == "x" * 4000
    assert response.headers["Content-Encoding"] == "gzip"
    assert int(response.headers["Content-Length"]) < 4000
    response = client.get("/")
    assert response.status_code == 200, response.text
