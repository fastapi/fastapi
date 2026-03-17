from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., ge=1, le=1000)):
    return {"item_id": item_id}


client = TestClient(app)


def test_valid_item_id():
    response = client.get("/items/100")
    assert response.status_code == 200
    assert response.json() == {"item_id": 100}


def test_item_id_below_range():
    response = client.get("/items/0")
    assert response.status_code == 422  # validation error


def test_item_id_above_range():
    response = client.get("/items/1001")
    assert response.status_code == 422  # validation error


def test_invalid_type():
    response = client.get("/items/abc")
    assert response.status_code == 422  # type validation error
