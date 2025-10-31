import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient


# Create app variants for different data types
def create_app(variant: str):
    app = FastAPI()

    if variant == "int":

        @app.put("/items/")
        def update_item(data: dict = Body(...)):
            item_id = data.get("item_id")
            return {"variant": "int", "item_id": item_id}

    elif variant == "str":

        @app.put("/items/")
        def update_item(data: dict = Body(...)):
            item_name = data.get("item_name")
            return {"variant": "str", "item_name": item_name}

    elif variant == "dict":

        @app.put("/items/")
        def update_item(data: dict = Body(...)):
            item = data.get("item")
            return {"variant": "dict", "item": item}

    else:
        raise ValueError(f"Unknown variant: {variant}")

    return app


@pytest.mark.parametrize(
    "variant,body,expected",
    [
        ("int", {"item_id": 42}, {"variant": "int", "item_id": 42}),
        ("str", {"item_name": "hello"}, {"variant": "str", "item_name": "hello"}),
        ("dict", {"item": {"a": 1}}, {"variant": "dict", "item": {"a": 1}}),
    ],
)
def test_body_variants(variant, body, expected):
    app = create_app(variant)
    client = TestClient(app)

    response = client.put("/items/", json=body)
    assert response.status_code == 200, response.text
    assert response.json() == expected
