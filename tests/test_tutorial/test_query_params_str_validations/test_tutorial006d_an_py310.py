from fastapi.testclient import TestClient

from docs_src.query_params_str_validations.tutorial006d_an_py310 import app

client = TestClient(app)


def test_read_items():
    response = client.get("/items/", params={"q": "None"})
    assert response.status_code == 200
    assert response.json() == {"q": None}
