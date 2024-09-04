from fastapi import FastAPI
from fastapi.testclient import TestClient

recognizing_app = FastAPI()
ignoring_app = FastAPI(ignore_trailing_whitespaces=True)

@recognizing_app.get("/example")
@ignoring_app.get("/example")
async def return_data():
    return {"msg": "Reached the route!"}

recognizing_client = TestClient(recognizing_app)
ignoring_client = TestClient(ignoring_app)

def test_recognizing_trailing_slash():
    response = recognizing_client.get("/example", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Reached the route!"
    response = recognizing_client.get("/example/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"].endswith("/example")

def test_ignoring_trailing_slash():
    response = ignoring_client.get("/example", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Reached the route!"
    response = ignoring_client.get("/example/", follow_redirects=False)
    assert response.status_code == 200
    assert response.json()["msg"] == "Reached the route!"
