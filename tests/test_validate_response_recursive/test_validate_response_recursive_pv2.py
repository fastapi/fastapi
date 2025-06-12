from fastapi.testclient import TestClient

from ..utils import needs_pydanticv2


@needs_pydanticv2
def test_recursive():
    from .app_pv2 import app

    client = TestClient(app)
    response = client.get("/items/recursive")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "sub_items": [{"name": "subitem", "sub_items": []}],
        "name": "item",
    }

    response = client.get("/items/recursive-submodel")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "item",
        "sub_items1": [
            {
                "name": "subitem",
                "sub_items2": [
                    {
                        "name": "subsubitem",
                        "sub_items1": [{"name": "subsubsubitem", "sub_items2": []}],
                    }
                ],
            }
        ],
    }
