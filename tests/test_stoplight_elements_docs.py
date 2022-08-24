from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(title="Example App")


@app.get("/a/b")
async def get_a_and_b():
    return {"a": "b"}


client = TestClient(app)


def test_elements_uit():
    response = client.get("/elements")
    assert response.status_code == 200, response.text
    print(response.text)
    assert app.title in response.text
    assert "Stoplight" in response.text


def test_response():
    response = client.get("/a/b")
    assert response.json() == {"a": "b"}
