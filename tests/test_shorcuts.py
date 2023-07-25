from fastapi import (
    Cookie,
    FastAPI,
    Form,
    Header,
    Path,
    Query,
)
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/some/{p}")
def with_shorctus(
    c: Cookie[int],
    f: Form[int],
    h: Header[int],
    p: Path[int],
    q: Query[int],
):
    return {
        "q": q,
        "c": c,
        "f": f,
        "h": h,
        "p": p,
    }


def test_shortcuts():
    client = TestClient(app, cookies={"c": "2"})
    response = client.post("/some/5?q=1", headers={"H": "4"}, data={"f": 3})
    assert response.status_code == 200, response.json()
    assert response.json() == {
        "q": 1,
        "c": 2,
        "f": 3,
        "h": 4,
        "p": 5,
    }
