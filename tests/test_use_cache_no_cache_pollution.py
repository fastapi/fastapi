from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

calls = []


def dep():
    calls.append(1)
    return len(calls)


app = FastAPI()


@app.get("/")
def read(
    once: int = Depends(dep, use_cache=False),
    cached: int = Depends(dep),
):
    return {"once": once, "cached": cached}


def test_use_cache_false_does_not_pollute_cache():
    calls.clear()
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert len(calls) == 2, f"dependency called {len(calls)} time(s), expected 2"
