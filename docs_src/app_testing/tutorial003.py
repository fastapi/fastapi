import warnings
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}

# startup event and shutdown event are deprecated, you should use lifespan instead
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)

    @app.on_event("startup")
    async def startup_event():
        items["foo"] = {"name": "Fighters"}
        items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}
