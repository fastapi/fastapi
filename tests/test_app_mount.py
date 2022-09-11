from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app2 = FastAPI()
app3 = FastAPI()


@app.get("/a")
async def a():
    return "a"


@app2.get("/b")
async def b():
    return "b"


app.mount("/2", app2)


@app3.get("/c")
def c():
    return "c"


router = APIRouter()
router.mount("/3", app3)
app.include_router(router)


client = TestClient(app)


def test_a():
    response = client.get("/a")
    assert response.status_code == 200, response.text
    assert response.json() == "a"


def test_b():
    response = client.get("/2/b")
    assert response.status_code == 200, response.text
    assert response.json() == "b"


def test_c():
    response = client.get("/3/c")
    assert response.status_code == 200, response.text
    assert response.json() == "c"
